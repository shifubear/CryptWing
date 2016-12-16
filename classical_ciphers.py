#
# CS106 Final Project
# CryptWing
#
# classical ciphers
#
# Shion Fukuzawa (sf27)
# December 15, 2016
#
# This file includes the implementations of the Transposition, Caesar, Viginere, and Playfair ciphers.
#
# Algorithms referenced from
#    http://practicalcryptography.com/
#

from cipher import Cipher


class TranspositionCipher(Cipher):
    """
    Algorithm:
        The transposition cipher takes a string of letters, then uses the oddness/evenness of the index of
        each character to create two new strings, then merges them together to create the cipher text.
    Security:
        Low
        This cipher does not alter the letter frequency at all, so a simple letter frequency test will be
        enough to detect and break it.
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
    Security:
        Low
        Although the letter frequencies will be shifted, the frequency distribution will still be visible,
        and shifting the characters to match the general English frequency distribution will be enough to
        break it.
    """

    def is_upper(self, char):
        """
        Tests if a character is uppercase
        :return: Boolean
        """
        return 64 < ord(char) < 91

    def is_lower(self, char):
        """
        Tests if a character is lowercase
        :return: Boolean
        """
        return 96 < ord(char) < 123

    def shift_char(self, char, key):
        """
        Shifts a character down by [key] amount.
        :return: The shifted character
        """
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
        Encrypts the text with the key using the algorithm of the caesar cipher
        :return: Encrypted text
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
        """
        Decrypts the text with the key using the algorithm of the caesar cipher
        :return: The attempted decrypted text
        """
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

    Security:
        Low - Medium
        As an applied version of the caesar cipher, this cipher is definitely more secure than the caesar
        cipher. However, splitting the text in to multiples of certain indices will produce multiple strings
        with standard letter frequency distributions. Also, the key is generally a word, which makes it a
        bit easier to guess.
    """

    def __init__(self):
        """
        Creates instance of caesar cipher, because this cipher applies the caesar cipher's algorithm
        multiple times.
        """
        self.caesar = CaesarCipher()

    def key_to_int(self, key):
        """
        Converts the key string to a list of integers, because the caesar cipher only works with integer
        keys.
        :return: List of integers
        """
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
        """
        Encrypts the text using the key with the Viginere cipher
        :return: Encrypted text
        """
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
        """
        Decrypts the text using the key with the Viginere cipher
        :return: Attempted decrypted text
        """
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


class PlayfairCipher(Cipher):
    """
    Algorithm:
        Referenced from http://practicalcryptography.com/ciphers/classical-era/playfair/
        The 'key' for a playfair cipher is generally a word, for the sake of example we will choose 'monarchy'.
        This is then used to generate a 'key square'
        m o n a r
        c h y b d
        e f g i k
        l p q s t
        u v w x z
        Any sequence of 25 letters can be used as a key, so long as all letters are in it and there are no repeats.
        Note that there is no 'j', it is combined with 'i'. We now apply the encryption rules to encrypt the plaintext.

        1. Remove any punctuation or characters that are not present in the key square (this may mean spelling out
           numbers, punctuation etc.).
        2. Identify any double letters in the plaintext and replace the second occurence with an 'x'
           e.g. 'hammer' -> 'hamxer'.
        3. If the plaintext has an odd number of characters, append an 'x' to the end to make it even.
        4. Break the plaintext into pairs of letters, e.g. 'hamxer' -> 'ha mx er'
        5. The algorithm now works on each of the letter pairs.
        6. Locate the letters in the key square, (the examples given are using the key square above)
            a. If the letters are in different rows and columns, replace the pair with the letters on the same
               row respectively but at the other pair of corners of the rectangle defined by the original pair.
               The order is important – the first encrypted letter of the pair is the one that lies on the same
               row as the first plaintext letter. 'ha' -> 'bo', 'es' -> 'il'
            b. If the letters appear on the same row of the table, replace them with the letters to their
               immediate right respectively (wrapping around to the left side of the row if a letter in the
               original pair was on the right side of the row). 'ma' -> 'or', 'lp' -> 'pq'
            c. If the letters appear on the same column of the table, replace them with the letters
               immediately below respectively (wrapping around to the top side of the column if a letter in
               the original pair was on the bottom side of the column). 'rk' -> 'dt', 'pv' -> 'vo'
    Security:
        Medium
        As opposed to previous ciphers which encrypt each character, this cipher is a digraph cipher which
        means it encrypts two character pairs at a time. This makes searching for frequencies harder, because
        as opposed to the 26 possibilities a monograph cipher has, this cipher must be run through a digraph
        frequency test, yielding 26^2 possibilities.
    """

    def __init__(self):
        """
        Creates instance of list of alphabet, used later for comparison, and an empty key_square to be
        filled when necessary
        """
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', \
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.key_square = []

    def get_key_square(self):
        """
        :return: key square contents. For debugging purposes
        """
        return self.key_square

    def fill_key_square(self, key):
        """
        Fills key square using the given key.
        """
        temp_key_square = []
        for c in key:
            if c not in temp_key_square:
                temp_key_square.append(c)
        for c in self.alphabet:
            if c not in temp_key_square:
                temp_key_square.append(c)

        for i in range(0, 25, 5):
            key_row = []
            for j in range(5):
                try:
                    key_row.append(temp_key_square[i + j])
                except IndexError:
                    pass
            self.key_square.append(key_row)

    def find_pair(self, digraph, encrypting=True):
        """
        Searches the key_square for the corresponding pair of the pair.
        :param encrypting: Search changes depending on whether encrypting or decrypting.
        """
        char1 = digraph[0]
        char2 = digraph[1]

        # Coordinates of each char on the key_square
        char1_x = 0
        char1_y = 0
        char2_x = 0
        char2_y = 0

        for y in range(5):
            for x in range(5):
                if self.key_square[y][x] == char1:
                    char1_x = x
                    char1_y = y
                elif self.key_square[y][x] == char2:
                    char2_x = x
                    char2_y = y

        newchar1 = ''
        newchar2 = ''
        if char1_y != char2_y:  # If not on the same row
            if char1_x != char2_x:  # If not on the same column
                newchar1 = self.key_square[char1_y][char2_x]
                newchar2 = self.key_square[char2_y][char1_x]
            else:  # If on the same column
                if encrypting:
                    try:
                        newchar1 = self.key_square[char1_y + 1][char1_x]
                    except IndexError:
                        newchar1 = self.key_square[0][char1_x]
                    try:
                        newchar2 = self.key_square[char2_y + 1][char2_x]
                    except IndexError:
                        newchar2 = self.key_square[0][char2_x]
                else:  # IF decrypting
                    try:
                        newchar1 = self.key_square[char1_y - 1][char1_x]
                    except IndexError:
                        newchar1 = self.key_square[-1][char1_x]
                    try:
                        newchar2 = self.key_square[char2_y - 1][char2_x]
                    except IndexError:
                        newchar2 = self.key_square[-1][char2_x]
        else:  # If on the same row
            if encrypting:
                try:
                    newchar1 = self.key_square[char1_y][char1_x + 1]
                except IndexError:
                    newchar1 = self.key_square[char1_y][0]
                try:
                    newchar2 = self.key_square[char2_y][char2_x + 1]
                except IndexError:
                    newchar2 = self.key_square[char2_y][0]
            else:
                try:
                    newchar1 = self.key_square[char1_y][char1_x - 1]
                except IndexError:
                    newchar1 = self.key_square[char1_y][-1]
                try:
                    newchar2 = self.key_square[char2_y][char2_x - 1]
                except IndexError:
                    newchar2 = self.key_square[char2_y][-1]

        return newchar1 + newchar2


    def encrypt(self, text, key=None):
        """
        Encrypts the text with the key using the Playfair cipher
        """
        # Check if key is viable
        if len(key) > 25:
            return "Key is too long"

        # Generate key square
        text = "".join(text.split())
        self.fill_key_square(key)

        # Step 1
        junk = "!@#$%^&*()-_=+\|][}{';\":/.?><,`~1234567890"
        for char in junk:
            key = key.replace(char, "")

        # Step 2, 4
        digraphs = []
        for i in range(0, len(text), 2):
            try:
                digraphs.append(text[i] + text[i + 1])
            except IndexError:
                digraphs.append(text[i] + 'x')

        # Step 3
        for i in range(len(digraphs)):
            if digraphs[i][0] == digraphs[i][1]:
                digraphs[i] = digraphs[i][0] + 'x'

        cipher_text = ""
        # Step 5
        for pair in digraphs:
            # Step 6
            cipher_text += self.find_pair(pair, encrypting=True)

        return cipher_text

    def decrypt(self, text, key=None):
        """
        Decrypts the text using the key using the playfair cipher.
        """

        self.fill_key_square(key)

        digraphs = []
        for i in range(0, len(text), 2):
            try:
                digraphs.append(text[i] + text[i + 1])
            except IndexError:
                print("This was NOT encrypted using the Playfair cipher, or was modified after encryption.")

        plain_text = ""
        for pair in digraphs:
            plain_text += self.find_pair(pair, encrypting=False)

        return plain_text

if __name__ == "__main__":
    t = TranspositionCipher()
    print("TRANSPOSITION e:", t.encrypt("Hello my name is Shion Fukuzawa"))  # Returns elmnmiSinuuaaHloyaeshoFkzw
    print("TRANSPOSITION d:", t.decrypt("elmnmiSinuuaaHloyaeshoFkzw"))

    c = CaesarCipher()
    print("CAESAR e:", c.encrypt("Shion Fukuzawa", 17))  # Returns Jyzfe Wlblqrnr
    print("CAESAR e:", c.encrypt("Victor Norman", "a"))  # Returns error message to print on GUI
    print("CAESAR d:", c.decrypt("Jyzfe Wlblqrnr", 17))  # Returns Shion Fukuzawa

    v = ViginereCipher()
    print("VIGINERE e:", v.encrypt("How does this even work", 'mindblown'))  # Returns Twj ezso fpvv pjaa ebul
    print("VIGINERE d:", v.decrypt("Twj ezso fpvv pjaa ebul", 'mindblown'))

    p = PlayfairCipher()
    playfair_ctext = p.encrypt("Hello world", 'hacker')
    print("PLAYFAIR e:", playfair_ctext)
    playfair_ptext = p.decrypt(playfair_ctext, 'hacker')
    print("PLAYFAIR d:", playfair_ptext)
