from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.finance.choices import ChargeRequestStatusChoices
from apps.finance.models import ChargeRequest
from apps.user.models import User


class ChargeRequestViewSetTest(APITestCase):

    def setUp(self):
        self.seller = User.objects.create_user(
            username="seller",
            password="sellerpass",
            is_staff=False,
            is_superuser=False
        )

        self.other_seller = User.objects.create_user(
            username="other_seller",
            password="otherpass",
            is_staff=False,
            is_superuser=False
        )

        self.request1 = ChargeRequest.objects.create(
            user=self.seller,
            amount=1000,
            status=ChargeRequestStatusChoices.pending
        )

        self.request2 = ChargeRequest.objects.create(
            user=self.other_seller,
            amount=500,
            status=ChargeRequestStatusChoices.pending
        )

        self.url = reverse("seller-charge-request-list")

    def test_seller_can_list_own_charge_requests(self):
        self.client.force_authenticate(user=self.seller)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.request1.id)

    def test_seller_can_create_charge_request(self):
        self.client.force_authenticate(user=self.seller)
        payload = {"amount": 2000}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 2000)

    def test_non_seller_cannot_access(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.force_authenticate(user=admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
