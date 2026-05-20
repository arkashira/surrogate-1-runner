use axentx_surrogate_1::api::credits::CreditBalances;
use axentx_surrogate_1::test_utils::TestApp;
use chrono::{Duration, Utc};
use std::sync::Once;

/// Initialise the logger only once – the test harness may run many tests.
static START: Once = Once::new();

fn init_logger() {
    START.call_once(|| {
        env_logger::init();
    });
}

#[tokio::test]
async fn test_get_credits_authenticated() {
    init_logger();

    // Spin up a fresh test app (database, server, etc.).
    let app = TestApp::spawn().await;

    // Make the request with a valid bearer token.
    let response = app
        .client
        .get(&format!("{}/api/credits", app.address))
        .bearer_auth(app.user1.token.clone())
        .send()
        .await
        .expect("failed to send request");

    // 200 OK
    assert_eq!(response.status(), 200);

    // Deserialize the JSON body.
    let body: CreditBalances = response
        .json()
        .await
        .expect("response body is not valid JSON");

    // Basic sanity checks – values should be non‑negative.
    assert!(body.monthly_balance >= 0.0, "negative monthly balance");
    assert!(body.bulk_balance >= 0.0, "negative bulk balance");

    // The timestamp must be within the last hour.
    let now = Utc::now();
    let last_updated = chrono::DateTime::parse_from_rfc3339(&body.last_updated)
        .expect("last_updated is not RFC3339");
    assert!(
        last_updated >= now - Duration::hours(1),
        "last_updated is too far in the past"
    );
}

#[tokio::test]
async fn test_get_credits_unauthenticated() {
    init_logger();

    let app = TestApp::spawn().await;

    // No auth header – should be rejected.
    let response = app
        .client
        .get(&format!("{}/api/credits", app.address))
        .send()
        .await
        .expect("failed to send request");

    assert_eq!(response.status(), 401);
}