"""Alerting module for drift detection notifications."""

from alerting.slack import SlackAlertHandler, AlertingConfig

__all__ = ["SlackAlertHandler", "AlertingConfig"]