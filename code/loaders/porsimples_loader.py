import os
import xml.etree.ElementTree as ET
import re
from nltk.tokenize.toktok import ToktokTokenizer

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus\

# Expecting Corpus in the following format
#   - PorSimples (parent directory)
#       - zh
#           - production1
#               - production1_strong-xces.xml
#               - production1_strong-s.xml
#               - production1_strong-logical.xml
#               - production1_strong.txt
#               - production1_natural-simplify.xml
#               - production1_natural-align.xml
#               - production1_natural-xces.xml
#               - production1_natural-pos.xml
#               - production1_natural-token.xml
#               - production1_natural-s.xml
#               - production1_natural-logical.xml
#               - production1_natural.txt
#               - production1-simplify.xml
#               - production1-align.xml
#               - production1-xces.xml
#               - production1-pos.xml
#               - production1-token.xml
#               - production1-s.xml
#               - production1-logical.xml
#               - production1.txt
#           - etc.
#       - folha
#           - etc.
class PorSimplesLoader(CorpusLoader):

    def __init__(self, keep_train_test_split=False, keep_subdivisions=False, keep_strong_natural_split=True):
        self.keep_train_test_split = keep_train_test_split # if the dataset has provided a train/test split return separate train/test corpora from the original split
        self.keep_subdivisions = keep_subdivisions # if the dataset was organized in some way keep the organization based on those divisions
        self.keep_strong_natural_split = keep_strong_natural_split # PorSimples is divided into natural simplifications and strong simplifications of those natural simplifications

    def load(self, path):
        output = []

        zero_hora_natural = Corpus([], word_tokenizer=ToktokTokenizer(), name="Zero Hora Natural", language="Brazilian Portuguese")
        zero_hora_strong = Corpus([], word_tokenizer=ToktokTokenizer(), name="Zero Hora Strong", language="Brazilian Portuguese")
        folha_natural = Corpus([], word_tokenizer=ToktokTokenizer(), name="Folha Natural", language="Brazilian Portuguese")
        folha_strong = Corpus([], word_tokenizer=ToktokTokenizer(), name="Folha Strong", language="Brazilian Portuguese")

        self.add_porsimples_directory(os.path.join(path, 'zh'), zero_hora_natural, zero_hora_strong)
        self.add_porsimples_directory(os.path.join(path, 'folha'), folha_natural, folha_strong)

        if(self.keep_subdivisions and self.keep_strong_natural_split):
            output = [zero_hora_natural, zero_hora_strong, folha_natural, folha_strong]
        elif(self.keep_subdivisions):
            zero_hora = Corpus(zero_hora_natural.documents + zero_hora_strong.documents, word_tokenizer=ToktokTokenizer(), name="PorSimples Zero Hora", language="Brazilian Portuguese")
            folha = Corpus(folha_natural.documents + folha_strong.documents, word_tokenizer=ToktokTokenizer(), name="PorSimples Folha", language="Brazilian Portuguese")
            output = [zero_hora, folha]
        elif(self.keep_strong_natural_split):
            natural = Corpus(zero_hora_natural.documents + folha_natural.documents, word_tokenizer=ToktokTokenizer(), name="PorSimples Natural", language="Brazilian Portuguese")
            strong = Corpus(zero_hora_strong.documents + folha_strong.documents, word_tokenizer=ToktokTokenizer(), name="PorSimples Strong", language="Brazilian Portuguese")
            output = [natural, strong]
        else:
            porsimples = Corpus(zero_hora_natural.documents + zero_hora_strong.documents + folha_natural.documents + folha_strong.documents, word_tokenizer=ToktokTokenizer(), name="PorSimples", language="Brazilian Portuguese")
            output = [porsimples]
        return output

    def add_porsimples_directory(self, directory, corpus_natural, corpus_strong):
        for dirname in os.listdir(directory):
            if dirname == '.DS_Store':
                continue
            corpus_natural.documents.append(self.create_porsimples_parallel_document(os.path.join(directory, dirname), "", "_natural", dirname, dirname + "-orig-to-natural"))
            corpus_strong.documents.append(self.create_porsimples_parallel_document(os.path.join(directory, dirname), "_natural", "_strong", dirname, dirname + "-natural-to-strong"))
    
    def create_porsimples_parallel_document(self, directory, original_suffix="", simple_suffix="_natural", filename="", name=""):
        original_text_file = os.path.join(directory, filename+original_suffix+".txt")
        simple_text_file = os.path.join(directory, filename+simple_suffix+".txt")
        original_segmentation = os.path.join(directory, filename+original_suffix+"-s.xml")
        simple_segmentation = os.path.join(directory, filename+simple_suffix+"-s.xml")
        alignment_file = os.path.join(directory, filename+original_suffix+"-align.xml")

        original_sents, original_to_simplified_alignment, max_original_alignment_index,\
            simplified_sents, simplified_to_original_alignment, max_simplified_alignment_index =\
                self.create_porsimples_alignment(original_text_file, simple_text_file, original_segmentation, simple_segmentation, alignment_file)

        assert max_original_alignment_index <= len(simplified_sents)
        assert max_simplified_alignment_index <= len(original_sents)
        
        return AlignedParallelDocument("sentence", original_sents, simplified_sents, original_to_simplified_alignment, simplified_to_original_alignment, name)

    def create_porsimples_alignment(self, original_text_file, simple_text_file, original_segmentation, simple_segmentation, alignment_file):
        original_sentences, original_mapping = self.segment_porsimples_document(original_text_file, original_segmentation, trust_paragraph_idx=(not '_natural' in original_text_file or 'production88' in original_text_file))
        simple_sentences, simple_mapping = self.segment_porsimples_document(simple_text_file, simple_segmentation, trust_paragraph_idx=('production88' in simple_text_file and '_natural' in simple_text_file), overwrite_paragraph=('production27' in simple_text_file or 'production35' in simple_text_file and '_strong' in simple_text_file))

        orig_to_simp_alignment = [[] for i in range(len(original_sentences))]
        simp_to_orig_alignment = [[] for i in range(len(simple_sentences))]

        max_orig_idx = 0
        max_simp_idx = 0

        with open(alignment_file, mode='r', encoding='latin_1') as f:
            alignment = ET.parse(f).getroot()
            for links in alignment[1]:
                for link in links:
                    source = link[0].attrib['{http://www.x3.org/1999/xlink}href']
                    dest = link[1].attrib['{http://www.x3.org/1999/xlink}href']
                    source_arr = []
                    dest_arr = []
                    if 'p0s1' in source:
                        source_arr = []
                    elif 'pointer' in source:
                        _, start, _, stop, _ = source.split("'")
                        start_idx = original_mapping[start]
                        stop_idx = original_mapping[stop]
                        source_arr = list(range(start_idx, stop_idx+1))
                    else:
                        source_arr = [original_mapping[source[1:]]]
                    if 'p0s1' in dest:
                        dest_arr = []
                    elif 'pointer' in dest:
                        _, start, _, stop, _ = dest.split("'")
                        start_idx = simple_mapping[start]
                        stop_idx = simple_mapping[stop]
                        dest_arr = list(range(start_idx, stop_idx+1))
                    else:
                        dest_arr = [simple_mapping[dest[1:]]]
                    for i in source_arr:
                        orig_to_simp_alignment[i].extend(dest_arr)
                    for i in dest_arr:
                        simp_to_orig_alignment[i].extend(source_arr)

                    if len(dest_arr) > 0:
                        max_orig_idx = max(dest_arr[-1], max_orig_idx)
                    if len(source_arr) > 0:
                        max_simp_idx = max(source_arr[-1], max_simp_idx)
        
        return original_sentences, orig_to_simp_alignment, max_orig_idx, simple_sentences, simp_to_orig_alignment, max_simp_idx


    def segment_porsimples_document(self, file_path, segmentation_path, trust_paragraph_idx=False, overwrite_paragraph=False):
        doc_paragraphs = []
        with open(file_path, mode='r', encoding='latin_1') as f:
            doc_paragraphs = f.readlines()
            doc_paragraphs = [line[:-1] for line in doc_paragraphs if line != '\n' and line!='\t\n' and line!=' \n']

        sentences = []
        mapping = {}
        segmentation = ET.parse(segmentation_path).getroot()
        last_p = 0
        last_s = 0
        p_idx = 0
        paragraph = []
        for struct in segmentation: 
            feat = struct[0]
            p, s= feat.attrib['value'].split('s')
            curr_p = int(p[1:])
            s = int(s)
            if last_p != curr_p:
                assert last_s == len(paragraph)
                if trust_paragraph_idx:
                    p_idx = curr_p
                else:
                    p_idx += 1
                # Must segment sentences ourselves because the indices provided aren't correct for all files :(
                paragraph = re.split('(\. |; |: |\? |! |\?"|\.com|!")', doc_paragraphs[p_idx])
                paragraph = [sent for sent in paragraph if sent!='' and sent!=' ' and sent!='.']
                new_paragraph = []
                for i in range(len(paragraph)):
                    if i%2 == 0:
                        new_paragraph.append(paragraph[i])
                    else:
                        new_paragraph[-1] = new_paragraph[-1] + paragraph[i]
                paragraph = new_paragraph

                if paragraph == []:
                    paragraph = doc_paragraphs[p_idx]

                # Edge case where sentence segmentation fails becuase of sentence 'Literalmente'
                # However "- Claro" is treated differently between strong and natural simplifications
                prepend_edge_cases = [('Literalmente. ', 'none'), ('- Claro. ', 'strong'), ('Resultado: ', 'none'), ('?". ', 'none'), ('Contraponto. ', 'none')]
                for edge_case, exception in prepend_edge_cases:
                    if edge_case in paragraph:
                        if exception=='none' or exception not in file_path:
                            idx = paragraph.index(edge_case)
                            paragraph.pop(idx)
                            if len(paragraph) > idx:
                                paragraph[idx] = edge_case + '. ' + paragraph[idx]
                # Edge cases where we actually do not want to split on colon
                append_edge_cases = ['580. ', '580 . ', 'R$ 2,486 . ', '-3,6 ºC ', 'Caixa Postal 70540 - CEP 22741-971', 'de 27 de outubro a 12 de novembro.']
                for edge_case in append_edge_cases:
                    if edge_case in paragraph:
                        idx = paragraph.index(edge_case)
                        paragraph.pop(idx)
                        if idx != 0:
                            paragraph[idx-1] = paragraph[idx-1] + ' ' + edge_case

                if 'No bairro Jardim Botânico, zona leste da Capital, às 7h os termômetros marcaram 0,3 ºC - a mais baixa temperatura na cidade desde 2000' in paragraph:
                    paragraph.pop(0)
                    paragraph.insert(0, 'a mais baixa temperatura na cidade desde 2000')
                    paragraph.insert(0, 'No bairro Jardim Botânico, zona leste da Capital, às 7h os termômetros marcaram 0,3 ºC')

                if 'As cartas deverão ser enviadas para Caixa Postal 70540 - CEP 22741-971' in paragraph and not trust_paragraph_idx:
                    paragraph.pop()

                if ['Irena dos Santos atravessava a Terceira Avenida, esquina com a Rua 2.500, às 8h 40min, quando foi atingida. ', 'Segundo a PM, o carro, com placas MDJ 9866, conduzido pelo soldado Jorge - o sobrenome não foi divulgado - deslocava-se pela avenida a caminho de uma ocorrência na Rua 2.870. ', 'Irena teria atravessado fora da faixa de pedestres e o policial na direção tentou frear, sem, no entanto, conseguir evitar o acidente. '] == paragraph:
                    paragraph = ['Irena dos Santos atravessava a Terceira Avenida, esquina com a Rua 2.500, às 8h 40min, quando foi atingida. ', 'Segundo a PM, o carro, com placas MDJ 9866, conduzido pelo soldado Jorge - o sobrenome não foi divulgado - deslocava-se pela avenida a caminho de uma ocorrência na Rua 2.870. Irena teria atravessado fora da faixa de pedestres e o policial na direção tentou frear, sem, no entanto, conseguir evitar o acidente. ']

                if ['Irena dos Santos atravessava a Terceira Avenida, na esquina com a Rua 2.500 às 8h40min , no momento em que foi atingida. ', 'De acordo com a PM, o carro deslocava-se pela avenida a caminho de uma ocorrência na Rua 2.870. ', 'O soldado Jorge conduzia o carro de placas MDJ 9866 . ', 'Irena teria atravessado fora da faixa de pedestres e o policial na direção tentou frear, mas não conseguiu evitar o acidente.'] == paragraph:
                    paragraph = ['Irena dos Santos atravessava a Terceira Avenida, na esquina com a Rua 2.500 às 8h40min , no momento em que foi atingida. ', 'De acordo com a PM, o carro deslocava-se pela avenida a caminho de uma ocorrência na Rua 2.870. ', 'O soldado Jorge conduzia o carro de placas MDJ 9866 . Irena teria atravessado fora da faixa de pedestres e o policial na direção tentou frear, mas não conseguiu evitar o acidente.']

                if ['- Cancelei a audiência em nome da educação. ', 'O que eles fizeram não é educação. ', 'O que eles fizeram não é exemplo para seus alunos - resumiu a governadora.'] == paragraph:
                    paragraph = ['- Cancelei a audiência em nome da educação. ', 'O que eles fizeram não é educação. O que eles fizeram não é exemplo para seus alunos - resumiu a governadora.']

                if ['A sexta-feira deveria ter sido o último dia do encontro. ', 'Mas as sessões foram adiadas para hoje. ', 'Isso nunca aconteceu antes. ', 'Sem que os países tivessem chegado a um acordo, os debates foram encerrados por volta das 23h. ', 'Um dos debatedores disse que, depois de um dia de negociações intensas nos bastidores e de muitos telefonemas entre as comissões de representantes e seus países, o clima dentro do plenário do centro de convenções era tranqüilo. ', 'O plenário do centro de convenções é onde as equipes de representantes conversam.'] == paragraph:
                    paragraph.pop()

            sentences.append(paragraph[s-1].strip('\n'))
            if not overwrite_paragraph:
                mapping[feat.attrib['value']] = len(sentences) - 1
            else:
                mapping['p' + str(p_idx) + 's' + str(s)] = len(sentences) - 1
            last_s = s
            last_p = curr_p
        assert last_s == len(paragraph)
        
        return sentences, mapping