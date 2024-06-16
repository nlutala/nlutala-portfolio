from django.test import Client, TestCase

class TestViews(TestCase):
    # ============== Tests for the index view ====================
    def test_index_is_accessible(self):
        client = Client()
        response = client.get("")
        assert response.status_code == 200
        assert response['content-type'] == "text/html; charset=utf-8"

    # ============== Tests for the projects view ====================
    def test_projects_is_accessible(self):
        client = Client()
        response = client.get("/projects")
        assert response.status_code == 200
        assert response['content-type'] == "text/html; charset=utf-8"

    '''
    Tests for the PDF Merger page
    '''
    def test_pdf_merger_is_accessible(self):
        client = Client()
        response = client.get("/projects/pdf-merger")
        assert response.status_code == 200
        assert response['content-type'] == "text/html; charset=utf-8"

    '''
    Test for the Password Generator page
    '''
    def test_password_generator_is_accessible_without_slash(self):
        client = Client()
        response = client.get("/projects/password-generator")
        assert response.status_code == 200
        assert response['content-type'] == "text/html; charset=utf-8"

    def test_password_generator_is_accessible_with_slash(self):
        client = Client()
        response = client.get("/projects/password-generator/")
        assert response.status_code == 200
        assert response['content-type'] == "text/html; charset=utf-8"

    # ============== Tests for the contact view ====================
    def test_contact_is_accessible(self):
        client = Client()
        response = client.get("/contact")
        assert response.status_code == 200
        assert response['content-type'] == "text/html; charset=utf-8"
