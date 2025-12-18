from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.user.models import User


class UserProfileViewTest(APITestCase):

    def setUp(self):
        self.seller_user = User.objects.create_user(
            username="seller",
            password="sellerpass",
            is_staff=False,
            is_superuser=False
        )

        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpass"
        )

        self.url = reverse("user-profile")

    def test_seller_can_get_profile(self):
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.seller_user.username)
        self.assertIn("id", response.data)
        self.assertIn("is_active", response.data)

    def test_non_seller_cannot_get_profile(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
