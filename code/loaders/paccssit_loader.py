import os
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - data-set (parent directory)
#       - PACCSS-IT.txt
#       - README
class PaCCSSIT_Loader(CorpusLoader):
    def load(self, path):
        paccssit = Corpus([], word_tokenizer=ToktokTokenizer(), name="PaCCSS-IT Corpus", language="Italian")
        self.create_paccssit_document(path, paccssit)
        return [paccssit]

    def create_paccssit_document(self, path, corpus):
        original_sents = []
        simple_sents = []
    
        paccssit_lines = []
        with open(os.path.join(path, 'PACCSS-IT.txt'), 'r') as file:
            paccssit_lines = file.readlines()

        for line in paccssit_lines[1:]:
            sents=line.split('\t')
            original_sents.append(sents[0].strip('\n'))
            simple_sents.append(sents[1].strip('\n'))

        o_to_s_alignment = [[i] for i in range(len(simple_sents))]
        s_to_o_alignment = [[i] for i in range(len(original_sents))]

        assert len(simple_sents) == len(original_sents)
        assert len(s_to_o_alignment) == len(o_to_s_alignment)

        corpus.documents.append(AlignedParallelDocument('sentence', original_sents, simple_sents, o_to_s_alignment, s_to_o_alignment, 'PaCCSS-IT'))
        
        