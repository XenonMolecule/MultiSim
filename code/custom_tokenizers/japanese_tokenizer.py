# fugashi paper: https://aclanthology.org/2020.nlposs-1.7.pdf
import fugashi

from datatypes import WordTokenizer

class JapaneseTokenizer(WordTokenizer):

    def __init__(self):
        self.fugashi_tagger = fugashi.Tagger()

    # Tokenize a sentence into several words (for counting words, word length, etc.)
    #
    # Parameters: 
    #  - sentence (string): a sentence that needs to be tokenized into words
    # Returns:
    #  - words (list[string]): a list of words produced by tokenizing the sentence
    def tokenize(self, sentence):
        return [word.surface for word in self.fugashi_tagger(sentence)]
        