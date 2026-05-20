use prometheus::{register_histogram_vec, HistogramVec};
use lazy_static::lazy_static;

lazy_static! {
    pub static ref REQUEST_LATENCY: HistogramVec = register_histogram_vec!(
        "request_latency_seconds",
        "Request latency in seconds.",
        &["provider"]
    )
    .unwrap();
}

pub fn observe_latency(provider: &str, duration: f64) {
    REQUEST_LATENCY.with_label_values(&[provider]).observe(duration);
}