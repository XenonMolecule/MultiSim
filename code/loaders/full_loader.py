import os
from custom_tokenizers.japanese_tokenizer import JapaneseTokenizer
from datatypes import Corpus, CorpusGroup, CorpusLoader, WordTokenizer
from loaders.alector_loader import AlectorLoader
from loaders.cbst_loader import CBSTLoader
from loaders.clear_loader import CLEARLoader
from loaders.dsim_loader import DSimLoader
from loaders.easy_japanese_extended_loader import EasyJapaneseExtendedLoader
from loaders.easy_japanese_loader import EasyJapaneseLoader
from loaders.geolino_loader import GEOLinoLoader
from loaders.german_news_loader import GermanNewsLoader
from loaders.newsela_es_loader import NewselaESLoader
from loaders.paccssit_loader import PaCCSSIT_Loader
from loaders.rsse_loader import RSSE_Loader
from loaders.ru_adapt_loader import RuAdaptLoader
from loaders.ru_wiki_large_loader import RuWikiLargeLoader
from loaders.simpitiki_loader import SimpitikiLoader
from loaders.simple_german_loader import SimpleGermanLoader
from loaders.simplext_loader import SimplextLoader
from loaders.porsimples_loader import PorSimplesLoader
from loaders.simplify_ur_loader import SimplifyUR_Loader
from loaders.terence_teacher_loader import TerenceTeacherLoader
from loaders.text_complexity_de_loader import TextComplexityDELoader
from loaders.wiki_large_fr_loader import WikiLargeFRLoader
from loaders.newsela_en_loader import NewselaENLoader
from loaders.wikiauto_en_loader import WikiAutoENLoader
from loaders.asset_loader import AssetLoader
from loaders.adminit_loader import AdminItLoader
from loaders.klexikon_loader import KlexikonLoader
from loaders.ts_slovene_loader import TextSimplificationSloveneLoader

import pickle

