from sqlalchemy.orm import Session
from .models import Fund, CashFlowEvent
from .schemas import CashFlowEventCreate

# Fetches a single fund by id
def get_fund(db: Session, fund_id: int) -> Fund | None:

    return db.get(Fund, fund_id)



# Fetches all funds
def get_funds(db) -> list[Fund]:

    return db.execute(select(Fund)).scalars().all()


# inserts a new cashflowevent row, links to a given fund, commits it, then returns that created object
def create_cash_flow_event(db: Session, fund_id: int, cash_flow: CashFlowEventCreate) -> CashFlowEvent:


    new_cash_flow = CashFlowEvent(fund_id = fund_id, date = cash_flow.date, amount = cash_flow.amount)
    db.add(new_cash_flow)
    db.commit()
    db.refresh(new_cash_flow) 
    return new_cash_flow

