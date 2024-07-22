import cryptography.hazmat.primitives.asymmetric import rsa


class Config:
    def __init__(self, rsa_key_path):
        with open(rsa_key_path + '.pub') as rsa_pub_file:
            rsa_data = rsa_pub_file.read()
            if isinstance (rsa_data,str):
                self.public_key = rsa_data
            else:
                self.public_key = rsa_data.encode('ascii')

        with open(rsa_key_path) as rsa_prv_file:
            rsa_data = rsa_prv_file.read()
            if isinstance (rsa_data,str):
                self.rsa_key = serialization.load_pem_private_key(
                        rsa_data, None, default_backend())
            else:
                self.rsa_key = serialization.load_pem_private_key(
                        rsa_data.encode('ascii'), None, default_backend())
