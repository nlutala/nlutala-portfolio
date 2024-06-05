from django.test import Client, TestCase

class TestViews(TestCase):
    # ============== Tests for the index view ====================
    def test_index_is_accessible(self):
        client = Client()
        response = client.post("")
        assert response.status_code == 200
        assert response.content_type == "text/html; charset=utf-8"

    def test_projects_page_is_accessible_from_index(self):
        client = Client()
        response = client.post("")
        response = client.get("/projects")
        assert response.status_code == 200

    def test_contact_page_is_accessible_from_index(self):
        client = Client()
        response = client.post("")
        response = client.get("/contact")
        assert response.status_code == 200

    # ============== Tests for the projects view ====================
    def test_projects_is_accessible(self):
        client = Client()
        response = client.post("projects")
        assert response.status_code == 200
        assert response.content_type == "text/html; charset=utf-8"

    def test_index_page_is_accessible_from_projects(self):
        client = Client()
        response = client.post("projects")
        response = client.get("")
        assert response.status_code == 200

    def test_contact_page_is_accessible_from_projects(self):
        client = Client()
        response = client.post("projects")
        response = client.get("/contact")
        assert response.status_code == 200

    # ============== Tests for the contact view ====================
    def test_contact_is_accessible(self):
        client = Client()
        response = client.post("contact")
        assert response.status_code == 200
        assert response.content_type == "text/html; charset=utf-8"

    def test_index_page_is_accessible_from_contact(self):
        client = Client()
        response = client.post("contact")
        response = client.get("")
        assert response.status_code == 200

    def test_projects_page_is_accessible_from_contact(self):
        client = Client()
        response = client.post("contact")
        response = client.get("/projects")
        assert response.status_code == 200
