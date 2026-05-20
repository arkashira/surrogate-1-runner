use sqlx::FromRow;

#[derive(Debug, FromRow, PartialEq, Eq, Clone)]
pub struct Account {
    pub id: i32,
    pub email: String,
    pub bulk_balance: i64,
    pub credit_threshold: i64,
}