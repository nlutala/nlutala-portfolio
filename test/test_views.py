from django.test import Client, TestCase
import os

class TestViews(TestCase):
    # ============== Tests for the index view ====================
    def test_index_is_accessible(self):
        client = Client()
        response = client.get("")
        assert response.status_code == 200
        assert self.assertTemplateUsed(template_name="index.html")
        assert response['content-type'] == "text/html; charset=utf-8"

    # ============== Tests for the projects view ====================
    def test_projects_is_accessible(self):
        client = Client()
        response = client.get("/projects")
        assert response.status_code == 200
        assert self.assertTemplateUsed(template_name="projects.html")
        assert response['content-type'] == "text/html; charset=utf-8"

    '''
    Tests for the PDF Merger page
    '''
    def test_pdf_merger_is_accessible(self):
        client = Client()
        response = client.get("/projects/pdf-merger")
        assert response.status_code == 200
        assert self.assertTemplateUsed(template_name="pdf_merger.html")
        assert response['content-type'] == "text/html; charset=utf-8"
        
    def test_client_stays_on_pdf_merger_page_if_submitted_no_files(self):
        client = Client()
        response = client.get("/projects/pdf-merger")
        response = client.post("/projects/pdf-merger")
        assert response.status_code == 200
        assert self.assertTemplateUsed(template_name="pdf_merger.html")
        assert response['content-type'] == "text/html; charset=utf-8"
        
    def test_client_stays_on_pdf_merger_page_if_submitted_one_file(self):
        client = Client()
        response = client.get("/projects/pdf-merger")
        BASE_DIR = os.path.dirname(__file__)
        file = os.path.join(BASE_DIR, "example_file_1.pdf")
        response = client.post("/projects/pdf-merger", {"formFileMultiple": file})
        assert response.status_code == 200
        assert self.assertTemplateUsed(template_name="pdf_merger.html")
        assert response['content-type'] == "text/html; charset=utf-8"
        
    def test_client_is_shown_merged_file_if_submitted_two_or_more_files(self):
        client = Client()
        response = client.get("/projects/pdf-merger")
        BASE_DIR = os.path.dirname(__file__)
        files = [
            os.path.join(BASE_DIR, "example_file_1.pdf"), 
            os.path.join(BASE_DIR, "example_file_2.pdf")
            ]
        response = client.post("/projects/pdf-merger", {"formFileMultiple": files})
        assert response.status_code == 200
        
        # The below is because the user is shown a page with their merged PDF file
        assert self.assertTemplateNotUsed("/projects/pdf_merger.html")

    '''
    Tests for the Password Generator page
    '''
    def test_pdf_merger_is_accessible_without_forward_slash(self):
        client = Client()
        response = client.get("/projects/password-generator")
        assert response.status_code == 200
        assert self.assertTemplateUsed(template_name="password_generator.html")
        assert response['content-type'] == "text/html; charset=utf-8"

    def test_pdf_merger_is_accessible_with_forward_slash(self):
        client = Client()
        response = client.get("/projects/password-generator/")
        assert response.status_code == 200
        assert self.assertTemplateUsed(template_name="password_generator.html")
        assert response['content-type'] == "text/html; charset=utf-8"

    # ============== Tests for the contact view ====================
    def test_contact_is_accessible(self):
        client = Client()
        response = client.get("/contact")
        assert response.status_code == 200
        assert response['content-type'] == "text/html; charset=utf-8"
