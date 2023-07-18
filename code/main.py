import os
import csv
import random
import pandas as pd
from analysis.doc_compression import DocumentCompression, plot_document_compressions, add_document_compression_to_existing_plot
from analysis.edit_distance_ratio import EditDistanceRatio, plot_edit_ratios
# from analysis.perplexity import Perplexity, get_THUMT_mGPT, get_sberbank_mGPT, plot_perp_pair
# from analysis.rsrs import RSRS, get_xlm_roberta_large_auto_cuda
from datatypes import Corpus, CorpusGroup
from loaders.full_loader import FullLoader
from loaders.newsela_en_loader import NewselaENLoader
from loaders.wikiauto_en_loader import WikiAutoENLoader
from loaders.asset_loader import AssetLoader
from loaders.adminit_loader import AdminItLoader
from loaders.simplify_ur_multirefloader import SimplifyUR_MultiRefLoader
from loaders.ru_wiki_large_loader import RuWikiLargeLoader
from loaders.wiki_large_fr_loader import WikiLargeFRLoader
from loaders.rsse_loader import RSSE_Loader
from loaders.clear_loader import CLEARLoader
from loaders.easy_japanese_extended_loader import EasyJapaneseExtendedLoader
from loaders.paccssit_loader import PaCCSSIT_Loader
from loaders.dsim_loader import DSimLoader
from loaders.newsela_es_loader import NewselaESLoader
from loaders.ru_adapt_loader import RuAdaptLoader
from loaders.easy_japanese_loader import EasyJapaneseLoader
from loaders.ts_slovene_loader import TextSimplificationSloveneLoader
from loaders.klexikon_loader import KlexikonLoader
from analysis.summary_stats import SummaryStats
from util.util import convert_language_name_to_code, better_names, better_lang, generate_csv
from custom_tokenizers.nltk_sentence_tokenizer import NLTKSentenceTokenizer
from datasets import load_dataset
from collections import defaultdict
from tqdm import tqdm

import nltk
nltk.download('punkt')

import pandas as pd

import matplotlib.pyplot as plt

def output_analysis(corpora:list, output_path:str, analysis:str, corp_op, group_op):
    stat_path = os.path.join(output_path, analysis)
    if not os.path.exists(stat_path):
        os.mkdir(stat_path)
    for corpus in corpora:
        print('Analyzing ' + corpus.name)
        language_path = os.path.join(stat_path, corpus.language)
        if not os.path.exists(language_path):
            os.mkdir(language_path)
        if type(corpus) is CorpusGroup:
            corpus_path = os.path.join(language_path, corpus.name)
            if not os.path.exists(corpus_path):
                os.mkdir(corpus_path)
            collection = []
            for c in corpus.corpora:
                collection.append(corp_op(corpus_path, c))
            group_op(corpus_path, corpus, collection)
        else:
            corp_op(language_path, corpus)

def output_summary_stats(corpora:list, path:str):
    def corpus_op(path:str, corpus:Corpus):
        with open(os.path.join(path, corpus.name + '.txt'), 'w') as output:
            output.write(str(SummaryStats(corpus)))
        return None

    def group_op(path:str, corpora:CorpusGroup, collection:list):
        with open(os.path.join(path, corpora.name + '.txt'), 'w') as output:
            output.write(str(SummaryStats(corpora.get_grouped_corpus())))

    output_analysis(corpora, path, 'stats', corpus_op, group_op)

