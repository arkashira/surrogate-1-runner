use actix_web::{App, HttpServer};
use std::sync::Arc;
use axentx_surrogate1::api::configure;
use axentx_surrogate1::api::routes::wholphin_events::AppState;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
    
    let state = Arc::new(AppState);

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(state.clone()))
            .configure(configure)
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}