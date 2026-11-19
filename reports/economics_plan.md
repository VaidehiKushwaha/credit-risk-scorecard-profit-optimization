# Economics plan (written before computing profits)

**Decision:** extend/maintain credit (approve) vs. restrict (decline), one period.
**Base case (Scenario A):** R = 6,000 NT$ per non-defaulting customer; LGD = 70%;
EAD = mean of max(BILL_AMT1, 0) on train. L = LGD x EAD. Cutoff rule: approve if PD <= p* = R/(R+L).
**Check:** empirical profit-optimal cutoff on train OOF must have p* inside its plateau (within 2% of max).
**Scenario B (customer-specific R and L):** same average economics, varying by customer (9.8).
**Strategies compared on test:** approve all; decline all; accuracy-optimal cutoff; policy rule
(decline if 2+ months late); scorecard at p*; LightGBM at p*; perfect-foresight ceiling.
**Sensitivity:** R in {3000..12000}, LGD in {0.5..0.9}; calibration shift; break-even revenue.
**Success criteria:** profit-optimal strategy beats approve-all and accuracy cutoff with 95% CI excluding 0;
challenger adopted only if paired profit uplift CI excludes 0 and the uplift is material.
