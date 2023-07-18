import os
from io import StringIO
from bs4 import BeautifulSoup
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import sent_tokenize

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter

from datatypes import AlignedParallelDocument, CorpusLoader, Corpus, ParallelDocument

# Expecting Corpus in the following format
#   - Corpus_for_Text_Simplification_of_German (parent directory)
#       - output_html_files
#           - 9_LS.tcf.pdf
#           - 9_AS.tcf.pdf
#           - 8_LS.tcf.pdf
#           - 8_AS.tcf.pdf
#           - ...
#       - output_pdf_files
#           - 5792_LS.tcf.html
#           - 5792_AS.tcf.html
#           - 5791_LS.tcf.html
#           - 5791_AS.tcf.html
#           - ...
class SimpleGermanLoader(CorpusLoader):
    def load(self, path):
        simple_german = Corpus([], word_tokenizer=ToktokTokenizer(), name = "Simple German", language="German")
        self.add_simple_german_directory(path, simple_german)
        return [simple_german]

    def add_simple_german_directory(self, path, corpus):
        self.add_simple_german_pdf_dir(os.path.join(path, 'output_pdf_files'), corpus)
        self.add_simple_german_html_dir(os.path.join(path, 'output_html_files'), corpus)

    def add_simple_german_pdf_dir(self, path, corpus):
        for filename in os.listdir(path):
            if '_LS.tcf.pdf' in filename:
                basename = filename[:-11]
                corpus.documents.append(self.create_simple_german_pdf_doc(os.path.join(path, basename + '_AS.tcf.pdf'), os.path.join(path, basename + '_LS.tcf.pdf'), basename))

    def create_simple_german_pdf_doc(self, orig_path, simp_path, name=''):
        original = self.parse_pdf(orig_path)
        simple = self.parse_pdf(simp_path)

        orig_items = sent_tokenize(original)
        simp_items = sent_tokenize(simple)

        return ParallelDocument('sentence', orig_items, simp_items, name)

    def parse_pdf(self, path):
        text = []
        # Adapted from http://survivalengineer.blogspot.com/2014/04/parsing-pdfs-in-python.html
        with open(path, 'rb') as orig_pdf:
            # Create the document model from the file
            document = PDFDocument(PDFParser(orig_pdf))
            # Try to parse the document
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            # Create a PDF resource manager object that stores shared resources.
            rsrcmgr = PDFResourceManager()
            # Create a buffer for the parsed text
            retstr = StringIO()
            # Spacing parameters for parsing
            laparams = LAParams()

            # Create a PDF interpreter object
            interpreter = PDFPageInterpreter(rsrcmgr, TextConverter(rsrcmgr, retstr, laparams = laparams))

            # Process each page contained in the document.
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
        
            text = retstr.getvalue().splitlines()
        text = ''.join(text)
        text = text.replace('\n', '').strip('\n')
        return text

    def add_simple_german_html_dir(self, path, corpus):
        for filename in os.listdir(path):
            if '_LS.tcf.html' in filename:
                basename = filename[:-12]
                corpus.documents.append(self.create_simple_german_html_doc(os.path.join(path, basename + '_AS.tcf.html'), os.path.join(path, basename + '_LS.tcf.html'), basename))

    def create_simple_german_html_doc(self, orig_path, simp_path, name=''):
        original = self.parse_html(orig_path)
        simple = self.parse_html(simp_path)

        orig_items = sent_tokenize(original)
        simp_items = sent_tokenize(simple)

        return ParallelDocument('sentence', orig_items, simp_items, name)

    def parse_html(self, path):
        text = ''
        with open(path, 'r') as html:
            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()
        text = text.replace('\n', '').strip('\n')
        return text