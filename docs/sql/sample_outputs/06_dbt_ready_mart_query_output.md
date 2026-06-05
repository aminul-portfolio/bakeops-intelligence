# Sample Output — 06 dbt-Ready Mart Query

Captured from a fresh BakeOps demo run.

## Fresh run context

- Command sequence:
  - `python manage.py seed_demo_data --reset`
  - `python manage.py build_bakery_metrics`
  - `python manage.py export_bi_csv`
- Workspace: SweetCakes Bakery
- Purpose: Shows the mart-style output that will later map to `mart_product_performance` in `bakeops-dbt`.
- Evidence capture: SQLite evidence DB loaded from BI CSV exports per `docs/sql/README.md`; `06_dbt_ready_mart_query.sql` executed with export `workspace_id` substituted for the documented `workspace_id = 1` rehearsal filter.

## Mart-style output

| cake_id | cake_name | units_sold | distinct_orders | operational_revenue | snapshot_revenue | gross_margin | waste_cost | waste_adjusted_margin | revenue_rank | waste_adjusted_margin_rank | margin_rank_gap | rank_movement | rank_movement_label | has_rank_inversion | action_flag |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 137 | Birthday Classic | 5 | 2 | 225.00 | 405.00 | 283.23 | 32.75 | 250.48 | 1 | 4 | 3 | -3 | margin_weaker_than_revenue_suggests | 1 | review |
| 140 | Wedding Rose | 2 | 1 | 190.00 | 190.00 | 134.94 | 0.00 | 134.94 | 2 | 2 | 0 | 0 | ranks_aligned | 0 | stable |
| 139 | Luxury Chocolate | 2 | 1 | 76.00 | 76.00 | 50.02 | 0.00 | 50.02 | 3 | 3 | 0 | 0 | ranks_aligned | 0 | stable |
| 138 | Lemon Poppy | 2 | 1 | 56.00 | 56.00 | 46.60 | 1.40 | 45.20 | 4 | 1 | -3 | 3 | margin_stronger_than_revenue_suggests | 0 | promote |

## Signature product detail

Birthday Classic (`cake_id` 137):

- `revenue_rank` = 1
- `waste_adjusted_margin_rank` = 4
- `has_rank_inversion` = 1
- `action_flag` = review
- `action_reason` = This product sells strongly, but waste-adjusted margin rank is weaker than revenue rank.

Note: `operational_revenue` (225.00) reflects paid-order facts only; `snapshot_revenue` (405.00) reflects the gold-layer snapshot built by `build_bakery_metrics`.

## Interpretation

This output demonstrates the planned dbt mart structure:
staging order data → intermediate product revenue/margins → final product performance mart.