def output_summary_stats_csv(corpora:list, path:str):
    names = []
    lang = []
    stats = []
    def corpus_op(path:str, corpus:Corpus):
        names.append(corpus.name)
        lang.append(convert_language_name_to_code(corpus.language))
        stats.append(SummaryStats(corpus))
        return None

    def group_op(path:str, corpora:CorpusGroup, collection:list):
        names.append(corpora.name)
        lang.append(convert_language_name_to_code(corpora.language))
        stats.append(SummaryStats(corpora.get_grouped_corpus()))

    output_analysis(corpora, path, 'stats', corpus_op, group_op)

    vocab_original = [f'{len(s.orig_token_counter):,}' for s in stats]
    vocab_simple = [f'{len(s.simp_token_counter):,}' for s in stats]
    token_original = [f'{s.orig_token_count:,}' for s in stats]
    token_simple = [f'{s.simp_token_count:,}' for s in stats]
    tok_per_sent_original = ["{:.2f}".format(round(s.orig_token_count/s.orig_sent_count, 2)) for s in stats]
    tok_per_sent_simple = ["{:.2f}".format(round(s.simp_token_count/s.simp_sent_count, 2)) for s in stats]
    chr_per_tok_original = ["{:.2f}".format(round(s.orig_char_count/s.orig_token_count, 2)) for s in stats]
    chr_per_tok_simple = ["{:.2f}".format(round(s.simp_char_count/s.simp_token_count, 2)) for s in stats]
    sent_per_doc_original = ["{:.2f}".format(round(s.orig_sent_count/len(s.corpus.documents), 2)) for s in stats]
    sent_per_doc_simple =  ["{:.2f}".format(round(s.simp_sent_count/len(s.corpus.documents), 2)) for s in stats]

    delete_pct = ["{:.1f}".format(round(s.deleted_count/s.orig_sent_count * 100, 1)) for s in stats]
    split_pct = ["{:.1f}".format(round(s.split_count/s.orig_sent_count * 100, 1)) for s in stats]
    same_pct = ["{:.1f}".format(round(s.same_count/s.orig_sent_count * 100, 1)) for s in stats]
    changed_pct = ["{:.1f}".format(round(s.reduced_count/s.orig_sent_count * 100, 1)) for s in stats]
    merged_pct = ["{:.1f}".format(round(s.merged_count/s.orig_sent_count * 100, 1)) for s in stats]
    insert_pct = ["{:.1f}".format(round(s.inserted_count/s.simp_sent_count * 100, 1)) for s in stats]

    basic_stats = {
        "Corpus" : names,
        "Lang": lang,
        "Vocab Size O": vocab_original,
        "Vocab Size S": vocab_simple,
        "Token Count O": token_original,
        "Token Count S": token_simple,
        "Tok/Sent O": tok_per_sent_original,
        "Tok/Sent S": tok_per_sent_simple,
        "Chr/Token O": chr_per_tok_original,
        "Chr/Token S": chr_per_tok_simple,
        "Sent/Doc O": sent_per_doc_original,
        "Sent/Doc S": sent_per_doc_simple}

    edit_ops = {
        "Corpus": names,
        "Deleted": delete_pct,
        "Split" : split_pct,
        "Same" : same_pct,
        "Changed" : changed_pct,
        "Merged" : merged_pct,
        "Inserted" : insert_pct
    }

    basic_stats_df = pd.DataFrame(basic_stats)
    edit_ops_df = pd.DataFrame(edit_ops)

    basic_stats_df.to_csv(os.path.join(path,'basic_stats.csv'))
    edit_ops_df.to_csv(os.path.join(path, 'edit_ops.csv'))


def output_document_compression_graphs(doc_corpora:list, output_dir:str, format:str):
    def corpus_op(path:str, corpus:Corpus):
        doc_comp = DocumentCompression(corpus)
        doc_comp.plot(os.path.join(path, corpus.name + '.' + format), format)
        return doc_comp

    def group_op(path:str, corpora:CorpusGroup, doc_comp_collection:list):
        ratios = []
        pdfs = []
        names = []
        for comp, corp in zip(doc_comp_collection, corpora.corpora):
            ratios.append(comp.ratios)
            pdfs.append(comp.pdf)
            names.append(corp.name)
        plot_document_compressions(ratios, pdfs, names, plt_title=better_names(corpora.name) + ' (' + better_lang(corpora.language) + ')', save_path=os.path.join(path,corpora.name + '.' + format), format=format)

    output_analysis(doc_corpora, output_dir, 'document compression', corpus_op, group_op)

