# surrogate-1 Documentation

## Introduction

The `surrogate-1` project is designed to handle parallel ingestion of public datasets for training purposes. It leverages the HuggingFace dataset repository `axentx/surrogate-1-training-pairs`. This documentation aims to provide comprehensive guidance for developers looking to understand and utilize the orchestration framework effectively.

## What This Does

Every 30 minutes (or upon manual trigger via `workflow_dispatch`), GitHub Actions initiates **16 parallel runners**. Each runner processes a distinct 1/16 slice of the public dataset list specified in `bin/dataset-enrich.sh`. The data undergoes streaming, normalization according to predefined schemas, deduplication using a central MD5 hash store, and is subsequently uploaded to a unique path within the dataset repository.

### Key Components

- **Runners**: Execute the dataset processing tasks in parallel.
- **Dataset List**: Defined in `bin/dataset-enrich.sh`, specifies the datasets to be processed.
- **Normalization**: Ensures data conforms to required schemas.
- **Deduplication**: Utilizes a central MD5 hash store to eliminate duplicates.
- **Upload**: Outputs processed data to a designated path in the dataset repository.

## Getting Started

To get started with `surrogate-1`, follow these steps:

1. **Clone the Repository**: Begin by cloning the `surrogate-1` repository to your local machine.
2. **Set Up Environment**: Ensure all necessary dependencies are installed and configured.
3. **Configure Settings**: Adjust settings in `bin/dataset-enrich.sh` to match your dataset requirements.
4. **Run the Process**: Trigger the workflow either manually or wait for the scheduled execution.

## Support Channels

For any questions, issues, or further assistance, please reach out through the following support channels:

- **GitHub Issues**: Report bugs or request features directly on the project's GitHub page.
- **Discord Server**: Join our community Discord server for real-time support and discussions.
- **Email Support**: Contact us at support@axentx.com for personalized assistance.

---

## Summary
- Created comprehensive documentation for `surrogate-1`.
- Detailed the project's functionality and key components.
- Provided a getting started guide for new users.
- Established support channels for user assistance.