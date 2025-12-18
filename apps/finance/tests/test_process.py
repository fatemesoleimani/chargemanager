from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.finance.choices import ChargeRequestStatusChoices
from apps.finance.models import Transaction, ChargeRequest, Wallet
from apps.user.models import User


class SellerWorkflowIntegrationAPITest(APITestCase):

    def setUp(self):
        self.seller1 = User.objects.create_user(username="seller1", password="pass", is_staff=False,
                                                is_superuser=False)
        self.seller2 = User.objects.create_user(username="seller2", password="pass", is_staff=False,
                                                is_superuser=False)
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")

        self.wallet1 = Wallet.objects.create(user=self.seller1)
        self.wallet2 = Wallet.objects.create(user=self.seller2)

        self.charge_request_url = reverse("seller-charge-request-list")
        self.phone_charge_url = reverse("charge-phone")

    def approve_charge_request_via_api(self, charge_request):
        self.client.force_authenticate(user=self.admin_user)
        action_url = reverse("admin-charge-request-action", kwargs={"pk": charge_request.id})
        response = self.client.post(action_url, {"action": "approve"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        charge_request.refresh_from_db()
        self.assertEqual(charge_request.status, ChargeRequestStatusChoices.approved)

    def test_seller_api_workflow(self):
        sellers = [
            (self.seller1, self.wallet1),
            (self.seller2, self.wallet2)
        ]
        deposit_amount = 1000
        sale_amount = 1

        deposit_count = 10
        sale_count = 1000

        for seller, wallet in sellers:
            for _ in range(deposit_count):
                self.client.force_authenticate(user=seller)
                response = self.client.post(
                    self.charge_request_url,
                    {"amount": deposit_amount},
                    format="json"
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                charge_request = ChargeRequest.objects.get(pk=response.data["id"])
                self.approve_charge_request_via_api(charge_request)

        for seller, wallet in sellers:
            wallet.refresh_from_db()
            self.assertEqual(wallet.balance, deposit_count * deposit_amount)

        for seller, wallet in sellers:
            self.client.force_authenticate(user=seller)
            for i in range(sale_count):
                response = self.client.post(
                    self.phone_charge_url, {"phone_number": f"09123456789", "amount": sale_amount},
                    format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        for seller, wallet in sellers:
            wallet.refresh_from_db()
            expected_balance = deposit_count * deposit_amount - sale_count * sale_amount
            self.assertEqual(wallet.balance, expected_balance)

        for seller, wallet in sellers:
            tx_count = Transaction.objects.filter(wallet=wallet).count()
            self.assertEqual(tx_count, deposit_count + sale_count)
