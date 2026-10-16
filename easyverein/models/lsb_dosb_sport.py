from easyverein.models.mixins.base import EasyVereinBase

from .mixins.empty_strings_mixin import EmptyStringsToNone
from .mixins.timestamps import TimestampsMixin


class LsbDosbSport(EasyVereinBase, EmptyStringsToNone, TimestampsMixin):
    """
    Pydantic Model for a LSB/DOSB Sport.
    """

    __v3_names__ = {"organizationelement_ptr": None}

    title: str | None = None
    sportNumber: str | None = None
    federationNumber: str | None = None
    organizationelement_ptr: int | None = None
