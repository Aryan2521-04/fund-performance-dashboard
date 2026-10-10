import pytest


def test_get_funds(client):
    response = client.get("/funds")
    assert response.status_code == 200
    funds = response.json()
    assert len(funds) == 4  # We seeded 4 funds
    assert funds[0]["name"] == "Fund I"
    assert funds[1]["name"] == "Fund II"
    assert funds[2]["name"] == "Fund III"
    assert funds[3]["name"] == "Fund IV"


def test_get_fund_by_id(client):
    response = client.get("/funds/1")
    assert response.status_code == 200
    fund = response.json()
    assert fund["name"] == "Fund I"
    assert fund["vintage_year"] == 2018
    assert len(fund["cash_flows"]) == 6
    assert len(fund["nav_snapshots"]) == 6
    assert "dpi" in fund
    assert "tvpi" in fund
    assert "irr_realized" in fund
    assert "irr_since_inception" in fund


def test_get_fund_not_found(client):
    response = client.get("/funds/999") 
    assert response.status_code == 404
    assert response.json() == {"detail": "Fund not found"}


def test_create_cash_flow(client):
    response = client.post("/funds/1/cashflows", json={"date": "2017-01-05", "amount": -50000})
    assert response.status_code == 200
    cf = response.json()
    assert cf["id"] is not None
    assert cf["date"] == "2017-01-05"
    assert float(cf["amount"]) == -50000

    call = client.get("/funds/1")
    assert call.status_code == 200
    fund = call.json()
    assert fund["cash_flows"][0]["date"] == "2017-01-05"


def test_create_cash_flow_fund_not_found(client):
    response = client.post("/funds/999/cashflows", json={"date": "2017-01-05", "amount": -50000})
    assert response.status_code == 404
    assert response.json() == {"detail": "Fund not found"}


def test_create_cash_flow_zero_amount(client):
    response = client.post("/funds/1/cashflows", json={"date": "2017-01-05", "amount": 0})
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()
