from concurrent.futures import ThreadPoolExecutor
from django.db import connection, close_old_connections
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.finance.models import Wallet
from apps.user.models import User
from apps.finance.services.wallet import WalletService


class TestSellerPhoneChargeStress(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.seller1 = User.objects.create_user(username="seller1", password="pass")
        self.seller2 = User.objects.create_user(username="seller2", password="pass")

        self.wallet1 = Wallet.objects.create(user=self.seller1, balance=0)
        self.wallet2 = Wallet.objects.create(user=self.seller2, balance=0)

        self.charge_url = reverse("charge-phone")

    @staticmethod
    def deposit(wallet, amount):
        WalletService.deposit(wallet, amount)

    def withdraw_request(self, user, amount):
        close_old_connections()
        client = APIClient()
        client.force_authenticate(user)
        response = client.post(self.charge_url, {
            "phone_number": "09123456789",
            "amount": amount
        }, format="json")
        connection.close()
        return response.status_code

    def test_stress_concurrent_transactions(self):
        for _ in range(10):
            self.deposit(self.wallet1, 100)
            self.deposit(self.wallet2, 200)

        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()
        assert self.wallet1.balance == 1000
        assert self.wallet2.balance == 2000

        results = []

        tasks = []
        for _ in range(500):
            tasks.append((self.seller1, 1))
            tasks.append((self.seller2, 1))

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.withdraw_request, user, amt) for user, amt in tasks]
            for f in futures:
                results.append(f.result())

        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()

        success1 = sum(1 for i, (user, _) in enumerate(tasks[:500*2:2]) if results[i*2] == 200)
        success2 = sum(1 for i, (user, _) in enumerate(tasks[1:500*2:2]) if results[i*2+1] == 200)

        print(f"Seller1: success={success1}, Wallet balance={self.wallet1.balance}")
        print(f"Seller2: success={success2}, Wallet balance={self.wallet2.balance}")

        assert self.wallet1.balance == 1000 - success1
        assert self.wallet2.balance == 2000 - success2
        assert success1 * 1 <= 1000
        assert success2 * 1 <= 2000
        assert len(results) == 1000
