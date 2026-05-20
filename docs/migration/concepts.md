
# Docker Compose vs Kubernetes: Concept Mapping

| Docker Compose | Kubernetes |
|---|---|
| **Volumes** | **Persistent Volumes (PV) and Persistent Volume Claims (PVC)** |
| - Defined in `volumes` section | - Defined as Kubernetes resources |
| - Mounted to services using `volumes` and `volume_mounts` | - Mounted to pods using `volumeMounts` |
| **Networks** | **Networks** |
| - Defined in `networks` section | - Defined as Kubernetes resources |
| - Services connect to networks using `networks` | - Pods connect to networks using `spec.network` |
| **Services** | **Deployments** |
| - Defined in `services` section | - Defined as Kubernetes resources |
| - Scale using `scale` command | - Scale using `replicas` field or `kubectl scale` command |
| **Environment Variables** | **Environment Variables** |
| - Defined in `environment` section | - Defined in `env` field |
| **Health Checks** | **Liveness and Readiness Probes** |
| - Defined in `healthcheck` section | - Defined in `livenessProbe` and `readinessProbe` fields |

## Summary
- Created a mapping table for Docker Compose and Kubernetes concepts.
- Included parallel concept mappings for volumes, networks, services, environment variables, and health checks.
- Provided brief explanations for each mapping.