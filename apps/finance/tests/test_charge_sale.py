from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.finance.models import Transaction
from apps.finance.models import Wallet
from apps.user.models import User


class SellerPhoneChargeViewTest(APITestCase):

    def setUp(self):
        self.seller = User.objects.create_user(username="seller", password="sellerpass")
        self.wallet = Wallet.objects.create(user=self.seller, balance=1000)

        self.url = reverse("charge-phone")

    def test_seller_can_charge_phone(self):
        self.client.force_authenticate(user=self.seller)
        payload = {"phone_number": "09123456789", "amount": 500}

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Phone charged successfully.")

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 500)

        tx = Transaction.objects.filter(wallet=self.wallet, amount=500).first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.charge_target, "09123456789")

    def test_seller_cannot_overcharge_wallet(self):
        self.client.force_authenticate(user=self.seller)
        payload = {"phone_number": "09123456789", "amount": 2000}

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient balance", str(response.data.get("detail", "")))

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1000)

    def test_non_seller_cannot_access(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.force_authenticate(user=admin)
        payload = {"phone_number": "09123456789", "amount": 100}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
