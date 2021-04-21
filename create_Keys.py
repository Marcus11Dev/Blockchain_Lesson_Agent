import os

from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa  
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import padding

# save file helper  
def save_file(filename, content):  
    filepath = os.path.dirname(os.path.abspath(__file__))
    f = open(filepath + "/" + filename, "wb")  
    f.write(content) 
    f.close()  

def create_key():
    # generate private key & write to disk  
    private_key = rsa.generate_private_key(  
        public_exponent=65537,  
        key_size=4096,  
        backend=default_backend()  
    )  

    pem = private_key.private_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PrivateFormat.PKCS8,  
        encryption_algorithm=serialization.NoEncryption() 
        #encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword') 
    )  

    save_file("private.pem", pem)  

    # generate public key  
    public_key = private_key.public_key()  
    pem = public_key.public_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PublicFormat.SubjectPublicKeyInfo  
    )  

    save_file("public.pem", pem)  
    