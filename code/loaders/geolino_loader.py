import os
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - GEOLino (parent directory)
#       - README.md
#       - geolino.test.src
#       - geolino.test.tgt
#       - geolino.valid.src
#       - geolino.valid.tgt
class GEOLinoLoader(CorpusLoader):
    def load(self, path):
        output = []

        test = Corpus([], word_tokenizer=ToktokTokenizer(), name="GEOLino Test Corpus", language="German")
        valid = Corpus([], word_tokenizer=ToktokTokenizer(), name="GEOLino Validation Corpus", language="German")

        self.load_geolino_directory(path, valid, test)

        if (not self.keep_train_test_split):
            geolino = Corpus(test.documents + valid.documents, word_tokenizer=ToktokTokenizer(), name="GEOLino Corpus", language="German")
            output = [geolino]
        else:
            output = [test, valid]

        return output

    def load_geolino_directory(self, path, valid_corpus, test_corpus):
        valid_corpus.documents.append(self.create_geolino_file(path, 'valid'))
        test_corpus.documents.append(self.create_geolino_file(path, 'test'))

    def create_geolino_file(self, path, suffix):
        original_sents = []
        simple_sents = []

        with open(os.path.join(path, 'geolino.'+suffix+'.src'), 'r') as file:
            original_sents = file.readlines()
            original_sents = [sent[:-1].strip('\n') for sent in original_sents]

        with open(os.path.join(path, 'geolino.'+suffix+'.tgt'), 'r') as file:
            simple_sents = file.readlines()
            simple_sents = [sent[:-1].strip('\n') for sent in simple_sents]

        o_to_s_mapping = [[i] for i in range(len(simple_sents))]
        s_to_o_mapping = [[i] for i in range(len(original_sents))]

        assert len(simple_sents) == len(original_sents)
        assert len(o_to_s_mapping) == len(s_to_o_mapping)

        return AlignedParallelDocument('sentence', original_sents, simple_sents, o_to_s_mapping, s_to_o_mapping, name= 'GEOLino ' + suffix)