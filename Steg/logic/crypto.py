from Crypto.Cipher import AES
from Crypto import Random

import hashlib

class Crypto(object):
    def __init__(self, password, msg=None, enc_msg=None):
        self.password = password
        self.message = self.convert_message(msg)
        self.enc_message = self.convert_enc_message(enc_msg)
        self.sha_passw = None
        self.pas_confirm = None

    @property
    def _sha_passw(self):
        """
            Transforms password by SHA-512 cryptografic 
            hash algorithm.

            Returns:
                sha_pass(list): created password in two parts, 32 byte each
                
        """
        if self.sha_passw is None:
            h = hashlib.sha512(b'%s' % self.password)
            passw = h.digest()
            self.sha_passw = [passw[:len(passw)/2],
                              passw[len(passw)/2:]]
        return self.sha_passw
        
    def convert_message(self, msg):
        """
            Function for splitting message into two equal parts
            
            Args:
                msg(str): given message
                
            Reurns:
                (list): splitted message
        """
        if msg:
            return [msg[:len(msg)/2],
                    msg[len(msg)/2:]]

    def convert_enc_message(self, enc_msg):
        """
            Function for splitting encrypted message into two equal parts
            
            Args:
                enc_msg(str): given encrypted message
                
            Reurns:
                (list): splitted encrypted message
        """
        if enc_msg:
            return [enc_msg[:len(enc_msg)/2],
                    enc_msg[len(enc_msg)/2:]]

    def encrypt(self):
        """
            Encryption of given text message
            Performed by AES algorithm

            Returns:
                msg(str): encrypted message
        """
        if self.message is not None:
            msg = str()
            for passw, mess in zip(self._sha_passw, self.message):
                key = b'%s' % passw
                iv = Random.new().read(AES.block_size)
                cipher = AES.new(key, AES.MODE_CFB, iv)
                msg += iv + cipher.encrypt(b'%s' % mess)

            return msg

    def decrypt(self):
        """
            Decryption of encrypted message.
            Performed by AES algoritm.
        
            Args:
                enc_message(str): message to decrypt

            Returns:
                msg(str): decrypted message
        """
        if self.enc_message is not None:
            result = str()
            for passw, mess in zip(self._sha_passw, self.enc_message):
                key = b'%s' % passw
                iv = Random.new().read(AES.block_size)
                cipher = AES.new(key, AES.MODE_CFB, iv)
                msg = cipher.decrypt(mess)
                result += msg[len(iv):]
            return result


if __name__ == '__main__':
    ob = Crypto('p21234', msg='Zakodowasdgjholhsd')
    encrypted = ob.encrypt()
    #print(encrypted)
    ob2 = Crypto('p21234', enc_msg=encrypted)
    decrypted = ob2.decrypt()
    print(decrypted)
