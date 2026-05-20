use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

/// Credit balance model representing an account's credit state
#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct Credit {
    pub account_id: String,
    pub monthly_balance: i64,
    pub bulk_balance: i64,
    pub last_updated: DateTime<Utc>,
}

impl Credit {
    pub fn new(account_id: String) -> Self {
        Self {
            account_id,
            monthly_balance: 0,
            bulk_balance: 0,
            last_updated: Utc::now(),
        }
    }

    pub fn total(&self) -> i64 {
        self.monthly_balance + self.bulk_balance
    }

    pub fn has_sufficient_credits(&self, amount: i64) -> bool {
        self.total() >= amount
    }

    /// Deduct from monthly balance first (priority), then bulk
    pub fn deduct(&mut self, amount: i64) -> Result<(), CreditError> {
        if !self.has_sufficient_credits(amount) {
            return Err(CreditError::InsufficientBalance {
                available: self.total(),
                requested: amount,
            });
        }

        if self.monthly_balance >= amount {
            self.monthly_balance -= amount;
        } else {
            let from_monthly = self.monthly_balance;
            let from_bulk = amount - from_monthly;
            self.monthly_balance = 0;
            self.bulk_balance = self.bulk_balance.saturating_sub(from_bulk);
        }

        self.last_updated = Utc::now();
        Ok(())
    }

    pub fn add_monthly(&mut self, amount: i64) {
        self.monthly_balance = self.monthly_balance.saturating_add(amount);
        self.last_updated = Utc::now();
    }

    pub fn add_bulk(&mut self, amount: i64) {
        self.bulk_balance = self.bulk_balance.saturating_add(amount);
        self.last_updated = Utc::now();
    }
}

#[derive(Debug, thiserror::Error)]
pub enum CreditError {
    #[error("Insufficient balance: available {available}, requested {requested}")]
    InsufficientBalance { available: i64, requested: i64 },
    
    #[error("Account not found: {0}")]
    AccountNotFound(String),
    
    #[error("Database error: {0}")]
    DatabaseError(String),
}

impl From<sqlx::Error> for CreditError {
    fn from(err: sqlx::Error) -> Self {
        CreditError::DatabaseError(err.to_string())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreditUpdate {
    pub monthly_balance: Option<i64>,
    pub bulk_balance: Option<i64>,
}

impl CreditUpdate {
    pub fn add_monthly(amount: i64) -> Self {
        Self {
            monthly_balance: Some(amount),
            bulk_balance: None,
        }
    }

    pub fn add_bulk(amount: i64) -> Self {
        Self {
            monthly_balance: None,
            bulk_balance: Some(amount),
        }
    }
}