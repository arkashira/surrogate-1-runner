#!/bin/bash

# Set the model artifacts directory
MODEL_ARTIFACTS_DIR=/opt/axentx/surrogate-1/model_artifacts

# Create a ModelArtifactAnalyzer instance
analyzer=$(python -c "from src.scanner.model_artifact_analyzer import ModelArtifactAnalyzer; print(ModelArtifactAnalyzer('$MODEL_ARTIFACTS_DIR'))")

# Run the analysis
reports=$(python -c "import json; print(json.dumps($analyzer.analyze()))")

# Print the compliance reports
echo "$reports"