from elasticsearch_dsl import Document, Date, Keyword, Text, Boolean

class AuditLogIndex(Document):
    model_id = Keyword()
    timestamp = Date()
    rule_results = Text()
    compliance_status = Keyword()

    class Index:
        name = 'audit_logs'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 1
        }