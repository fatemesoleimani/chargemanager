from rest_framework import status
from rest_framework.exceptions import APIException


class WalletException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Wallet operation failed"
    default_code = "wallet_error"


class InsufficientBalanceException(WalletException):
    default_detail = "Insufficient balance"
    default_code = "insufficient_balance"


class ChargeRequestNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Charge request not found"
    default_code = "charge_request_not_found"


class ChargeRequestAlreadyProcessed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Charge request already processed"
    default_code = "charge_request_already_processed"
