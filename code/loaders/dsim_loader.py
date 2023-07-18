import os
import re
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - DSim (parent directory)
#       - bitext_fin_t_new_split
#       - bitext_fin_t_new_mapping
#       - bitext_fin_s_new
class DSimLoader(CorpusLoader):
    def load(self, path):
        dsim = Corpus([], word_tokenizer=ToktokTokenizer(), name = "DSim Corpus", language="Danish")
        self.add_dsim_directory(path, dsim)
        return [dsim]

    def add_dsim_directory(self, path, corpus):
        orig_sents = self.parse_dsim_file(os.path.join(path, 'bitext_fin_s_new'))
        simp_sents = self.parse_dsim_file(os.path.join(path, 'bitext_fin_t_new_split'))
        o_to_s, s_to_o = self.create_dsim_alignment(os.path.join(path, 'bitext_fin_t_new_mapping'), len(orig_sents))

        assert len(s_to_o) == len(simp_sents)
        assert len(o_to_s) == len(orig_sents)
        assert s_to_o == self.create_opposite_alignment(o_to_s, len(simp_sents))
        
        corpus.documents.append(AlignedParallelDocument('sentence', orig_sents, simp_sents, o_to_s, s_to_o, 'DSim'))

    def parse_dsim_file(self, path):
        sentences = []
        with open(path, 'r') as file:
            pos_sentences = file.readlines()
            for pos_sentence in pos_sentences:
                sentence = ''.join(re.split(r"/[A-Z][A-Z]", pos_sentence))
                sentence = ''.join(re.split(r"/[A-Z]", sentence))
                sentence = sentence[:-1]
                sentences.append(sentence.strip('\n'))
        return sentences

    def create_dsim_alignment(self, path, num_original_sents):
        s_to_o = []
        with open(path, 'r') as file:
            s_to_o = file.readlines()
            s_to_o = [[int(num[:-1])-1] for num in s_to_o]
        o_to_s = self.create_opposite_alignment(s_to_o, num_original_sents)

        return o_to_s, s_to_o
    
    def create_opposite_alignment(self, alignment, num_sents_to_map):
        new_alignment = [[] for _ in range(num_sents_to_map)]
        for i, nums in enumerate(alignment):
            for num in nums:
                new_alignment[num].append(i)
        return new_alignment