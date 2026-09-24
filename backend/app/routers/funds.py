from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, metrics, schemas
from .. fund_service import compute_fund_metrics

router = APIRouter()

# Get /funds

@router.get("/funds", response_model=list[schemas.FundSummary])
def list_funds(db: Session = Depends(get_db)):

    # Get all funds by calling crud.get_funds(db)

    funds = crud.get_funds(db)

    result = []

    for fund in funds: 

        # calls helper function
        dpi, tvpi, irr, irr_nav = compute_fund_metrics(fund)
        
        #builds summary schema
        summary = schemas.FundSummary(id = fund.id, name = fund.name, vintage_year = fund.vintage_year, 
                               dpi = dpi, tvpi = tvpi,  irr_realized = irr, irr_since_inception = irr_nav)
        
        #appends that schema into results
        result.append(summary)

        return result




# Get /funds{fund_id}
@router.get("/funds/{fund_id}", response_model=schemas.FundDetail)
def get_fund_detail(fund_id: int, db: Session = Depends(get_db)):

    # gets a single fund instead of all
    fund = crud.get_fund(db, fund_id)

    # makes sure fund exists, if it dosen't raises an error
    if fund is None:
        raise HTTPException(status_code=404, detail="Fund dosen't exist in datbase")

    # same helper function
    dpi, tvpi, irr, irr_nav = compute_fund_metrics(fund)
        
    #builds cash flow out and nav snapshots schemas
    cash_flows_out = [schemas.CashFlowEventOut.model_validate(cf) for cf in fund.cash_flows]
    nav_snapshots_out = [schemas.NavSnapshotOut.model_validate(ns) for ns in fund.nav_snapshots]

    # returns fund summary + the two schemas built earlier
    return schemas.FundDetail(id = fund.id, name = fund.name, vintage_year = fund.vintage_year, 
                            dpi = dpi, tvpi = tvpi,  irr_realized = irr, irr_since_inception = irr_nav,
                            cash_flows = cash_flows_out, nav_snapshots= nav_snapshots_out)
    



# POST /funds/{fund_id}/cashflows
@router.post("/funds/{fund_id}/cashflows", response_model=schemas.CashFlowEventOut)
def create_cash_flow(fund_id: int, cash_flow: schemas.CashFlowEventCreate, db: Session = Depends(get_db)):

    # gets single fund
    fund = crud.get_fund(db, fund_id)

    # same check as before
    if fund is None:
        raise HTTPException(status_code=404, detail="Fund dosen't exist, can't create cash flow event without fund")

    # creates cash flow event
    new_cash_flow = crud.create_cash_flow_event(db, fund_id, cash_flow)

    #builds cashfloweventout schema
    cash_flow_out = schemas.CashFlowEventOut.model_validate(new_cash_flow)

    return cash_flow_out






