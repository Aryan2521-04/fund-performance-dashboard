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
