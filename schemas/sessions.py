from pydantic import BaseModel

class SessionBase(BaseModel):
    provider: str
    data: str

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int

    class Config:
        orm_mode = True