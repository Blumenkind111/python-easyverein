"""
Invoice Item model
"""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from easyverein.models.mixins.base import EasyVereinBase, EasyVereinFilter

from ..core.types import EasyVereinReference, FilterIntList, Sphere
from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.required_attributes import required_mixin
from .mixins.timestamps import TimestampsMixin


class InvoiceItemBase(EasyVereinBase):
    """
    | Representative Model Class | Update Model Class | Create Model Class |
    | --- | --- | --- |
    | `InvoiceItem` | `InvoiceItemUpdate` | `InvoiceItemCreate` |

    !!! tip "Creating Invoice Items"
        Invoice Items can either be created together with the invoice using `invoice.create_with_items`, or
        added to an existing invoice that is still in the draft state. In the latter case, the tax and gross
        settings must match those of the invoice this item is being attached to, otherwise invoice generation
        (setting `isDraft` to `False`) will fail on EV API side.
    """

    relatedInvoice: EasyVereinReference | Invoice | None = None
    quantity: float | None = None
    unitPrice: float | None = None
    totalPrice: float | None = None
    title: str | None = None
    description: str | None = None
    taxRate: float | None = None
    gross: bool | None = None
    taxName: str | None = None
    sphere: Sphere | None = None
    billingAccount: EasyVereinReference | BillingAccount | None = None
    costCentre: Annotated[str, Field(max_length=8)] | None = None
    articleObject: EasyVereinReference | None = None
    deductedExistingBalance: bool | None = None


class InvoiceItem(InvoiceItemBase, EmptyStringsToNone, TimestampsMixin):
    """
    Pydantic model representing an InvoiceItem
    """

    __v3_names__ = {"organizationelement_ptr": None}

    copiedFromParent: Any | None = Field(default=None, alias="_copiedFromParent")
    electronic_total_price_with_tax: float | None = None
    organizationelement_ptr: int | None = None


class InvoiceItemCreate(
    InvoiceItemBase,
    required_mixin(["title", "quantity", "unitPrice"]),  # type: ignore
):
    """
    Pydantic model representing an InvoiceItem
    """


class InvoiceItemUpdate(InvoiceItemBase):
    """
    Pydantic model used to patch an InvoiceItem
    """


class InvoiceItemFilter(EasyVereinFilter):
    """
    Pydantic model used to filter invoice items
    """

    __v3_names__ = {
        "relatedInvoice__not": "related_invoice__ne",
        "billingAccount__not": "billing_account__ne",
    }

    id__in: FilterIntList | None = None
    title: str | None = None
    taxName: str | None = None
    quantity__gte: int | None = None
    quantity__lte: int | None = None
    description: str | None = None
    billingAccount__isnull: bool | None = None
    relatedInvoice: int | None = None
    relatedInvoice__not: int | None = None
    relatedInvoice__isDraft: bool | None = None
    relatedInvoice__isTemplate: bool | None = None
    billingAccount: str | None = None
    billingAccount__not: str | None = None
    ordering: str | None = None
    search: str | None = None


from .billing_account import BillingAccount  # noqa: E402
from .invoice import Invoice  # noqa: E402
