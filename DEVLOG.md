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
Decision: removed type from CashFlowEvent entirely. Since this project's cash flows are strictly binary (contribution/distribution) and fully determined by amount's sign, storing a derived fact separately violated a basic normalization principle don't store what you can compute for no real benefit. If a future need arose to distinguish more granular categories that sign alone can't capture (e.g., management fees vs. capital calls, both negative but meaningfully different), that would justify reintroducing an explicit field. For now, direction can be derived on demand (e.g., a computed property) if ever needed for display or filtering, without risking drift from the source of truth.
