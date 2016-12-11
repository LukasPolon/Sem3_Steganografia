from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto import Random
import sys
import struct
import hashlib
import subprocess

class Crypto(object):
    def __init__(self, password, msg=None, enc_msg=None):
        self.password = password
        self.message = msg
        self.enc_message = enc_msg
        self.sha_passw = None
        self.pas_confirm = None

    @property
    def _sha_passw(self):
        """
            Transforms password by SHA-256 cryptografic 
            hash algorithm.

            Returns:
                sha_pass(string): created password
                
        """
        if self.sha_passw is None:
            h = hashlib.sha256(b'%s' % self.password)
            self.sha_passw = h.digest()

        return self.sha_passw

    def encrypt(self):
        """
            Encryption of given text message
            Performed by AES algorithm

            Returns:
                msg(str): encrypted message
        """
        if self.message is not None:
            print('password: ' + self._sha_passw)
            key = b'%s' % self._sha_passw
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            msg = iv + cipher.encrypt(b'%s' % self.message)

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
            print('password: ' + self._sha_passw)
            key = b'%s' % self._sha_passw
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            msg = cipher.decrypt(self.enc_message)
            return msg[len(iv):]


if __name__ == '__main__':
    ob = Crypto('p', msg='Zakodowana wiadomosc')
    encrypted = ob.encrypt()
    print(encrypted)
    ob2 = Crypto('p', enc_msg=encrypted)
    decrypted = ob2.decrypt()
    print(decrypted)
