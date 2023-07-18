from loaders.clear_loader import CLEARLoader
from datatypes import CorpusLoader

# Expecting Corpus in the following format
#   - corpus_coling (parent directory)
#       - FR.wiki.full.aner.ori.valid.dst
#       - FR.wiki.full.aner.ori.train.dst
#       - FR.wiki.full.aner.ori.test.dst
#       - FR.wiki.full.aner.ori.valid.src
#       - FR.wiki.full.aner.ori.train.src
#       - FR.wiki.full.aner.ori.test.src
class WikiLargeFRLoader(CLEARLoader):
    def __init__(self, keep_train_test_split=False, keep_subdivisions=False, prefix='FR.wiki.full.aner.ori', allow_sentence_splits=True):
        super().__init__(keep_train_test_split, keep_subdivisions, prefix, 'WikiLargeFR', allow_sentence_splits)