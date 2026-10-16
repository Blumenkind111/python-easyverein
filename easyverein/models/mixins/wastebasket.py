"""Fields for resources that support the wastebasket."""

from pydantic import BaseModel, Field

from easyverein.core.types import DateTime


class WastebasketMixin(BaseModel):
    """Deletion metadata for objects with wastebasket support."""

    deleteAfterDate: DateTime | None = Field(default=None, alias="_deleteAfterDate")
    """Date after which a deleted object may be purged."""
    deletedBy: str | None = Field(default=None, alias="_deletedBy")
    """User who moved the object to the wastebasket."""
