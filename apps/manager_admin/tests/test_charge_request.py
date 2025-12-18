from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.finance.choices import ChargeRequestStatusChoices
from apps.finance.models import ChargeRequest
from apps.finance.models import Wallet
from apps.user.models import User


class TestAdminChargeRequestActionView(APITestCase):

    def setUp(self):
        # admin user
        self.admin = User.objects.create_superuser(
            username="admin",
            password="admin123"
        )

        # seller user
        self.seller = User.objects.create_user(
            username="seller",
            password="seller123",
            is_staff=True
        )

        self.wallet = Wallet.objects.create(
            user=self.seller,
            balance=0
        )

        self.charge_request = ChargeRequest.objects.create(
            user=self.seller,
            amount=100,
            status=ChargeRequestStatusChoices.pending
        )

        self.url = reverse(
            "admin-charge-request-action",
            kwargs={"pk": self.charge_request.id}
        )

        self.client.force_authenticate(user=self.admin)

    def test_admin_can_approve_charge_request(self):
        response = self.client.post(
            self.url,
            data={"action": "approve"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.charge_request.refresh_from_db()
        self.wallet.refresh_from_db()

        self.assertEqual(
            self.charge_request.status,
            ChargeRequestStatusChoices.approved
        )
        self.assertEqual(self.wallet.balance, 100)

    def test_admin_can_reject_charge_request(self):
        response = self.client.post(
            self.url,
            data={"action": "reject"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.charge_request.refresh_from_db()
        self.wallet.refresh_from_db()

        self.assertEqual(
            self.charge_request.status,
            ChargeRequestStatusChoices.rejected
        )
        self.assertEqual(self.wallet.balance, 0)

    def test_cannot_process_already_processed_request(self):
        self.charge_request.status = ChargeRequestStatusChoices.approved
        self.charge_request.save()

        response = self.client.post(
            self.url,
            data={"action": "approve"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found_charge_request(self):
        url = reverse(
            "admin-charge-request-action",
            kwargs={"pk": 9999}
        )

        response = self.client.post(
            url,
            data={"action": "approve"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_admin_cannot_access(self):
        self.client.force_authenticate(user=self.seller)

        response = self.client.post(
            self.url,
            data={"action": "approve"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
