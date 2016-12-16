"""


Algorithms referenced from
    http://practicalcryptography.com/
"""

from CryptWing.cipher import Cipher


class TranspositionCipher(Cipher):
    """
    Algorithm:
        The transposition cipher takes a string of letters, then uses the oddness/evenness of the index of
        each character to create two new strings, then merges them together to create the cipher text.
    Security:
        Low
        This cipher does not alter the letter frequency at all, so a simple letter frequency test will be
        enough to break it.
    """
    def encrypt(self, text, key=None):
        """
        Encrypts the text using the algorithm mentioned above.
        """
        text = "".join(text.split())
        even_chars = ""
        odd_chars = ""
        char_count = 0
        for ch in text:
            if char_count % 2 == 0:
                even_chars += ch
            else:
                odd_chars += ch
            char_count += 1
        return "%s%s" % (odd_chars, even_chars)

    def decrypt(self, plain_text, key=None):
        """
        Decryption is done by splitting the text in half, then taking a character from each string and
        combining those characters to bring back the plain text. A key is unnecessary, so even if something
        is passed, there will be no effect.
        :return: The cipher text taken through the decryption algorithm.
        """
        text = ""
        halflen = len(plain_text) // 2
        odd_chars = plain_text[:halflen]
        even_chars = plain_text[halflen:]
        for idx in range(len(odd_chars)):
            text += even_chars[idx]
            text += odd_chars[idx]
        return text


class CaesarCipher(Cipher):
    """
    Algorithm:
        The caesar cipher shifts the plaintext a certain number of characters. The integer key that is selected
        defines the number of characters the text is shifted.
    """

    def is_upper(self, char):
        return 64 < ord(char) < 91

    def is_lower(self, char):
        return 96 < ord(char) < 123

    def shift_char(self, char, key):

        # A = 65, Z = 90
        # a = 97, z = 122
        if self.is_upper(char):
            num = ord(char) + key
            if num > 90:
                num -= 26
        elif self.is_lower(char):
            num = ord(char) + key
            if num > 122:
                num -= 26
        else:
            return char
        return chr(num)

    def encrypt(self, text, key=None):
        """

        :param text:
        :param key:
        :return:
        """
        try:
            key = int(key)
        except:
            return "To use the caesar cipher, the key must be an integer."

        if isinstance(key, int):
            cipher_text = ""
            for c in text:
                cipher_text += self.shift_char(c, key)
            return cipher_text

    def decrypt(self, text, key=None):
        try:
            key = int(key)
        except:
            return "To use the caesar cipher, the key must be an integer."
        if isinstance(key, int):
            plain_text = ""
            for c in text:
                plain_text += self.shift_char(c, 26 - key)
            return plain_text


class ViginereCipher(Cipher):
    """
    Algorithm:
        The Viginere Cipher accepts a keyword as the key, then uses that to encrypt the message.
        To encrypt the plaintext, repeat the keyword above the plaintext, then shift the plaintext
        by number (of the corresponding key letter, converted to a number based on it's position in the
        alphabet.
        eg.
            [key]: sushi
            [plaintext]: Let's meet tonight in our usual meeting place.
            [Comparison]:sushi sush isushis us his ushis ushisus hisus
                         dy
    """

    def __init__(self):
        self.caesar = CaesarCipher()

    def key_to_int(self, key):
        key_list = []
        # ASCII
        #   0~9: 48~57
        #   A~Z: 65~90
        #   a~z: 97~122
        for c in key:
            if 48 <= ord(c) <= 57:
                key_list.append(ord(c) - 48)
            elif 65 <= ord(c) <= 90:
                key_list.append(ord(c) - 65)
            elif 97 <= ord(c) <= 122:
                key_list.append(ord(c) - 97)
            else:
                pass

        return key_list

    def encrypt(self, text, key=None):
        cipher_text = ""
        key_list = self.key_to_int(key)

        for i in range(0, len(text), len(key_list)):
            for j in range(len(key_list)):
                try:
                    cipher_text += self.caesar.encrypt(text[i + j], key_list[j])
                except IndexError:
                    break
        return cipher_text

    def decrypt(self, text, key=None):
        plain_text = ""
        keys = self.key_to_int(key)
        key_list = []
        for key in keys:
            key_list.append(26 - key)

        for i in range(0, len(text), len(key_list)):
            for j in range(len(key_list)):
                try:
                    plain_text += self.caesar.encrypt(text[i + j], key_list[j])
                except IndexError:
                    break
        return plain_text

if __name__ == "__main__":
    t = TranspositionCipher()
    print(t.encrypt("Hello my name is Shion Fukuzawa poop"))
    c = CaesarCipher()
    print(c.encrypt("Shion Fukuzawa", 17))
    print(c.encrypt("Victor Norman", "a"))
    print(c.decrypt("Jyzfe Wlblqrnr", 9))