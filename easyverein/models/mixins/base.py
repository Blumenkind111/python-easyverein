from pydantic import PositiveInt

from easyverein.core.types import EasyVereinReference
from easyverein.models.mixins.versioned import VersionedModel


class EasyVereinBase(VersionedModel):
    """
    Identity fields shared by API objects.
    """

    id: PositiveInt | None = None
    org: EasyVereinReference | None = None


class EasyVereinFilter(VersionedModel):
    """
    Base class for all filter models.

    Filter attributes use the API v2.0 names and are translated automatically when using API v3.0.
    """

    __v3_names__ = {
        # v3.0 removed the `deleted` filter, use the recycle bin methods (`get_deleted`) instead
        "deleted": None,
    }
