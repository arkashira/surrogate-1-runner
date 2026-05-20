+-------------------+          +------------------------+
|  RightsizerCLI    |          |  RightsizerEngine      |
| (arg parsing)     |<-------->|  (orchestrator)       |
+-------------------+          +-----------+------------+
                                        |
                                        v
+-------------------+          +------------------------+
|  InstanceFetcher  |          |  UtilizationFetcher    |
|  (EC2 describe)   |<-------->|  (CloudWatch)          |
+-------------------+          +-----------+------------+
                                        |
                                        v
+-------------------+          +------------------------+
|  InstanceTypeInfo |          |  RecommendationEngine  |
|  (describe types) |<-------->|  (CPU/Memory + cost)   |
+-------------------+          +-----------+------------+
                                        |
                                        v
+-------------------+          +------------------------+
|  Resizer          |          |  Auditor               |
|  (stop/modify/start) |<------>|  (audit report)        |
+-------------------+          +------------------------+