from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.finance.choices import TransactionTypeChoices
from apps.finance.models import Transaction
from apps.finance.models import Wallet
from apps.user.models import User


class AdminTransactionListViewTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpass"
        )

        self.wallet = Wallet.objects.create(user=self.admin_user, balance=5000)

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

        self.url = reverse("admin-transaction-list")

    def test_admin_can_list_transactions(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 2)

        returned_ids = [tx["id"] for tx in results]
        self.assertIn(self.tx1.id, returned_ids)
        self.assertIn(self.tx2.id, returned_ids)

    def test_non_admin_cannot_list_transactions(self):
        seller = User.objects.create_user(username="seller", password="sellerpass")
        self.client.force_authenticate(user=seller)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
