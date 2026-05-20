use crate::relay::relay::Relay;
use crate::relay::config::RelayConfig;
use crate::relay::types::Transaction;
use anyhow::Result;

pub struct PrivateTransactionRelayAPI {
    relay: Relay,
}

impl PrivateTransactionRelayAPI {
    pub fn new(config: RelayConfig) -> Self {
        let relay = Relay::new(config);
        PrivateTransactionRelayAPI { relay }
    }

    pub fn enable_private_transaction(&self, tx: &Transaction) -> Result<Transaction> {
        let obfuscated_tx = self.relay.obfuscate_transaction(tx)?;
        self.relay.relay_transaction(&obfuscated_tx)?;
        Ok(obfuscated_tx)
    }
}