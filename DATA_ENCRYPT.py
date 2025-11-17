import base64
import binascii
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import unpad,pad
import json
 
class EncryptAndDecryptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
 
        with open('C:/Medyaan/Medyaan_Backend_Monolithic/private_key.pem', 'rb') as key_file:
            private_key_pem = key_file.read()
        self.private_key = RSA.import_key(private_key_pem)
 
    def decrypt_rsa(self, encrypted_data):
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        decrypted_data = cipher_rsa.decrypt(base64.b64decode(encrypted_data))
        return decrypted_data
 
    def decrypt_aes(self, ciphertext, key, iv):
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(binascii.unhexlify(ciphertext)), AES.block_size)
        return decrypted_data.decode('utf-8')
   
    def encrypt_aes(self, plaintext, key, iv):
        key = bytes.fromhex(key)
        iv = bytes.fromhex(iv)
 
        plaintext_bytes = plaintext.encode('utf-8')
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = pad(plaintext_bytes, AES.block_size)
        encrypted_bytes = cipher_aes.encrypt(padded_plaintext)
        return encrypted_bytes.hex()
 
    def process_json_values(self, data):
        if isinstance(data, dict):
            return {key: self.process_json_values(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.process_json_values(item) for item in data]
        elif isinstance(data, str):
            return self.encrypt_aes(data, self.aes_key, self.aes_iv)
        else:
            return data
 
    def __call__(self, request):
        try:
            encrypted_aes_key = request.headers.get('X-Encrypted-AES-Key')
            encrypted_aes_iv = request.headers.get('X-Encrypted-AES-IV')
            aes_key = self.decrypt_rsa(encrypted_aes_key)
            aes_iv = self.decrypt_rsa(encrypted_aes_iv)
            self.aes_key = aes_key.hex()
            self.aes_iv = aes_iv.hex()    
            if request.method == 'GET' and request.GET:
                if encrypted_aes_key and encrypted_aes_iv:
                               
                    query_params = request.GET.copy()
                    for key, value in request.GET.items():
                        plaintext = self.decrypt_aes(value, aes_key, aes_iv)                    
                        query_params[key] = plaintext
 
                    request.GET = query_params
 
            elif request.method in ['POST', 'PUT', 'DELETE'] and request.body:
 
                if encrypted_aes_key and encrypted_aes_iv:
                    try:
                        post_data = json.loads(request.body.decode('utf-8'))
 
                        for key, value in post_data.items():
                            if isinstance(value, str):
                                plaintext = self.decrypt_aes(value, aes_key, aes_iv)
                                post_data[key] = plaintext
                    except json.JSONDecodeError:
                        post_data = request.POST.copy()
 
                        for key, value in request.POST.items():
                            plaintext = self.decrypt_aes(value, aes_key, aes_iv)
                            post_data[key] = plaintext
                    request._body = json.dumps(post_data).encode('utf-8')
 
            response = self.get_response(request)
            if response.get('Content-Type') == 'application/json':
                try:
                    data = json.loads(response.content.decode('utf-8'))
                    if isinstance(data, dict):
                        for key, val in data.items():
                            if key in ['status', 'message']:
                                continue
                            encrypted_data = self.process_json_values(val)
                            data[key] = encrypted_data
 
                    response.content = json.dumps(data).encode('utf-8')
 
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print("Error encrypting JSON response:", e)
            return response
        except Exception as e:
            print("ERROR",e)
            import traceback
            traceback.print_exc()
 
 