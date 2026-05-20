use axum::{
    routing::get,
    Router,
    Extension,
};
use std::net::SocketAddr;
use crate::middleware::LatencyLogger;
use crate::metrics::REQUEST_LATENCY;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(|| async { "Hello, World!" }))
        .route("/metrics", get(metrics_handler))
        .layer(Extension(LatencyLogger::new()))
        .layer(axum::middleware::from_fn_with_state(
            LatencyLogger::new(),
            crate::middleware::log_latency,
        ));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("Listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn metrics_handler() -> String {
    prometheus::Encoder::encode_to_string(&prometheus::TextEncoder::new(), &REQUEST_LATENCY.collect()).unwrap()
}