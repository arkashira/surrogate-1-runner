# CI/CD Integration Guide for Mesh File Health Probe

This document provides integration instructions for the mesh file health probe across popular CI/CD systems.

## Overview

The mesh file health probe is designed to validate the integrity and readiness of mesh files within your CI/CD pipelines. It outputs structured JSON that can be consumed by monitoring systems and alerting tools.

## Jenkins Integration

### Prerequisites
- Jenkins 2.0+
- Node.js plugin installed (for JSON parsing)

### Configuration Steps

1. Add a build step to execute the health probe: