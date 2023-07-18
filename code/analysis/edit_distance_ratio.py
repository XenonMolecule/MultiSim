from datatypes import AlignedParallelDocument, Corpus

from sklearn.neighbors import KernelDensity
from fuzzywuzzy import fuzz
import numpy as np
import matplotlib.pyplot as plt

class EditDistanceRatio:
    def __init__(self, corpus:Corpus = None):
        self.corpus = corpus
        self.calculate_edit_ratio(self.corpus)

    def calculate_edit_ratio(self, corpus:Corpus=None, skip_kde=False):
        if(corpus == None):
            if (self.corpus != None):
                corpus = self.corpus
            else:
                return
        else:
            self.corpus = corpus
        
        assert type(self.corpus.documents[0]) is AlignedParallelDocument

        ratios = []
        self.pairs = 0
        # calculate edit ratio
        for document in corpus.documents:
            for orig, simp in document.get_sentence_pairs():
                ratios.append([(100-fuzz.ratio(orig, simp))/100.0])
                self.pairs+=1
        
        self.ratios = np.sort(np.array(ratios), axis=0)

        if not skip_kde:
            kde = KernelDensity(kernel='gaussian', bandwidth=0.05).fit(self.ratios)
            self.pdf = np.exp(kde.score_samples(self.ratios))
        else:
            self.pdf = []

    def plot(self, save_path = ''):
        plot_edit_ratios([self.ratios], [self.pdf], [self.corpus.name], self.pairs, self.corpus.name, save_path)

def plot_edit_ratios(ratios, pdfs, names, doc_count=0, plt_title='', save_path=''):
    assert len(ratios) == len(pdfs)
    assert len(ratios) == len(names)

    _, ax = plt.subplots()
    colors = ['#000000', '#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
    colors = colors[:len(ratios)]

    max_pdf = 0
    min_pdf = 100

    for ratio, pdf, name, color in zip(ratios, pdfs, names, colors):
        assert len(ratio[:,0]) == len(pdf)
        ax.plot(
            ratio[:, 0],
            pdf,
            color=color,
            lw=1,
            linestyle="-",
            label=name,
        )
        max_pdf = max(max_pdf, max(pdf))
        min_pdf = min(min_pdf, min(pdf))
    
    endpoint_x = 1.0
    ymax = max_pdf + 0.05
    ymin = min_pdf - 0.05

    if(len(ratios) == 1):
        doc_str = "N={0} sentence pairs".format(doc_count)
        ax.text(0.05, ymax - ((ymax-ymin)*0.05), doc_str)
    else:    
        ax.legend(loc="upper left")
    
    ax.set_title(plt_title)
    ax.set_xlabel('Edit Distance Ratio')
    ax.set_ylabel('Density')

    ax.set_xlim(0, endpoint_x)
    ax.set_ylim(ymin, ymax)

    if not save_path == '':
        plt.savefig(save_path, bbox_inches='tight')
    else:
        plt.show()
    plt.close()