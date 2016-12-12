from DENscytale.cipher import *


class TranspositionCipher(Cipher):

    def encrypt(self, text):
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
        text = ""
        halflen = len(plain_text) // 2
        odd_chars = plain_text[:halflen]
        even_chars = plain_text[halflen:]
        for idx in range(len(odd_chars)):
            text += even_chars[idx]
            text += odd_chars[idx]
        return text


if __name__ == "__main__":
    t = TranspositionCipher()
    print(t.encrypt("Hello my name is Shion Fukuzawa poop"))
    pass