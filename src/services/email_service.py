import os
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

@dataclass
class StatusChangeContext:
    entity_type: str
    entity_id: str
    entity_name: str
    previous_status: str
    new_status: str
    changed_by: Optional[str]
    changed_at: str
    public_url: str
    owner_email: str
    subscriber_emails: List[str]

class StatusChangeEmailSender:
    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: int = 587,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
        use_tls: bool = True,
        sender: Optional[str] = None,
        templates_dir: str = TEMPLATES_DIR,
    ):
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST")
        self.smtp_port = int(smtp_port or os.getenv("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
        self.use_tls = use_tls
        self.sender = sender or os.getenv("EMAIL_SENDER") or "no-reply@axentx.local"

        self._validate_config()

        env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.template = env.get_template("emails/status_change.html")

    def _validate_config(self) -> None:
        if not self.smtp_host:
            raise RuntimeError("SMTP_HOST is required to send email")

    def render_status_change(self, ctx: StatusChangeContext) -> str:
        return self.template.render(
            entity_type=ctx.entity_type,
            entity_id=ctx.entity_id,
            entity_name=ctx.entity_name,
            previous_status=ctx.previous_status,
            new_status=ctx.new_status,
            changed_by=ctx.changed_by,
            changed_at=ctx.changed_at,
            public_url=ctx.public_url,
        )

    def send_status_change(self, ctx: StatusChangeContext) -> None:
        html_body = self.render_status_change(ctx)

        recipients = list(set([ctx.owner_email] + ctx.subscriber_emails))
        if not recipients:
            return

        msg = EmailMessage()
        msg["Subject"] = f"[Status] {ctx.entity_type} '{ctx.entity_name}' → {ctx.new_status}"
        msg["From"] = self.sender
        msg["To"] = ", ".join(recipients)
        msg.add_header("List-Unsubscribe", f"<mailto:{self.sender}?subject=unsubscribe>")
        msg.set_content(
            f"""\
Status change for {ctx.entity_type} '{ctx.entity_name}'

Previous: {ctx.previous_status}
New:      {ctx.new_status}
Changed:  {ctx.changed_at}
By:       {ctx.changed_by or "system"}

View: {ctx.public_url}
"""
        )
        msg.add_alternative(html_body, subtype="html")

        self._send(msg, recipients)

    def _send(self, msg: EmailMessage, recipients: List[str]) -> None:
        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
            if self.use_tls:
                server.starttls()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.sender, recipients, msg.as_string())