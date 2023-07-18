import os

from datatypes import MultiRefDocument, CorpusLoader, Corpus
from custom_tokenizers.urdu_tokenizer import UrduTokenizer

# Expecting Corpus in the following format
# This is the version of SimplifyUR to load for training/evaluating a machine learning model,
# but for statistical measures USE SimplifyUR_Loader!!!!!!
#   - SimplifyUR (parent directory)
#       - Complex.txt
#       - Simplified.txt
class SimplifyUR_MultiRefLoader(CorpusLoader):
    def load(self, path):
        simplify_ur = Corpus([], word_tokenizer=UrduTokenizer(), name="SimplifyUR", language='Urdu')
        self.load_simplify_ur_directory_multiref(path, simplify_ur)
        return [simplify_ur]

    def load_simplify_ur_directory_multiref(self, path, corpus):
        complex_sents = []
        with open(os.path.join(path, 'Complex.txt'), 'r') as complex:
            complex_sents = complex.read().split('--')
        complex_sents[0] = complex_sents[0][1:]
        complex_sents = [sent.replace('\n', '') for sent in complex_sents]

        simple_sents = []
        with open(os.path.join(path, 'Simplified.txt'), 'r') as simple:
            simple_sents = simple.read().split('--')
        simple_sents = [simple.split('\n') for simple in simple_sents]
        simple_sents[0][0] = simple_sents[0][0][1:]
        for i, group in enumerate(simple_sents):
            simple_sents[i] = [sent for sent in group if sent!='']
        
        complex_sents = complex_sents[:-1]
        simple_sents = simple_sents[:-1]

        final_orig_sents = []
        final_simp_sents = []
        for i, simplifications in enumerate(simple_sents):
            final_orig_sents.append(complex_sents[i].strip('\n'))
            final_simp_sents.append([simplification.strip('\n') for simplification in simplifications])

        assert len(final_simp_sents) == len(final_orig_sents)

        corpus.documents.append(MultiRefDocument('sentence', final_orig_sents, final_simp_sents, name='SimplifyUR'))