use crate::relay::Relay;
use crate::error::Error;
use crate::types::Transaction;
use serde::Serialize;

#[derive(Serialize)]
pub struct RelayTransactionRequest {
    pub transaction: Transaction,
    pub destination_chain: String,
}

pub trait RelayApi {
    fn send_transaction(&self, request: RelayTransactionRequest) -> Result<(), Error>;
}

impl RelayApi for Relay {
    fn send_transaction(&self, request: RelayTransactionRequest) -> Result<(), Error> {
        // Logic to send transaction across chains using private relays
        // ...
        Ok(())
    }
}