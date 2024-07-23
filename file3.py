import cryptography.hazmat.primitives.asymmetric import rsa
import socket

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
                
    def Sign(self, data):
        """Signs given data using a private key.

        Parameters
        ----------
        data : TODO
            TODO

        Returns
        -------
        TODO
            The signed ``data``

        """
        return self.rsa_key.sign(data, padding.PKCS1v15(), utils.Prehashed(hashes.SHA1()))
    
    def store_paste(self, paste_data, config):
        host = config['outputs']['syslog_output']['host']
        port = config['outputs']['syslog_output']['port']

        syslog_line = '"{0}" "{1}" "{2}" "{3}" "{4}"'.format(paste_data['@timestamp'],
                                                paste_data['pasteid'],
                                                paste_data['YaraRule'],
                                                paste_data['scrape_url'],
                                                paste_data['pastesite'])
        syslog = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        syslog.connect((host, port))
        syslog.send(syslog_line.encode('utf-8'))
        syslog.close()
