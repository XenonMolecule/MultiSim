# MultiSim

![Figure showing four complex and simple sentence pairs.  One pair in English, one in Japanese, one in Urdu, and one in Russian.  The English complex sentence reads "He settled in London, devoting himself chiefly to practical teaching." which is paired with the simple sentence "He lived in London. He was a teacher."](MultiSimEx.png "MultiSim Example")

Code and Data for using the MultiSim Benchmark from the ACL 2023 paper [Revisiting non-English Text Simplification: A Unified Multilingual Benchmark](https://aclanthology.org/2023.acl-long.269/)

# HuggingFace

The data is available on HuggingFace [here](https://huggingface.co/datasets/MichaelR207/MultiSimV2)!

## Usage
```python
from datasets import load_dataset

dataset = load_dataset("MichaelR207/MultiSim")
```

# Citation
If you use this benchmark please cite our paper:
```
@inproceedings{ryan-etal-2023-revisiting,
    title = "Revisiting non-{E}nglish Text Simplification: A Unified Multilingual Benchmark",
    author = "Ryan, Michael  and
      Naous, Tarek  and
      Xu, Wei",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.269",
    pages = "4898--4927",
    abstract = "Recent advancements in high-quality, large-scale English resources have pushed the frontier of English Automatic Text Simplification (ATS) research. However, less work has been done on multilingual text simplification due to the lack of a diverse evaluation benchmark that covers complex-simple sentence pairs in many languages. This paper introduces the MultiSim benchmark, a collection of 27 resources in 12 distinct languages containing over 1.7 million complex-simple sentence pairs. This benchmark will encourage research in developing more effective multilingual text simplification models and evaluation metrics. Our experiments using MultiSim with pre-trained multilingual language models reveal exciting performance improvements from multilingual training in non-English settings. We observe strong performance from Russian in zero-shot cross-lingual transfer to low-resource languages. We further show that few-shot prompting with BLOOM-176b achieves comparable quality to reference simplifications outperforming fine-tuned models in most languages. We validate these findings through human evaluation.",
}
```

# Contact
**Michael Ryan**: [Scholar](https://scholar.google.com/citations?user=8APGEEkAAAAJ&hl=en) | [Twitter](http://twitter.com/michaelryan207) | [Github](https://github.com/XenonMolecule) | [LinkedIn](https://www.linkedin.com/in/michael-ryan-207/) | [Research Gate](https://www.researchgate.net/profile/Michael-Ryan-86) | [Personal Website](http://michaelryan.tech/) | [michaeljryan@gatech.edu](mailto://michaeljryan@gatech.edu)

# Data Availability
## Public Datasets
Most of the public datasets are available as a part of this MultiSim Repo.  A few are still pending availability.  For all resources we provide alternative download links.
| Dataset | Language | Availability in MultiSim Repo | Alternative Link |
|---|---|---|---|
| ASSET  | English | Available | https://huggingface.co/datasets/asset |
| WikiAuto | English | Available | https://huggingface.co/datasets/wiki_auto |
| CLEAR | French | Available | http://natalia.grabar.free.fr/resources.php#remi |
| WikiLargeFR | French | Available | http://natalia.grabar.free.fr/resources.php#remi |
| GEOLino | German | Available | https://github.com/Jmallins/ZEST-data |
| TextComplexityDE | German | Available | https://github.com/babaknaderi/TextComplexityDE |
| AdminIT | Italian | Available | https://github.com/Unipisa/admin-It |
| Simpitiki | Italian | Available | https://github.com/dhfbk/simpitiki# |
| PaCCSS-IT | Italian | Available | http://www.italianlp.it/resources/paccss-it-parallel-corpus-of-complex-simple-sentences-for-italian/ |
| Terence and Teacher | Italian | Available | http://www.italianlp.it/resources/terence-and-teacher/ |
| Easy Japanese | Japanese | Available | https://www.jnlp.org/GengoHouse/snow/t15 |
| Easy Japanese Extended | Japanese | Available | https://www.jnlp.org/GengoHouse/snow/t23 |
| RuAdapt Encyclopedia | Russian | Available | https://github.com/Digital-Pushkin-Lab/RuAdapt |
| RuAdapt Fairytales | Russian | Available | https://github.com/Digital-Pushkin-Lab/RuAdapt |
| RuSimpleSentEval | Russian | Available | https://github.com/dialogue-evaluation/RuSimpleSentEval |
| RuWikiLarge | Russian | Available | https://github.com/dialogue-evaluation/RuSimpleSentEval |
| SloTS | Slovene | Available | https://github.com/sabina-skubic/text-simplification-slovene |
| SimplifyUR | Urdu | Pending | https://github.com/harisbinzia/SimplifyUR |
| PorSimples | Brazilian Portuguese | Available | [sandra@icmc.usp.br](mailto:sandra@icmc.usp.br) |

## On Request Datasets
The authors of the original papers must be contacted for on request datasets.  Contact information for the authors of each dataset is provided below.
| Dataset | Language | Contact |
|---|---|---|
| CBST | Basque | http://www.ixa.eus/node/13007?language=en <br/> [itziar.gonzalezd@ehu.eus](mailto:itziar.gonzalezd@ehu.eus) |
| DSim | Danish | [sk@eyejustread.com](mailto:sk@eyejustread.com) |
| Newsela EN | English | [https://newsela.com/data/](https://newsela.com/data/) |
| Newsela ES | Spanish | [https://newsela.com/data/](https://newsela.com/data/) |
| German News | German | [ebling@cl.uzh.ch](mailto:ebling@cl.uzh.ch) |
| Simple German | German | [ebling@cl.uzh.ch](mailto:ebling@cl.uzh.ch) |
| Simplext | Spanish | [horacio.saggion@upf.edu](mailto:horacio.saggion@upf.edu) |
| RuAdapt Literature | Russian | Partially Available: https://github.com/Digital-Pushkin-Lab/RuAdapt <br/> Full Dataset: [anna.dmitrieva@helsinki.fi](mailto:anna.dmitrieva@helsinki.fi) |

# Specific Citations
Please cite the individual datasets that you use within the MultiSim benchmark as appropriate.  Proper bibtex attributions for each of the datasets are included below

## AdminIT
```
@inproceedings{miliani-etal-2022-neural,
    title = "Neural Readability Pairwise Ranking for Sentences in {I}talian Administrative Language",
    author = "Miliani, Martina  and
      Auriemma, Serena  and
      Alva-Manchego, Fernando  and
      Lenci, Alessandro",
    booktitle = "Proceedings of the 2nd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 12th International Joint Conference on Natural Language Processing",
    month = nov,
    year = "2022",
    address = "Online only",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.aacl-main.63",
    pages = "849--866",
    abstract = "Automatic Readability Assessment aims at assigning a complexity level to a given text, which could help improve the accessibility to information in specific domains, such as the administrative one. In this paper, we investigate the behavior of a Neural Pairwise Ranking Model (NPRM) for sentence-level readability assessment of Italian administrative texts. To deal with data scarcity, we experiment with cross-lingual, cross- and in-domain approaches, and test our models on Admin-It, a new parallel corpus in the Italian administrative language, containing sentences simplified using three different rewriting strategies. We show that NPRMs are effective in zero-shot scenarios ({\textasciitilde}0.78 ranking accuracy), especially with ranking pairs containing simplifications produced by overall rewriting at the sentence-level, and that the best results are obtained by adding in-domain data (achieving perfect performance for such sentence pairs). Finally, we investigate where NPRMs failed, showing that the characteristics of the training data, rather than its size, have a bigger effect on a model{'}s performance.",
}
```

## ASSET
```
@inproceedings{alva-manchego-etal-2020-asset,
    title = "{ASSET}: {A} Dataset for Tuning and Evaluation of Sentence Simplification Models with Multiple Rewriting Transformations",
    author = "Alva-Manchego, Fernando  and
      Martin, Louis  and
      Bordes, Antoine  and
      Scarton, Carolina  and
      Sagot, Beno{\^\i}t  and
      Specia, Lucia",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.424",
    pages = "4668--4679",
}
```
## CBST
```
@article{10.1007/s10579-017-9407-6,
  title={{The corpus of Basque simplified texts (CBST)}},
  author={Gonzalez-Dios, Itziar and Aranzabe, Mar{\'\i}a Jes{\'u}s and D{\'\i}az de Ilarraza, Arantza},
  journal={Language Resources and Evaluation},
  volume={52},
  number={1},
  pages={217--247},
  year={2018},
  publisher={Springer}
}
```
## CLEAR
```
@inproceedings{grabar-cardon-2018-clear,
    title = "{CLEAR} {--} Simple Corpus for Medical {F}rench",
    author = "Grabar, Natalia  and
      Cardon, R{\'e}mi",
    booktitle = "Proceedings of the 1st Workshop on Automatic Text Adaptation ({ATA})",
    month = nov,
    year = "2018",
    address = "Tilburg, the Netherlands",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W18-7002",
    doi = "10.18653/v1/W18-7002",
    pages = "3--9",
}
```
## DSim
```
@inproceedings{klerke-sogaard-2012-dsim,
    title = "{DS}im, a {D}anish Parallel Corpus for Text Simplification",
    author = "Klerke, Sigrid  and
      S{\o}gaard, Anders",
    booktitle = "Proceedings of the Eighth International Conference on Language Resources and Evaluation ({LREC}'12)",
    month = may,
    year = "2012",
    address = "Istanbul, Turkey",
    publisher = "European Language Resources Association (ELRA)",
    url = "http://www.lrec-conf.org/proceedings/lrec2012/pdf/270_Paper.pdf",
    pages = "4015--4018",
    abstract = "We present DSim, a new sentence aligned Danish monolingual parallel corpus extracted from 3701 pairs of news telegrams and corresponding professionally simplified short news articles. The corpus is intended for building automatic text simplification for adult readers. We compare DSim to different examples of monolingual parallel corpora, and we argue that this corpus is a promising basis for future development of automatic data-driven text simplification systems in Danish. The corpus contains both the collection of paired articles and a sentence aligned bitext, and we show that sentence alignment using simple tf*idf weighted cosine similarity scoring is on line with state―of―the―art when evaluated against a hand-aligned sample. The alignment results are compared to state of the art for English sentence alignment. We finally compare the source and simplified sides of the corpus in terms of lexical and syntactic characteristics and readability, and find that the one―to―many sentence aligned corpus is representative of the sentence simplifications observed in the unaligned collection of article pairs.",
}
```
## Easy Japanese
```
@inproceedings{maruyama-yamamoto-2018-simplified,
    title = "Simplified Corpus with Core Vocabulary",
    author = "Maruyama, Takumi  and
      Yamamoto, Kazuhide",
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://aclanthology.org/L18-1185",
}
```
## Easy Japanese Extended
```
@inproceedings{katsuta-yamamoto-2018-crowdsourced,
    title = "Crowdsourced Corpus of Sentence Simplification with Core Vocabulary",
    author = "Katsuta, Akihiro  and
      Yamamoto, Kazuhide",
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://aclanthology.org/L18-1072",
}
```
## GEOLino
```
@inproceedings{mallinson2020,
  title={Zero-Shot Crosslingual Sentence Simplification},
  author={Mallinson, Jonathan and Sennrich, Rico and Lapata, Mirella},
  year={2020},
  booktitle={2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020)}
}
```
## German News
```
@inproceedings{sauberli-etal-2020-benchmarking,
    title = "Benchmarking Data-driven Automatic Text Simplification for {G}erman",
    author = {S{\"a}uberli, Andreas  and
      Ebling, Sarah  and
      Volk, Martin},
    booktitle = "Proceedings of the 1st Workshop on Tools and Resources to Empower People with REAding DIfficulties (READI)",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.readi-1.7",
    pages = "41--48",
    abstract = "Automatic text simplification is an active research area, and there are first systems for English, Spanish, Portuguese, and Italian. For German, no data-driven approach exists to this date, due to a lack of training data. In this paper, we present a parallel corpus of news items in German with corresponding simplifications on two complexity levels. The simplifications have been produced according to a well-documented set of guidelines. We then report on experiments in automatically simplifying the German news items using state-of-the-art neural machine translation techniques. We demonstrate that despite our small parallel corpus, our neural models were able to learn essential features of simplified language, such as lexical substitutions, deletion of less relevant words and phrases, and sentence shortening.",
    language = "English",
    ISBN = "979-10-95546-45-0",
}
```
## Newsela EN/ES
```
@article{xu-etal-2015-problems,
    title = "Problems in Current Text Simplification Research: New Data Can Help",
    author = "Xu, Wei  and
      Callison-Burch, Chris  and
      Napoles, Courtney",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "3",
    year = "2015",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/Q15-1021",
    doi = "10.1162/tacl_a_00139",
    pages = "283--297",
    abstract = "Simple Wikipedia has dominated simplification research in the past 5 years. In this opinion paper, we argue that focusing on Wikipedia limits simplification research. We back up our arguments with corpus analysis and by highlighting statements that other researchers have made in the simplification literature. We introduce a new simplification dataset that is a significant improvement over Simple Wikipedia, and present a novel quantitative-comparative approach to study the quality of simplification data resources.",
}
```
## PaCCSS-IT
```
@inproceedings{brunato-etal-2016-paccss,
    title = "{P}a{CCSS}-{IT}: A Parallel Corpus of Complex-Simple Sentences for Automatic Text Simplification",
    author = "Brunato, Dominique  and
      Cimino, Andrea  and
      Dell{'}Orletta, Felice  and
      Venturi, Giulia",
    booktitle = "Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2016",
    address = "Austin, Texas",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D16-1034",
    doi = "10.18653/v1/D16-1034",
    pages = "351--361",
}
```
## PorSimples
```
@inproceedings{aluisio-gasperin-2010-fostering,
    title = "Fostering Digital Inclusion and Accessibility: The {P}or{S}imples project for Simplification of {P}ortuguese Texts",
    author = "Alu{\'\i}sio, Sandra  and
      Gasperin, Caroline",
    booktitle = "Proceedings of the {NAACL} {HLT} 2010 Young Investigators Workshop on Computational Approaches to Languages of the {A}mericas",
    month = jun,
    year = "2010",
    address = "Los Angeles, California",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W10-1607",
    pages = "46--53",
}
```
```
@inproceedings{10.1007/978-3-642-16952-6_31,
  author="Scarton, Carolina and Gasperin, Caroline and Aluisio, Sandra",
  editor="Kuri-Morales, Angel and Simari, Guillermo R.",
  title="Revisiting the Readability Assessment of Texts in Portuguese",
  booktitle="Advances in Artificial Intelligence -- IBERAMIA 2010",
  year="2010",
  publisher="Springer Berlin Heidelberg",
  address="Berlin, Heidelberg",
  pages="306--315",
  isbn="978-3-642-16952-6"
}
```
## RSSE
```
@inproceedings{sakhovskiy2021rusimplesenteval,
  title={{RuSimpleSentEval-2021 shared task:} evaluating sentence simplification for Russian},
  author={Sakhovskiy, Andrey and Izhevskaya, Alexandra and Pestova, Alena and Tutubalina, Elena and Malykh, Valentin and Smurov, Ivana and Artemova, Ekaterina},
  booktitle={Proceedings of the International Conference “Dialogue},
  pages={607--617},
  year={2021}
}
```
## RuAdapt
```
@inproceedings{Dmitrieva2021Quantitative,
  title={A quantitative study of simplification strategies in adapted texts for L2 learners of Russian},
  author={Dmitrieva, Anna and Laposhina, Antonina and Lebedeva, Maria},
  booktitle={Proceedings of the International Conference “Dialogue},
  pages={191--203},
  year={2021}
}
```
```
@inproceedings{dmitrieva-tiedemann-2021-creating,
    title = "Creating an Aligned {R}ussian Text Simplification Dataset from Language Learner Data",
    author = {Dmitrieva, Anna  and
      Tiedemann, J{\"o}rg},
    booktitle = "Proceedings of the 8th Workshop on Balto-Slavic Natural Language Processing",
    month = apr,
    year = "2021",
    address = "Kiyv, Ukraine",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.bsnlp-1.8",
    pages = "73--79",
    abstract = "Parallel language corpora where regular texts are aligned with their simplified versions can be used in both natural language processing and theoretical linguistic studies. They are essential for the task of automatic text simplification, but can also provide valuable insights into the characteristics that make texts more accessible and reveal strategies that human experts use to simplify texts. Today, there exist a few parallel datasets for English and Simple English, but many other languages lack such data. In this paper we describe our work on creating an aligned Russian-Simple Russian dataset composed of Russian literature texts adapted for learners of Russian as a foreign language. This will be the first parallel dataset in this domain, and one of the first Simple Russian datasets in general.",
}
```
## RuWikiLarge
```
@inproceedings{sakhovskiy2021rusimplesenteval,
  title={{RuSimpleSentEval-2021 shared task:} evaluating sentence simplification for Russian},
  author={Sakhovskiy, Andrey and Izhevskaya, Alexandra and Pestova, Alena and Tutubalina, Elena and Malykh, Valentin and Smurov, Ivana and Artemova, Ekaterina},
  booktitle={Proceedings of the International Conference “Dialogue},
  pages={607--617},
  year={2021}
}
```
## SIMPITIKI
```
@article{tonelli2016simpitiki,
  title={SIMPITIKI: a Simplification corpus for Italian},
  author={Tonelli, Sara and Aprosio, Alessio Palmero and Saltori, Francesca},
  journal={Proceedings of CLiC-it},
  year={2016}
}
```
## Simple German
```
@inproceedings{battisti-etal-2020-corpus,
    title = "A Corpus for Automatic Readability Assessment and Text Simplification of {G}erman",
    author = {Battisti, Alessia  and
      Pf{\"u}tze, Dominik  and
      S{\"a}uberli, Andreas  and
      Kostrzewa, Marek  and
      Ebling, Sarah},
    booktitle = "Proceedings of the Twelfth Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.404",
    pages = "3302--3311",
    abstract = "In this paper, we present a corpus for use in automatic readability assessment and automatic text simplification for German, the first of its kind for this language. The corpus is compiled from web sources and consists of parallel as well as monolingual-only (simplified German) data amounting to approximately 6,200 documents (nearly 211,000 sentences). As a unique feature, the corpus contains information on text structure (e.g., paragraphs, lines), typography (e.g., font type, font style), and images (content, position, and dimensions). While the importance of considering such information in machine learning tasks involving simplified language, such as readability assessment, has repeatedly been stressed in the literature, we provide empirical evidence for its benefit. We also demonstrate the added value of leveraging monolingual-only data for automatic text simplification via machine translation through applying back-translation, a data augmentation technique.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```
## Simplext
```
@article{10.1145/2738046,
    author = {Saggion, Horacio and \v{S}tajner, Sanja and Bott, Stefan and Mille, Simon and Rello, Luz and Drndarevic, Biljana},
    title = {Making It Simplext: Implementation and Evaluation of a Text Simplification System for Spanish},
    year = {2015},
    issue_date = {June 2015}, publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    volume = {6},
    number = {4},
    issn = {1936-7228},
    url = {https://doi.org/10.1145/2738046},
    doi = {10.1145/2738046},
    journal = {ACM Trans. Access. Comput.},
    month = {may},
    articleno = {14},
    numpages = {36},
    keywords = {Spanish, text simplification corpus, human evaluation, readability measures} 
}
```
## SimplifyUR
```
@inproceedings{qasmi-etal-2020-simplifyur,
    title = "{S}implify{UR}: Unsupervised Lexical Text Simplification for {U}rdu",
    author = "Qasmi, Namoos Hayat  and
      Zia, Haris Bin  and
      Athar, Awais  and
      Raza, Agha Ali",
    booktitle = "Proceedings of the Twelfth Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.428",
    pages = "3484--3489",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```
## SloTS
```
@misc{gorenc2022slovene,
	 title = {Slovene text simplification dataset {SloTS}},
	 author = {Gorenc, Sabina and Robnik-{\v S}ikonja, Marko},
	 url = {http://hdl.handle.net/11356/1682},
	 note = {Slovenian language resource repository {CLARIN}.{SI}},
	 copyright = {Creative Commons - Attribution 4.0 International ({CC} {BY} 4.0)},
	 issn = {2820-4042},
	 year = {2022}
}
```
## Terence and Teacher
```
@inproceedings{brunato-etal-2015-design,
    title = "Design and Annotation of the First {I}talian Corpus for Text Simplification",
    author = "Brunato, Dominique  and
      Dell{'}Orletta, Felice  and
      Venturi, Giulia  and
      Montemagni, Simonetta",
    booktitle = "Proceedings of the 9th Linguistic Annotation Workshop",
    month = jun,
    year = "2015",
    address = "Denver, Colorado, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W15-1604",
    doi = "10.3115/v1/W15-1604",
    pages = "31--41",
}
```
## TextComplexityDE
```
@article{naderi2019subjective,
  title={Subjective Assessment of Text Complexity: A Dataset for German Language},
  author={Naderi, Babak and Mohtaj, Salar and Ensikat, Kaspar and M{\"o}ller, Sebastian},
  journal={arXiv preprint arXiv:1904.07733},
  year={2019}
}
```
## WikiAuto
```
@inproceedings{acl/JiangMLZX20,
  author    = {Chao Jiang and
               Mounica Maddela and
               Wuwei Lan and
               Yang Zhong and
               Wei Xu},
  editor    = {Dan Jurafsky and
               Joyce Chai and
               Natalie Schluter and
               Joel R. Tetreault},
  title     = {Neural {CRF} Model for Sentence Alignment in Text Simplification},
  booktitle = {Proceedings of the 58th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2020, Online, July 5-10, 2020},
  pages     = {7943--7960},
  publisher = {Association for Computational Linguistics},
  year      = {2020},
  url       = {https://www.aclweb.org/anthology/2020.acl-main.709/}
}
```
## WikiLargeFR
```
@inproceedings{cardon-grabar-2020-french,
    title = "{F}rench Biomedical Text Simplification: When Small and Precise Helps",
    author = "Cardon, R{\'e}mi  and
      Grabar, Natalia",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://aclanthology.org/2020.coling-main.62",
    doi = "10.18653/v1/2020.coling-main.62",
    pages = "710--716",
    abstract = "We present experiments on biomedical text simplification in French. We use two kinds of corpora {--} parallel sentences extracted from existing health comparable corpora in French and WikiLarge corpus translated from English to French {--} and a lexicon that associates medical terms with paraphrases. Then, we train neural models on these parallel corpora using different ratios of general and specialized sentences. We evaluate the results with BLEU, SARI and Kandel scores. The results point out that little specialized data helps significantly the simplification.",
}
```

# Acknowledgement
This research is supported in part by the NSF awards IIS-2144493 and IIS-2112633, ODNI and IARPA via the BETTER program (contract 2019- 19051600004) and the HIATUS program (contract 2022-22072200004). The views and conclusions contained herein are those of the authors and should not be interpreted as necessarily representing the official policies, either expressed or implied, of NSF, ODNI, IARPA, or the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for governmental purposes, notwithstanding any copyright annotation therein.