# Expecting Corpus in the Following Format
#   - Corpora
#       -English
#           - newsela-auto
#               - newsela-auto
#                   -all_data
#                       - newsela-auto-all-data.json
#           - wiki-auto-master
#           - asset-main
#       - Spanish
#           - SimplextData
#           - newsela_es
#       - Basque
#           - CBST
#               - ETSC_CBST
#       - Brazilian Portuguese
#           - PorSimples
#       - Italian
#           - TerenceTeacher
#               - CORPORA_TEXT_SIMP
#           - SIMPITIKI
#               - simpitiki-master
#           - PaCCSS-IT
#               - data-set
#           - admin-It-main
#               - OP
#               - RD
#               - RS
#       - French
#           - corpus_coling
#           - alector_corpus-master
#       - Danish
#           - DSim
#       - German
#           - GEOLino
#           - TextComplexityDE
#           - APA_sentence-aligned_LHA
#           - Corpus_for_Text_Simplification_of_German
#       - Japanese
#           - EasyJapanese
#           - EasyJapaneseExtended
#       - Russian
#           - RuSimpleSentEval
#           - RuAdaptUnreleased
#           - RuWikiLarge
#       - Urdu
#           - SimplifyUR
class FullLoader(CorpusLoader):
    def __init__(self, path=""):
        if not 'corpora.pkl' in path:
            self.load(path)
            self.version = 0.0
        else:
            self.from_pickle(path)

    def load(self, path):
        self.simplext = SimplextLoader(keep_subdivisions=False).load(os.path.join(path,'Spanish', 'SimplextData'))[0]
        self.cbst_str, self.cbst_int = CBSTLoader(keep_subdivisions=True).load(os.path.join(path,'Basque','CBST', 'ETSC_CBST'))
        self.cbst = CorpusGroup([self.cbst_str, self.cbst_int], name="CBST", language="Basque", consolidate_for_large_analysis=False)
        self.porsimples_natural, self.porsimples_strong = PorSimplesLoader(keep_strong_natural_split=True, keep_subdivisions=False).load(os.path.join(path, 'Brazilian Portuguese', 'PorSimples'))
        self.porsimples = CorpusGroup([self.porsimples_natural, self.porsimples_strong], name="PorSimples", language="Brazilian Portuguese", consolidate_for_large_analysis=False)
        self.simpitiki_pa, self.simpitiki_itwiki = SimpitikiLoader(keep_subdivisions=True).load(os.path.join(path,'Italian', 'SIMPITIKI', 'simpitiki-master'))
        self.simpitiki = CorpusGroup([self.simpitiki_pa, self.simpitiki_itwiki], name="Simpitiki", language="Italian", consolidate_for_large_analysis=False)
        self.terence, self.teacher = TerenceTeacherLoader(keep_subdivisions=True).load(os.path.join(path,'Italian', 'TerenceTeacher', 'CORPORA_TEXT_SIMP'))
        self.terence_teacher = CorpusGroup([self.terence, self.teacher], name="TerenceTeacher", language="Italian", consolidate_for_large_analysis=False)
        self.paccssit = PaCCSSIT_Loader().load(os.path.join(path,'Italian','PaCCSS-IT','data-set'))[0]
        self.clear = CLEARLoader(keep_train_test_split=False).load(os.path.join(path,'French','corpus_coling'))[0]
        self.wiki_large_fr = WikiLargeFRLoader(keep_train_test_split=False).load(os.path.join(path,'French','corpus_coling'))[0]
        self.dsim = DSimLoader().load(os.path.join(path,'Danish','DSim'))[0]
        self.geolino = GEOLinoLoader(keep_train_test_split=False).load(os.path.join(path, 'German', 'GEOLino'))[0]
        self.easy_japanese = EasyJapaneseLoader().load(os.path.join(path, 'Japanese','EasyJapanese'))[0]
        self.easy_japanese_extended = EasyJapaneseExtendedLoader(keep_subdivisions=False).load(os.path.join(path, 'Japanese', 'EasyJapaneseExtended'))[0]
        self.text_complexity_de = TextComplexityDELoader().load(os.path.join(path, 'German', 'TextComplexityDE'))[0]
        self.rsse = RSSE_Loader(keep_train_test_split=False).load(os.path.join(path, 'Russian', 'RuSimpleSentEval'))[0]
        self.simplify_ur = SimplifyUR_Loader(allow_repeats=True).load(os.path.join(path,'Urdu','SimplifyUR'))[0]
        self.german_news_a2, self.german_news_b1 = GermanNewsLoader(keep_subdivisions=True).load(os.path.join(path, 'German', 'APA_sentence-aligned_LHA'))
        self.german_news = CorpusGroup([self.german_news_a2, self.german_news_b1], name="German News", language="German", consolidate_for_large_analysis=False)
        self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4 = NewselaESLoader(keep_subdivisions=True).load(os.path.join(path, 'Spanish','newsela_es'))
        self.newsela = CorpusGroup([self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4], name="Newsela ES", language="Spanish", consolidate_for_large_analysis=False)
        self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c, self.ru_adapt_ab, self.ru_adapt_literature =\
            RuAdaptLoader(keep_subdivisions=True).load(os.path.join(path,'Russian','RuAdaptUnreleased'))
        self.ru_adapt = CorpusGroup([self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c, self.ru_adapt_ab, self.ru_adapt_literature],\
            name="RuAdapt", language="Russian", consolidate_for_large_analysis=False)
        self.ru_adapt_ency = CorpusGroup([self.ru_adapt_ab, self.ru_adapt_a_c, self.ru_adapt_b_c],name="RuAdapt Ency", language="Russian", consolidate_for_large_analysis=True)
        self.simple_german = SimpleGermanLoader().load(os.path.join(path, 'German', 'Corpus_for_Text_Simplification_of_German'))[0]
        self.alector = AlectorLoader().load(os.path.join(path, 'French', 'alector_corpus-master'))[0]
        self.ru_wiki_large = RuWikiLargeLoader(keep_train_test_split=False).load(os.path.join(path,'Russian','RuWikiLarge'))[0]
        self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4 = NewselaENLoader(keep_subdivisions=True).load(os.path.join(path,'English', 'newsela-auto', 'newsela-auto', 'all_data','newsela-auto-all-data.json'))
        self.newsela_en = CorpusGroup([self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4], name="Newsela EN", language="English")
        self.wiki_auto_en = WikiAutoENLoader(keep_subdivisions=False).load(os.path.join(path, 'English', 'wiki-auto-master'))[0]
        self.asset = AssetLoader(keep_train_test_split=False).load(os.path.join(path, 'English', 'asset-main'))[0]
        self.adminit = AdminItLoader(keep_subdivisions=False).load(os.path.join(path, 'Italian', 'admin-It-main'))[0]
        self.klexikon = KlexikonLoader(keep_train_test_split=False).load(os.path.join(path, 'German', 'klexikon'))[0]
        self.slots = TextSimplificationSloveneLoader(keep_train_test_split=False).load(os.path.join(path, 'Slovene', 'text-simplification-slovene-main'))[0]

        self.spanish = CorpusGroup([self.simplext, self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4], name="Spanish", language="Spanish", consolidate_for_large_analysis=False)
        self.italian = CorpusGroup([self.terence, self.teacher, self.simpitiki_itwiki, self.adminit, self.paccssit], name="Italian", language="Italian", consolidate_for_large_analysis=False)
        self.french = CorpusGroup([self.clear, self.wiki_large_fr, self.alector], name="French", language="French", consolidate_for_large_analysis=False)
        self.japanese = CorpusGroup([self.easy_japanese, self.easy_japanese_extended], name="Japanese", language="Japanese", consolidate_for_large_analysis=False)
        self.brazilian_portuguese = CorpusGroup([self.porsimples_natural, self.porsimples_strong], name="Brazilian Portuguese", language="Brazilian Portuguese", consolidate_for_large_analysis=False)
        self.german = CorpusGroup([self.simple_german, self.text_complexity_de, self.geolino, self.german_news_a2, self.german_news_b1, self.klexikon], name="German", language="German", consolidate_for_large_analysis=False)
        self.basque = CorpusGroup([self.cbst_int, self.cbst_str], name="Basque", language="Basque", consolidate_for_large_analysis=False)
        self.danish = CorpusGroup([self.dsim], name="Danish", language="Danish", consolidate_for_large_analysis=False)
        self.urdu = CorpusGroup([self.simplify_ur], name="Urdu", language="Urdu", consolidate_for_large_analysis=False)
        self.russian = CorpusGroup([self.ru_wiki_large, self.rsse, self.ru_adapt_literature, self.ru_adapt_fairy, self.ru_adapt_ab, self.ru_adapt_a_c, self.ru_adapt_b_c], name="Russian", language="Russian", consolidate_for_large_analysis=False)
        self.english = CorpusGroup([self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.asset], name="English", language="English", consolidate_for_large_analysis=False)
        self.slovene = CorpusGroup([self.slots], name="Slovene", language="Slovene", consolidate_for_large_analysis=False)

        return [self.newsela_en_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4, self.wiki_auto_en, self.asset, self.simplext, self.cbst_str, 
            self.cbst_int, self.porsimples_natural, self.porsimples_strong, self.adminit, self.simpitiki_itwiki,\
            self.terence, self.teacher, self.paccssit, self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese,\
            self.easy_japanese_extended, self.text_complexity_de, self.rsse, self.simplify_ur, self.german_news_a2, self.german_news_b1,\
            self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4, self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c,\
            self.ru_adapt_ab, self.ru_adapt_literature, self.simple_german, self.alector, self.ru_wiki_large, self.klexikon, self.slots]

    def get_all_corpora_raw(self):
        return [self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.asset, self.simplext,\
            self.cbst_str, self.cbst_int, self.porsimples_natural, self.porsimples_strong, self.adminit, self.simpitiki_itwiki,\
            self.terence, self.teacher, self.paccssit, self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese,\
            self.easy_japanese_extended, self.text_complexity_de, self.rsse, self.simplify_ur, self.german_news_a2, self.german_news_b1,\
            self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4, self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c,\
            self.ru_adapt_ab, self.ru_adapt_literature, self.simple_german, self.alector, self.ru_wiki_large, self.klexikon, self.slots]

    def get_all_corpora(self):
        return [self.newsela_en, self.wiki_auto_en, self.asset, self.simplext, self.cbst, self.porsimples, self.simpitiki, self.terence_teacher, self.paccssit,\
            self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese, self.easy_japanese_extended, self.text_complexity_de,\
            self.rsse, self.simplify_ur, self.german_news, self.newsela, self.ru_adapt, self.simple_german, self.alector, self.ru_wiki_large, self.klexikon, self.slots, self.adminit]

    def get_doc_aligned_raw(self):
        return [self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.asset, self.simplext, 
            self.cbst_str, self.cbst_int, self.porsimples_natural, self.porsimples_strong, self.terence, self.teacher,\
            self.text_complexity_de, self.german_news_a2, self.german_news_b1, self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4,\
            self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c, self.ru_adapt_ab, self.ru_adapt_literature, self.simple_german, self.alector, self.klexikon]

    def get_doc_aligned(self):
        return [self.newsela_en, self.wiki_auto_en, self.simplext, self.cbst, self.porsimples, self.terence_teacher, self.text_complexity_de,\
            self.german_news, self.newsela, self.ru_adapt, self.simple_german, self.alector, self.klexikon]

    def get_sentence_aligned_raw(self):
        return [self.asset, self.adminit, self.simpitiki_itwiki, self.paccssit, self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese,\
            self.easy_japanese_extended, self.rsse, self.simplify_ur, self.ru_wiki_large, self.slots]

    def get_sentence_aligned(self):
        return [self.asset, self.simpitiki, self.paccssit, self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese, self.easy_japanese_extended,\
            self.rsse, self.ru_wiki_large, self.slots]

    def get_aligned_raw(self):
        return [self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.asset, self.simplext,\
            self.cbst_str, self.cbst_int, self.porsimples_natural, self.porsimples_strong, self.adminit, self.simpitiki_itwiki,\
            self.terence, self.teacher, self.paccssit, self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese,\
            self.easy_japanese_extended, self.text_complexity_de, self.rsse, self.simplify_ur, self.german_news_a2, self.german_news_b1,\
            self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4, self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c,\
            self.ru_adapt_ab, self.ru_adapt_literature, self.ru_wiki_large, self.slots]

    def get_aligned(self):
        return [self.newsela_en, self.wiki_auto_en, self.asset, self.simplext, self.cbst, self.porsimples, self.simpitiki, self.terence_teacher,\
            self.paccssit, self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese, self.easy_japanese_extended,\
            self.text_complexity_de, self.rsse, self.simplify_ur, self.german_news, self.newsela, self.ru_adapt, self.ru_wiki_large, self.slots]

    def get_all_corpora_language_grouping(self):
        return [self.english, self.spanish, self.italian, self.french, self.japanese, self.brazilian_portuguese, self.german, self.basque, self.danish, self.urdu, self.russian, self.slovene]

    def get_all_corpora_raw_paper_order(self):
        return [self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.asset, self.simplext,\
            self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4, self.terence, self.teacher, self.simpitiki_itwiki,\
            self.adminit, self.paccssit, self.clear, self.wiki_large_fr, self.alector, self.easy_japanese, self.easy_japanese_extended, self.porsimples_natural,\
            self.porsimples_strong, self.simple_german, self.text_complexity_de, self.geolino, self.german_news_a2, self.german_news_b1, self.cbst_int, self.cbst_str,\
            self.dsim, self.simplify_ur, self.ru_wiki_large, self.rsse, self.ru_adapt_literature, self.ru_adapt_fairy, self.ru_adapt_ab, self.ru_adapt_a_c, self.ru_adapt_b_c]

    def get_all_doc_aligned_sent_aligned_raw_paper_order(self):
        return [self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.simplext,\
            self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4, self.terence, self.teacher, self.porsimples_natural,\
            self.porsimples_strong, self.text_complexity_de, self.simple_german, self.german_news_a2, self.german_news_b1, self.cbst_int, self.cbst_str,\
            self.ru_adapt_literature, self.ru_adapt_fairy, self.ru_adapt_ab, self.ru_adapt_a_c, self.ru_adapt_b_c]

    def get_all_doc_aligned_grouped_paper_order(self):
        wikiauto_group = CorpusGroup([self.wiki_auto_en], name="WikiAutoEN", language="English", consolidate_for_large_analysis=False)
        simplext_group = CorpusGroup([self.simplext], name="Simplext", language="Spanish", consolidate_for_large_analysis=False)
        alector_group = CorpusGroup([self.alector], name="Alector", language="French", consolidate_for_large_analysis=False)
        simple_german_group = CorpusGroup([self.simple_german], name="Simple German", language="German", consolidate_for_large_analysis=False)
        text_comp_de_group = CorpusGroup([self.text_complexity_de], name="TextComplexityDE", language="German", consolidate_for_large_analysis=False)
        klexikon_group = CorpusGroup([self.klexikon], name="Klexikon", language="German", consolidate_for_large_analysis=False)

        return [self.newsela_en, wikiauto_group, simplext_group, self.newsela, self.terence_teacher, alector_group, self.porsimples, simple_german_group,\
            text_comp_de_group, self.german_news, self.cbst, self.ru_adapt, klexikon_group]

    # Corpuses are grouped by dataset/collection method (ie. Newsela ES is all together since they are all the same domain but only separated by level)
    # on the other hand Simpitiki Wiki and Simpitiki PA remain separate because they are different types of documents (domains: wiki vs public administration)
    # Also simple german and alector removed because they are not aligned
    def get_all_corpora_experiment_grouping(self):
        return [self.newsela_en, self.wiki_auto_en, self.asset, self.simplext, self.newsela, self.terence, self.teacher, self.simpitiki_itwiki,\
            self.adminit, self.paccssit, self.clear, self.wiki_large_fr, self.easy_japanese, self.easy_japanese_extended,\
            self.porsimples, self.text_complexity_de, self.geolino, self.german_news, self.cbst, self.dsim, self.simplify_ur,\
            self.ru_wiki_large, self.rsse, self.ru_adapt_literature, self.ru_adapt_fairy, self.ru_adapt_ency, self.klexikon, self.slots]

    def to_pickle(self, dir_to_save_to):
        self.easy_japanese.word_tokenizer = WordTokenizer()
        self.easy_japanese_extended.word_tokenizer = WordTokenizer()
        self.japanese.word_tokenizer = WordTokenizer()
        with open(os.path.join(dir_to_save_to, 'corpora.pkl'), 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    def from_pickle(self, path_to_load_from):
        loader = CorpusLoader()
        with open(os.path.join(path_to_load_from), 'rb') as pickle_file:
            loader = pickle.load(pickle_file)
        self.simplext = loader.simplext
        self.cbst_str, self.cbst_int = loader.cbst_str, loader.cbst_int
        self.cbst = CorpusGroup([self.cbst_str, self.cbst_int], name="CBST", language="Basque", consolidate_for_large_analysis=False)
        self.porsimples_natural, self.porsimples_strong = loader.porsimples_natural, loader.porsimples_strong
        self.porsimples = CorpusGroup([self.porsimples_natural, self.porsimples_strong], name="PorSimples", language="Brazilian Portuguese", consolidate_for_large_analysis=False)
        self.simpitiki_pa, self.simpitiki_itwiki = loader.simpitiki_pa, loader.simpitiki_itwiki
        self.simpitiki = CorpusGroup([self.simpitiki_pa, self.simpitiki_itwiki], name="Simpitiki", language="Italian", consolidate_for_large_analysis=False)
        self.terence, self.teacher = loader.terence, loader.teacher
        self.terence_teacher = CorpusGroup([self.terence, self.teacher], name="TerenceTeacher", language="Italian", consolidate_for_large_analysis=False)
        self.paccssit = loader.paccssit
        self.clear = loader.clear
        self.wiki_large_fr = loader.wiki_large_fr
        self.dsim = loader.dsim
        self.geolino = loader.geolino
        self.easy_japanese = Corpus(loader.easy_japanese.documents, word_tokenizer=JapaneseTokenizer(), name=loader.easy_japanese.name, language=loader.easy_japanese.language)
        self.easy_japanese_extended = Corpus(loader.easy_japanese_extended.documents, word_tokenizer=JapaneseTokenizer(), name=loader.easy_japanese_extended.name, language=loader.easy_japanese_extended.language)
        self.text_complexity_de = loader.text_complexity_de
        self.rsse = loader.rsse
        self.simplify_ur = loader.simplify_ur
        self.german_news_a2, self.german_news_b1 = loader.german_news_a2, loader.german_news_b1
        self.german_news = CorpusGroup([self.german_news_a2, self.german_news_b1], name="German News", language="German", consolidate_for_large_analysis=False)
        self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4 = loader.newsela_0_1, loader.newsela_1_2, loader.newsela_2_3, loader.newsela_3_4
        self.newsela = CorpusGroup([self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4], name="Newsela ES", language="Spanish", consolidate_for_large_analysis=False)
        self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c, self.ru_adapt_ab, self.ru_adapt_literature =\
            loader.ru_adapt_fairy, loader.ru_adapt_b_c, loader.ru_adapt_a_c, loader.ru_adapt_ab, loader.ru_adapt_literature
        self.ru_adapt = CorpusGroup([self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c, self.ru_adapt_ab, self.ru_adapt_literature],\
            name="RuAdapt", language="Russian", consolidate_for_large_analysis=False)
        self.ru_adapt_ency = CorpusGroup([self.ru_adapt_ab, self.ru_adapt_a_c, self.ru_adapt_b_c],name="RuAdapt Ency", language="Russian", consolidate_for_large_analysis=True)
        self.simple_german = loader.simple_german
        self.alector = loader.alector
        self.ru_wiki_large = loader.ru_wiki_large
        self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4 = loader.newsela_en_0_1, loader.newsela_en_1_2, loader.newsela_en_2_3, loader.newsela_en_3_4
        self.newsela_en = CorpusGroup([self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4], name="Newsela EN", language="English", consolidate_for_large_analysis=False)
        self.wiki_auto_en = loader.wiki_auto_en
        self.asset = loader.asset
        self.adminit = loader.adminit
        self.klexikon = loader.klexikon
        self.slots = loader.slots

        self.spanish = CorpusGroup([self.simplext, self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4], name="Spanish", language="Spanish", consolidate_for_large_analysis=False)
        self.italian = CorpusGroup([self.terence, self.teacher, self.simpitiki_itwiki, self.adminit, self.paccssit], name="Italian", language="Italian", consolidate_for_large_analysis=False)
        self.french = CorpusGroup([self.clear, self.wiki_large_fr, self.alector], name="French", language="French", consolidate_for_large_analysis=False)
        self.japanese = CorpusGroup([self.easy_japanese, self.easy_japanese_extended], name="Japanese", language="Japanese", consolidate_for_large_analysis=False)
        self.brazilian_portuguese = CorpusGroup([self.porsimples_natural, self.porsimples_strong], name="Brazilian Portuguese", language="Brazilian Portuguese", consolidate_for_large_analysis=False)
        self.german = CorpusGroup([self.simple_german, self.text_complexity_de, self.geolino, self.german_news_a2, self.german_news_b1, self.klexikon], name="German", language="German", consolidate_for_large_analysis=False)
        self.basque = CorpusGroup([self.cbst_int, self.cbst_str], name="Basque", language="Basque", consolidate_for_large_analysis=False)
        self.danish = CorpusGroup([self.dsim], name="Danish", language="Danish", consolidate_for_large_analysis=False)
        self.urdu = CorpusGroup([self.simplify_ur], name="Urdu", language="Urdu", consolidate_for_large_analysis=False)
        self.russian = CorpusGroup([self.ru_wiki_large, self.rsse, self.ru_adapt_literature, self.ru_adapt_fairy, self.ru_adapt_ab, self.ru_adapt_a_c, self.ru_adapt_b_c], name="Russian", language="Russian", consolidate_for_large_analysis=False)
        self.english = CorpusGroup([self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.asset], name="English", language="English", consolidate_for_large_analysis=False)
        self.slovene = CorpusGroup([self.slots], name="Slovene", language="Slovene", consolidate_for_large_analysis=False)

        self.version = loader.version

        return [self.newsela_en_0_1, self.newsela_en_1_2, self.newsela_en_2_3, self.newsela_en_3_4, self.wiki_auto_en, self.asset, self.simplext,\
            self.cbst_str, self.cbst_int, self.porsimples_natural, self.porsimples_strong, self.adminit, self.simpitiki_itwiki,\
            self.terence, self.teacher, self.paccssit, self.clear, self.wiki_large_fr, self.dsim, self.geolino, self.easy_japanese,\
            self.easy_japanese_extended, self.text_complexity_de, self.rsse, self.simplify_ur, self.german_news_a2, self.german_news_b1,\
            self.newsela_0_1, self.newsela_1_2, self.newsela_2_3, self.newsela_3_4, self.ru_adapt_fairy, self.ru_adapt_b_c, self.ru_adapt_a_c,\
            self.ru_adapt_ab, self.ru_adapt_literature, self.simple_german, self.alector, self.ru_wiki_large, self.klexikon, self.slots]