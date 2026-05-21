#!/bin/bash

while [ $# -gt 0 ]; do
  case $1 in
    --ci)
      CI_MODE=true
      shift
      ;;
    --output)
      OUTPUT_FILE=$2
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [ "$CI_MODE" = true ]; then
  # Run the CLI with --ci flag
  ./cli --ci
  if [ $? -ne 0 ]; then
    exit 1
  fi
fi

if [ -n "$OUTPUT_FILE" ]; then
  # Output a summary comment
  echo "## Summary" > $OUTPUT_FILE
  echo "Missing imports:" >> $OUTPUT_FILE
  ./cli --ci >> $OUTPUT_FILE
fi