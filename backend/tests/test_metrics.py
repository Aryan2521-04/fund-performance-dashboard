import pytest
from datetime import date
from pyxirr import xirr
from app.metrics import calculate_dpi, calculate_tvpi, calculate_irr 

def test_irr_simple():
    cash_flows = [(date(2025, 1, 1), -100), (date(2026, 1, 1), 110)]
    assert calculate_irr(cash_flows) == pytest.approx(xirr(cash_flows), abs=1e-4)
