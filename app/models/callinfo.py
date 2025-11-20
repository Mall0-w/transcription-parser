from pydantic import BaseModel

class CallInfo(BaseModel):
    age: int | None = None
    time_of_accident: str | None = None
    party_at_fault: str | None = None
    loss_cause: str | None = None
    claimant_name: str | None = None
    claimant_address: str | None = None

class RollingCallInfo(CallInfo):
    summary: str
