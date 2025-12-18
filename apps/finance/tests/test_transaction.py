from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.finance.choices import TransactionTypeChoices
from apps.finance.models import Transaction
from apps.finance.models import Wallet
from apps.user.models import User


class TransactionListViewTest(APITestCase):

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

        self.wallet = Wallet.objects.create(user=self.seller, balance=5000)

        self.tx1 = Transaction.objects.create(
            wallet=self.wallet,
            amount=1000,
            type=TransactionTypeChoices.deposit,
            charge_target="Initial deposit"
        )
        self.tx2 = Transaction.objects.create(
            wallet=self.wallet,
            amount=500,
            type=TransactionTypeChoices.withdraw,
            charge_target="PhoneCharge:09123456789"
        )

        self.url = reverse("transaction-list")

    def test_seller_can_list_transactions(self):
        self.client.force_authenticate(user=self.seller)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 2)

        returned_ids = [tx["id"] for tx in results]
        self.assertIn(self.tx1.id, returned_ids)
        self.assertIn(self.tx2.id, returned_ids)

    def test_non_seller_cannot_list_transactions(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.force_authenticate(user=admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
