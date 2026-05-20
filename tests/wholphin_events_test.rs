use actix_web::{test, App};
use axentx_surrogate1::api::configure;
use axentx_surrogate1::api::routes::wholphin_events::WholphinEventBatch;
use serde_json::json;

#[actix_rt::test]
async fn test_ingest_wholphin_events() {
    let app = test::init_service(App::new().configure(configure)).await;

    let payload = WholphinEventBatch {
        device_id: "device-123".to_string(),
        app_version: "1.2.3".to_string(),
        events: vec![json!({"event": "click", "timestamp": 123456})],
    };

    let req = test::TestRequest::post()
        .uri("/api/v1/wholphin/events")
        .set_json(&payload)
        .to_request();

    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
}