import random
import math

class SentenceTokenizer:

    # Tokenize a paragraph into several sentences (for counting sentences in a paragraph
    #     aligned corpus for example)
    #
    # Parameters: 
    #  - paragraph (string): a paragraph that needs to be tokenized into sentences
    # Returns:
    #  - sentences (list[string]): a list of sentences produced by tokenizing the paragraph
    def tokenize(self, paragraph):
        pass

class WordTokenizer:

    # Tokenize a sentence into several words (for counting words, word length, etc.)
    #
    # Parameters: 
    #  - sentence (string): a sentence that needs to be tokenized into words
    # Returns:
    #  - words (list[string]): a list of words produced by tokenizing the sentence
    def tokenize(self, sentence):
        pass

class CorpusGroup:
    def __init__(self, corpora, name="", language="", consolidate_for_large_analysis=False, sentence_tokenizer=SentenceTokenizer(), word_tokenizer=WordTokenizer()):
        self.corpora = corpora
        self.name = name
        self.language = language
        self.consolidate_for_large_analysis = consolidate_for_large_analysis # Should this group appear in aggregate analysis as one unit or separate corpora
        
        if not type(sentence_tokenizer) is SentenceTokenizer or len(self.corpora) == 0:
            self.sentence_tokenizer = sentence_tokenizer
        else:
            self.sentence_tokenizer = self.corpora[0].sentence_tokenizer
        
        if not type(word_tokenizer) is WordTokenizer or len(self.corpora) == 0:
            self.word_tokenizer = word_tokenizer
        else:
            self.word_tokenizer = self.corpora[0].word_tokenizer

    def get_grouped_corpus(self):
        docs = []
        for corpus in self.corpora:
            docs.extend(corpus.documents)
        return Corpus(docs, sentence_tokenizer=self.sentence_tokenizer, word_tokenizer=self.word_tokenizer, name=self.name, language=self.language)

class Corpus:
    def __init__(self, documents, sentence_tokenizer=SentenceTokenizer(), word_tokenizer=WordTokenizer(), name="", language=""):
        self.documents = documents
        self.sentence_tokenizer = sentence_tokenizer
        self.word_tokenizer = word_tokenizer
        self.name = name
        self.language = language
    
    # returns (training, test) where training and test are in the format (orig, simp)
    def get_training_test_split(self, ratio, seed=3600):
        assert ratio >= 0 and ratio <= 1
        if type(self.documents[0]) is MultiRefDocument:
            all_pairs = []
            for document in self.documents:
                assert type(document) is MultiRefDocument
                for orig, simp_refs in zip(document.original_items, document.simplified_references):
                    all_pairs.append((orig, simp_refs))
            random.Random(seed).shuffle(all_pairs)
            split_idx = math.floor(len(all_pairs) * ratio)
            train = all_pairs[:split_idx]
            test = all_pairs[split_idx:]
            return train, test
        else:
            all_pairs = []
            for document in self.documents:
                assert type(document) is AlignedParallelDocument
                all_pairs.extend(document.get_sentence_pairs())
            random.Random(seed).shuffle(all_pairs)
            split_idx = math.floor(len(all_pairs) * ratio)
            train = all_pairs[:split_idx]
            test = all_pairs[split_idx:]
            return train, test

class Document:
    def __init__(self, granularity, original_items, name=""):
        self.original_items = original_items # sentences or paragraphs
        self.granularity = granularity # "sentence" or "paragraph"
        self.name = name

class ParallelDocument(Document):
    def __init__(self, granularity, original_items, simplified_items, name=""):
        self.original_items = original_items
        self.simplified_items = simplified_items
        self.granularity = granularity
        self.name = name

class MultiRefDocument(Document):
    def __init__(self, granularity, original_items, simplified_references, name=""):
        self.original_items = original_items
        self.simplified_references = simplified_references # simplified references is a list of one or more simplifications for every original item
        self.granularity = granularity
        self.name = name

class AlignedParallelDocument(ParallelDocument):
    def __init__(self, granularity, original_items, simplified_items, original_to_simplified_alignment, simplified_to_original_alignment, name=""):
        self.original_items = original_items
        self.simplified_items = simplified_items
        self.granularity = granularity
        self.original_to_simplified_alignment = original_to_simplified_alignment
        self.simplified_to_original_alignment = simplified_to_original_alignment
        self.name = name

    def get_sentence_pairs(self):
        unvisited_original = list(range(len(self.original_items)))

        queue = []

        pairs = []
        while len(unvisited_original) > 0:
            queue = [unvisited_original[0]]
            original = []
            simplified = []
            iter_visited_orig = set()
            iter_visited_simp = set()
            while len(queue) > 0:
                curr_idx = queue.pop(0)
                if curr_idx in unvisited_original:
                    unvisited_original.remove(curr_idx)
                if curr_idx not in iter_visited_orig:
                    iter_visited_orig.add(curr_idx)
                    original.append(self.original_items[curr_idx])

                    mapping = self.original_to_simplified_alignment[curr_idx]
                    for simp_idx in mapping:
                        if simp_idx not in iter_visited_simp:
                            iter_visited_simp.add(simp_idx)
                            simplified.append(self.simplified_items[simp_idx])
                            simp_mapping = self.simplified_to_original_alignment[simp_idx]
                            for orig_idx in simp_mapping:
                                queue.append(orig_idx)
            orig = ''.join(original)
            simp = ''.join(simplified)
            if len(orig) > 0 and len(simp) > 0:
                pairs.append((orig, simp))
        return pairs

class CorpusLoader:
    def __init__(self, keep_train_test_split=False, keep_subdivisions=False):
        self.keep_train_test_split = keep_train_test_split # if the dataset has provided a train/test split return separate train/test corpora from the original split
        self.keep_subdivisions = keep_subdivisions # if the dataset was organized in some way keep the organization based on those divisions
    
    # Load a dataset into one or more corpora (Corpus class defined above)
    #
    # Parameters: 
    #  - path (string): path to the directory containing the corpus
    # Returns:
    #  - corpora (list[Corpora]): the list of all the corpora built from this dataset
    def load(self, path):
        pass