def output_document_compression_single_graph(doc_corpora:list, output_dir:str, format:str, figure_dims:tuple):
    _, ax = plt.subplots(nrows=figure_dims[0], ncols=figure_dims[1])

    for i, corpora in enumerate(tqdm(doc_corpora)):
        ratios = []
        pdfs = []
        names = []
        for corpus in corpora.corpora:
            doc_comp = DocumentCompression(corpus)
            ratios.append(doc_comp.ratios)
            pdfs.append(doc_comp.pdf)
            names.append(corpus.name)
        add_document_compression_to_existing_plot(ax[i//figure_dims[1], i%figure_dims[1]], ratios, pdfs, names, better_names(corpora.name) + ' (' + better_lang(corpora.language) + ')')

    plt.gcf().set_size_inches(18, 8)

    if not output_dir == '':
        plt.savefig(output_dir + '/document-compression.' + format, bbox_inches='tight', format=format)
    else:
        plt.show()
    plt.close()
        

def output_edit_ratio_graphs(aligned_corpora:list, output_dir:str):
    def corpus_op(path:str, corpus:Corpus):
        edit_dist = EditDistanceRatio(corpus)
        edit_dist.plot(os.path.join(path, corpus.name + '.png'))
        return edit_dist
    
    def group_op(path:str, corpora:CorpusGroup, edit_dist_collection:list):
        ratios = []
        pdfs = []
        names = []
        for dist, corp in zip(edit_dist_collection, corpora.corpora):
            ratios.append(dist.ratios)
            pdfs.append(dist.pdf)
            names.append(corp.name)
        plot_edit_ratios(ratios, pdfs, names, plt_title=corpora.name, save_path=os.path.join(path,corpora.name + '.png'))

    output_analysis(aligned_corpora, output_dir, 'edit distance ratio', corpus_op, group_op)

def output_txt_files(aligned_corpora:list, output_dir:str):
    def corpus_op(path:str, corpus:Corpus):
        original_sents = []
        simple_sents = []
        for document in corpus.documents:
            original_sents.extend(document.original_items)
            simple_sents.extend(document.simplified_items)
        orig_text = ' '.join(original_sents)
        simp_text = ' '.join(simple_sents)
        with open(os.path.join(path, corpus.name + '-original.txt'), 'w') as output:
            output.write(orig_text)
        with open(os.path.join(path, corpus.name + '-simple.txt'), 'w') as output:
            output.write(simp_text)
        return None

    def group_op(path:str, corpora:CorpusGroup, collection:list):
        pass

    output_analysis(aligned_corpora, output_dir, 'text', corpus_op, group_op)

def output_tsv_files(aligned_corpora:list, output_dir:str):
    def corpus_op(path:str, corpus:Corpus):
        original_sents = []
        simple_sents = []
        for document in corpus.documents:
            original_sents.extend(document.original_items)
            simple_sents.extend(document.simplified_items)
        with open(os.path.join(path, corpus.name + '-original.tsv'), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for sentence in original_sents:
                csvwriter.writerow([sentence])
        with open(os.path.join(path, corpus.name + '-simple.tsv'), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for sentence in simple_sents:
                csvwriter.writerow([sentence])
        

    def group_op(path:str, corpora:CorpusGroup, collection:list):
        pass

    output_analysis(aligned_corpora, output_dir, 'tsv', corpus_op, group_op)

# def output_perplexity_calculation(parallel_corpora:list, output_dir:str, models:list):
#     def corpus_op(path:str, corpus:Corpus):
#         for model in models:
#             if not os.path.exists(os.path.join(path, corpus.name + '-' + model.name + '.png')):
#                 model_set = [model]
#                 perplexity = Perplexity(corpus, model_set)
#                 output_txt = ""
#                 if not os.path.exists(os.path.join(path, corpus.name + '.txt')):
#                     output_txt = str(perplexity)
#                 else:
#                     output_txt = str(perplexity).split('\n')[-1]
#                 with open(os.path.join(path, corpus.name + '.txt'), 'a') as output:
#                     output.write('\n' + output_txt)
#                 plot_perp_pair(perplexity.original_stats[0], perplexity.simplified_stats[0], model.name + " Sentence Level Perplexity Distribution", os.path.join(path, corpus.name + '-' + model.name + '.png'))
#         return None
    
#     def group_op(path:str, corpora:CorpusGroup, collection:list):
#         pass
    
#     output_analysis(parallel_corpora, output_dir, 'perplexity', corpus_op, group_op)

# def output_rsrs_calculation(parallel_corpora:list, output_dir:str, models:list):
#     def corpus_op(path:str, corpus:Corpus):
#         for model in models:
#             model_set = [model]
#             rsrs = RSRS(corpus, model_set, output_dir=path, calc_orig=(not os.path.exists(os.path.join(path, corpus.name + '-' + model.name + '-original.csv'))), calc_simp=(not os.path.exists(os.path.join(path, corpus.name + '-' + model.name + '-simple.csv'))))
#         return None
    
#     def group_op(path:str, corpora:CorpusGroup, collection:list):
#         pass
    
#     output_analysis(parallel_corpora, output_dir, 'rsrs', corpus_op, group_op)

def generate_csv_split_repeats(language_path, corpus_name, orig, simp):
    train_dict = defaultdict(lambda:[])
    true_o_train = []
    true_s_train = []
    if (type(simp[0]) == list):
        for o,s in zip(orig,simp):
            for sent in s:
                true_s_train.append(sent)
                true_o_train.append(o)
        train_dict['original'] = true_o_train
        train_dict['simple'] = true_s_train
    else:
        train_dict = {'original': orig, 'simple': simp}
    train = pd.DataFrame.from_dict(train_dict)
    train.to_csv(language_path + '/' + corpus_name + "_train.csv", index=False)

def generate_csv_multiref_repeats(language_path, corpus_name, orig, simp):
    test_dict = defaultdict(lambda:[])
    if (type(simp[0]) == list):
        test_dict['original'] = orig
        refs = max([len(s) for s in simp])
        for s in simp:
            for i in range(refs):
                suffix = str(i) if i > 0 else ""
                if (i < len(s)):
                    test_dict['simple' + suffix].append(s[i])
                else:
                    test_dict['simple' + suffix].append("")
    else:
        test_dict = {'original': orig, 'simple': simp}
    test = pd.DataFrame.from_dict(test_dict)
    test.to_csv(language_path + '/' + corpus_name + "_test.csv", index=False)

def output_train_test_csv(parallel_corpora:list, output_dir:str, ratio, seed=3600):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for corpus in parallel_corpora:
        print('Splitting ' + corpus.name)
        language_path = os.path.join(output_dir, corpus.language)
        if not os.path.exists(language_path):
            os.mkdir(language_path)
        if type(corpus) is CorpusGroup:
            train_list, test_list = [], []
            for c in corpus.corpora:
                c_train, c_test = c.get_training_test_split(ratio, seed)
                train_list.extend(c_train)
                test_list.extend(c_test)
            
            random.Random(seed).shuffle(train_list)
            random.Random(seed).shuffle(test_list)

            o_train, s_train = zip(*train_list)
            o_test, s_test = zip(*test_list)

            if (ratio > 0.0):
                generate_csv_split_repeats(language_path, corpus.name, o_train, s_train)
            if (ratio < 1.0):
                generate_csv_multiref_repeats(language_path, corpus.name, o_test, s_test)
        else:
            corp_train, corp_test = corpus.get_training_test_split(ratio, seed)

            if (ratio > 0.0):
                o_train, s_train = zip(*corp_train)
                generate_csv_split_repeats(language_path, corpus.name, o_train, s_train)
            if (ratio < 1.0):
                o_test, s_test = zip(*corp_test)
                generate_csv_multiref_repeats(language_path, corpus.name, o_test, s_test)

def update_pickle(corpus_path, pickle_path):
    loader = FullLoader(corpus_path)
    loader.to_pickle(pickle_path)

if __name__ == "__main__":
    # TODO REPLACE WITH PATH TO CORPORA PICKLE FILE OR PATH TO CORPORA FOLDER!!!
    loader = FullLoader("/Users/michaelryan/Downloads/Corpora/corpora.pkl")

    # BELOW IS KEPT AS EXAMPLES OF HOW TO CALL THE ABOVE FUNCTIONS

    # output_summary_stats(loader.get_all_corpora(), "./output/")
    # output_summary_stats_csv(loader.get_all_corpora(), "./output/")
    output_document_compression_single_graph(loader.get_all_doc_aligned_grouped_paper_order(), "./output/", "pdf", (3,5))

    # loader.to_pickle("/Users/michaelryan/Downloads/Corpora/")
    # corpora = loader.get_all_corpora_experiment_grouping()
    # output_train_test_csv(corpora, '/Users/michaelryan/Documents/School/GaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/', 0.8)

    # data_train = load_dataset("./MultilingualSimplification.py", name="all", split="train")
    # data_test = load_dataset("./MultilingualSimplification.py", name="all", split="test")

    # print(data_train)
    # print(data_test)

    # raw_datasets = load_dataset("./MultilingualSimplification.py", name = "Simplext")

    # print(raw_datasets["train"])
    # print(raw_datasets["test"])

    # newsela_en_loader = NewselaENLoader(keep_subdivisions=False)
    # newsela_en = newsela_en_loader.load("/Users/michaelryan/Downloads/Corpora/English/newsela-auto/newsela-auto/all_data/newsela-auto-all-data.json")[0]
    # output_train_test_csv([newsela_en], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 0.9932)
    # wiki_auto = WikiAutoENLoader(keep_subdivisions=False).load("/Users/michaelryan/Downloads/Corpora/English/wiki-auto-master")[0]
    # output_train_test_csv([wiki_auto], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 0.9829)

    # rsse_dev, rsse_test = RSSE_Loader(keep_train_test_split=True).load("/Users/michaelryan/Downloads/Corpora/Russian/RuSimpleSentEval")
    # output_train_test_csv([rsse_dev, rsse_test], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 1.0)

    # clear_train, clear_valid, clear_test = CLEARLoader(keep_train_test_split=True, allow_sentence_splits=False).load("/Users/michaelryan/Downloads/Corpora/French/corpus_coling")
    # output_train_test_csv([clear_train, clear_valid, clear_test], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 1.0)

    # paccssit = PaCCSSIT_Loader().load("/Users/michaelryan/Downloads/Corpora/Italian/PaCCSS-IT/data-set")[0]
    # output_train_test_csv([paccssit], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 0.96)
    # dsim = DSimLoader().load(os.path.join('/Users/michaelryan/Downloads/Corpora','Danish','DSim'))[0]
    # output_train_test_csv([dsim], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 0.9582)
    # newsela_es = NewselaESLoader(keep_subdivisions=False).load(os.path.join("/Users/michaelryan/Downloads/Corpora", 'Spanish','newsela_es'))[0]
    # output_train_test_csv([newsela_es], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 0.9392)
    # _, _, _, _, literature = RuAdaptLoader(keep_subdivisions=True).load(os.path.join("/Users/michaelryan/Downloads/Corpora",'Russian','RuAdaptUnreleased'))
    # output_train_test_csv([literature], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 0.9172)
    # easy_japanese = EasyJapaneseLoader().load(os.path.join("/Users/michaelryan/Downloads/Corpora", 'Japanese','EasyJapanese'))[0]
    # output_train_test_csv([easy_japanese], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 0.96)
    # klexikon = KlexikonLoader(keep_train_test_split=False).load("/Users/michaelryan/Downloads/Corpora/German/klexikon")[0]
    # output_train_test_csv([train, val, test], "/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/data/", 1.0)
    # slots = TextSimplificationSloveneLoader(keep_train_test_split=False).load(os.path.join("/Users/michaelryan/Downloads/Corpora",'Slovene','text-simplification-slovene-main'))[0]
    # output_summary_stats([klexikon],'/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/output')
    # adminit = AdminItLoader().load(os.path.join("/Users/michaelryan/Downloads/Corpora", 'Italian','admin-It-main'))[0]
    # output_summary_stats([adminit],'/Users/michaelryan/Documents/School/GeorgiaTech/Research/MultilingualSimplification/multilingual-text-simplification/output')

