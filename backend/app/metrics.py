from scipy.optimize import brentq



# Fund: ID, name, vintage_year
# CashFlowEvent: id, fund_id, date, type (contribution/distribution), amount
# NAVSnapshot: id, fund_id, date, value


# writing straight functions, no DB just using math


def calculate_dpi(distributions, contributions):

    if contributions == 0:
        return 0
    return distributions / contributions

def calculate_tvpi(distributions, contributions, nav):
    if contributions == 0:
        return 0
    return (distributions + nav) / contributions

## TODO: implement IRR calculation using own newton method clauclator and brentq. 
# def calculate_irr(cash_flows_with_dates):