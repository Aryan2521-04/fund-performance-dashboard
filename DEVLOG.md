09/13/26:

While testing seed data Fund II and III showed strongly negative IRR's despite TVPI values above 1.0 (suggesting the funds had created value overall). Investigated and confirmed this isn't a bug. It's because calculate_irr only counts realized cash flows, while TVPI includes unrealized NAV in its numerator. For a fund still holding significant unrealized value, this means IRR-as-implemented will understate true performance relative to TVPI.
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

9/15/26:

While building CashFlowEvent, got stuck on a design decision: should type (contribution/distribution) be stored as its own column, and if so, as a String or an Enum? Initially leaned toward Enum over String, since Enum enforces valid values at the database level since a plain String column would accept any text, including typos or inconsistent casing ("Contribution" vs "contribution"), with no safeguard.
But Enum only solves part of the problem. Both Fund cash flows already encode direction through the sign of amount (negative = contribution, postive = distribution). Storing type as a separate field, Enum or not, creates redundant data: two fields encoding the same fact, with no guarantee they stay in sync. A row could exist where amount = -50000 but type = DISTRIBUTION, and nothing in the schema would catch that contradiction.

9/24/26:

After completing funds.py and testing the routers, making sure the code was running as intended, during a test session I found a edge case that results in the crash of the app. It's when calculate_irr_with_nav assumes nav_date is always real, so when it gets None when there is no nav_date (as per fallback) it wasn't taught what to do with the None, so it just blindly validates it and appends it, crashing the app. Test cases that I had used didn't cover this, but using mock data while testing helped me uncover some bugs like this one. Easy fix, it was to implemtn a guard within calculate_irr_with_nav, where if nav_date is None, it returns the calculation using the realized irr.
Additonally found another bug where there was a decimal / float division mismatch between ORM data and pure math functions, so I put float wrapper in certain values within fund_service.py where it was needed, such as cf.amount and nav_value.

9/29/26:

Decimal/JSON serialization issue was found while testing the main frontend page. Basically DPI and TVPI values were showing up as 0E + 2 when they should've should up as 0's. Traced it to FundSummary.dpi/tvpi being typed as Decimal | None in schemas.py. Pydantic serializes Decimal to JSON as its string representation, preserving exact precision, but Python's Decimal uses scientific notation for some values (e.g. Decimal("0") / Decimal("50000.00") produces Decimal("0E+2"), not Decimal("0")). The frontend received that string as-is and rendered it literally. Fix was simple, just changed the return type to Floar | None for DPI and TVPI.

10/6/26:

Wrote the API tests for all three endpoints (GET /funds, GET /funds/{id}, POST /funds/{id}/cashflows), covering the 404s and the zero-amount validator (422). Writing them turned up two bugs. The first was that the relationships had no order_by. fund_service took nav_snapshots[-1] assuming it was the latest-dated row, but it was really just the last one inserted. I wrote a test that POSTs a backdated (2017) cash flow and checks that it comes back first. My first version of the assert used [-1], which would have passed against the buggy code, because it was checking for the bug. After adding order_by="CashFlowEvent.date" and order_by="NavSnapshot.date" in models.py, the corrected test passes.

The second was a stale NAV in calculate_irr_with_nav. If the NAV date is before the last cash flow, the NAV already includes value that was later paid out as a distribution, so that money gets counted twice. In my test case this turned a -38% realized IRR into +5.7%. I added a guard that falls back to realized-only IRR when nav_date < the last cash flow date, the same approach as the existing None guard. I chose a fallback over raising an error so that one bad cash flow can't make GET /funds return 500 for every fund. A NAV dated the same day as the last cash flow still counts, and I added a test for that case so the guard can't be changed to <= without a test failing.
