import os
import json
from nltk.tokenize.toktok import ToktokTokenizer
import nltk

from datatypes import AlignedParallelDocument, Corpus, CorpusLoader

# Expecting Corpus in the following format
#   - text-simplification-slovene (parent directory)
#       - database
#           - evalvacijska.json
#           - testna.json
#           - ucna.json
class TextSimplificationSloveneLoader(CorpusLoader):
    def load(self, path):
        output = []

        train = Corpus([], word_tokenizer=ToktokTokenizer(), name="Text Simplification Slovene Train", language="Slovene")
        validation = Corpus([], word_tokenizer=ToktokTokenizer(), name="Text Simplification Slovene Validation", language="Slovene")
        test = Corpus([], word_tokenizer=ToktokTokenizer(), name="Text Simplification Slovene Test", language="Slovene")

        self.load_ts_slovene_file(os.path.join(path, "database", "ucna.json"), train, "train")
        self.load_ts_slovene_file(os.path.join(path, "database", "evalvacijska.json"), validation, "validation")
        self.load_ts_slovene_file(os.path.join(path, "database", "testna.json"), test, "test")

        if (self.keep_train_test_split):
            output = [train, validation, test]
        else:
            ts_slovene = Corpus(train.documents + validation.documents + test.documents, word_tokenizer=ToktokTokenizer(), name="Text Simplification Slovene", language="Slovene")
            output = [ts_slovene]

        return output

    def load_ts_slovene_file(self, path, corpus, name):
        data = []
        with open(path) as f:
            data = [line.strip() for line in f.readlines()]
        json_data = [json.loads(d) for d in data]
        original = []
        simple = []
        o_idx = 0
        o_to_s = []
        s_idx = 0
        s_to_o = []
        for item in json_data:
            origs = nltk.sent_tokenize(item['kompleksni'])
            original.extend(origs)
            o_indices = [o_idx + i for i in range(len(origs))]
            simps = nltk.sent_tokenize(item['enostavni'])
            simple.extend(simps)
            s_indices = [s_idx + i for i in range(len(simps))]
            for _ in range(len(origs)):
                o_to_s.append(s_indices)
            for _ in range(len(simps)):
                s_to_o.append(o_indices)
            o_idx += len(origs)
            s_idx += len(simps)
        corpus.documents.append(AlignedParallelDocument('sentence', original, simple, o_to_s, s_to_o, name=name))