from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto import Random
import sys
import struct
import hashlib

class Crypto(object):
    def __init__(self, message, password):
        self.message = message
        self.password = password
        self.encrypted_message = None
        self.sha_passw = None

    @property
    def _sha_passw(self):
        """
            Transforms password by SHA-256 cryptografic 
            hash algorithm.

            Returns:
                sha_pass(string): created password
                
        """
        if self.sha_passw is None:
            h = hashlib.sha256(b'%s' % self.message)
            self.sha_passw = h.digest()

        return self.sha_passw

    @property
    def _encrypted_message(self):
        """
            Encryption of given text message
            Performed by AES algorithm
        """
        if self.encrypted_message is None:
            key = b'%s' % self._sha_passw
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            msg = iv + cipher.encrypt(b'%s' % self.message)
        return msg

    def decrypt(self):
        """
            Decryption of encrypted message.
            Performed by AES algoritm.
        """
        pass


if __name__ == '__main__':
    ob = Crypto('abcd', 'pa')
    print(ob._encrypted_message)
