import cryptography

def computeEncryptionKey(password, dictOwnerPass, dictUserPass, dictOE, dictUE, fileID, pElement, dictKeyLength = 128, revision = 3, encryptMetadata = False, passwordType = None):
    '''
        Compute an encryption key to encrypt/decrypt the PDF file
        
        @param password: The password entered by the user
        @param dictOwnerPass: The owner password from the standard security handler dictionary
        @param dictUserPass: The user password from the standard security handler dictionary
        @param dictOE: The owner encrypted string from the standard security handler dictionary
        @param dictUE:The user encrypted string from the standard security handler dictionary
        @param fileID: The /ID element in the trailer dictionary of the PDF file
        @param pElement: The /P element of the Encryption dictionary
        @param dictKeyLength: The length of the key
        @param revision: The algorithm revision
        @param encryptMetadata: A boolean extracted from the standard security handler dictionary to specify if it's necessary to encrypt the document metadata or not
        @param passwordType: It specifies the given password type. It can be 'USER', 'OWNER' or None.
        @return: A tuple (status,statusContent), where statusContent is the encryption key in case status = 0 or an error message in case status = -1
    '''
    try:
        if revision != 5:
            keyLength = dictKeyLength/8
            lenPass = len(password)
            if lenPass > 32:
                password = password[:32]
            elif lenPass < 32:
                password += paddingString[:32-lenPass]
            md5input = password + dictOwnerPass + struct.pack('<i',int(pElement)) + fileID
            if revision > 3 and not encryptMetadata:
                md5input += '\xFF'*4
            key = hashlib.md5(md5input).digest()
            if revision > 2:
                counter = 0
                while counter < 50:
                    key = hashlib.md5(key[:keyLength]).digest()
                    counter += 1
                key = key[:keyLength]
            elif revision == 2:
                key = key[:5]
            return (0, key)
        else:
            if passwordType == 'USER':
                password = password.encode('utf-8')[:127]
                kSalt = dictUserPass[40:48]
                intermediateKey = hashlib.sha256(password + kSalt).digest()
                ret = aes.decryptData('\0'*16+dictUE, intermediateKey)
            elif passwordType == 'OWNER':
                password = password.encode('utf-8')[:127]
                kSalt = dictOwnerPass[40:48]
                intermediateKey = hashlib.sha256(password + kSalt + dictUserPass).digest()
                ret = aes.decryptData('\0'*16+dictOE, intermediateKey)
            return ret
    except:
        return (-1, 'ComputeEncryptionKey error: %s %s' % (str(sys.exc_info()[0]),str(sys.exc_info()[1])))