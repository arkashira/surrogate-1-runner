+-------------------+          +-------------------+          +-------------------+
| CI/CD / Deploy    |  --->    | signature_runner  |  --->    | AuditStorage      |
| (Jenkins, GH, …) |          | (run_signature_…) |          | (JSON files)      |
+-------------------+          +-------------------+          +-------------------+
                                   |
                                   |   (if changes ≥ THRESHOLD)
                                   v
                           +-------------------+
                           | SRENotifier       |
                           |  - Email          |
                           |  - Slack webhook  |
                           |  - PagerDuty API  |
                           +-------------------+
                                   |
                                   v
                           +-------------------+
                           | Monitoring /      |
                           | Alerting (Prom)   |
                           +-------------------+