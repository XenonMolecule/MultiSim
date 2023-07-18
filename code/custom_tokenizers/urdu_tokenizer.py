# Urduhack site: https://docs.urduhack.com/en/stable/about.html
import urduhack
from urduhack.tokenization import word_tokenizer

from datatypes import WordTokenizer

class UrduTokenizer(WordTokenizer):
    def __init__(self):
        urduhack.download()

    # Tokenize a sentence into several words (for counting words, word length, etc.)
    #
    # Parameters: 
    #  - sentence (string): a sentence that needs to be tokenized into words
    # Returns:
    #  - words (list[string]): a list of words produced by tokenizing the sentence
    def tokenize(self, sentence):
        return word_tokenizer(sentence)
        