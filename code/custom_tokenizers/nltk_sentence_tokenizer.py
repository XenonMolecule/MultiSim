import nltk

class NLTKSentenceTokenizer:

    # Tokenize a paragraph into several sentences (for counting sentences in a paragraph
    #     aligned corpus for example)
    #
    # Parameters: 
    #  - paragraph (string): a paragraph that needs to be tokenized into sentences
    # Returns:
    #  - sentences (list[string]): a list of sentences produced by tokenizing the paragraph
    def tokenize(self, paragraph):
        return nltk.sent_tokenize(paragraph)
