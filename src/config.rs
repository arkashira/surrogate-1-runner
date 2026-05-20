use serde::Deserialize;
use config::{Config, ConfigError, Environment, File};

#[derive(Debug, Deserialize, Clone)]
pub struct Settings {
    pub database_url: String,
    pub email_from: String,
    pub max_emails_per_min: u32,
    pub alert_cron: String, // e.g. "0 * * * *" – every hour
}

impl Settings {
    pub fn from_env() -> Result<Self, ConfigError> {
        Config::builder()
            .add_source(File::with_name("Settings").required(false))
            .add_source(Environment::default().separator("_"))
            .build()?
            .try_deserialize()
    }
}