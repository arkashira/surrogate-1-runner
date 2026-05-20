"""
error_handler
==============

A lightweight, configurable error‑notification system for data‑ingestion pipelines.

Features
--------
* **Email** (SMTP) and **Slack** (incoming webhook) notifications.
* Rich error context (type, message, stack trace, dataset/shard/runner IDs, etc.).
* Asynchronous dispatch – the ingestion job never blocks on network I/O.
* Environment‑driven configuration – no secrets in code.
* Decorator helper for quick integration.

Typical usage
-------------