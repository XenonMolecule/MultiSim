import os

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus
from custom_tokenizers.urdu_tokenizer import UrduTokenizer

# Expecting Corpus in the following format
# This is the version of SimplifyUR to load for most statistical measures, but for 
# training/evaluating a machine learning model USE SimplifyUR_MultiRefLoader!!!!!!
#   - SimplifyUR (parent directory)
#       - Complex.txt
#       - Simplified.txt
class SimplifyUR_Loader(CorpusLoader):
    def __init__(self, keep_train_test_split=False, keep_subdivisions=False, allow_repeats=True):
        self.keep_train_test_split = keep_train_test_split # if the dataset has provided a train/test split return separate train/test corpora from the original split
        self.keep_subdivisions = keep_subdivisions # if the dataset was organized in some way keep the organization based on those divisions
        self.allow_repeats=allow_repeats # SimplifyUR has multiple simplifications of the same sentence.  Enable or disable this in the output

    def load(self, path):
        name_suffix = '' if self.allow_repeats else ' No Repeats'
        simplify_ur = Corpus([], word_tokenizer=UrduTokenizer(), name="SimplifyUR" + name_suffix, language='Urdu')
        self.load_simplify_ur_directory(path, simplify_ur, self.allow_repeats)
        return [simplify_ur]

    def load_simplify_ur_directory(self, path, corpus, allow_repeats=True):
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
            if not allow_repeats:
                final_orig_sents.append(complex_sents[i].strip('\n'))
                final_simp_sents.append(simplifications[0].strip('\n'))
            else:
                for simplification in simplifications:
                    final_orig_sents.append(complex_sents[i].strip('\n'))
                    final_simp_sents.append(simplification.strip('\n'))
        
        o_to_s_alignment = [[i] for i in range(len(final_simp_sents))]
        s_to_o_alignment = [[i] for i in range(len(final_orig_sents))]

        assert len(final_simp_sents) == len(final_orig_sents)
        assert len(s_to_o_alignment) == len(o_to_s_alignment)

        name_suffix = '' if self.allow_repeats else ' No Repeats'
        corpus.documents.append(AlignedParallelDocument('sentence', final_orig_sents, final_simp_sents, o_to_s_alignment, s_to_o_alignment, name='SimplifyUR' + name_suffix))