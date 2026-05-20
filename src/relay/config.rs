use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Deserialize, Serialize, Debug)]
pub struct RelayConfig {
    pub relay_url: String,
    pub private_key: String,
    pub public_key: String,
}

impl RelayConfig {
    pub fn new(relay_url: String, private_key: String, public_key: String) -> Self {
        RelayConfig {
            relay_url,
            private_key,
            public_key,
        }
    }
}