from pydantic import BaseModel, Field

class TransactionLogBase(BaseModel):
    db_type: str = Field(..., alias="database_type")
    transaction_id: str
    commit_status: bool
    isolation_level: str
    log: str

    class Config:
        orm_mode = True

class TransactionLog(TransactionLogBase):
    id: int