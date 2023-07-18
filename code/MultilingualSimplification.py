# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MultiSim is a growing collection of Text Simplfication datasets in multiple languages.  Each dataset is a set of complex and simple sentence pairs."""

import pandas as pd
import os
from collections import defaultdict

import datasets

_CITATION = """\
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
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
MultiSim is a growing collection of Text Simplfication datasets in multiple languages.  Each dataset is a set of complex and simple sentence pairs.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/XenonMolecule/MultiSim"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = """MIT License

Copyright (c) 2023 Michael Ryan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

_SUBCORPORA = {
    "NewselaEN": {
        "path": "../data/English/Newsela EN",
        "language": "en"
    },
    "WikiAutoEN": {
        "path": "../data/English/WikiAuto",
        "language": "en"
    },
    "ASSET": {
        "path": "../data/English/ASSET",
        "language": "en"
    },
    "Simplext": {
        "path": "../data/Spanish/Simplext",
        "language": "es"
    },
    "NewselaES": {
        "path": "../data/Spanish/Newsela ES",
        "language": "es"
    },
    "Terence": {
        "path" : "../data/Italian/Terence",
        "language": "it"
    },
    "Teacher": {
        "path": "../data/Italian/Teacher",
        "language": "it"
    },
    "SimpitikiWiki": {
        "path": "../data/Italian/Simpitiki Italian Wikipedia",
        "language": "it"
    },
    "AdminIt": {
        "path": "../data/Italian/AdminIT",
        "language": "it"
    },
    "PaCCSS-IT": {
        "path": "../data/Italian/PaCCSS-IT Corpus",
        "language": "it"
    },
    "CLEAR" : {
        "path" : "../data/French/CLEAR Corpus",
        "language": "fr"
    },
    "WikiLargeFR": {
        "path" : "../data/French/WikiLargeFR Corpus",
        "language": "fr"
    },
    "EasyJapanese": {
        "path": "../data/Japanese/Easy Japanese Corpus",
        "language": "ja"
    },
    "EasyJapaneseExtended": {
        "path": "../data/Japanese/Easy Japanese Extended",
        "language": "ja"
    },
    "PorSimples" : {
        "path": "../data/Brazilian Portuguese/PorSimples",
        "language": "pt-br"
    },
    "TextComplexityDE" : {
        "path": "../data/German/TextComplexityDE Parallel Corpus",
        "language": "de"
    },
    "GEOLinoTest" : {
        "path" : "../data/German/GEOLino Corpus",
        "language": "de"
    },
    "GermanNews" : {
        "path" : "../data/German/German News",
        "language": "de"
    },
    "CBST": {
        "path" : "../data/Basque/CBST",
        "language": "eu"
    },
    "DSim": {
        "path": "../data/Danish/DSim Corpus",
        "language": "da"
    },
    "SimplifyUR": {
        "path": "../data/Urdu/SimplifyUR",
        "language": "ur"
    },
    "RuWikiLarge": {
        "path" : "../data/Russian/RuWikiLarge",
        "language": "ru"
    },
    "RSSE" : {
        "path": "../data/Russian/RSSE Corpus",
        "language": "ru"
    },
    "RuAdaptLit" : {
        "path": "../data/Russian/RuAdapt Literature",
        "language": "ru"
    },
    "RuAdaptFairytales" : {
        "path": "../data/Russian/RuAdapt Fairytales",
        "language": "ru"
    },
    "RuAdaptEncy" : {
        "path" : "../data/Russian/RuAdapt Ency",
        "language": "ru"
    },
    "TSSlovene" : {
        "path" : "../data/Slovene/Text Simplification Slovene",
        "language": "sl"
    }
}

_LANGUAGES = {
    "English":'en',
    "Spanish":'es', 
    "Italian":'it', 
    "French" : 'fr',
    "Japanese": 'ja',
    "Brazilian Portuguese": 'pt-br',
    "German": 'de',
    "Basque": 'eu',
    "Danish": 'da',
    "Urdu": 'ur',
    "Russian": 'ru',
    "Slovene": 'sl'
}


class MultilingualSimplification(datasets.GeneratorBasedBuilder):
    """MultiSim is a growing collection of Text Simplfication datasets in multiple languages.  Each dataset is a set of complex and simple sentence pairs."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        # datasets.BuilderConfig(name="NewselaEN", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="WikiAutoEN", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="ASSET", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="Simplext", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="NewselaES", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="Terence", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="Teacher", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="SimpitikiWiki", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="AdminIt", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="PaCCSS-IT", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="CLEAR", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="WikiLargeFR", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="EasyJapanese", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="EasyJapaneseExtended", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="PorSimples", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="TextComplexityDE", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="GEOLinoTest", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="GermanNews", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="CBST", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="DSim", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="SimplifyUR", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="RuWikiLarge", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="RSSE", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="RuAdaptLit", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="RuAdaptFairytales", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="RuAdaptEncy", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="TSSlovene", version=VERSION, description="TODO: Descriptions"),
        
        datasets.BuilderConfig(name="English", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="Spanish", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="Italian", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="French", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="Japanese", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="Brazilian Portuguese", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="German", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="Basque", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="Danish", version=VERSION, description="TODO: Descriptions"),
        # datasets.BuilderConfig(name="Urdu", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="Russian", version=VERSION, description="TODO: Descriptions"),
        datasets.BuilderConfig(name="Slovene", version=VERSION, description="TODO: Descriptions"),

        datasets.BuilderConfig(name="all", version=VERSION, description="TODO: Descriptions"),
    ]

    DEFAULT_CONFIG_NAME = "all"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "original": datasets.Value("string"),
                "simple": datasets.Sequence(feature={"simplifications" : datasets.Value("string")})
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        filepaths = []
        if (self.config.name == 'all'):
            for subcorpus in _SUBCORPORA:
                filepaths.append(_SUBCORPORA[subcorpus]['path'])
        elif (self.config.name in _LANGUAGES):
            lang_code = _LANGUAGES[self.config.name]
            for subcorpus in _SUBCORPORA:
                if _SUBCORPORA[subcorpus]['language'] == lang_code:
                    filepaths.append(_SUBCORPORA[subcorpus]['path'])
        elif (self.config.name in _SUBCORPORA):
            filepaths = [_SUBCORPORA[self.config.name]['path']]
        else:
            print("Invalid configuration name: " + self.config.name + ".  Try 'all', 'English', 'ASSET', etc.")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": filepaths,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": filepaths,
                    "split": "val",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": filepaths,
                    "split": "test"
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepaths, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        df = pd.DataFrame()

        if (len(filepaths) > 1):
            for filepath in filepaths:
                if os.path.exists(filepath + "_" + split + ".csv"):
                    df = pd.concat([df, pd.read_csv(filepath + "_" + split + ".csv")])

            # shuffle the combined dataset
            df = df.sample(frac=1, random_state=3600).reset_index(drop=True)
        else:
            if os.path.exists(filepaths[0] + "_" + split + ".csv"):
                df = pd.read_csv(filepaths[0] + "_" + split + ".csv")

        if len(df) > 0:
            for key, row in df.iterrows():
                # Yields examples as (key, example) tuples
                original = row["original"]
                simple = []
                for label,content in row.items():
                    if label != "original" and type(content) != float:
                        simple.append({"simplifications": content})
                yield key, {
                    "original": original,
                    "simple": simple
                }