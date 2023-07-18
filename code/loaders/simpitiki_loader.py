import os
import xml.etree.ElementTree as ET

from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - simpitiki-master (parent directory)
#       - src
#           - ...
#       - corpus
#           - simpitiki-v1.xml
#           - simpitiki-v2.xml
class SimpitikiLoader(CorpusLoader):

    def load(self, path):
        output = []

        trento = Corpus([], word_tokenizer=ToktokTokenizer(), name="Simpitiki Trento", language="Italian")
        itwiki = Corpus([], word_tokenizer=ToktokTokenizer(), name="Simpitiki Italian Wikipedia", language="Italian")

        self.add_simpitiki_file(os.path.join(path, 'corpus/simpitiki-v2.xml'), trento, itwiki)

        if (not self.keep_subdivisions):
            simpitiki = Corpus(trento.documents + itwiki.documents, word_tokenizer=ToktokTokenizer(), name = "Simpitiki", language="Italian")
            output = [simpitiki]
        else:
            output = [trento, itwiki]
        
        return output

    def add_simpitiki_file(self, path, trento_corpus, itwiki_corpus):
        trento_orig_sentences = []
        trento_simp_sentences = []
        itwiki_orig_sentences = []
        itwiki_simp_sentences = []

        corpus = ET.parse(path).getroot()

        for simplification in corpus[1]:
            original = ''
            if (simplification[0].text):
                original = simplification[0].text.replace('<del>','').replace('</del>','')
            simple = ''
            if (simplification[1].text):
                simple = simplification[1].text.replace('<ins>','').replace('</ins>', '')
            
            if simplification.attrib['origin'] == 'tn':
                trento_orig_sentences.append(original.strip('\n'))
                trento_simp_sentences.append(simple.strip('\n'))
            else:
                itwiki_orig_sentences.append(original.strip('\n'))
                itwiki_simp_sentences.append(simple.strip('\n'))
            
        trento_o_to_s_mapping = list([i] for i in range(len(trento_simp_sentences)))
        trento_s_to_o_mapping = list([i] for i in range(len(trento_orig_sentences)))
        itwiki_o_to_s_mapping = list([i] for i in range(len(itwiki_simp_sentences)))
        itwiki_s_to_o_mapping = list([i] for i in range(len(itwiki_orig_sentences)))

        trento = AlignedParallelDocument('sentence', trento_orig_sentences, trento_simp_sentences, trento_o_to_s_mapping, trento_s_to_o_mapping, 'trento')
        itwiki = AlignedParallelDocument('sentence', itwiki_orig_sentences, itwiki_simp_sentences, itwiki_o_to_s_mapping, itwiki_s_to_o_mapping, 'itwiki')

        trento_corpus.documents.append(trento)
        itwiki_corpus.documents.append(itwiki)