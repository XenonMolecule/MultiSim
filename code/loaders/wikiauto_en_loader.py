import os
from nltk.tokenize.toktok import ToktokTokenizer
import json
from tqdm import tqdm

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - wiki-auto-master (parent directory)
#       - wiki-auto-part-1-data.json
class WikiAutoENLoader(CorpusLoader):

    def load(self, path):
        output = []

        part1 = Corpus([], word_tokenizer=ToktokTokenizer(), name = "WikiAuto Part 1", language="English")
        part2 = Corpus([], word_tokenizer=ToktokTokenizer(), name = "WikiAuto Part 2", language="English")

        self.load_wikiauto_json(os.path.join(path, "wiki-auto-part-1-data.json"), part1)
        self.load_wikiauto_json(os.path.join(path, "wiki-auto-part-2-data.json"), part2)

        if (not self.keep_subdivisions):
            wiki_auto_documents = part1.documents + part2.documents
            wiki_auto = Corpus(wiki_auto_documents, word_tokenizer=ToktokTokenizer(), name="WikiAuto", language="English")
            output = [wiki_auto]
        else:
            output = [part1, part2]

        return output

    def load_wikiauto_json(self, path, wikiauto):
        f = open(path)

        data = json.load(f)

        for doc in tqdm(data):
            wikiauto.documents.append(self.create_wikiauto_doc(data[doc]))

        f.close()

    def create_wikiauto_doc(self, object):
        o_sentences, o_imap = self.build_sentence_mapping(object["normal"]["content"])
        s_sentences, s_imap = self.build_sentence_mapping(object["simple"]["content"])

        o_to_s_map = [[] for _ in range(len(o_sentences))]
        s_to_o_map = [[] for _ in range(len(s_sentences))]

        for alignment_pair in object["sentence_alignment"]:
            simpIndex = s_imap[alignment_pair[0]]
            origIndex = o_imap[alignment_pair[1]]

            o_to_s_map[origIndex].append(simpIndex)
            s_to_o_map[simpIndex].append(origIndex)
        
        return AlignedParallelDocument('sentence', o_sentences, s_sentences, o_to_s_map, s_to_o_map, object["normal"]["title"])


    def build_sentence_mapping(self, object):
        sentences = []
        indices = {}
        for key, sentence in object.items():
            indices[key] = len(sentences)
            sentences.append(sentence)
        return sentences, indices
