use actix_web::{web, App, HttpServer};
use sqlx::PgPool;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let database_url = "postgres://username:password@localhost/database";
    let pool = PgPool::connect(database_url).await.unwrap();

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(pool.clone()))
            .configure(metrics_routes)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}