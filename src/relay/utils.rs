use crate::relay::types::Transaction;

pub fn obscure_trade_intent(transaction: &Transaction) -> Transaction {
    let mut obscured_transaction = transaction.clone();
    obscured_transaction.sender = "obscured_sender".to_string();
    obscured_transaction.receiver = "obscured_receiver".to_string();
    obscured_transaction
}