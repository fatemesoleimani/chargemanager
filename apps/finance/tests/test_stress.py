import threading
from concurrent.futures import ThreadPoolExecutor

from django.db import connection, close_old_connections
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.finance.models import Wallet
from apps.user.models import User


class TestSellerPhoneChargeConcurrency(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.user = User.objects.create_user(
            username="seller",
            password="pass"
        )
        self.wallet = Wallet.objects.create(user=self.user, balance=1000)
        self.url = reverse("charge-phone")

    def make_request(self, results, index):
        close_old_connections()

        client = APIClient()
        client.force_authenticate(self.user)

        response = client.post(self.url, {
            "phone_number": "09123456789",
            "amount": 15
        }, format="json")

        results[index] = response.status_code

        connection.close()

    def test_parallel_withdrawals(self):
        results = {}
        count_thread = 190

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [
                executor.submit(self.make_request, results, i)
                for i in range(count_thread)
            ]
            for f in futures:
                f.result()

        self.wallet.refresh_from_db()

        success_count = list(results.values()).count(200)
        fail_count = list(results.values()).count(400)

        assert success_count * 15 <= 1000
        assert fail_count == count_thread - success_count
        self.wallet.refresh_from_db()
        assert self.wallet.balance == 1000 - (success_count * 15)
