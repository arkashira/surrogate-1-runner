//! Simple email helper built on `lettre`.  All credentials are read from
//! environment variables so that no secrets are checked into source control.

use lettre::transport::smtp::authentication::Credentials;
use lettre::{Message, SmtpTransport, Transport};
use std::env;

/// Sends a plain‑text email.  Returns `Ok(())` on success or a boxed error
/// with a human‑readable description on failure.
pub fn send_email_alert(to: &str, subject: &str, body: &str) -> Result<(), Box<dyn std::error::Error>> {
    // Required env vars – panic early if they are missing.
    let smtp_host = env::var("SMTP_HOST")?;
    let smtp_user = env::var("SMTP_USER")?;
    let smtp_pass = env::var("SMTP_PASS")?;
    let from_addr = env::var("SMTP_FROM").unwrap_or_else(|_| "alerts@axentx.com".into());

    let email = Message::builder()
        .from(from_addr.parse()?)
        .to(to.parse()?)
        .subject(subject)
        .body(body.to_string())?;

    let creds = Credentials::new(smtp_user, smtp_pass);
    let mailer = SmtpTransport::relay(&smtp_host)?
        .credentials(creds)
        .build();

    mailer.send(&email)?;
    Ok(())
}