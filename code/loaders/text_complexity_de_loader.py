import os
import pandas as pd
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, Corpus, CorpusLoader

# Expecting Corpus in the following format
#   - TextComplexityDE (parent directory)
#       - web_22
#       - TextComplexityDE19
#           - source.csv
#           - ratings.csv
#           - parallel_corpus.csv
#           - TextComplexityDE19.xlsx
#       - README.md
#       - LICENSE
class TextComplexityDELoader(CorpusLoader):
    def load(self, path):
        text_complexity_de = Corpus([], word_tokenizer=ToktokTokenizer(), name='TextComplexityDE Parallel Corpus', language='German')
        self.load_text_complexity_de_file(os.path.join(path,'TextComplexityDE19','TextComplexityDE19.xlsx'), text_complexity_de)
        return [text_complexity_de]
    
    def load_text_complexity_de_file(self, path, corpus):
        xlsx = pd.ExcelFile(path)
        parallel_corpus = pd.read_excel(xlsx, 'Selected_valid_simplifications')

        article_ids = parallel_corpus['Article_ID'].to_list()
        article_names = parallel_corpus['Article'].to_list()
        original = parallel_corpus['Original_Sentence'].to_list()
        simplified = parallel_corpus['Simplification'].to_list()

        current_original = []
        current_simplified = []
        last_id = 1
        for id, article, orig, simp in zip(article_ids, article_names, original, simplified):
            if id != last_id:
                o_to_s = [[i] for i in range(len(current_simplified))]
                s_to_o = [[i] for i in range(len(current_original))]
                corpus.documents.append(AlignedParallelDocument('sentence', current_original, current_simplified, o_to_s, s_to_o, name=article))
                current_original = []
                current_simplified = []
            current_original.append(orig.strip('\n'))
            current_simplified.append(simp.strip('\n'))
            last_id = id
        o_to_s = [[i] for i in range(len(current_simplified))]
        s_to_o = [[i] for i in range(len(current_original))]
        corpus.documents.append(AlignedParallelDocument('sentence', current_original, current_simplified, o_to_s, s_to_o, name=article[-1]))