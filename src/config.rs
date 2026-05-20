use std::fs;
use serde_yaml::{self, Value};
use crate::provider::{ProviderType, Provider};

pub fn load_config(path: &str) -> HashMap<String, Provider> {
    let contents = fs::read_to_string(path).expect("Failed to read config file");
    let yaml: Value = serde_yaml::from_str(&contents).expect("Failed to parse YAML");

    let mut providers = HashMap::new();

    if let Some(yaml_providers) = yaml.get("providers") {
        if let Some(yaml_providers_array) = yaml_providers.as_sequence() {
            for provider_yaml in yaml_providers_array {
                if let Some(provider_type) = provider_yaml.get("type").and_then(|v| v.as_str()) {
                    let provider_type_enum: ProviderType = provider_type.into();
                    let provider = Provider {
                        provider_type: provider_type_enum,
                        // Initialize other fields based on the YAML configuration
                    };
                    providers.insert(provider_type.to_string(), provider);
                } else {
                    eprintln!("Warning: Unknown provider type found in config.");
                }
            }
        }
    }

    providers
}