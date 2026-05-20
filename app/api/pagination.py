from rest_framework.pagination import LimitOffsetPagination
from typing import Dict, Any


class CostPagination(LimitOffsetPagination):
    """
    Pagination for the workers list.

    * Default limit = 100 (covers the “> 100 workers” requirement).
    * Max limit     = 200 (prevents pathological payloads).
    * Query‑string parameters are ``limit`` and ``offset`` – the DRF defaults.
    """
    default_limit = 100
    max_limit = 200
    limit_query_param = "limit"
    offset_query_param = "offset"

    # ------------------------------------------------------------------
    # Helper that returns ONLY the pagination meta‑data (no “results” key)
    # ------------------------------------------------------------------
    def get_meta(self) -> Dict[str, Any]:
        """
        Returns a dict that can be merged into the top‑level response.
        Mirrors the structure of DRF’s default paginated response but
        without the nested ``results`` list – the list lives under the
        ``workers`` key that we control.
        """
        return {
            "limit": self.limit,
            "offset": self.offset,
            "count": self.count,
        }