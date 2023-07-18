import os
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus, ParallelDocument

# Expecting Corpus in the following format
#   - alector_corpus-master (parent directory)
#   - corpus
#       - 0_source.txt
#       - 0_target.txt
#       - 1_source.txt
#       - 1_target.txt
#       - ...
class AlectorLoader(CorpusLoader):
    def load(self, path):
        alector = Corpus([], word_tokenizer=ToktokTokenizer(), name="Alector Corpus", language="French")
        self.load_alector_directory(os.path.join(path, 'corpus'), alector)
        return [alector]

    def load_alector_directory(self, path, corpus):
        for filename in os.listdir(path):
            if '_target.txt' in filename:
                basename = filename[:-11]
                corpus.documents.append(self.create_alector_doc(os.path.join(path, basename + '_source.txt'), os.path.join(path, basename + '_target.txt'), basename))

    def create_alector_doc(self, orig_path, simp_path, name=''):
        original_sents = []
        with open(orig_path, 'r') as orig:
            original_sents = orig.readlines()
            original_sents = [origin.replace('\n', '').strip('\n') for origin in original_sents]

        simple_sents = []
        with open(simp_path, 'r') as simp:
            simple_sents = simp.readlines()
            simple_sents = [simple.replace('\n','').strip('\n') for simple in simple_sents]

        return ParallelDocument('sentence', original_sents, simple_sents, name)