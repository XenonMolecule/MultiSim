import os
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - APA_sentence-aligned_LHA
#       - A2-OR
#           - 0_2019_A2.simpde
#           - 0_2019.de
#           - ...
#       - B1-OR
#           - 1_2019_B1.simpde
#           - 1_2019.de
#           - ...
class GermanNewsLoader(CorpusLoader):
    def load(self, path):
        output = []

        a2 = Corpus([], word_tokenizer=ToktokTokenizer(), name="German News A2-OR", language="German")
        b1 = Corpus([], word_tokenizer=ToktokTokenizer(), name="German News B2-OR", language="German")

        self.load_german_news_directory(os.path.join(path,'A2-OR'), a2, 'A2-OR')
        self.load_german_news_directory(os.path.join(path,'B1-OR'), b1, 'B1-OR')

        if (not self.keep_subdivisions):
            german_news = Corpus(a2.documents + b1.documents, word_tokenizer=ToktokTokenizer(), name="German News Corpus", language="German")
            output = [german_news]
        else:
            output = [a2, b1]
        
        return output

    def load_german_news_directory(self, path, corpus, level='A2-OR'):
        for filename in os.listdir(path):
            if '.simpde' in filename:
                base_name = filename[:-10]
                corpus.documents.append(self.create_german_news_document(os.path.join(path,base_name+'.de'), os.path.join(path, filename), name=level+'/'+base_name))

    def create_german_news_document(self, original_path, simple_path, name=''):
        orig_sentences, simp_sentences = [], []
        o_to_s, s_to_o = [], []

        original_lines = []
        with open(original_path, 'r') as original:
            original_lines = original.readlines()
            original_lines = [line.replace('\n', '') for line in original_lines if line != '']

        simple_lines = []
        with open(simple_path, 'r') as simple:
            simple_lines = simple.readlines()
            simple_lines = [line.replace('\n', '') for line in simple_lines if line != '']

        assert len(original_lines) == len(simple_lines)

        o_idx, s_idx = 0, 0
        orig_indices, simp_indices = {}, {}
        for orig, simp in zip(original_lines, simple_lines):
            if orig not in orig_indices:
                orig_indices[orig] = o_idx
                orig_sentences.append(orig.strip('\n'))
                o_to_s.append([])
                o_idx += 1
            if simp not in simp_indices:
                simp_indices[simp] = s_idx
                simp_sentences.append(simp.strip('\n'))
                s_to_o.append([])
                s_idx += 1
            o_to_s[orig_indices[orig]].append(simp_indices[simp])
            s_to_o[simp_indices[simp]].append(orig_indices[orig])

        o_to_s = [sorted(align) for align in o_to_s]
        s_to_o = [sorted(align) for align in s_to_o]
        
        return AlignedParallelDocument('sentence', orig_sentences, simp_sentences, o_to_s, s_to_o, name)