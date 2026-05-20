"""
Utility module for converting currency amounts between different currencies.
Currently supports a static set of conversion rates. In a production
environment, this would call an external exchange rate API.
"""

from __future__ import annotations

import datetime
from typing import Dict

# Static conversion rates relative to USD
# These rates are illustrative and should be refreshed regularly.
STATIC_RATES: Dict[str, float] = {
    "USD": 1.0,
    "EUR": 1.10,   # 1 EUR = 1.10 USD
    "GBP": 1.25,   # 1 GBP = 1.25 USD
    "JPY": 0.009,  # 1 JPY = 0.009 USD
    "AUD": 0.70,   # 1 AUD = 0.70 USD
}

class CurrencyConverter:
    """
    Converter that can transform monetary amounts from one currency to another.
    """

    def __init__(self, rates: Dict[str, float] | None = None) -> None:
        """
        Initialize the converter with optional custom rates.
        :param rates: Mapping of currency code to USD conversion rate.
        """
        self.rates = rates or STATIC_RATES

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert an amount from one currency to another.

        :param amount: The monetary amount to convert.
        :param from_currency: The ISO currency code of the source amount.
        :param to_currency: The ISO currency code of the target amount.
        :return: The converted amount rounded to 2 decimal places.
        :raises ValueError: If either currency is unsupported.
        """
        if from_currency not in self.rates:
            raise ValueError(f"Unsupported source currency: {from_currency}")
        if to_currency not in self.rates:
            raise ValueError(f"Unsupported target currency: {to_currency}")

        # Convert to USD first, then to target currency
        amount_in_usd = amount * self.rates[from_currency]
        converted_amount = amount_in_usd / self.rates[to_currency]
        return round(converted_amount, 2)

    def update_rates(self, new_rates: Dict[str, float]) -> None:
        """
        Merge new rates into the existing rate table.
        :param new_rates: Mapping of currency code to USD conversion rate.
        """
        self.rates.update(new_rates)

    def get_rate(self, currency: str) -> float:
        """
        Retrieve the USD conversion rate for a given currency.
        :param currency: ISO currency code.
        :return: Conversion rate.
        """
        return self.rates.get(currency, 0.0)