from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, metrics, schemas


# Get /funds

def list_funds(db: Session = Depends(get_db)):

    # Get all funds by calling crud.get_funds(db)

    funds = crud.get_funds(db)











# Get /funds{fund_id}


# POST /funds/{fund_id}/cashflows

