from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.finance.choices import ChargeRequestStatusChoices
from apps.finance.models import ChargeRequest
from apps.user.models import User


class AdminChargeRequestListViewTest(APITestCase):

    def setUp(self):
        ChargeRequest.objects.all().delete()

        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpass"
        )

        self.request1 = ChargeRequest.objects.create(
            user=self.admin_user,
            amount=1000,
            status=ChargeRequestStatusChoices.pending
        )
        self.request2 = ChargeRequest.objects.create(
            user=self.admin_user,
            amount=2000,
            status=ChargeRequestStatusChoices.approved
        )

        self.url = reverse("admin-charge-request-list")

    def test_admin_can_list_charge_requests(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 2)
        returned_ids = [item["id"] for item in results]
        self.assertIn(self.request1.id, returned_ids)
        self.assertIn(self.request2.id, returned_ids)

    def test_non_admin_cannot_list_charge_requests(self):
        seller = User.objects.create_user(username="seller", password="sellerpass")
        self.client.force_authenticate(user=seller)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
