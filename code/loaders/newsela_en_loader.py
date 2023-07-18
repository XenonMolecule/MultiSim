from nltk.tokenize.toktok import ToktokTokenizer
import json
from tqdm import tqdm

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - newsela-auto-all-data.json (only file)
# 
# If you downloaded the newsela dataset from the authors you can expect to find this folder in this directory:
#   - newsela-auto (parent directory)
#       - newsela-auto
#           - all_data
#               - newsela-auto-all-data.json
class NewselaENLoader(CorpusLoader):

    def load(self, path):
        output = []
        zero_to_one = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela EN 0-1", language="English")
        one_to_two = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela EN 1-2", language="English")
        two_to_three = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela EN 2-3", language="English")
        three_to_four = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela EN 3-4", language="English")

        self.load_newsela_en_json(path, zero_to_one, one_to_two, two_to_three, three_to_four)

        if (not self.keep_subdivisions):
            newsela_en_documents = zero_to_one.documents + one_to_two.documents + two_to_three.documents + three_to_four.documents
            newsela_en = Corpus(newsela_en_documents, word_tokenizer=ToktokTokenizer(), name="Newsela EN", language="English")
            output = [newsela_en]
        else:
            output = [zero_to_one, one_to_two, two_to_three, three_to_four]
        
        return output
    
    def load_newsela_en_json(self, path, z_o, o_t, t_t, t_f):
        corpora = [z_o, o_t, t_t, t_f]

        f = open(path)

        data = json.load(f)

        for doc in tqdm(data):
            sentences = []
            imaps = []
            o_to_s_maps = []
            s_to_o_maps = []
            for i in range(5):
                sents, indices = self.load_newsela_en_doc(data[doc][str(i)])
                sentences.append(sents)
                imaps.append(indices)
                if (i < 4):
                    o_to_s_maps.append([[] for _ in range(len(sents))])
                if (i > 0):
                    s_to_o_maps.append([[] for _ in range(len(sents))])
            
            for alignment_pair in data[doc]["sentence_alignment"]:
                _, lvlOrig, _, _ = alignment_pair[0][len(doc):].split("-")
                _, lvlSimp, _, _ = alignment_pair[1][len(doc):].split("-")
                lvlOrig = int(lvlOrig)
                lvlSimp = int(lvlSimp)
                if (int(lvlSimp)-int(lvlOrig) != 1):
                    continue

                origIndex = imaps[lvlOrig][alignment_pair[0]]
                simpIndex = imaps[lvlSimp][alignment_pair[1]]

                o_to_s_maps[lvlOrig][origIndex].append(simpIndex)
                s_to_o_maps[lvlOrig][simpIndex].append(origIndex)

            for i in range(len(corpora)):
                corpora[i].documents.append(AlignedParallelDocument('sentence', sentences[i], sentences[i+1], o_to_s_maps[i], s_to_o_maps[i], name=doc + str(i) + "-" + str(i+1)))

        f.close()

    def load_newsela_en_doc(self, object):
        sentences = []
        indices = {}
        for key, sentence in object.items():
            indices[key] = len(sentences)
            sentences.append(sentence)
        return sentences, indices