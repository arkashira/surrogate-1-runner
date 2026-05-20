"""
Price aggregation utilities.

This module provides an in‑memory store for price data coming from multiple
vendors.  It exposes helper functions that are used by the API layer to
persist new price entries, fetch the lowest current price for a component,
and retrieve the full price history.

The store keeps data in the following structure: