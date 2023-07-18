import os
from posixpath import basename
import xml.etree.ElementTree as ET

from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus

# Expecting Corpus in the following format
#   - CORPORA_TEXT_SIMP
#       - Teacher
#           - 1_anna_frank_last_senza_ann.txt
#           - ...
#       - Terence
#           - Un_estate
#               - un_estatedaricordare1.txt
#               - ...
#           - UgoScellino
#               - ...
#           - ...
#       - README.md
class TerenceTeacherLoader(CorpusLoader):

    def load(self, path):
        output = []

        terence = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Terence", language = "Italian")
        teacher = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Teacher", language = "Italian")

        self.build_terence_teacher_corpus(path, terence, teacher)

        if (not self.keep_subdivisions):
            terence_teacher = Corpus(terence.documents + teacher.documents, word_tokenizer=ToktokTokenizer(), name = "Terence Teacher", language = "Italian")
            output = [terence_teacher]
        else:
            output = [terence, teacher]

        return output

    def build_terence_teacher_corpus(self, path, terence, teacher):
        self.add_terence_teacher_directory(os.path.join(path, 'Teacher'), teacher, True)
        for dirname in os.listdir(os.path.join(path, 'Terence')):
            if dirname != '.DS_Store':
                self.add_terence_teacher_directory(os.path.join(path,'Terence',dirname), terence, False)

    def add_terence_teacher_directory(self, directory, corpus, teacher=True):
        for filename in os.listdir(directory):
            if '.txt' in filename:
                base_name = filename[:-4]
                corpus.documents.append(self.create_terence_teacher_parallel_document(os.path.join(directory, filename), teacher, name=base_name))

    def create_terence_teacher_parallel_document(self, path, teacher=True, name=""):
        orig_doc, simp_doc = None, None
    
        if(teacher):
            original, simplified = "", ""
            with open(path, 'r') as file:
                xml = file.read().replace('\n','').split('</doc>')
                original = xml[0] + "</doc>"
                simplified = xml[1] + "</doc>"
            
            orig_doc = ET.fromstring(original)
            simp_doc = ET.fromstring(simplified)

        else:
            with open(path, 'r') as file:
                xml = file.readlines()
                xml = [line for line in xml if '//' not in line]
                xml = ''.join(xml)
                doc = ET.fromstring(xml)
                orig_doc = doc[0]
                simp_doc = doc[1]

        o_sent, o_to_s, s_sent, s_to_o = self.create_terence_teacher_alignment(orig_doc, simp_doc, teacher)

        return AlignedParallelDocument('sentence', o_sent, s_sent, o_to_s, s_to_o, name)

    def create_terence_teacher_alignment(self, parsed_original, parsed_simple, teacher = True):
        attr = 'frase_all' if teacher else 'frase_al'
        
        o_sents = []
        o_to_s_alignment = []
        o_max_alignment_index = 0
        s_to_o_alignment = [[] for i in range(len(parsed_simple))]
        s_max_alignment_index = 0

        for i, sentence in enumerate(parsed_original):
            o_sents.append(sentence.text.strip('\n'))
            alignment = sentence.attrib[attr].split(';')
            if len(alignment) >= 1 and len(alignment[0]) > 0:
                indices = [int(s)-1 for s in alignment if s!='']
                o_max_alignment_index = max(o_max_alignment_index, max(indices))
                s_max_alignment_index = i
                o_to_s_alignment.append(indices)
                for idx in indices:
                    s_to_o_alignment[idx].append(i)
            else:
                o_to_s_alignment.append([])

        s_sents = []

        for sentence in parsed_simple:
            s_sents.append(sentence.text.strip('\n'))
        
        assert o_max_alignment_index <= len(s_sents)
        assert s_max_alignment_index <= len(o_sents)

        return o_sents, o_to_s_alignment, s_sents, s_to_o_alignment