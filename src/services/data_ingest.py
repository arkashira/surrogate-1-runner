import logging
from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, ValidationError, validator
from sqlalchemy.orm import Session

from ..models import PricingRawData

log = logging.getLogger(__name__)


class PricingData(BaseModel):
    """
    Pydantic schema for a single pricing record.
    All fields are required and type‑checked.
    """
    product_id: str
    market: str
    price: float
    currency: str
    timestamp: datetime  # parsed automatically by Pydantic

    @validator("currency")
    def currency_must_be_three_letters(cls, v: str) -> str:
        if len(v) != 3 or not v.isalpha():
            raise ValueError("currency must be a 3‑letter ISO code")
        return v.upper()


def ingest_pricing_data(raw_records: List[Dict[str, Any]], db: Session) -> Dict[str, int]:
    """
    Validate each dict against ``PricingData``.
    * Valid rows are turned into ``PricingRawData`` ORM objects.
    * Invalid rows are logged (but do **not** abort the whole batch).
    * All valid rows are inserted with ``bulk_save_objects`` for speed.

    Returns a dict with counts: ``{'accepted': int, 'rejected': int}``.
    """
    accepted: List[PricingRawData] = []
    rejected = 0

    for idx, rec in enumerate(raw_records):
        try:
            # Pydantic will coerce types (e.g. string → datetime)
            model = PricingData(**rec)

            orm_obj = PricingRawData(
                product_id=model.product_id,
                market=model.market,
                price=model.price,
                currency=model.currency,
                timestamp=model.timestamp,
                raw_json=rec,
            )
            accepted.append(orm_obj)
        except ValidationError as exc:
            rejected += 1
            log.warning(
                "Record %d failed validation: %s – errors: %s",
                idx,
                rec,
                exc.errors(),
            )
        except Exception as exc:  # defensive – should never happen
            rejected += 1
            log.exception("Unexpected error processing record %d: %s", idx, rec)

    if not accepted:
        log.info("No valid pricing records to insert")
        return {"accepted": 0, "rejected": rejected}

    try:
        db.bulk_save_objects(accepted)
        db.commit()
        log.info("Inserted %d valid pricing records", len(accepted))
    except Exception:
        db.rollback()
        log.exception("Database insertion failed")
        raise

    return {"accepted": len(accepted), "rejected": rejected}