"""Models for bank accounts."""

from __future__ import annotations

from pydantic import Field

from easyverein.models.mixins.base import EasyVereinBase, EasyVereinFilter

from ..core.types import Date, EasyVereinReference, FilterIntList, HexColor, Sphere
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin
from .mixins.timestamps import TimestampsMixin
from .mixins.wastebasket import WastebasketMixin


class BankAccountBase(EasyVereinBase, WastebasketMixin):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `BankAccount` | `BankAccountUpdate` | `BankAccountCreate` |
    """

    name: str | None = Field(default=None, max_length=200)
    color: HexColor = None
    short: str | None = Field(default=None, max_length=4)
    accountHolder: str | None = Field(default=None, max_length=200)
    bankName: str | None = Field(default=None, max_length=200)
    IBAN: str | None = Field(default=None, max_length=32)
    BIC: str | None = Field(default=None, max_length=11)
    startsaldo: float | None = None
    importSaldo: float | None = None
    sphere: Sphere | None = None
    computeStartsaldoOnImport: bool | None = None
    last_imported_date: Date | None = None
    creditor_address: EasyVereinReference | ContactDetails | None = None


class BankAccount(BankAccountBase, EmptyStringsToNone, TimestampsMixin):
    """Bank account returned by the API."""

    billingAccount: EasyVereinReference | BillingAccount | None = None


class BankAccountCreate(BankAccountBase, required_mixin(["name", "short"])):  # type: ignore
    """Data for creating a bank account."""


class BankAccountUpdate(BankAccountBase):
    """Data for updating a bank account."""


class BankAccountFilter(EasyVereinFilter):
    """Filters for listing bank accounts."""

    id__in: FilterIntList | None = None
    name: str | None = None
    short: str | None = None
    sphere: Sphere | None = None
    deleted: bool | None = None
    ordering: str | None = None
    search: str | None = None


from .billing_account import BillingAccount  # noqa: E402
from .contact_details import ContactDetails  # noqa: E402
