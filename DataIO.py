import json


def load_words(filename="words_dictionary.json"):
    try:
        with open(filename, "r") as english_dictionary:
            valid_words = json.load(english_dictionary)
            return valid_words
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    a = load_words()
