from surrogate_1.models.transaction_schema import TransactionLogBase
from surrogate_1.utils.db_utils import connect_to_db

class TransactionService:
    async def capture_transaction_logs(self, logs: List[TransactionLogBase]):
        db_connections = {}
        captured_logs = []

        for log in logs:
            if log.db_type not in db_connections:
                db_connections[log.db_type] = await connect_to_db(log.db_type)

            connection = db_connections[log.db_type]
            captured_log = await connection.execute(log.log)
            captured_logs.append(captured_log)

        return captured_logs