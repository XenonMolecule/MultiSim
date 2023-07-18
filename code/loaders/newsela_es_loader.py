import os
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import sent_tokenize
from fuzzywuzzy import process
from tqdm import tqdm

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - newsela_es (parent directory)
#       - newsela_es_documents
#           - 17century-selfies-spanish.es.0.txt
#           - 17century-selfies-spanish.es.1.txt
#           - 17century-selfies-spanish.es.2.txt
#           - ...
#       - newsela_es_aligned
#           - 17century-selfies-spanish.es.1.txt_ALIGNED_WITH_17century-selfies-spanish.es.0.txt
#           - 17century-selfies-spanish.es.2.txt_ALIGNED_WITH_17century-selfies-spanish.es.0.txt
#           - 17century-selfies-spanish.es.2.txt_ALIGNED_WITH_17century-selfies-spanish.es.1.txt
#           - ...
class NewselaESLoader(CorpusLoader):

    def load(self, path):
        output = []
        zero_to_one = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela ES 0-1", language="Spanish")
        one_to_two = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela ES 1-2", language="Spanish")
        two_to_three = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela ES 2-3", language="Spanish")
        three_to_four = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Newsela ES 3-4", language="Spanish")

        self.load_newsela_es_directory(path, zero_to_one, one_to_two, two_to_three, three_to_four)

        if (not self.keep_subdivisions):
            newsela_es_documents = zero_to_one.documents + one_to_two.documents + two_to_three.documents + three_to_four.documents
            newsela_es = Corpus(newsela_es_documents, word_tokenizer=ToktokTokenizer(), name="Newsela ES", language="Spanish")
            output = [newsela_es]
        else:
            output = [zero_to_one, one_to_two, two_to_three, three_to_four]
        
        return output
    
    def load_newsela_es_directory(self, path, z_o, o_t, t_t, t_f):
        corpora = [z_o, o_t, t_t, t_f]

        filenames = self.get_filename_list(os.path.join(path, 'newsela_es_documents'))
        for filename in tqdm(filenames):
            for i in range(4):
                o_sents, o_mapping = self.load_newsela_es_text_document(os.path.join(path, 'newsela_es_documents', filename + '.' + str(i) + '.txt'))
                s_sents, s_mapping = self.load_newsela_es_text_document(os.path.join(path, 'newsela_es_documents', filename + '.' + str(i+1) + '.txt'))
                o_to_s, s_to_o = self.build_newsela_es_alignment(os.path.join(path, 'newsela_es_aligned', filename + '.' + str(i+1) + '.txt_ALIGNED_WITH_'+filename+'.'+str(i)+'.txt'), o_mapping, o_sents, s_mapping, s_sents)
                corpora[i].documents.append(AlignedParallelDocument('sentence', o_sents, s_sents, o_to_s, s_to_o, name=filename + ' ' + str(i) + str(i+1)))

    def get_filename_list(self, path):
        file_set = set()
        file_list = []
        for filename in os.listdir(path):
            base_name = filename[:-6]
            if base_name not in file_set:
                file_list.append(base_name)
                file_set.add(base_name)
        return file_list

    def load_newsela_es_text_document(self, path):
        paragraphs = []
        with open(path, 'r') as file:
            paragraphs = file.read().split("\n\n")

        sentences = [] 
        for p in paragraphs:
            sents = sent_tokenize(p)
            sents = [s.strip('\n') for s in sents]
            sentences.extend(sents)
        
        sentence_mapping = {}
        for i, s in enumerate(sentences):
            sentence_mapping[s] = i
        
        return sentences, sentence_mapping

    def build_newsela_es_alignment(self, path, o_map, orig_sent, s_map, simp_sent):
        alignments = []
        with open(path, 'r') as file:
            alignments = [line for line in file.read().split('\n\n') if line != '']
        o_to_s = [[] for _ in range(len(orig_sent))]
        s_to_o = [[] for _ in range(len(simp_sent))]
        for alignment in alignments:
            a = alignment.split('\t')
            simp = a[1]
            orig = a[-1]

            exclude = ['> ', '.', '_', ' -']
            if (orig in exclude or simp in exclude):
                continue

            o_idx = -1
            try:
                o_idx = o_map[orig]
            except KeyError:
                o_idx = o_map[process.extractOne(orig, orig_sent)[0]]
            
            s_idx = -1
            try:
                s_idx = s_map[simp]
            except KeyError:
                s_idx = s_map[process.extractOne(simp, simp_sent)[0]]

            o_to_s[o_idx].append(s_idx)
            s_to_o[s_idx].append(o_idx)
        
        o_to_s = [sorted(a) for a in o_to_s]
        s_to_o = [sorted(a) for a in s_to_o]

        return o_to_s, s_to_o