

class Analyzer:
    def __init__(self):
        self.text = ""
        self.letter_dict = {}
        self.pair_dict = {}

    def letter_count(self, text):
        """

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