import os
import xml.etree.ElementTree as ET
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - SimplextData (parent directory)
#       - simplext_corpus_part1
#           - FILE.full.xml
#           - FILE.simp.xml
#      - simplext_corpus_part2
#           - FILE.full.xml
#           - FILE.simp.xml
class SimplextLoader(CorpusLoader):
    def load(self, path):
        output = []
    
        if(self.keep_subdivisions):
            corpus1 = Corpus([], word_tokenizer=ToktokTokenizer(), name="Simplext Part 1", language="Spanish")
            corpus2 = Corpus([], word_tokenizer=ToktokTokenizer(), name="Simplext Part 2", language="Spanish")
            self.add_simplext_directory(os.path.join(path, 'simplext_corpus_part1'), corpus1)
            self.add_simplext_directory(os.path.join(path, 'simplext_corpus_part2'), corpus2)
            output.append(corpus1)
            output.append(corpus2)
        else:
            corpus = Corpus([], word_tokenizer=ToktokTokenizer(), name="Simplext", language="Spanish")
            self.add_simplext_directory(os.path.join(path, 'simplext_corpus_part1'), corpus)
            self.add_simplext_directory(os.path.join(path, 'simplext_corpus_part2'), corpus)
            output.append(corpus)
        
        return output

    def add_simplext_directory(self, directory, corpus):
        for filename in os.listdir(directory):
            if '.full.xml' in filename:
                base_name = filename[:-9]
                corpus.documents.append(self.create_simplext_parallel_document(os.path.join(directory, filename), os.path.join(directory, base_name + '.simp.xml'), base_name))

    def create_simplext_parallel_document(self, original_path, simple_path, name=""):
        
        original_sents, original_to_simplified_alignment, max_original_alignment_index = self.create_simplext_alignment(original_path)
        simplified_sents, simplified_to_original_alignment, max_simplified_alignment_index = self.create_simplext_alignment(simple_path)

        assert max_original_alignment_index <= len(simplified_sents)
        assert max_simplified_alignment_index <= len(original_sents)
        
        return AlignedParallelDocument("sentence", original_sents, simplified_sents, original_to_simplified_alignment, simplified_to_original_alignment, name)

    def create_simplext_alignment(self, path):
        document = ET.parse(path).getroot()

        sents = []
        doc_to_doc_alignment = []
        max_alignment_index = 0

        for sentence in document:
            text = sentence.text.strip('\n')
            sents.append(text)
            alignment = sentence.attrib['alignedSents'].split(';')
            if len(alignment) >= 1 and len(alignment[0]) > 0:
                indices = [int(s) for s in alignment]
                max_alignment_index = max(max_alignment_index, max(indices))
                doc_to_doc_alignment.append(indices)
            else:
                doc_to_doc_alignment.append([])
        
        return sents, doc_to_doc_alignment, max_alignment_index