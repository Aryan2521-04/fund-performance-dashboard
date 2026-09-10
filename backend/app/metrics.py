from scipy.optimize import brentq
from datetime import date



# Fund: ID, name, vintage_year
# CashFlowEvent: id, fund_id, date, type (contribution/distribution), amount
# NAVSnapshot: id, fund_id, date, value


# writing straight functions, no DB just using math


def calculate_dpi(distributions, contributions):

    """
    distributions: total distributions to LPs
    contributions: total contributions from LPs
    """

    if contributions == 0:
        return 0
    return distributions / contributions

def calculate_tvpi(distributions, contributions, nav):

    """
    distributions: total distributions to LPs
    contributions: total contributions from LPs
    nav: current net asset value of the fund
    """

    if contributions == 0:
        return 0
    return (distributions + nav) / contributions

## TODO: implement IRR calculation using own newton method clauclator and brentq. 
def calculate_irr(cash_flows_with_dates): 
    """
    cash_flows_with_dates: list of (date, amount) tuples, sorted by date.
    Contributions should be negative, distributions/NAV positive.
    """

    def xpnv(rate): 
        t0 = cash_flows_with_dates[0][0]
        return sum(
            amount / (1 + rate) ** ((date - t0).days / 365)
            for d, amount in cash_flows_with_dates
        )

    try:
        return brentq(xpnv, -0.9999, 10)
    except ValueError:
        return None
