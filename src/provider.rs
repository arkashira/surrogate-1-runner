use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone)]
pub enum ProviderType {
    // Define known provider types here
    KnownProvider1,
    KnownProvider2,
    Unknown(String),
}

impl From<String> for ProviderType {
    fn from(value: String) -> Self {
        match value.as_str() {
            "KnownProvider1" => ProviderType::KnownProvider1,
            "KnownProvider2" => ProviderType::KnownProvider2,
            _ => ProviderType::Unknown(value),
        }
    }
}

#[derive(Clone)]
pub struct Provider {
    pub provider_type: ProviderType,
    // Other fields...
}

pub type ProviderRegistry = Arc<RwLock<HashMap<String, Provider>>>;

pub fn register_provider(provider_registry: &ProviderRegistry, provider: Provider) {
    let mut registry = provider_registry.write().unwrap();
    registry.insert(provider.provider_type.to_string(), provider);
}

pub fn get_provider(provider_registry: &ProviderRegistry, provider_type: &str) -> Option<Provider> {
    let registry = provider_registry.read().unwrap();
    registry.get(provider_type).cloned()
}