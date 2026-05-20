# Workflow Templates

Surrogate-1 provides pre-built workflow templates as starting points for common tasks.

## Features
- **Categorized** by use-case (DevOps, Data Engineering, ML Engineering)
- **Documented** with purpose, inputs, and customization options
- **Importable** directly into the low-code workflow editor

## Available Templates

| ID | Name | Category | Description |
|----|------|-----------|-------------|
| `ci_cd_pipeline` | CI/CD Pipeline | DevOps | Standard CI/CD workflow using GitHub Actions |
| `data_ingest` | Data Ingest | Data Engineering | Ingest public datasets into surrogate-1 pipeline |
| `model_training` | Model Training | ML Engineering | Distributed training for Surrogate-1 models |

## Usage
1. Browse templates in `metadata.yaml` or `templates.json`
2. Import the `example_config` YAML into your repository
3. Customize parameters in the AxentX low-code editor
4. Commit and push to activate

## API Access
Programmatic access available via `/docs/templates.json` for integration with external tools.