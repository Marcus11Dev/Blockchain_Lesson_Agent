import requests
import json
import os

from TeamCloud_Modul.Node import Node
from TeamCloud_Modul.json_parser import Message, JSON_Parser, get_checksum, Block, Blockchain
from cryptography.hazmat.primitives import serialization  
from create_Keys import create_key

class Agent:
    def __init__(self, name, debug=True):
        self.name = name
        #self.url = "http://localhost:8000/"

        #self.url = "http://localhost:1337/"
        self.url = "https://pamastmarkt.azurewebsites.net/"

        # Init paths
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.public_key_path = self.filepath + "\public.pem"
        self.private_key_path = self.filepath + "\private.pem"
        self.json_parser = JSON_Parser()

        # Init public and private key
        if not (os.path.exists(self.public_key_path) and 
            os.path.getsize(self.public_key_path) > 0 and 
            os.path.exists(self.private_key_path) and 
            os.path.getsize(self.private_key_path) > 0):
            create_key()
            print("Keys being created")

        with open(self.public_key_path, "rb") as key_file:
            pubkey = key_file.read()
            self.__public_key = serialization.load_pem_public_key(pubkey)

        with open(self.private_key_path, "rb") as key_file:
            self.__private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )

        self.node = Node(name = name, private_key = self.__private_key, public_key = self.__public_key)

        self.registration(debug=debug)


    def print_chain(self, pretty=True):
        self.node.print_chain(pretty=pretty)

    def print_balance(self):
        self.node.print_balance()
    
    def print_quotes(self, product):
        self.node.print_quotes(product = product)

    def registration(self, debug=True):
        try:
            # Built Message
            pem = self.__public_key.public_bytes(  
                encoding=serialization.Encoding.PEM,  
                format=serialization.PublicFormat.SubjectPublicKeyInfo  
            ) 

            request_msg = Message(sender=self.name,receiver='Cloud',parser_type='type_default', message_type='default', payload={"user": self.name, "password": pem.decode('utf-8')},checksum='checksum')

            # Parse Message to JSON
            json_request_msg = self.json_parser.parse_message_to_dump(request_msg)

            # Request
            json_response_msg = requests.post(url=self.url + "/Registration/", json=json_request_msg).json()
           
            # Parse JSON to Message
            response_msg = self.json_parser.parse_dump_to_message(json_response_msg)
            
            # Sync Blockchain
            if response_msg.payload['status'] < 2:
                self.__sync_blockchain()

            info_handler={
                0:'[Info] Successfully registered',
                1:'[Info] Successfully logged in',
                2:'[Error] Name already exists. Choose another username',
                3:'[Error] Registration failed',
            }
            if debug==True: print(info_handler.get(response_msg.payload['status'],"Error occured")) 

        except Exception as e:
            if debug==True: print('[Error] Error occured. Registration call failed.')
            if debug==True: print(e)

    def __sync_blockchain(self):
        ############################################# Get Header Message #############################################

        start_hash, stop_hash = self.node.get_payload_for_get_headers_msg()
        payload = [start_hash, stop_hash]

        # Built Message
        request_msg = Message(sender=self.name,
                                receiver='receiver',
                                parser_type='type_default',
                                message_type='get_headers_msg',
                                payload=payload,
                                checksum=get_checksum(payload))

        # Parse Message to JSON
        json_request_msg = self.json_parser.parse_message_to_dump(request_msg)
        
        # Request
        json_response_msg = requests.post(url=self.url + "/Blockchain/", json=json_request_msg).json()

        # Parse JSON to Message
        response_msg = self.json_parser.parse_dump_to_message(json_response_msg)

        self.node.handle_incoming_message(response_msg)
        # workaround
        self.node.handle_incoming_message(response_msg)
        ############################################# Get Blocks Message #############################################
        
        payload = self.node.get_payload_for_get_blocks_msg()

        request_msg = Message(sender=self.name,
                                receiver='receiver',
                                parser_type='type_default',
                                message_type='get_blocks_msg',
                                payload=payload,
                                checksum=get_checksum(payload))
        
        # Parse Message to JSON
        json_request_msg = self.json_parser.parse_message_to_dump(request_msg)
        
        # Request
        json_response_msg = requests.post(url=self.url + "/Blockchain/", json=json_request_msg).json()
        
        # Parse JSON to Message
        response_msg = self.json_parser.parse_dump_to_message(json_response_msg)

        self.node.handle_incoming_message(response_msg)
    
    def quote(self, quote_list=[], debug=True): 
        try:
            payload = {"quote_list": quote_list}

            # Built Message
            request_msg = Message(sender=self.name,receiver='Cloud',parser_type='type_default', message_type='default', payload=payload,checksum='checksum')

            # Parse Message to JSON
            json_request_msg = self.json_parser.parse_message_to_dump(request_msg)

            # Request
            json_response_msg = requests.post(url=self.url + "/Quote/", json=json_request_msg).json()

            # Parse JSON to Message
            response_msg = self.json_parser.parse_dump_to_message(json_response_msg)
            
            info_handler={
                0:'[Info] Successfully Quote Call.',
                1:'[Warning] Quotes List is Empty. Try later again.',
                2:'[Warning] Quote Call failed. Syntax Error.',
            }
            if debug==True: print(info_handler.get(response_msg.payload['status'],"Error occured"))

            if response_msg.payload['status'] == 0:
                # Extract Response
                response = response_msg.payload['quotes']['List']
                return {'Status': True, 'Response': response}
                
        except Exception as e:
            if debug==True: print('[Error] Error occured. Quote call failed.')
            if debug==True: print(e)

        return {'Status': False, 'Response': {}}

    def buy(self, product, quantity, debug=True):
        try:
            # Get Quote Data
            response_quote = self.quote([product], debug=debug)

            # Check Quote Call was successfully
            if response_quote["Status"] == True:
                if self.node.check_transaction_validity(self.name, 'Cloud', product, quantity, response_quote["Response"][product]):
                    payload = {"product": product, "quantity": quantity}
                    signature = self.node.create_signature(payload)
                    payload.update({'signature':signature})

                    # Built Message
                    request_msg = Message(sender=self.name,receiver='Cloud',parser_type='type_default', message_type='default', payload=payload,checksum='checksum')

                    # Parse Message to JSON
                    json_request_msg = self.json_parser.parse_message_to_dump(request_msg)

                    # Request
                    json_response_msg = requests.post(url=self.url + "/Buy/", json=json_request_msg).json()

                    # Parse JSON to Message
                    response_msg = self.json_parser.parse_dump_to_message(json_response_msg)

                    info_handler={
                        0:'[Info] Transaction successfully.',
                        1:'[Warning] Buy Call failed caused by Quote.',
                        2:'[Warning] Buy Call failed. Validity check failed.',
                        3:'[Error] Signature comparison faced an issue.',
                        4:'[Error] Buy Call failed. Syntax Error.',
                    }
                    if debug==True: print(info_handler.get(response_msg.payload['status'],"Error occured"))

                    if response_msg.payload['status'] == 0: 
                        # Sync Blockchain
                        self.__sync_blockchain()

                        return {'Status': True, 'Response': None}
                else:
                   if debug==True: print("[Warning] Buy Call failed. Validity check failed.")
                   return {'Status': False, 'Response': None} 
            else:
                if debug==True: print("[Warning] Buy Call failed caused by Quote.")
                return {'Status': False, 'Response': None}
        except Exception as e:
            if debug==True: print('[Error] Error occured. Buy call failed.')
            if debug==True: print(e)

        return {'Status': False, 'Response': None}

    def sell(self, product, quantity, debug=True):
        try:
            # Get Quote Data
            response_quote = self.quote([product], debug=debug)

            # Check Quote Call was successfully
            if response_quote["Status"] == True:
                if self.node.check_transaction_validity('Cloud', self.name, product, quantity, response_quote["Response"][product]):
                    payload = {"product": product, "quantity": quantity}
                    signature = self.node.create_signature(payload)
                    payload.update({'signature':signature})

                    # Built Message
                    request_msg = Message(sender=self.name,receiver='Cloud',parser_type='type_default', message_type='default', payload=payload,checksum='checksum')

                    # Parse Message to JSON
                    json_request_msg = self.json_parser.parse_message_to_dump(request_msg)

                    # Request
                    json_response_msg = requests.post(url=self.url + "/Sell/", json=json_request_msg).json()

                    # Parse JSON to Message
                    response_msg = self.json_parser.parse_dump_to_message(json_response_msg)

                    info_handler={
                        0:'[Info] Transaction successfully.',
                        1:'[Warning] Sell Call failed caused by Quote.',
                        2:'[Warning] Sell Call failed. Validity check failed.',
                        3:'[Error] Signature comparison faced an issue.',
                        4:'[Error] Sell Call failed. Syntax Error.',
                    }
                    if debug==True: print(info_handler.get(response_msg.payload['status'],"Error occured"))

                    if response_msg.payload['status'] == 0: 
                        # Sync Blockchain
                        self.__sync_blockchain()

                        return {'Status': True, 'Response': None}
                else:
                   if debug==True: print("[Warning] Sell Call failed. Validity check failed.")
                   return {'Status': False, 'Response': None} 
            else:
                if debug==True: print("[Warning] Sell Call failed caused by Quote.")
                return {'Status': False, 'Response': None}
        except Exception as e:
            if debug==True: print('[Error] Error occured. Sell call failed.')
            if debug==True: print(e)

        return {'Status': False, 'Response': None}
