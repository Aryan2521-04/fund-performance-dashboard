from pydantic import BaseModel, field_validator
from datetime import date as date_type
from decimal import Decimal



class CashFlowEventCreate(BaseModel):

    date: date_type
    amount: Decimal

    # Sanity check
    @field_validator("amount")
    @classmethod
    # Make sure junk value isn't put in such as 0 which does absolutley nothing 
    def validate_amount(cls, value):    
        if value == 0:
            raise ValueError("Amount cant be 0")
        return value

class CashFlowEventOut(BaseModel):

    id: int
    date: date_type
    amount: Decimal

    # Reads fields directly from object attributes 
    model_config = {"from_attributes": True} 


class NavSnapshotOut(BaseModel):

    id: int
    date: date_type
    value: Decimal

    model_config = {"from_attributes": True}


class FundSummary(BaseModel):

    id: int
    name: str
    vintage_year: int
    dpi: Decimal | None
    tvpi: Decimal | None
    irr_realized: float | None # Floats should be fine here since it's a rate
    irr_since_inception: float | None 

    model_config = {"from_attributes": True}


# Inheriting data from FundSummary
class FundDetail(FundSummary):

    cash_flows: list[CashFlowEventOut]  
    nav_snapshots: list[NavSnapshotOut]

