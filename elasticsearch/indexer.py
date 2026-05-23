from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index
from models.audit_log import AuditLog
from elasticsearch.index_mapping import AuditLogIndex

def index_audit_logs():
    connections.create_connection(hosts=['localhost'])
    index = Index('audit_logs')
    index.document(AuditLogIndex)

    audit_logs = AuditLog.objects.all()
    for log in audit_logs:
        doc = AuditLogIndex(
            meta={'id': log.id},
            model_id=log.model_id,
            timestamp=log.timestamp,
            rule_results=log.rule_results,
            compliance_status=log.compliance_status
        )
        doc.save()