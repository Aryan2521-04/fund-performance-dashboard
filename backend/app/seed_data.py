from datetime import date
from .database import SessionLocal
from .models import Fund, CashFlowEvent, NavSnapshot


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

def seed_database():

    db = SessionLocal()

    # clearing existing data
    existing_funds = db.query(Fund).all()
    for fund in existing_funds:
        db.delete(fund)
    db.commit()

    # seeding new data
    for fund_dict in get_sample_funds():
        fund = Fund(name=fund_dict["name"], vintage_year=fund_dict["vintage_year"])

        for cash_flow_date, cash_flow_amount in fund_dict["cash_flows"]:
            cash_flow = CashFlowEvent(date=cash_flow_date, amount=cash_flow_amount)
            fund.cash_flows.append(cash_flow)

        for nav_snapshot_date, nav_snapshot_value in fund_dict["nav_snapshots"]:
            nav_snapshot = NavSnapshot(date=nav_snapshot_date, value=nav_snapshot_value)
            fund.nav_snapshots.append(nav_snapshot)

        db.add(fund)
    db.commit()
    db.close()
    print("Database seeded with sample data.")


if __name__ == "__main__":

    seed_database()