import os
import csv
from custom_tokenizers.nltk_sentence_tokenizer import NLTKSentenceTokenizer
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - RuWikiLarge (parent directory)
#       - wiki_train_cleaned_translated_sd.csv
#       - wiki_test_cleaned_translated_sd.csv
#       - wiki_dev_cleaned_translated_sd.csv
class RuWikiLargeLoader(CorpusLoader):
    def __init__(self, keep_train_test_split=False, keep_subdivisions=False, allow_sentence_splits=True):
        self.keep_train_test_split = keep_train_test_split # if the dataset has provided a train/test split return separate train/test corpora from the original split
        self.keep_subdivisions = keep_subdivisions # if the dataset was organized in some way keep the organization based on those divisions
        self.allow_sentence_splits = allow_sentence_splits

    def load(self, path):
        output = []

        train = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(),word_tokenizer=ToktokTokenizer(), name="RuWikiLarge Train", language="Russian")
        test = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name="RuWikiLarge Test", language="Russian")
        dev = Corpus([], sentence_tokenizer=NLTKSentenceTokenizer(), word_tokenizer=ToktokTokenizer(), name="RuWikiLarge Dev", language="Russian")

        self.add_ru_wiki_large_directory(path, train, test, dev)

        if (not self.keep_train_test_split):
            ru_wiki_large = Corpus(train.documents + test.documents + dev.documents, word_tokenizer=ToktokTokenizer(), name="RuWikiLarge", language="Russian")
            output = [ru_wiki_large]
        else:
            output = [train, test, dev]

        return output

    def add_ru_wiki_large_directory(self, path, train, test, dev):
        train.documents.append(self.create_ru_wiki_large_document(os.path.join(path, 'wiki_train_cleaned_translated_sd.csv'), 'train', train))
        test.documents.append(self.create_ru_wiki_large_document(os.path.join(path, 'wiki_test_cleaned_translated_sd.csv'), 'test', test))
        dev.documents.append(self.create_ru_wiki_large_document(os.path.join(path, 'wiki_dev_cleaned_translated_sd.csv'), 'dev', dev))

    def create_ru_wiki_large_document(self, path, name='', corpus=None):
        original_sents = []
        simple_sents = []

        with open(path, newline='') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in csvreader:
                original_sents.append(row[3])
                simple_sents.append(row[4])

        original_sents = original_sents[1:]
        simple_sents = simple_sents[1:]

        if not self.allow_sentence_splits:
            o_to_s_alignment = [[i] for i in range(len(simple_sents))]
            s_to_o_alignment = [[i] for i in range(len(original_sents))]

            assert len(simple_sents) == len(original_sents)
            assert len(s_to_o_alignment) == len(o_to_s_alignment)

            return AlignedParallelDocument('sentence', original_sents, simple_sents, o_to_s_alignment, s_to_o_alignment, name=name)
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
            
            return AlignedParallelDocument('sentence', all_orig_sents, all_simple_sents, o_to_s_mapping, s_to_o_mapping, name=name)