use std::sync::Arc;
use tokio::sync::RwLock;
use crate::provider::{ProviderRegistry, ProviderType, Provider, register_provider};
use crate::config::load_config;

#[tokio::main]
async fn main() {
    let provider_registry: ProviderRegistry = Arc::new(RwLock::new(HashMap::new()));
    let config_path = "config.yaml";
    let providers = load_config(config_path);

    for (_, provider) in providers {
        register_provider(&provider_registry, provider);
    }

    // Example routing logic using provider type
    let provider_type = "KnownProvider1";
    if let Some(provider) = get_provider(&provider_registry, provider_type) {
        match provider.provider_type {
            ProviderType::KnownProvider1 => {
                println!("Using KnownProvider1 client");
                // Use KnownProvider1 client logic
            },
            ProviderType::KnownProvider2 => {
                println!("Using KnownProvider2 client");
                // Use KnownProvider2 client logic
            },
            ProviderType::Unknown(unknown_type) => {
                eprintln!("Warning: Unknown provider type: {}", unknown_type);
            },
        }
    }
}