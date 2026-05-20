# surrogate-1-runner

Parallel public-dataset ingest workers for the
[axentx/surrogate-1-training-pairs](https://huggingface.co/datasets/axentx/surrogate-1-training-pairs)
HuggingFace dataset.

## What this does

Every 30 minutes (or on `workflow_dispatch`), GitHub Actions launches **16 parallel runners**. Each runner takes a deterministic 1/16 slice (`slug-hash bucket = SHARD_ID`) of the public dataset list defined in `bin/dataset-enrich.sh`, streams, normalizes per-schema, dedups via the central md5 hash store, and uploads its output to a unique path on the dataset repo.

## Troubleshooting and Remediation

### Connectivity Issues
1. Verify network connectivity to the public dataset source (e.g., HuggingFace API) using `curl` or `httping`.
2. Check firewall rules and VPC security groups to ensure the runner has access to the dataset endpoints.
3. Validate the `dataset-enrich.sh` script's configuration for correct API URLs and authentication tokens.

### IAM Permissions Issues
1. Confirm the GitHub Actions runner service account has the necessary permissions (e.g., `read` on the dataset repo, `write` to the output path).
2. Review the IAM policy attached to the runner role, ensuring it includes the required actions (e.g., `repo:contents`, `actions:workflow`).
3. Test IAM permissions using the AWS IAM console or `aws sts get-caller-identity` within the runner environment.

### Validation Scripts
The project includes validation scripts (`bin/validate-connectivity.sh`, `bin/validate-iam.sh`) that can be run to automatically check for common issues. Run them with: