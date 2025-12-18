from django.db import transaction

from apps.finance.choices import TransactionTypeChoices
from apps.finance.exceptions import InsufficientBalanceException
from apps.finance.models import Transaction, Wallet


class WalletService:

    @staticmethod
    @transaction.atomic
    def deposit(wallet, amount):
        wallet.balance += amount
        wallet.save(update_fields=["balance"])
        Transaction.objects.create(wallet=wallet, amount=amount, type=TransactionTypeChoices.deposit)

    @staticmethod
    @transaction.atomic
    def withdraw(wallet_id, amount, reference):
        wallet = (
            Wallet.objects
            .select_for_update()
            .get(id=wallet_id)
        )
        if wallet.balance < amount:
            raise InsufficientBalanceException()
        wallet.balance -= amount
        wallet.save(update_fields=["balance"])
        Transaction.objects.create(wallet=wallet, amount=amount, type=TransactionTypeChoices.withdraw,
                                   charge_target=reference)
