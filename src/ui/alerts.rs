//! User interface module for displaying real‑time attack alerts.
//!
//! This module defines the `Alert` type and provides helper functions
//! to render alerts to the console.  It is intentionally lightweight
//! so that it can be used in both CLI and web contexts without
//! pulling in heavy dependencies.

use std::fmt;
use std::time::{SystemTime, UNIX_EPOCH};

/// Severity level of an alert.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Severity {
    Info,
    Warning,
    Critical,
}

impl fmt::Display for Severity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self {
            Severity::Info => "INFO",
            Severity::Warning => "WARN",
            Severity::Critical => "CRIT",
        };
        write!(f, "{}", s)
    }
}

/// A single attack alert.
#[derive(Debug, Clone)]
pub struct Alert {
    /// Unique identifier for the alert.
    pub id: u64,
    /// Human‑readable message.
    pub message: String,
    /// Severity of the alert.
    pub severity: Severity,
    /// Timestamp in seconds since UNIX_EPOCH.
    pub timestamp: u64,
}

impl Alert {
    /// Create a new alert.
    pub fn new(id: u64, message: impl Into<String>, severity: Severity) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        Self {
            id,
            message: message.into(),
            severity,
            timestamp,
        }
    }
}

impl fmt::Display for Alert {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "[{}] {}: {} (id={})",
            self.timestamp, self.severity, self.message, self.id
        )
    }
}

/// Render a slice of alerts to stdout.
///
/// The function prints each alert on its own line.  In a real
/// application this could be replaced with a GUI component or
/// a web socket push.
pub fn render_alerts(alerts: &[Alert]) {
    for alert in alerts {
        println!("{}", alert);
    }
}

/// Example helper that simulates receiving alerts from a stream.
///
/// In production this would be replaced by an async stream or
/// a channel.  The function accepts a callback that will be
/// invoked for each alert.
pub fn listen_for_alerts<F>(mut callback: F)
where
    F: FnMut(Alert) + Send + 'static,
{
    // For demonstration purposes we generate a few alerts.
    // In a real system this would be driven by an event source.
    let demo_alerts = vec![
        Alert::new(1, "Transaction 12345 under attack", Severity::Critical),
        Alert::new(2, "Suspicious activity detected", Severity::Warning),
        Alert::new(3, "Health check passed", Severity::Info),
    ];

    for alert in demo_alerts {
        callback(alert);
    }
}