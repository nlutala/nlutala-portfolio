'''
A class that merges a pdf inputted by a user
'''

from pypdf import PdfWriter
import os

class PDFMerger():
    def __init__(self) -> None:
        '''
        Params:
        pdf (string) - list of pdf file names from the current directory of this script (pdf_merger.py)
        '''
        self.pdfs = []
        self.base_dir = os.path.dirname(__file__)
        self.merger = PdfWriter()
        
    def get_pdfs(self) -> list:
        return self.pdfs
        
    def get_base_dir(self) -> str:
        return self.base_dir
        
    def add_pdf_files(self, pdfs: list) -> None:
        self.pdfs = pdfs
        if len(self.pdfs) == 0:
            raise ValueError("There are no PDF files in this directory to merge.")
        elif len(self.pdfs) == 1:
            raise ValueError("There is only PDF file in this directory. There needs to be 2 or more PDF files in this directory to merge.")

    def merge_pdfs(self, filename: str):
        '''
        Params:
        filename (str) - a name for the new merged pdf
        
        Returns the merged pdf in a new screen
        '''
        # Create the file
        if len(filename.strip()) == 0:
            filename = "merged_file.pdf"
        
        for pdf in self.pdfs:
            if pdf.endswith(".pdf"):
                self.merger.append(os.path.join(self.base_dir, pdf))
            else: # Else statement may be redundant as I check for this below.
                raise TypeError("Expected PDF file(s) but a file with another file extension was given instead.")
        
        if filename.endswith(".pdf"):
            self.merger.write(os.path.join(self.base_dir, filename))
            self.merger.close()
            
            for p in self.pdfs:
                os.remove(os.path.join(self.base_dir, p))
            return os.path.join(self.base_dir, filename)
        else:
            self.merger.write(os.path.join(self.base_dir, f"{filename}.pdf"))
            self.merger.close()
            
            for p in self.pdfs:
                os.remove(os.path.join(self.base_dir, p))
            return os.path.join(self.base_dir, filename)
        
        