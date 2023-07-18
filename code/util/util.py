import pandas as pd

language_map = {\
    "English": "en",\
    "Spanish": "es",\
    "Italian": "it",\
    "French": "fr",\
    "Japanese": "ja",\
    "Brazilian Portuguese": "pt-br",\
    "BrazilianPortuguese": "pt-br",\
    "German": "de",\
    "Basque": "eu",\
    "Russian": "ru",\
    "Danish": "da",\
    "Urdu": "ur",\
    "Slovene": "sl",\
}

def convert_language_name_to_code(language):
    if language in language_map:
        return language_map[language]
    return language

name_map = {
    "Simpitiki Italian Wikipedia": "Simpitiki Wiki",
    "RuAdapt Encyclopedia B-C": "RuAdapt Enc B-C",
    "Simpitiki Trento":"Simpitiki PA",
    "PorSimples Strong":"PorSimples Str",
    "GEOLino Corpus":"GEOLinoTest",
    "SimplifyUR":"SimplifyUR",
    "Easy Japanese Corpus":"Easy Japanese",
    "Terence":"Terence",
    "Structural CBST":"CBST Structural",
    "Newsela ES 1-2":"Newsela ES 1-2",
    "Newsela ES 0-1":"Newsela ES 0-1",
    "Intuitive CBST":"CBST Intuitive",
    "CLEAR Corpus":"CLEAR",
    "PorSimples Natural":"PorSimples Nat",
    "RuAdapt Literature":"RuAdapt Lit",
    "RuAdapt Encyclopedia A-B":"RuAdapt Enc A-B",
    "RuAdapt Encyclopedia A-C":"RuAdapt Enc A-C",
    "Newsela ES 2-3":"Newsela ES 2-3",
    "PaCCSS-IT Corpus":"PaCCSS-IT",
    "Newsela ES 3-4":"Newsela ES 3-4",
    "Easy Japanese Extended":"Easy Japanese Ext",
    "Teacher":"Teacher",
    "TextComplexityDE Parallel Corpus":"TextComplexityDE",
    "DSim Corpus":"DSim",
    "RuWikiLarge":"RuWikiLarge",
    "WikiLargeFR Corpus":"WikiLargeFR",
    "RSSE Corpus":"RSSE",
    "RuAdapt Fairytales":"RuAdapt Fairy",
    "German News B2-OR":"German News B2",
    "Simplext":"Simplext",
    "German News A2-OR":"German News A2",
    "TerenceTeacher": "Terence & Teacher"
}

def better_names(name):
    if name in name_map:
        return name_map[name]
    return name

def better_lang(lang):
    if lang == "BrazilianPortuguese":
        return "Brazilian Portuguese"
    return lang

# converts ('original','simple') pairs to Pandas DataFrame with columns 'original', 'simple'
def pairs_to_pandas(pairs):
    orig, simp = zip(*pairs)
    pair_pd = pd.DataFrame.from_dict({'original':orig, 'simple':simp})
    return pair_pd

# output ('original', 'simple') pairs to csv file
def generate_csv(o_s_pairs, output_path):
    df = pairs_to_pandas(o_s_pairs)
    df.to_csv(output_path, index=False)

