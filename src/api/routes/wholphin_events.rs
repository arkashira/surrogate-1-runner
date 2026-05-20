use actix_web::{post, web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

/// Event payload received from Wholphin workers.
#[derive(Debug, Deserialize, Serialize)]
pub struct WholphinEventBatch {
    pub device_id: String,
    pub app_version: String,
    pub events: Vec<serde_json::Value>,
}

/// Application state placeholder.
/// In production: database connections, config, external service clients.
pub struct AppState;

/// POST /api/v1/wholphin/events
///
/// Accepts a batch of events from Wholphin workers.
/// Returns 200 OK on successful receipt.
#[post("/api/v1/wholphin/events")]
pub async fn ingest_wholphin_events(
    payload: web::Json<WholphinEventBatch>,
    _state: web::Data<Arc<AppState>>,
) -> impl Responder {
    // Log receipt (replace with persistence/forwarding in production)
    log::info!(
        "Received Wholphin batch: device_id={}, app_version={}, event_count={}",
        payload.device_id,
        payload.app_version,
        payload.events.len()
    );

    HttpResponse::Ok().finish()
}

/// Register routes with the Actix web service config.
pub fn register_routes(cfg: &mut actix_web::web::ServiceConfig) {
    cfg.service(ingest_wholphin_events);
}