import os
import csv
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - RuAdaptUnreleased (parent directory)
#       - c_b_sent.csv
#       - cats_out_sent.csv
#       - all_cats_out_sent.csv
#       - c_a_sent.csv
#       - b_a_sent.csv
class RuAdaptLoader(CorpusLoader):
    def load(self, path):
        output = []

        fairytales = Corpus([], word_tokenizer=ToktokTokenizer(), name="RuAdapt Fairytales", language="Russian")
        isslovar_c_b = Corpus([], word_tokenizer=ToktokTokenizer(), name="RuAdapt Encyclopedia B-C", language="Russian")
        isslovar_c_a = Corpus([], word_tokenizer=ToktokTokenizer(), name="RuAdapt Encyclopedia A-C", language="Russian")
        isslovar_b_a = Corpus([], word_tokenizer=ToktokTokenizer(), name="RuAdapt Encyclopedia A-B", language="Russian")
        literature = Corpus([], word_tokenizer=ToktokTokenizer(), name="RuAdapt Literature", language="Russian")

        self.load_ru_adapt_directory(path, fairytales, literature, isslovar_c_b, isslovar_c_a, isslovar_b_a)

        if(not self.keep_subdivisions):
            ru_adapt_docs = fairytales.documents + isslovar_c_b.documents + isslovar_c_a.documents + isslovar_b_a.documents + literature.documents
            ru_adapt = Corpus(ru_adapt_docs, word_tokenizer=ToktokTokenizer(), name="RuAdapt", language="Russian")
            output = [ru_adapt]
        else:
            output = [fairytales, isslovar_c_b, isslovar_c_a, isslovar_b_a, literature]
        
        return output

    def load_ru_adapt_directory(self, path, fairy, literature, c_b, c_a, b_a):
        self.build_ru_adapt_file(os.path.join(path, 'cats_out_sent.csv'), fairy)
        self.build_ru_adapt_file(os.path.join(path, 'all_cats_out_sent.csv'), literature)
        self.build_ru_adapt_file(os.path.join(path, 'c_b_sent.csv'),c_b)
        self.build_ru_adapt_file(os.path.join(path, 'c_a_sent.csv'),c_a)
        self.build_ru_adapt_file(os.path.join(path, 'b_a_sent.csv'),b_a)

    def build_ru_adapt_file(self, path, corpus):
        with open(path, newline='') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=',', quotechar='"')
            last_name = ''
            orig_sents, simp_sents = [], []
            orig_map, simp_map = {}, {}
            o_to_s, s_to_o = [], []
            o_idx, s_idx = 0, 0
            for i, row in enumerate(csvreader):
                if i==0:
                    continue
                name, simp, orig = row[0], row[2], row[5]
                if name != last_name and i!=1:
                    corpus.documents.append(AlignedParallelDocument('sentence', orig_sents, simp_sents, o_to_s, s_to_o, last_name))
                    orig_sents, simp_sents = [], []
                    orig_map, simp_map = {}, {}
                    o_to_s, s_to_o = [], []
                    o_idx, s_idx = 0, 0
                if orig not in orig_map:
                    orig_sents.append(orig.strip('\n'))
                    orig_map[orig] = o_idx
                    o_idx += 1
                    o_to_s.append([])
                if simp not in simp_map:
                    simp_sents.append(simp.strip('\n'))
                    simp_map[simp] = s_idx
                    s_idx += 1
                    s_to_o.append([])
                o_to_s[orig_map[orig]].append(simp_map[simp])
                s_to_o[simp_map[simp]].append(orig_map[orig])
                last_name = name
            corpus.documents.append(AlignedParallelDocument('sentence', orig_sents, simp_sents, o_to_s, s_to_o, last_name))
            
