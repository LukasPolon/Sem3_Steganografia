from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto import Random

class Crypto(object):
    def __init__(self, text, password):
        self.text = text
        self.password = password
        self.encrypted_text = None

    def sha_passw(self):
        """
            Transforms password by SHA-512 cryptografic 
            hash algorithm.

            Returns:
                sha_pass(string): created password
                
        """
        h = SHA512.new()
        h.update(b'%s' % self.password)
        return h.hexdigest()

    @property
    def _encrypted_text(self):
        """
            Encryption of given text message
        """

    def decrypt(self):
        pass


if __name__ == '__main__':
    ob = Crypto('abcd', 'pass')
    print(ob.sha_passw())
