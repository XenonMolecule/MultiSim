import os
from nltk.tokenize.toktok import ToktokTokenizer
from custom_tokenizers.nltk_sentence_tokenizer import NLTKSentenceTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - corpus_coling (parent directory)
#       - clear.valid.dst
#       - clear.train.dst
#       - clear.test.dst
#       - clear.valid.src
#       - clear.train.src
#       - clear.test.src
class CLEARLoader(CorpusLoader):
    def __init__(self, keep_train_test_split=False, keep_subdivisions=False, prefix='clear', name='CLEAR', allow_sentence_splits=False):
        self.keep_train_test_split = keep_train_test_split # if the dataset has provided a train/test split return separate train/test corpora from the original split
        self.keep_subdivisions = keep_subdivisions # if the dataset was organized in some way keep the organization based on those divisions
        self.prefix = prefix # leave this as clear to load the clear corpus!! (Used because Wiki Large FR has same format so loader can be shared)
        self.name = name # Name for naming the corpus purposes
        self.allow_sentence_splits = allow_sentence_splits # Can the dataset be m:n (meaning the sentences can be sentence groups)

    def load(self, path):
        output = []

        train = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name=self.name + " Train", language = "French")
        validation = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name=self.name + " Validation", language = "French")
        test = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name=self.name + " Test", language = "French")

        self.load_clear_directory(path, train, validation, test)

        if (self.keep_train_test_split):
            output = [train, validation, test]
        else:
            clear = Corpus(train.documents + validation.documents + test.documents, word_tokenizer=ToktokTokenizer(), name=self.name + " Corpus", language= "French")
            output = [clear]

        return output

    def load_clear_directory(self, path, train_corpus, valid_corpus, test_corpus):
        train_corpus.documents.append(self.create_clear_file(path, 'train', train_corpus))
        valid_corpus.documents.append(self.create_clear_file(path, 'valid', valid_corpus))
        test_corpus.documents.append(self.create_clear_file(path, 'test', test_corpus))

    def create_clear_file(self, path, suffix, corpus):
        original_sents = []
        simple_sents = []

        with open(os.path.join(path, self.prefix+'.'+suffix+'.src'), 'r') as file:
            original_sents = file.readlines()
            original_sents = [sent[:-1] for sent in original_sents]

        with open(os.path.join(path, self.prefix+'.'+suffix+'.dst'), 'r') as file:
            simple_sents = file.readlines()
            simple_sents = [sent[:-1] for sent in simple_sents]

        if not self.allow_sentence_splits:
            o_to_s_mapping = [[i] for i in range(len(simple_sents))]
            s_to_o_mapping = [[i] for i in range(len(original_sents))]

            assert len(simple_sents) == len(original_sents)
            assert len(o_to_s_mapping) == len(s_to_o_mapping)

            return AlignedParallelDocument('sentence', original_sents, simple_sents, o_to_s_mapping, s_to_o_mapping, name=self.prefix + ' ' + suffix)
        else:
            all_orig_sents, all_simple_sents = [], []
            o_to_s_mapping = []
            s_to_o_mapping = []
            o, s = 0, 0
            for orig, simp in zip(original_sents, simple_sents):
                original = corpus.sentence_tokenizer.tokenize(orig)
                simple = corpus.sentence_tokenizer.tokenize(simp)

                for o_sent in original:
                    o_map = list(range(s, s+len(simple)))
                    o_to_s_mapping.append(o_map)
                    all_orig_sents.append(o_sent.strip('\n'))
                for s_sent in simple:
                    s_map = list(range(o, o+len(original)))
                    s_to_o_mapping.append(s_map)
                    all_simple_sents.append(s_sent.strip('\n'))
                o+=len(original)
                s+=len(simple)
            
            return AlignedParallelDocument('sentence', all_orig_sents, all_simple_sents, o_to_s_mapping, s_to_o_mapping, name=self.prefix + ' ' + suffix)


        