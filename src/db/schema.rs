//! `credits` table helpers – async, compile‑time checked SQL.
//!
//! The table stores a per‑account credit balance with a monthly and bulk
//! component, and tracks the last time the row was updated.

use anyhow::Result;
use chrono::NaiveDateTime;
use sqlx::{sqlite::SqlitePool, SqliteQueryResult};

/// Idempotently creates the `credits` table.  
/// This is a thin wrapper around the migration; it is kept for backward‑compatibility
/// with code that called `create_credits_table` directly.
pub async fn create_credits_table(pool: &SqlitePool) -> Result<SqliteQueryResult> {
    // The same DDL as the migration – harmless if the table already exists.
    let ddl = r#"
        CREATE TABLE IF NOT EXISTS credits (
            account_id TEXT PRIMARY KEY,
            monthly_balance INTEGER NOT NULL DEFAULT 0,
            bulk_balance INTEGER NOT NULL DEFAULT 0,
            last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    "#;
    Ok(sqlx::query(ddl).execute(pool).await?)
}

/// Insert a new row or update an existing one (UPSERT).
///
/// * `account_id` – unique identifier for the account (e.g. a UUID or user name).  
/// * `monthly` – the monthly credit balance.  
/// * `bulk` – the bulk (non‑expiring) credit balance.
///
/// Returns the number of rows affected (always 1).
pub async fn upsert_credits(
    pool: &SqlitePool,
    account_id: &str,
    monthly: i64,
    bulk: i64,
) -> Result<SqliteQueryResult> {
    let stmt = r#"
        INSERT INTO credits (account_id, monthly_balance, bulk_balance, last_updated)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(account_id) DO UPDATE SET
            monthly_balance = excluded.monthly_balance,
            bulk_balance    = excluded.bulk_balance,
            last_updated    = CURRENT_TIMESTAMP;
    "#;

    Ok(sqlx::query(stmt)
        .bind(account_id)
        .bind(monthly)
        .bind(bulk)
        .execute(pool)
        .await?)
}

/// Fetch the balances for a given account.
///
/// Returns `None` if the account does not exist.
pub async fn get_credits(
    pool: &SqlitePool,
    account_id: &str,
) -> Result<Option<(i64, i64, NaiveDateTime)>> {
    let row = sqlx::query!(
        r#"
        SELECT monthly_balance, bulk_balance, last_updated
        FROM credits
        WHERE account_id = ?
        "#,
        account_id
    )
    .fetch_optional(pool)
    .await?;

    Ok(row.map(|r| (r.monthly_balance, r.bulk_balance, r.last_updated)))
}

/// Delete a credit row. Returns the number of rows deleted (0 or 1).
pub async fn delete_credits(pool: &SqlitePool, account_id: &str) -> Result<SqliteQueryResult> {
    Ok(sqlx::query("DELETE FROM credits WHERE account_id = ?")
        .bind(account_id)
        .execute(pool)
        .await?)
}