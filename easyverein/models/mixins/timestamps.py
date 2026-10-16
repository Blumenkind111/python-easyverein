"""Timestamp fields returned by API resources."""

from pydantic import BaseModel

from easyverein.core.types import DateTime


class TimestampsMixin(BaseModel):
    """Creation and modification times on resource responses."""

    created_at: DateTime | None = None
    updated_at: DateTime | None = None
