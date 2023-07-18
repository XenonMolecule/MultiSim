import os
import xml.etree.ElementTree as ET
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - ETSC_CBST (parent directory)
#       - FILE_str.txt
#       - FILE_int.txt
#       - FILE_str.ann
#       - FILE_int.ann
class CBSTLoader(CorpusLoader):
    def load(self, path):
        output = []

        if(self.keep_subdivisions):
            structural = Corpus([], word_tokenizer=ToktokTokenizer(), name="Structural CBST", language="Basque")
            intuitive = Corpus([], word_tokenizer=ToktokTokenizer(), name="Intuitive CBST", language="Basque")
            self.add_CBST_document_set(path, structural, "str")
            self.add_CBST_document_set(path, intuitive, "int")
            output.append(structural)
            output.append(intuitive)
        else:
            corpus = Corpus([], word_tokenizer=ToktokTokenizer(), name = "CBST", language="Basque")
            self.add_CBST_document_set(path, corpus, "str")
            self.add_CBST_document_set(path, corpus, "int")
            output.append(corpus)

        return output

    def add_CBST_document_set(self, directory, corpus, suffix="str", filenames=["Bernoulli", "Exoplanetak", "Etxeko"]):
        for filename in filenames:
            corpus.documents.append(self.create_CBST_parallel_document(os.path.join(directory, filename + "_" + suffix + ".txt"), filename + "_" + suffix))

    def create_CBST_parallel_document(self, path, name=""):
        original = ""
        simplified = ""
        with open(path, 'r') as file:
            xml = file.read().replace('\n','').split('</doc>')
            original = xml[0] + "</doc>"
            simplified = xml[1] + "</doc>"
        
        original_sents, original_to_simplified_alignment, max_original_alignment_index = self.create_CBST_alignment(original)
        simplified_sents, simplified_to_original_alignment, max_simplified_alignment_index = self.create_CBST_alignment(simplified)
        
        assert max_original_alignment_index <= len(simplified_sents)
        assert max_simplified_alignment_index <= len(original_sents)
        
        return AlignedParallelDocument("sentence", original_sents, simplified_sents, original_to_simplified_alignment, simplified_to_original_alignment, name)
            
    def create_CBST_alignment(self, xml_str):
        document = ET.fromstring(xml_str)

        sents = []
        doc_to_doc_alignment = []
        max_alignment_index = 0

        for sentence in document:
            sents.append(sentence.text.strip('\n'))
            alignment = sentence.attrib['frase_all'].split(';')
            if len(alignment) >= 1 and len(alignment[0]) > 0:
                indices = [int(s)-1 for s in alignment]
                max_alignment_index = max(max_alignment_index, max(indices))
                doc_to_doc_alignment.append(indices)
            else:
                doc_to_doc_alignment.append([])
        
        return sents, doc_to_doc_alignment, max_alignment_index