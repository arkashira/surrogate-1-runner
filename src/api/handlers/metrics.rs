use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;

#[derive(Deserialize)]
struct MetricsRequest {
    device_id: i32,
}

#[derive(Serialize)]
struct MetricsResponse {
    avg_duration_ms: f64,
    count: i64,
}

async fn get_metrics(
    pool: web::Data<PgPool>,
    request: web::Query<MetricsRequest>,
) -> impl Responder {
    let device_id = request.device_id;
    let query = format!("SELECT AVG(duration_ms) as avg_duration_ms, COUNT(*) as count FROM flash_data WHERE device_id = $1");
    let result = sqlx::query_as::<_, (f64, i64)>(&query)
        .bind(device_id)
        .fetch_one(pool.get_ref())
        .await;

    match result {
        Ok((avg_duration_ms, count)) => {
            let response = MetricsResponse {
                avg_duration_ms,
                count,
            };
            HttpResponse::Ok().json(response)
        }
        Err(_) => HttpResponse::NotFound().finish(),
    }
}

pub fn metrics_routes(cfg: &mut web::ServiceConfig) {
    cfg.route("/api/v1/metrics/flash", web::get().to(get_metrics));
}