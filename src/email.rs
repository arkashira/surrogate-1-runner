use async_trait::async_trait;
use anyhow::Result;
use std::sync::Arc;

/// The contract that the alert job depends on.
#[async_trait]
pub trait EmailSender: Send + Sync + 'static {
    async fn send(&self, to: &str, subject: &str, body: &str) -> Result<()>;
}

/// Production implementation that uses `lettre`.
pub struct LettreEmailSender {
    mailer: lettre::AsyncSmtpTransport<lettre::Tokio1Executor>,
    from: String,
}

impl LettreEmailSender {
    pub fn new(smtp_host: &str, smtp_user: &str, smtp_pass: &str, from: &str) -> Self {
        let creds = lettre::transport::smtp::authentication::Credentials::new(
            smtp_user.to_owned(),
            smtp_pass.to_owned(),
        );

        let mailer = lettre::AsyncSmtpTransport::<lettre::Tokio1Executor>::relay(smtp_host)
            .expect("invalid SMTP host")
            .credentials(creds)
            .build();

        Self {
            mailer,
            from: from.to_owned(),
        }
    }
}

#[async_trait]
impl EmailSender for LettreEmailSender {
    async fn send(&self, to: &str, subject: &str, body: &str) -> Result<()> {
        let email = lettre::Message::builder()
            .from(self.from.parse()?)
            .to(to.parse()?)
            .subject(subject)
            .body(body.to_owned())?;

        self.mailer.send(email).await?;
        Ok(())
    }
}