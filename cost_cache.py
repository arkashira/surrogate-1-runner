class CostCache:
    """
    High‑level cache that stores :class:`CostData` objects grouped by
    ``account_id`` and ``service``.  Internally it re‑uses ``InMemoryCache`` so
    we keep the thread‑safety and TTL logic in one place.
    """

    def __init__(self, ttl: int = DEFAULT_TTL):
        # The underlying generic cache stores CostData objects keyed by a tuple.
        self._cache = InMemoryCache[CostData](ttl=ttl)

    # ------------------------------------------------------------------
    # Public helpers – they hide the tuple‑key implementation from callers
    # ------------------------------------------------------------------
    def _make_key(self, account_id: str, service: str) -> Tuple[str, str]:
        return (account_id, service)

    def get(self, account_id: str, service: str) -> Optional[CostData]:
        """Return cached ``CostData`` or ``None`` if missing/expired."""
        key = self._make_key(account_id, service)
        try:
            return self._cache.get(key)
        except KeyError:
            return None

    def set(self, account_id: str, service: str, cost_data: CostData) -> None:
        """Cache *cost_data* for the given ``account_id`` / ``service`` pair."""
        key = self._make_key(account_id, service)
        self._cache.set(key, cost_data)

    def clear(self) -> None:
        """Flush the entire cost cache."""
        self._cache.clear()