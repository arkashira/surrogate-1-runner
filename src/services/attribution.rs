// ─────────────────────────────────────────────────────────────────────────────
//  src/services/attribution.rs
// ─────────────────────────────────────────────────────────────────────────────

use chrono::{DateTime, Duration, Utc};
use std::error::Error;
use std::fmt;

// ---------------------------------------------------------------------------
// Domain models – normally re‑exported from the crate's `models` module.
// ---------------------------------------------------------------------------
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct CommitEvent {
    pub sha: String,
    pub repo: String,
    pub branch: String,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct CostRecord {
    pub repo: String,
    pub branch: String,
    pub cost_usd: f64,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct CommitCost {
    pub sha: String,
    pub repo: String,
    pub branch: String,
    pub total_usd: f64,
}

// ---------------------------------------------------------------------------
// Database abstraction
// ---------------------------------------------------------------------------
pub trait Database {
    /// Persist a batch of `CommitCost`s.  Implementations may choose any storage
    /// strategy (SQL, NoSQL, in‑memory, etc.).
    fn insert_commit_costs(&mut self, commit_costs: Vec<CommitCost>) -> Result<(), DatabaseError>;
}

#[derive(Debug)]
pub struct DatabaseError {
    pub msg: String,
}

impl fmt::Display for DatabaseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Database error: {}", self.msg)
    }
}
impl Error for DatabaseError {}

impl DatabaseError {
    pub fn new<S: Into<String>>(msg: S) -> Self {
        DatabaseError { msg: msg.into() }
    }
}

// ---------------------------------------------------------------------------
// Core attribution logic
// ---------------------------------------------------------------------------

/// Return **all** `CostRecord`s that belong to the same repo/branch and whose
/// timestamps fall within `window` (centered on the commit timestamp).
///
/// The default window used by the public helper `attribute_commit` is ±1 hour,
/// but callers can pass any `Duration`.
pub fn match_commit_to_cost_records(
    commit: &CommitEvent,
    records: &[CostRecord],
    window: Duration,
) -> Vec<CostRecord> {
    let start = commit.timestamp - window;
    let end = commit.timestamp + window;

    records
        .iter()
        .filter(|r| {
            r.repo == commit.repo
                && r.branch == commit.branch
                && r.timestamp >= start
                && r.timestamp <= end
        })
        .cloned()
        .collect()
}

/// High‑level helper that **aggregates** the matching records into a single
/// `CommitCost`.  The window defaults to ±1 hour (the behaviour from candidate 1)
/// but can be overridden for longer windows (e.g. 12 h as in candidate 2).
pub fn attribute_commit(
    commit: &CommitEvent,
    records: &[CostRecord],
    window: Option<Duration>,
) -> CommitCost {
    let window = window.unwrap_or_else(|| Duration::hours(1));
    let matched = match_commit_to_cost_records(commit, records, window);

    let total_usd = matched.iter().map(|r| r.cost_usd).sum();

    CommitCost {
        sha: commit.sha.clone(),
        repo: commit.repo.clone(),
        branch: commit.branch.clone(),
        total_usd,
    }
}

/// Persist the aggregated cost for a single commit.  This is the function that
/// production code will call after it has built the `CommitCost`.
pub fn store_commit_cost<D: Database>(
    db: &mut D,
    commit_cost: CommitCost,
) -> Result<(), DatabaseError> {
    db.insert_commit_costs(vec![commit_cost])
}