import os
from nltk.tokenize.toktok import ToktokTokenizer
import pandas as pd
from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - asset-main (parent directory)
#       - dataset
#           - asset.valid.simp.9
#           - ...
#           - asset.valid.simp.0
#           - asset.valid.orig
#           - asset.test.simp.9
#           - ...
#           - asset.test.orig
class AssetLoader(CorpusLoader):
    
    def load(self, path):
        output = []

        valid = Corpus([], word_tokenizer=ToktokTokenizer(), name = "ASSET Valid", language="English")
        test = Corpus([], word_tokenizer=ToktokTokenizer(), name = "ASSET Test", language="English")

        self.load_split(os.path.join(path,'dataset'), "valid", valid)
        self.load_split(os.path.join(path,'dataset'), "test", test)

        if (not self.keep_train_test_split):
            asset_documents = valid.documents + test.documents
            asset = Corpus(asset_documents, word_tokenizer=ToktokTokenizer(), name="ASSET", language="English")
            output = [asset]
        else:
            output = [valid, test]

        return output

    def load_split(self, path, split, corpus):
        original = []
        with open(os.path.join(path,"asset." + split + ".orig")) as orig_file:
            original = orig_file.readlines()
            original = [line.strip() for line in original]

        o_to_s = [[i] for i in range(len(original))]
        s_to_o = [[i] for i in range(len(original))]
        
        for i in range(10):
            simplified = []
            with open(os.path.join(path, "asset." + split + ".simp." + str(i))) as simp_file:
                simplified = simp_file.readlines()
                simplified = [line.strip() for line in simplified]
            corpus.documents.append(AlignedParallelDocument("sentence", original, simplified, o_to_s, s_to_o, name="asset." + split + ".simp." + str(i)))

    def output_refs_to_csv(self, path, split, output):
        corpus = Corpus([], word_tokenizer=ToktokTokenizer(), name = "ASSET " + split, language="English")

        self.load_split(os.path.join(path,'dataset'), split, corpus)

        df = pd.DataFrame.from_dict({
            'original':corpus.documents[0].original_items,
            'simple0':corpus.documents[0].simplified_items,
            'simple1':corpus.documents[1].simplified_items,
            'simple2':corpus.documents[2].simplified_items,
            'simple3':corpus.documents[3].simplified_items,
            'simple4':corpus.documents[4].simplified_items,
            'simple5':corpus.documents[5].simplified_items,
            'simple6':corpus.documents[6].simplified_items,
            'simple7':corpus.documents[7].simplified_items,
            'simple8':corpus.documents[8].simplified_items,
            'simple9':corpus.documents[9].simplified_items,
        })

        df.to_csv(output, index=False)