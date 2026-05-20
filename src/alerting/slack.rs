use std::collections::HashMap;
use std::sync::Mutex;
use chrono::{DateTime, Duration, Utc};
use lazy_static::lazy_static;
use reqwest::Client;
use serde_json::json;
use crate::alerting::Config;

lazy_static! {
    static ref LAST_ALERT: Mutex<HashMap<String, DateTime<Utc>>> = Mutex::new(HashMap::new());
    static ref HTTP_CLIENT: Client = Client::new();
}

pub async fn send_slack_alert(
    config: &Config,
    device_id: &str,
    count: u32,
    avg_duration: f64,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let mut map = LAST_ALERT.lock().unwrap();
    if let Some(last) = map.get(device_id) {
        if Utc::now() - *last < Duration::hours(1) {
            return Ok(());
        }
    }
    map.insert(device_id.to_string(), Utc::now());

    let payload = json!({
        "text": format!(
            "⚠️ *Device Alert*\n• Device ID: `{}`\n• Flash count: `{}` per minute\n• Avg duration: `{:.2} ms`",
            device_id, count, avg_duration
        )
    });

    let resp = HTTP_CLIENT
        .post(&config.slack_webhook_url)
        .json(&payload)
        .send()
        .await?;

    if !resp.status().is_success() {
        let status = resp.status();
        let body = resp.text().await.unwrap_or_default();
        return Err(format!(
            "Slack webhook returned non-success status {}: {}",
            status, body
        )
        .into());
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::MutexGuard;

    fn clear_rate_limit() {
        let mut map = LAST_ALERT.lock().unwrap();
        map.clear();
    }

    #[tokio::test]
    async fn test_rate_limit() {
        clear_rate_limit();
        let config = Config {
            slack_webhook_url: "http://localhost:9999".to_string(),
        };

        let res = send_slack_alert(&config, "dev1", 10, 123.4).await;
        assert!(res.is_err());

        let res2 = send_slack_alert(&config, "dev1", 12, 200.0).await;
        assert!(res2.is_ok());
    }

    #[tokio::test]
    async fn test_missing_webhook() {
        clear_rate_limit();
        let config = Config {
            slack_webhook_url: "".to_string(),
        };

        let res = send_slack_alert(&config, "dev2", 5, 50.0).await;
        assert!(res.is_err());
    }
}