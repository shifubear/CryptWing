#
# CS106 Final Project
# CryptWing
#
# Analyzer class that never got the chance to fully be utilized on the GUI... yet
#
# Shion Fukuzawa (sf27)
# December 15, 2016
#


class Analyzer:
    """
    Analyzer class
    Currently capable of:
        Counting letter frequency
    """
    def __init__(self):
        self.text = ""
        self.letter_dict = {}
        self.pair_dict = {}

    def letter_count(self, text):
        """
        Counts the number of seperate characters that exist in the file.
        :param text:
        :return:
        """
        self.letter_dict.clear()
        for letter in text:
            if letter in self.letter_dict.keys():
                self.letter_dict[letter] += 1
            else:
                self.letter_dict[letter] = 1
        print(self.letter_dict)

if __name__ == "__main__":
    a = Analyzer()
    a.letter_count("SHION FUKUZAWA")