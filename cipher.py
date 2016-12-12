"""
Shion Fukuzawa (sf27)

"""


class Cipher:
    """
    Cipher base class.
    Implements the main constructor, string method,
    and empty encrypt/decrypt methods.
    """

    def __init__(self):
        """

        """
        pass

    def encrypt(self, text):
        """
        :param text: A string of the message to encrypt.
        :return: The encrypted text as a string.
        """
        print("Encrypting '" + text + "'...")
        pass

    def decrypt(self, text, key=None):
        """
        Uses the cipher's decryption method to decrypt the text
        :param text:
        :param key:
        :return:
        """
        print("Decrypting '" + text + "'...")
        pass

if __name__ == "__main__":
    c = Cipher()
    c.encrypt("Hello")
    c.decrypt("Onomatopoeia")