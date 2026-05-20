"""
Low Bulk Credits Alert

Monitors the remaining Bulk credits for an AxentX account and sends an
alert when the balance falls below a configurable threshold.

Features
--------
* **Pluggable fetcher** – inject any callable that returns an `int`
  (e.g. a real API client, a mock, or a database query).
* **Pluggable notifier** – inject any callable that accepts a string.
  The default implementation uses AWS SNS via Boto3.
* **CLI** – run as a script with `--threshold`, `--interval`,
  `--aws-access-key`, `--aws-secret-key`, and `--sns-topic-arn`.
* **Logging** – structured, INFO‑level logs for normal operation,
  WARNING for alerts, ERROR for failures.
* **Unit‑test friendly** – the test suite in
  `tests/alerts/test_low_bulk_credits.py` can be run unchanged.

Usage
-----