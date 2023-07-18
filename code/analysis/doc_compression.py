from datatypes import Corpus

from sklearn.neighbors import KernelDensity
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from util.util import convert_language_name_to_code, better_names, better_lang

class DocumentCompression:
    def __init__(self, corpus:Corpus = None):
        self.corpus = corpus
        self.calculate_document_compression(self.corpus)

    def calculate_document_compression(self, corpus:Corpus=None):
        if(corpus == None):
            if (self.corpus != None):
                corpus = self.corpus
            else:
                return
        else:
            self.corpus = corpus
        
        ratios = []
        # calculate document compression
        for document in corpus.documents:
            simple_len = len(''.join(document.simplified_items))
            original_len = len(''.join(document.original_items))

            if (simple_len != 0 and original_len == 0):
                continue

            if simple_len == 0 and original_len == 0:
                ratio = 1
            else:
                ratio = simple_len/original_len
            ratios.append([ratio])
        
        self.ratios = np.sort(np.array(ratios), axis=0)

        kde = KernelDensity(kernel='gaussian', bandwidth=0.05).fit(self.ratios)
        self.pdf = np.exp(kde.score_samples(self.ratios))

    def plot(self, save_path = '', format='png'):
        plot_document_compressions([self.ratios], [self.pdf], [self.corpus.name], better_names(self.corpus.name) + ' (' + better_lang(self.corpus.language) + ')', save_path, format)

def plot_document_compressions(ratios, pdfs, names, plt_title='', save_path='', format='png'):
    _, ax = plt.subplots()

    add_document_compression_to_existing_plot(ax, ratios, pdfs, names, plt_title)

    if not save_path == '':
        plt.savefig(save_path, bbox_inches='tight', format=format)
    else:
        plt.show()
    plt.close()

def add_document_compression_to_existing_plot(ax, ratios, pdfs, names, plt_title=''):
    assert len(ratios) == len(pdfs)
    assert len(ratios) == len(names)

    colors = ['#000000', '#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
    colors = colors[:len(ratios)]

    max_pdf = 0
    min_pdf = 100

    for ratio, pdf, name, color in zip(ratios, pdfs, names, colors):
        assert len(ratio[:,0]) == len(pdf)

        font = {'family' : 'monospace',
                'weight' : 'normal',
                'size'   : 8}
        plt.rc('font', **font) 

        ax.plot(
            ratio[:, 0],
            pdf,
            color=color,
            lw=1,
            linestyle="-",
            label=better_names(name) + ' (' + str(len(ratio)) + ' docs)',
        )
        max_pdf = max(max_pdf, max(pdf))
        min_pdf = min(min_pdf, min(pdf))
    
    endpoint_x = 2.0
    ymax = max_pdf + 0.05
    ymin = min_pdf - 0.05

    for ratio, pdf, color in zip(ratios, pdfs, colors):
        mean = np.mean(ratio[:,0])
        idx_mean = (np.abs(ratio[:,0] - mean)).argmin()
        ax.plot([mean, mean], [ymin, pdf[idx_mean]], color=color, linestyle='--', lw=1, label="_")

    ax.legend(loc="upper right")
    
    ax.set_title(plt_title)
    # ax.set_xlabel('Compression Ratio', font=font)
    # ax.set_ylabel('Density', font=font)

    ax.set_xlim(0, endpoint_x)
    ax.set_ylim(ymin, ymax)

    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
