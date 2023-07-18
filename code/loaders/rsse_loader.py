import os
import csv
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - RuSimpleSentEval (parent directory)
#       - sents
#           - dev_sents.csv
#           - public_test_sents.csv
#       - test_only
#           - public_test_only.csv
#           - hidden_test_only.csv
class RSSE_Loader(CorpusLoader):
    def load(self, path):
        output = []

        dev = Corpus([], word_tokenizer=ToktokTokenizer(), name='RSSE Dev Corpus', language='Russian')
        test = Corpus([], word_tokenizer=ToktokTokenizer(), name='RSSE Test Corpus', language='Russian')

        self.load_rsse_directory(path, dev, test)

        if (not self.keep_train_test_split):
            rsse = Corpus(dev.documents + test.documents, word_tokenizer=ToktokTokenizer(), name='RSSE Corpus', language='Russian')
            output = [rsse]
        else:
            output = [dev, test]
        
        return output

    def load_rsse_directory(self, path, dev_corpus, test_corpus):
        self.load_rsse_file(os.path.join(path, 'sents', 'dev_sents.csv'), dev_corpus, name='RSSE Dev')
        self.load_rsse_file(os.path.join(path, 'sents', 'public_test_sents.csv'), test_corpus, name='RSSE Test')

    def load_rsse_file(self, path, corpus, name=''):
        original_sents = []
        simple_sents = []

        with open(path, newline='') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for i, row in enumerate(csvreader):
                original_sents.append(row[1].strip('\n'))
                simple_sents.append(row[2].strip('\n'))
        
        original_sents = original_sents[1:]
        simple_sents = simple_sents[1:]

        o_to_s_alignment = [[i] for i in range(len(simple_sents))]
        s_to_o_alignment = [[i] for i in range(len(original_sents))]

        assert len(simple_sents) == len(original_sents)
        assert len(s_to_o_alignment) == len(o_to_s_alignment)

        corpus.documents.append(AlignedParallelDocument('sentence', original_sents, simple_sents, o_to_s_alignment, s_to_o_alignment, name=name))