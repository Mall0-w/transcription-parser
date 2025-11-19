from pydantic import BaseModel

class CallInfo(BaseModel):
    age: int | None = None
    time_of_accident: str | None = None
    party_at_fault: str | None = None
    loss_cause: str | None = None
    