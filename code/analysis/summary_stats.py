from datatypes import Corpus, Document, ParallelDocument, AlignedParallelDocument
from collections import Counter
from util.util import convert_language_name_to_code

from fuzzywuzzy import fuzz

class SummaryStats:
    def __init__(self, corpus:Corpus = None):
        self.corpus = corpus
        self.calculate_summary_stats(self.corpus)

    def calculate_summary_stats(self, corpus:Corpus=None):
        if(corpus == None):
            if (self.corpus != None):
                corpus = self.corpus
            else:
                return
        else:
            self.corpus = corpus

        self.orig_token_counter = Counter()
        self.simp_token_counter = Counter()

        self.orig_paragraph_count, self.orig_sent_count, self.orig_token_count, self.orig_char_count = 0, 0, 0, 0
        self.simp_paragraph_count, self.simp_sent_count, self.simp_token_count, self.simp_char_count = 0 ,0, 0, 0
        self.deleted_count, self.split_count, self.same_count, self.reduced_count, self.merged_count, self.inserted_count = 0, 0, 0, 0, 0, 0

        for document in corpus.documents:
           p, s, t, c = self.count_instances(document, self.orig_token_counter, True)
           self.orig_paragraph_count += p
           self.orig_sent_count += s
           self.orig_token_count += t
           self.orig_char_count += c

           if (type(document) is ParallelDocument or type(document) is AlignedParallelDocument):
                p, s, t, c = self.count_instances(document, self.simp_token_counter, False)
                self.simp_paragraph_count += p
                self.simp_sent_count += s
                self.simp_token_count += t
                self.simp_char_count += c

    def count_instances(self, document:Document, token_counter:Counter, original:bool):
        paragraph_count, sent_count, token_count, char_count = 0, 0, 0, 0

        items = document.original_items if original else document.simplified_items
        
        for i, item in enumerate(items):
            char_count += len(item)
            tokens = []
            if (document.granularity == 'paragraph'):
                paragraph_count += 1
                sentences = self.corpus.sentence_tokenizer.tokenize(item)
                sent_count += len(sentences)
                for sentence in sentences:
                    tokens = self.corpus.word_tokenizer.tokenize(sentence)
            elif(document.granularity == 'sentence'):
                sent_count += 1
                tokens = self.corpus.word_tokenizer.tokenize(item)
            token_counter.update(tokens)
            token_count += len(tokens)
            if (type(document) is AlignedParallelDocument):
                if (original):
                    orig_alignment = document.original_to_simplified_alignment[i]
                    simp_alignment = []
                    simple_item = ""
                    if(orig_alignment != []):
                        simp_alignment = document.simplified_to_original_alignment[orig_alignment[0]]
                        simple_item = document.simplified_items[orig_alignment[0]]
                    self.update_orig_to_simp_align_counts(document.original_to_simplified_alignment[i], simp_alignment, item, simple_item, document.granularity)
                else:
                    self.update_simp_to_orig_align_counts(document.simplified_to_original_alignment[i])
        
        return paragraph_count, sent_count, token_count, char_count
    
    def update_orig_to_simp_align_counts(self, orig_alignment:list, simp_alignment:list, original:str, simplified:str, granularity:str):
        if (len(orig_alignment) == 0):
            self.deleted_count += 1
        if (len(orig_alignment) >= 2):
            self.split_count += 1
        if (len(orig_alignment) == 1):
            if (len(simp_alignment) == 1):
                ratio = fuzz.ratio(original, simplified)
                if ratio >= 95:
                    self.same_count += 1
                else:
                    self.reduced_count += 1
            elif (len(simp_alignment) >= 2):
                self.merged_count += 1

    def update_simp_to_orig_align_counts(self, simp_alignment:list):
        if (len(simp_alignment) == 0):
            self.inserted_count += 1
    
    def __repr__(self):
        if (self.corpus == None):
            return "Uninitialized"
        output = ["Summary Statistics for " + self.corpus.name]
        output.append("-"*len(output[0]))
        output.append(str(len(self.corpus.documents)) + " Documents\n")
        if (type(self.corpus.documents[0]) is AlignedParallelDocument):
            total = self.orig_sent_count if self.corpus.documents[0].granularity == 'sentence' else self.orig_paragraph_count

            output.append("\t\tcount\tpercentage")
            output.append("1-0 Deleted\t" + str(self.deleted_count) + "\t" + str(self.deleted_count/total))
            output.append("1-n Split\t" + str(self.split_count) + "\t" + str(self.split_count/total))
            output.append("1-1 Same\t" + str(self.same_count) + "\t" + str(self.same_count/total))
            output.append("1-1 Changed\t" + str(self.reduced_count) + "\t" + str(self.reduced_count/total))
            output.append("n-1 Merged\t" + str(self.merged_count) + "\t" + str(self.merged_count/total))
            output.append("0-1 Inserted\t" + str(self.inserted_count) + "\t" + "NA")
            output.append("")
        if (type(self.corpus.documents[0]) is ParallelDocument or type(self.corpus.documents[0]) is AlignedParallelDocument):
            output.append("\t\t\toriginal\t\tsimplified\t\t% Change")
            if (self.corpus.documents[0].granularity == 'paragraph'):
                output.append(format_per_change_row("Paragraph Count", self.orig_paragraph_count, self.simp_paragraph_count))
            output.append(format_per_change_row("Sentence Count\t", self.orig_sent_count, self.simp_sent_count))
            output.append(format_per_change_row("Token Count\t", self.orig_token_count, self.simp_token_count))
            output.append(format_per_change_row("Vocab Size\t", len(self.orig_token_counter), len(self.simp_token_counter)))
            output.append(format_per_change_row("Average Tokens / Sent", self.orig_token_count/self.orig_sent_count, self.simp_token_count/self.simp_sent_count))
            output.append(format_per_change_row("Average Char / Sentence", self.orig_char_count/self.orig_sent_count, self.simp_char_count/self.simp_sent_count))
            output.append(format_per_change_row("Average Char / Token", self.orig_char_count/self.orig_token_count, self.simp_char_count/self.simp_token_count))
            if (self.corpus.documents[0].granularity == 'paragraph'):
                output.append(format_per_change_row("Average Paragraphs / Article", self.orig_paragraph_count/len(self.corpus.documents), self.simp_paragraph_count/len(self.corpus.documents)))
            output.append(format_per_change_row("Average Sent / Article", self.orig_sent_count/len(self.corpus.documents), self.simp_sent_count/len(self.corpus.documents)))
        elif (type(self.corpus.documents[0]) is Document):
            output.append("\t\t\toriginal")
            if (self.corpus.documents[0].granularity == 'paragraph'):
                output.append("Paragraph Count\t" + str(self.orig_paragraph_count))
            output.append("Sentence Count\t\t" + str(self.orig_sent_count))
            output.append("Token Count\t\t" + str(self.orig_token_count))
            output.append("Vocab Size\t\t" + str(len(self.orig_token_counter)))
            output.append("Average Tokens / Sent\t" + str(self.orig_token_count/self.orig_sent_count))
            output.append("Average Char / Sentence\t" + str(self.orig_char_count/self.orig_sent_count))
            output.append("Average Char / Token\t" + str(self.orig_char_count/self.orig_token_count))
            if (self.corpus.documents[0].granularity == 'paragraph'):
                output.append("Average Paragraphs / Article\t" + str(self.orig_paragraph_count/len(self.corpus.documents)))
            output.append("Average Sent / Article\t" + str(self.orig_sent_count/len(self.corpus.documents)))
        
        return "\n".join(output)

    def to_basic_stats_latex_row(self):
        if(self.corpus == None):
            return "Uninititalized"
        output = [self.corpus.name]
        output.append(convert_language_name_to_code(self.corpus.language))
        output.append(str("{:,}".format(len(self.orig_token_counter))))
        output.append(str("{:,}".format(len(self.simp_token_counter))))
        output.append(str("{:,}".format(self.orig_token_count)))
        output.append(str("{:,}".format(self.simp_token_count)))
        output.append(str(round(self.orig_token_count/self.orig_sent_count, 2)))
        output.append(str(round(self.simp_token_count/self.simp_sent_count, 2)))
        output.append(str(round(self.orig_char_count/self.orig_token_count, 2)))
        output.append(str(round(self.simp_char_count/self.simp_token_count, 2)))

        # Should print --- for non document aligned corpora but I can do that manually
        output.append(str(round(self.orig_sent_count/len(self.corpus.documents), 2)))
        output.append(str(round(self.simp_sent_count/len(self.corpus.documents), 2)) + " \\\\")

        return " & ".join(output)

    def to_edit_ops_latex_row(self):
        # Simplext & 16.1\% & 32.2\% & 3.5\% & 47.3\% & 0.7\% & 19.3\% \\
        if(self.corpus == None):
            return "Uninititalized"
        output = [self.corpus.name]
        output.append(str(round(self.deleted_count/self.orig_sent_count * 100, 1)) + "\\%")
        output.append(str(round(self.split_count/self.orig_sent_count * 100, 1)) + "\\%")
        output.append(str(round(self.same_count/self.orig_sent_count * 100, 1)) + "\\%")
        output.append(str(round(self.reduced_count/self.orig_sent_count * 100, 1)) + "\\%")
        output.append(str(round(self.merged_count/self.orig_sent_count * 100, 1)) + "\\%")
        output.append(str(round(self.inserted_count/self.simp_sent_count * 100, 1)) + "\\% \\\\")

        return " & ".join(output)

def format_per_change_row(stat_name, num1, num2):
    sep1 = " \t\t\t" if len(str(num1)) <= 7 else " \t"
    sep2 = " \t\t\t" if len(str(num1)) <= 7 else " \t"

    return stat_name + "\t" + str(num1) + sep1 + str(num2) + sep2 + str(per_change(num1, num2))

def per_change(num1, num2):
    return (num2 - num1)/num1