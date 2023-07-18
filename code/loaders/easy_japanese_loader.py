import os
import pandas as pd

from custom_tokenizers.japanese_tokenizer import JapaneseTokenizer
from datatypes import AlignedParallelDocument, Corpus, CorpusLoader

# Expecting Corpus in the following format
#   - EasyJapanese (parent directory)
#       - T15-2020.1.7.xlsx
class EasyJapaneseLoader(CorpusLoader):
    def load(self, path):
        easy_japanese = Corpus([], word_tokenizer=JapaneseTokenizer(), name="Easy Japanese Corpus", language="Japanese")
        self.load_easy_japanese_file(os.path.join(path,'T15-2020.1.7.xlsx'), easy_japanese)
        return [easy_japanese]

    def load_easy_japanese_file(self, path, corpus):
        df = pd.read_excel(path)
        
        original_sents = df['#日本語(原文)'].to_list()
        simple_sents = df['#やさしい日本語'].to_list()

        original_sents = [o_sent.strip('\n') for o_sent in original_sents]
        simple_sents = [s_sent.strip('\n') for s_sent in simple_sents]

        o_to_s = [[i] for i in range(len(simple_sents))]
        s_to_o = [[i] for i in range(len(original_sents))]

        corpus.documents.append(AlignedParallelDocument('sentence', original_sents, simple_sents, o_to_s, s_to_o, name='Easy Japanese'))