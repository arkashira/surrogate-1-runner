use sqlx::sqlite::SqlitePool;
use sqlx::migrate::MigrateDatabase;

pub async fn init_db(url: &str) -> anyhow::Result<SqlitePool> {
    // Create the file if it does not exist (for file‑based SQLite)
    if !SqlitePool::database_exists(url).await? {
        SqlitePool::create_database(url).await?;
    }

    let pool = SqlitePool::connect(url).await?;
    // Apply all pending migrations (the folder `migrations/` is relative to the binary)
    sqlx::migrate!("./migrations").run(&pool).await?;
    Ok(pool)
}