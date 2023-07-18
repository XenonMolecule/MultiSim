import os
import pandas as pd

from custom_tokenizers.japanese_tokenizer import JapaneseTokenizer
from datatypes import AlignedParallelDocument, Corpus, CorpusLoader

# Expecting Corpus in the following format
#   - EasyJapaneseExtended
#       - T23-2020.1.7.xlsx
class EasyJapaneseExtendedLoader(CorpusLoader):
    def load(self, path):
        output=[]

        easy_jp_ext_main = Corpus([], word_tokenizer=JapaneseTokenizer(), name="Easy Japanese Extended Main", language="Japanese")
        easy_jp_ext_eval = Corpus([], word_tokenizer=JapaneseTokenizer(), name="Easy Japanese Extended Eval", language="Japanese")

        self.load_easy_japanese_ext_file(os.path.join(path, 'T23-2020.1.7.xlsx'), easy_jp_ext_main, easy_jp_ext_eval)

        if (not self.keep_subdivisions):
            easy_jp_ext = Corpus(easy_jp_ext_main.documents + easy_jp_ext_eval.documents, word_tokenizer=JapaneseTokenizer(), name="Easy Japanese Extended", language="Japanese")
            output = [easy_jp_ext]
        else:
            output = [easy_jp_ext_main, easy_jp_ext_eval]
        return output

    def load_easy_japanese_ext_file(self, path, corpus_main, corpus_eval):
        df = pd.ExcelFile(path)
        self.load_easy_japanese_ext_main(pd.read_excel(df, '平易化コーパス'), corpus_main)
        self.load_easy_japanese_ext_eval(pd.read_excel(df, '評価用'), corpus_eval)
        
    def load_easy_japanese_ext_main(self, main_df, corpus):
        original_sents = main_df['#日本語(原文)'].to_list()
        simple_sents = main_df['#やさしい日本語'].to_list()

        o_to_s = [[i] for i in range(len(simple_sents))]
        s_to_o = [[i] for i in range(len(original_sents))]

        corpus.documents.append(AlignedParallelDocument('sentence', original_sents, simple_sents, o_to_s, s_to_o, name="Easy Japanese Extended Main"))

    def load_easy_japanese_ext_eval(self, eval_df, corpus):
        original = eval_df['#日本語(原文)'].to_list()
        Ab = eval_df['Ab'].to_list()
        Ac = eval_df['Ac'].to_list()
        Af = eval_df['Af'].to_list()
        Ae = eval_df['Ae'].to_list()
        Ah = eval_df['Ah'].to_list()
        Ak = eval_df['Ak'].to_list()
        Al = eval_df['Al'].to_list()
        simple = [Ab, Ac, Af, Ae, Ah, Ak, Al]

        original_sents = []
        simplified_sents = []

        for i, sent in enumerate(original):
            for j in range(len(simple)):
                original_sents.append(sent.strip('\n'))
                simplified_sents.append(simple[j][i].strip('\n'))
        
        o_to_s = [[i] for i in range(len(simplified_sents))]
        s_to_o = [[i] for i in range(len(original_sents))]

        corpus.documents.append(AlignedParallelDocument('sentence', original_sents, simplified_sents, o_to_s, s_to_o, name="Easy Japanese Extended Eval"))