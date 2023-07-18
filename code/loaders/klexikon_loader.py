import os
import json
from nltk.tokenize.toktok import ToktokTokenizer
import nltk

from datatypes import ParallelDocument, Corpus, CorpusLoader

# Expecting Corpus in the following format
#   - klexikon (parent directory)
#       - data
#           - test.json
#           - train.json
#           - validation.json
class KlexikonLoader(CorpusLoader):
    def load(self, path):
        output = []

        train = Corpus([], word_tokenizer=ToktokTokenizer(), name="Klexikon Train", language="German")
        validation = Corpus([], word_tokenizer=ToktokTokenizer(), name="Klexikon Validation", language="German")
        test = Corpus([], word_tokenizer=ToktokTokenizer(), name="Klexikon Test", language="German")

        self.load_klexikon_file(os.path.join(path, "data", "train.json"), train, "train")
        self.load_klexikon_file(os.path.join(path, "data", "validation.json"), validation, "validation")
        self.load_klexikon_file(os.path.join(path, "data", "test.json"), test, "test")

        if (self.keep_train_test_split):
            output = [train, validation, test]
        else:
            klexikon = Corpus(train.documents + validation.documents + test.documents, word_tokenizer=ToktokTokenizer(), name="Klexikon", language="German")
            output = [klexikon]

        return output

    def clean_sent_list(self, sents):
        return [sent.strip() for sent in sents if sent != '']

    def load_klexikon_file(self, path, corpus, name):
        data = []
        with open(path) as f:
            data = [line.strip() for line in f.readlines()]
        json_data = [json.loads(d) for d in data]

        for item in json_data:
            corpus.documents.append(ParallelDocument("sentence", self.clean_sent_list(item['wiki_sentences']), self.clean_sent_list(item['klexikon_sentences']), name=item["title"]))
        