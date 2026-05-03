from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class ConnectorError(Exception):
    """Base connector error with consistent model."""

    def __init__(
        self,
        code: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        retryable: bool = False,
    ) -> None:
        self.code = code
        self.message = message
        self.context = context or {}
        self.retryable = retryable
        super().__init__(f"[{code}] {message}")


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderStatus(str, Enum):
    NEW = "new"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"


class RiskResult(str, Enum):
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class Order:
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    qty: float
    price: Optional[float] = None
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    client_order_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class Fill:
    order_id: str
    symbol: str
    side: OrderSide
    qty: float
    price: float
    fill_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class Quote:
    symbol: str
    bid: float
    ask: float
    last: float
    volume: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    snapshot: Dict[str, Any]
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class RiskCheckRequest:
    symbol: str
    qty: float
    side: OrderSide
    current_position: float
    position_limit: float
    price: float


@dataclass(frozen=True)
class RiskCheckResponse:
    symbol: str
    result: RiskResult
    reason: Optional[str] = None
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))