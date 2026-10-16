"""Methods for the bank-account endpoint."""

import logging

from ..core.client import EasyvereinClient
from ..models.bank_account import BankAccount, BankAccountCreate, BankAccountFilter, BankAccountUpdate
from .mixins.crud import CRUDMixin
from .mixins.recycle_bin import RecycleBinMixin


class BankAccountMixin(
    CRUDMixin[BankAccount, BankAccountCreate, BankAccountUpdate, BankAccountFilter],
    RecycleBinMixin[BankAccount],
):
    def __init__(self, client: EasyvereinClient, logger: logging.Logger):
        super().__init__()
        self.endpoint_name = "bank-account"
        self.return_type = BankAccount
        self.c = client
        self.logger = logger
