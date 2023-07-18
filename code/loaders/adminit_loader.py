import os
from nltk.tokenize.toktok import ToktokTokenizer
from custom_tokenizers.nltk_sentence_tokenizer import NLTKSentenceTokenizer

import pandas as pd
from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - admin-It-main (parent directory)
#       - OP
#           - 182operation-comp.txt
#           - 182operation-simp.txt
#           - ...
#       - RD
#           - 127rewriting-comp.txt
#           - 127rewriting-simp.txt
#           - ...
#       - RS
#           - 0rewriting-comp.txt
#           - 0rewriting-simp.txt
#           - ...
class AdminItLoader(CorpusLoader):
    
    def load(self, path):
        output = []

        op = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name = "AdminIT Operations", language="Italian")
        rd = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name = "AdminIT Rewritten Sents", language="Italian")
        rs = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name = "AdminIT Rewritten Docs", language="Italian")

        self.load_split(os.path.join(path,'OP'), "OP", op)
        self.load_split(os.path.join(path,'RD'), "RD", rd)
        self.load_split(os.path.join(path,'RS'), "RS", rs)

        if (not self.keep_subdivisions):
            adminit = op.documents + rd.documents + rs.documents
            adminit = Corpus(adminit, sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name="AdminIT", language="Italian")
            output = [adminit]
        else:
            output = [op, rd, rs]

        return output

    def load_split(self, path, split, corpus):
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            # checking if it is a file
            if os.path.isfile(f):
                name = filename.split('-')
                if (name[1] == 'comp.txt'):
                    orig_sents = []
                    o_to_s = [[0]]
                    with open(f) as orig:
                        orig_sents.append(orig.readlines()[0].strip())
                    simp_sents = []
                    s_to_o = [[0]]
                    with open(os.path.join(path, name[0] + '-simp.txt')) as simp:
                        simp_sents.append(simp.readlines()[0].strip())
                    corpus.documents.append( \
                        AlignedParallelDocument(granularity="paragraph" if split == "RD" else "sentence",\
                            original_items=orig_sents,\
                            simplified_items=simp_sents,\
                            original_to_simplified_alignment=o_to_s,\
                            simplified_to_original_alignment=s_to_o,\
                            name=name[0]\
                        )\
                    )
