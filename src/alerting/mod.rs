use std::env;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct Config {
    pub slack_webhook_url: String,
}

impl Config {
    pub fn from_env() -> Result<Self, Box<dyn std::error::Error + Send + Sync>> {
        let config: Config = toml::from_str(&env::var("CONFIG")?)?;
        Ok(config)
    }
}