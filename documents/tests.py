from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User


class DocumentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test1234"
        )

        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": "testuser",
                "password": "test1234"
            }
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def test_dashboard(self):
        response = self.client.get("/api/documents/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search(self):
        response = self.client.get("/api/documents/search/?q=test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recycle_bin(self):
        response = self.client.get("/api/documents/recycle_bin/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)