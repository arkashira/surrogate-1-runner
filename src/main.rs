use actix::{Actor, Addr, System};
use actix_web::{web, App, HttpServer};
use axentx_surrogate_1::api::ws::metrics_ws::{
    metrics_ws, MetricsWs, MetricsBroadcaster, spawn_metrics_producer,
};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // 1. Create the broadcast channel and spawn the producer task.
    let broadcaster = spawn_metrics_producer();

    // 2. Start the WebSocket actor – it will subscribe to the broadcaster.
    let ws_actor = MetricsWs::new(broadcaster.clone()).start();

    // 3. Run the HTTP server.
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(ws_actor.clone()))
            .route("/dashboard/wholphin/ws", web::get().to(metrics_ws))
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}