from .metrics import calculate_dpi, calculate_tvpi, calculate_irr, calculate_irr_with_nav
from .models import Fund
from decimal import Decimal


def compute_fund_metrics(fund: Fund) -> tuple[Decimal | None, Decimal | None, float | None, float | None]:

    # Same logic as what was orignally in seed_data with the sanity check, but now there is an attributie call to cash_flows
    distributions = sum(cf.amount for cf in fund.cash_flows if cf.amount > 0)
    contributions = -sum(cf.amount for cf in fund.cash_flows if cf.amount < 0)
    # Insted of one line to grab date and value from nav_snapshpts there is two line to grab them now as they're not a tuple anymore
    nav_value = fund.nav_snapshots[-1].value if fund.nav_snapshots else 0
    nav_date = fund.nav_snapshots[-1].date if fund.nav_snapshots else None
    
    dpi = calculate_dpi(distributions, contributions)
    tvpi = calculate_tvpi(distributions, contributions, nav_value)

    # wrapping .amount in float to let calculations go through, without this calculations will fall through as 
    # decimal to float calculation isn't allowed
    cash_flow_tuples = [(cf.date, float(cf.amount)) for cf in fund.cash_flows]

    irr = calculate_irr(cash_flow_tuples) 
    # same float wrapping as before, identical reasoning
    irr_nav = calculate_irr_with_nav(cash_flow_tuples, float(nav_value), nav_date)

    return dpi, tvpi, irr, irr_nav

