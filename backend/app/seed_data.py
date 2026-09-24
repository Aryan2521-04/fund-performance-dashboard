from datetime import date
from .metrics import calculate_dpi, calculate_tvpi, calculate_irr, calculate_irr_with_nav
from .fund_service import compute_fund_metrics


def get_sample_funds():
    return [
        {
            "name": "Fund I",
            "vintage_year": 2018,
            "cash_flows": [
                (date(2018, 1, 15), -200000),   # capital call
                (date(2018, 9, 10), -150000),   # capital call
                (date(2019, 3, 1), -100000),    # capital call (total called: 450,000)
                (date(2020, 11, 1), 80000),     # first distribution, ~2 yrs after last call
                (date(2022, 5, 15), 250000),    # distribution
                (date(2023, 8, 1), 400000),     # final distribution
            ],
            "nav_snapshots": [
                (date(2018, 12, 31), 420000),   # most capital just invested
                (date(2019, 12, 31), 480000),   # NAV grows as investments mature
                (date(2020, 12, 31), 460000),   # dips slightly after first distribution
                (date(2021, 12, 31), 500000),
                (date(2022, 12, 31), 300000),   # drops after big distribution
                (date(2023, 12, 31), 100000),   # nearing end of life
            ]
        },
        {
            "name": "Fund II",
            "vintage_year": 2019,
            "cash_flows": [
                (date(2019, 2, 1), -300000),
                (date(2019, 11, 1), -150000),
                (date(2020, 7, 1), -100000),    # total called: 550,000
                (date(2021, 9, 1), 150000),
                (date(2022, 12, 1), 350000),
            ],
            "nav_snapshots": [
                (date(2019, 12, 31), 430000),
                (date(2020, 12, 31), 520000),
                (date(2021, 12, 31), 400000),
                (date(2022, 12, 31), 150000),
            ]
        },
        {
            "name": "Fund III",
            "vintage_year": 2021,
            "cash_flows": [
                (date(2021, 3, 1), -250000),
                (date(2021, 10, 1), -150000),
                (date(2022, 6, 1), -100000),    # total called: 500,000
                (date(2023, 11, 1), 120000),    # only one distribution so far, still early in life
            ],
            "nav_snapshots": [
                (date(2021, 12, 31), 380000),
                (date(2022, 12, 31), 450000),
                (date(2023, 12, 31), 400000),
            ]
        },
        {
            # young fund, contributions only, no distributions yet
            "name": "Fund IV",
            "vintage_year": 2023,
            "cash_flows": [
                (date(2023, 2, 1), -350000),
                (date(2023, 8, 1), -200000),    # total called: 550,000
            ],
            "nav_snapshots": [
                (date(2023, 12, 31), 520000),   # roughly = called capital, slightly grown
            ]
        }
    ]

# sanity check

if __name__ == "__main__":

    # Place holder loop, will be replaced by helper function later on
    for fund in get_sample_funds():
        distributions = sum(amount for d, amount in fund["cash_flows"] if amount > 0)
        contributions = -sum(amount for d, amount in fund["cash_flows"] if amount < 0)
        nav = fund["nav_snapshots"][-1][1] if fund["nav_snapshots"] else 0
        irr = calculate_irr(fund["cash_flows"]) 
        dpi = calculate_dpi(distributions, contributions)
        tvpi = calculate_tvpi(distributions, contributions, nav)
        # fail check so it dosen't crash on fund IV
        if irr is None:
            irr_display = "N/A"
        else:
            irr_display = f"{irr:.2%}"
        print(f"{fund['name']} (vintage {fund['vintage_year']}): DPI={dpi:.2f}, TVPI={tvpi:.2f}, IRR={irr_display}, IRR with NAV={calculate_irr_with_nav(fund['cash_flows'], nav, fund['nav_snapshots'][-1][0]):.2%}") 





""" 
implemented later
def seed_database():
    funds = [
        {"name": "Fund I", "vintage_year": 2018},
        {"name": "Fund II", "vintage_year": 2019},
        {"name": "Fund III", "vintage_year": 2021},
        {"name": "Fund IV", "vintage_year": 2023},

    ]

    for fund in funds:
"""
        