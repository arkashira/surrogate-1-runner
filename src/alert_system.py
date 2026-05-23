"""
Threshold‑based P&L alert system.

The module contains a single public class, `ThresholdAlert`, that
checks profit / loss values against user‑defined thresholds and
sends an email when any threshold is breached.

The design favours:

*   **Testability** – an `EmailSender` protocol is injected.
*   **Clarity** – the public API is tiny and self‑documenting.
*   **Extensibility** – you can replace the email backend without touching
    the alert logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol, Tuple, Optional


class EmailSender(Protocol):
    """Protocol for an object that can send an e‑mail."""

    def send(self, subject: str, body: str, recipients: List[str]) -> None:
        """Send an e‑mail to the given recipients."""
        ...


@dataclass
class ThresholdAlert:
    """
    Configure profit/loss thresholds and send alerts.

    Parameters
    ----------
    profit_threshold : float
        Profit value that triggers an alert when exceeded.
    loss_threshold : float
        Loss value that triggers an alert when exceeded.
    recipients : list[str]
        E‑mail addresses that receive the alert.
    email_sender : EmailSender
        Object that implements the :class:`EmailSender` protocol.
    """

    profit_threshold: float
    loss_threshold: float
    recipients: List[str]
    email_sender: EmailSender

    def check_and_alert(self, profit: float, loss: float) -> Optional[str]:
        """
        Evaluate the supplied profit/loss values and send an alert if needed.

        Returns
        -------
        str | None
            The subject line that was sent, or ``None`` if no alert was required.
        """
        alerts: List[Tuple[str, float]] = []

        if profit > self.profit_threshold:
            alerts.append(
                (
                    f"Profit threshold exceeded: {profit:.2f} > "
                    f"{self.profit_threshold:.2f}",
                    profit,
                )
            )

        if loss > self.loss_threshold:
            alerts.append(
                (
                    f"Loss threshold exceeded: {loss:.2f} > "
                    f"{self.loss_threshold:.2f}",
                    loss,
                )
            )

        if not alerts:
            return None

        subject = "Profit & Loss Threshold Alert"
        body_lines = [
            f"Alert triggered at {len(alerts)} threshold(s).",
            "",
        ]

        for msg, value in alerts:
            body_lines.append(f"- {msg} (value: {value:.2f})")

        body_lines.extend(
            [
                "",
                "Please review the recent financial data and take necessary action.",
            ]
        )

        body = "\n".join(body_lines)

        self.email_sender.send(subject, body, self.recipients)
        return subject