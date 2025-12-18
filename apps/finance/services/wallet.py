from django.db import transaction

from apps.finance.choices import TransactionTypeChoices
from apps.finance.exceptions import InsufficientBalanceException
from apps.finance.models import Transaction


class WalletService:

    @staticmethod
    @transaction.atomic
    def deposit(wallet, amount):
        wallet.balance += amount
        wallet.save(update_fields=["balance"])
        Transaction.objects.create(wallet=wallet, amount=amount, type=TransactionTypeChoices.deposit)

    @staticmethod
    @transaction.atomic
    def withdraw(wallet, amount, reference):
        if wallet.balance < amount:
            raise InsufficientBalanceException()
        wallet.balance -= amount
        wallet.save(update_fields=["balance"])
        Transaction.objects.create(wallet=wallet, amount=amount, type=TransactionTypeChoices.withdraw,
                                   charge_target=reference)
