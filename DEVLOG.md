09/13/26:

While testing the seed data, Funds II and III showed strongly negative IRRs despite TVPI values above 1.0 (suggesting the funds had created value overall). I investigated and confirmed this isn't a bug: calculate_irr only counts realized cash flows, while TVPI includes unrealized NAV in its numerator. For a fund still holding significant unrealized value, this means IRR-as-implemented will understate true performance relative to TVPI.
This is a known consideration in PE performance reporting: reporting a fund's "IRR since inception" while it's still active typically requires including current NAV as a terminal cash flow on the valuation date.
Added calculate_irr_with_nav(cash_flows_with_dates, nav, nav_date) to metrics.py. It appends the latest NAV snapshot as a terminal cash flow
(re-sorted into the series) and passes that through the existing calculate_irr, treating current NAV as a hypothetical liquidation value on the
snapshot date — this is the standard convention for reporting "IRR since inception" on a still-active fund. calculate_irr itself was left
unchanged, since realized-only IRR is still a valid (if different) metric on its own.

Re-ran the sanity check to confirm IRR now moves in the same direction as TVPI for every fund:

- Fund I: 11.83% → 14.75% (TVPI 1.84)
- Fund II: -3.13% → 5.53% (TVPI 1.18)
- Fund III: -48.31% → 1.67% (TVPI 1.04)
- Fund IV: N/A → -7.40%

09/15/26:

While building CashFlowEvent, I got stuck on a design decision: should type (contribution/distribution) be stored as its own column, and if so, as a String or an Enum? I initially leaned toward Enum over String, since Enum enforces valid values at the database level, while a plain String column would accept any text, including typos or inconsistent casing ("Contribution" vs "contribution"), with no safeguard.
But Enum only solves part of the problem. Fund cash flows already encode direction through the sign of amount (negative = contribution, positive = distribution). Storing type as a separate field, Enum or not, creates redundant data: two fields encoding the same fact, with no guarantee they stay in sync. A row could exist where amount = -50000 but type = DISTRIBUTION, and nothing in the schema would catch that contradiction.

09/24/26:

After completing funds.py and testing the routers to make sure the code was running as intended, I found an edge case that crashes the app. calculate_irr_with_nav assumed nav_date always had a value, so when a fund had no NAV snapshot (the fallback case) it received None, had no way to handle it, and appended it to the cash flows anyway, crashing the app. My existing test cases didn't cover this, but testing with mock data helped me uncover bugs like this one. The fix was easy: a guard in calculate_irr_with_nav that returns the realized IRR when nav_date is None.
I also found a Decimal/float division mismatch between the ORM data and the pure math functions, so I added float() wrappers around the values in fund_service.py that needed them, such as cf.amount and nav_value.

09/29/26:

I found a Decimal/JSON serialization issue while testing the main frontend page. DPI and TVPI values were showing up as 0E+2 when they should have shown up as 0. Traced it to FundSummary.dpi/tvpi being typed as Decimal | None in schemas.py. Pydantic serializes Decimal to JSON as its string representation, preserving exact precision, but Python's Decimal uses scientific notation for some values (e.g. Decimal("0") / Decimal("50000.00") produces Decimal("0E+2"), not Decimal("0")). The frontend received that string as-is and rendered it literally. The fix was simple: I changed the type of DPI and TVPI to float | None.

10/06/26:

Wrote the API tests for all three endpoints (GET /funds, GET /funds/{id}, POST /funds/{id}/cashflows), covering the 404s and the zero-amount validator (422). Writing them turned up two bugs. The first was that the relationships had no order_by. fund_service took nav_snapshots[-1] assuming it was the latest-dated row, but it was really just the last one inserted. I wrote a test that POSTs a backdated (2017) cash flow and checks that it comes back first. My first version of the assert used [-1], which would have passed against the buggy code because it was checking for the bug. After adding order_by="CashFlowEvent.date" and order_by="NavSnapshot.date" in models.py, the corrected test passes.

The second was a stale NAV in calculate_irr_with_nav. If the NAV date is before the last cash flow, the NAV already includes value that was later paid out as a distribution, so that money gets counted twice. In my test case this turned a -38% realized IRR into +5.7%. I added a guard that falls back to realized-only IRR when nav_date < the last cash flow date, the same approach as the existing None guard. I chose a fallback over raising an error so that one bad cash flow can't make GET /funds return 500 for every fund. A NAV dated the same day as the last cash flow still counts, and I added a test for that case so the guard can't be changed to <= without a test failing.
