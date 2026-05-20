use chrono::{DateTime, Utc};
use serde::Serialize;

#[derive(sqlx::FromRow, Debug)]
pub struct Event {
    pub id: i64,
    pub created_at: DateTime<Utc>,
    pub event_type: String,
    pub device_id: String,
    pub app_version: String,
}

#[derive(Serialize)]
pub struct CsvEventRow {
    pub event_id: String,
    pub timestamp: String,
    pub event_type: String,
    pub device_id: String,
    pub app_version: String,
}

impl From<Event> for CsvEventRow {
    fn from(e: Event) -> Self {
        Self {
            event_id: e.id.to_string(),
            timestamp: e.created_at.to_rfc3339(),
            event_type: e.event_type,
            device_id: e.device_id,
            app_version: e.app_version,
        }
    }
}