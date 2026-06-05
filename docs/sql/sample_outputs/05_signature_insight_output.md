# Sample Output — 05 Signature Insight SQL

Captured from a fresh BakeOps demo run.

## Fresh run context

- Command sequence:
  - `python manage.py seed_demo_data --reset`
  - `python manage.py build_bakery_metrics`
  - `python manage.py export_bi_csv`
- Workspace: SweetCakes Bakery
- Cakes seeded: 12
- Product performance snapshot rows: 4
- Evidence capture: SQLite evidence DB loaded from BI CSV exports per `docs/sql/README.md`; primary reviewer query (query 1) executed against imported tables. Export `workspace_id` is 15 on this run (SQL files document `workspace_id = 1` as the evidence rehearsal anchor).

## Reviewer query output

| cake_name | revenue_rank | waste_adjusted_margin_rank | margin_rank_gap | rank_movement | action_flag | action_reason |
|---|---:|---:|---:|---:|---|---|
| Birthday Classic | 1 | 4 | 3 | -3 | review | This product sells strongly, but waste-adjusted margin rank is weaker than revenue rank. |

Additional columns from query 1:

| cake_name | variant_label | revenue | waste_cost | waste_adjusted_margin | has_margin_rank_inversion |
|---|---|---:|---:|---:|---:|
| Birthday Classic | 8" - serves 10-12 | 405.00 | 32.75 | 250.48 | 1 |

## Interpretation

Birthday Classic is the top revenue product but falls to rank 4 after waste-adjusted margin is considered. This is the project's signature rank-inversion insight.
