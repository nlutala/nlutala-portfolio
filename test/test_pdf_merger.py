'''
Tests for the pdf_merger script
'''
from django.test import TestCase
from website.projects.pdf_merger import PDFMerger
from pypdf import PdfReader
import os

class TestPDFMerger(TestCase):
    def test_PDFMerger_pdfs_are_the_same_as_user_files_inputted_if_over_two_files(self):
        BASE_DIR = os.path.dirname(__file__)
        pdfs = [
            os.path.join(BASE_DIR, "example_file_1.pdf"),
            os.path.join(BASE_DIR, "example_file_2.pdf")
            ]
        merger = PDFMerger()
        merger.add_pdf_files(pdfs)
        assert len(pdfs) == len(merger.get_pdfs())
    
    def test_valueerror_is_raised_if_number_of_pdfs_is_zero(self):
        pdfs = []
        with self.assertRaises(ValueError):
            merger = PDFMerger()
            merger.add_pdf_files(pdfs)

    def test_valueerror_is_raised_if_number_of_pdfs_is_one(self):
        BASE_DIR = os.path.dirname(__file__)
        pdfs = [os.path.join(BASE_DIR, "example_file_1.pdf")]
        with self.assertRaises(ValueError):
            merger = PDFMerger()
            merger.add_pdf_files(pdfs)

    '''
    To look into later
    def test_number_of_pages_for_the_merged_pdf(self):
        BASE_DIR = os.path.dirname(__file__)
        pdfs = [
            os.path.join(BASE_DIR, "example_file_1.pdf"),
            os.path.join(BASE_DIR, "example_file_2.pdf")
            ]
        merger = PDFMerger()
        merger.merge_pdfs(response.get('mergedFileName', ""))
        file = [file for file in os.listdir(merger.get_base_dir())][0]
        output_file = os.path.join(merger.get_base_dir(), file)
        file1_num_pages = PdfReader(pdfs[0]).get_num_pages()
        file2_num_pages = PdfReader(pdfs[1]).get_num_pages()
        merged_file_num_pages = PdfReader(output_file).get_num_pages()
        assert file1_num_pages + file2_num_pages == merged_file_num_pages
        os.remove(output_file)
    '''
