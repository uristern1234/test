import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def Sign(self, data):
        return self.rsa_key.sign(
            data, padding.PKCS1v15(), utils.Prehashed(hashes.SHA1()))