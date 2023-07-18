from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import WordTokenizer

class PorSimplesTokenizer(WordTokenizer):

    def __init__(self):
        self.tokenizer_dict = {}
        self.toktok = ToktokTokenizer()

    def add_sentence(self, sentence, tokens):
        self.tokenizer_dict[sentence] = tokens

    def merge_tokenizer(self, tokenizer):
        self.tokenizer_dict.update(tokenizer)

    # Tokenize a sentence into several words (for counting words, word length, etc.)
    #
    # Parameters: 
    #  - sentence (string): a sentence that needs to be tokenized into words
    # Returns:
    #  - words (list[string]): a list of words produced by tokenizing the sentence
    def tokenize(self, sentence):
        tokens = self.tokenizer_dict.get(sentence)
        if tokens:
            return tokens
        else:
            return self.toktok.tokenize(sentence)