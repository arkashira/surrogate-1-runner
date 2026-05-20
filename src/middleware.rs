use std::time::{Instant};
use axum::{
    body::Body,
    http::{Request, Response},
    middleware::Next,
    Extension,
};
use tracing::{info, debug};
use crate::metrics::observe_latency;

#[derive(Clone)]
pub struct LatencyLogger;

impl LatencyLogger {
    pub fn new() -> Self {
        LatencyLogger {}
    }
}

pub async fn log_latency<B>(
    Extension(logger): Extension<LatencyLogger>,
    request: Request<B>,
    next: Next<B>,
) -> Response<Body> {
    let start = Instant::now();
    let request_id = request.headers().get("X-Request-ID").map(|v| v.to_str().unwrap_or_default()).unwrap_or("unknown");
    let provider_name = request.headers().get("X-Provider-Name").map(|v| v.to_str().unwrap_or_default()).unwrap_or("unknown");

    info!("Request started for provider {} with request ID {}", provider_name, request_id);

    let response = next.run(request).await;

    let duration = start.elapsed().as_secs_f64();
    info!("Request completed for provider {} with request ID {}. Duration: {:?}", provider_name, request_id, duration);

    observe_latency(provider_name, duration);

    response
}