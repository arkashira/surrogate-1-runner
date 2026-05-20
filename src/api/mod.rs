use actix_web::web;
use crate::api::routes::wholphin_events::register_routes;

pub fn configure(cfg: &mut web::ServiceConfig) {
    register_routes(cfg);
}