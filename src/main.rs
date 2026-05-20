use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct ChatRequest {
    model: String,
    messages: Vec<Message>,
}

#[derive(Deserialize, Serialize)]
struct Message {
    role: String,
    content: String,
}

async fn chat_completions(req: web::Json<ChatRequest>) -> impl Responder {
    // Forward the request to the appropriate provider based on the model field.
    // For simplicity, we'll just echo the request back.
    let response = ChatResponse {
        id: "test-id".to_string(),
        object: "chat.completion".to_string(),
        created: 1677652288,
        model: req.model.clone(),
        choices: vec![Choice {
            index: 0,
            message: Message {
                role: "assistant".to_string(),
                content: "Hello! How can I assist you today?".to_string(),
            },
            finish_reason: Some("stop".to_string()),
        }],
        usage: Usage {
            prompt_tokens: 5,
            completion_tokens: 7,
            total_tokens: 12,
        },
    };

    HttpResponse::Ok().json(response)
}

#[derive(Serialize)]
struct ChatResponse {
    id: String,
    object: String,
    created: i64,
    model: String,
    choices: Vec<Choice>,
    usage: Usage,
}

#[derive(Serialize)]
struct Choice {
    index: usize,
    message: Message,
    finish_reason: Option<String>,
}

#[derive(Serialize)]
struct Usage {
    prompt_tokens: usize,
    completion_tokens: usize,
    total_tokens: usize,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/v1/chat/completions", web::post().to(chat_completions))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}