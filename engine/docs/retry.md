# Retry Logic for Workflows

The surrogate-1 engine now supports automatic retry of workflow executions.  
This feature ensures that transient failures (network hiccups, temporary
service outages, etc.) do not cause a workflow to be permanently marked as
failed.

## How it works

`engine.ExecuteWithRetry` wraps a workflow function and re‑invokes it on
failure up to a configurable number of attempts.