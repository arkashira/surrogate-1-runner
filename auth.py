"""
Secure authentication protocol for the surrogate-1 terminal environment.

This module provides a simple JWT‑based authentication mechanism that can be
used by the terminal service to validate incoming requests.  The implementation
is intentionally lightweight to keep the runtime overhead minimal while still
offering strong security guarantees.

Features
--------
* Token generation with configurable expiry.
* Token verification that checks signature, expiration, and payload integrity.
* Helper to load configuration from ``config.json`` located in the same
  directory as this module.

Configuration
-------------
The module expects a ``config.json`` file with the following structure: