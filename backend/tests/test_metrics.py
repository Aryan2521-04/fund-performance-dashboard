import pytest
from datetime import date
from pyxirr import xirr
from app.metrics import calculate_dpi, calculate_tvpi, calculate_irr, calculate_irr_with_nav

# DPI Tests:

def test_dpi_normal():
    distributions = 15000
    contributions = 10000
    assert calculate_dpi(distributions, contributions) == 1.5

    # hand check = 15000 / 10000 = 1.5

def test_dpi_zero_contributions():
    distributions = 15000
    contributions = 0
    assert calculate_dpi(distributions, contributions) is None

#TVPI Tests:

def test_tvpi_normal():
    distributions = 15000
    contributions = 10000
    nav = 5000
    assert calculate_tvpi(distributions, contributions, nav) == 2.0

    # hand check = (15000 + 5000) / 10000 = 2.0

def test_tvpi_zero_contributions():
    distributions = 15000
    contributions = 0
    nav = 5000
    assert calculate_tvpi(distributions, contributions, nav) is None

# IRR Tests:

def test_irr_simple():
    cash_flows = [(date(2025, 1, 1), -100000), (date(2026, 1, 1), 110000)]
    assert calculate_irr(cash_flows) == pytest.approx(xirr(cash_flows), abs=1e-4)

def test_irr_multiple_cash_flows():
    cash_flows = [
        (date(2025, 1, 1), -1000000), # capital call
        (date(2026, 1, 1), -200000), # another capital call
        (date(2027, 1, 1), 300000), # distribution 
        (date(2028, 1, 1), 400000), # final distribution / NAV realization
    ]
    my_result = calculate_irr(cash_flows)
    reference_result = xirr(cash_flows) # pre-calculated using pyxirr library
    assert abs(my_result - reference_result) < 1e-4

def test_irr_no_cash_flows():
    cash_flows = []
    assert calculate_irr(cash_flows) is None

def test_irr_all_same_sign():
    cash_flows = [(date(2025, 1, 1), -1000000), (date(2026, 1, 1), -200000)] # all contributions, no distributions
    assert calculate_irr(cash_flows) is None

def test_irr_with_nav():
    # Same cash flow and nav snapshots as FUND III in seed data
    cash_flows = [
        (date(2021, 3, 1), -250000),
        (date(2021, 10, 1), -150000),
        (date(2022, 6, 1), -100000),    
        (date(2023, 11, 1), 120000), 
    ]
    nav_snapshots = [
        (date(2021, 12, 31), 380000),
        (date(2022, 12, 31), 450000),
        (date(2023, 12, 31), 400000),
    ]

    # Calculate IRR using only realized cash flows
    realized_only_irr = calculate_irr(cash_flows)
    # Calculate IRR including the latest NAV snapshot as a terminal cash flow
    since_inception_irr = calculate_irr_with_nav(cash_flows, nav_snapshots[-1][1], nav_snapshots[-1][0])
    # Check that the IRR including NAV is greater than the realized-only IRR
    assert since_inception_irr > realized_only_irr
    assert since_inception_irr > -0.10
