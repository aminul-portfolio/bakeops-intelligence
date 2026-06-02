# Phase 1 SQL Evidence — Reviewer Summary

## What was delivered

A **SQLite-compatible** SQL evidence layer under `docs/sql/` that queries BakeOps BI exports (facts, dimensions, gold snapshots). No application code, migrations, or production database changes were made.

## Skills demonstrated

| Area | Evidence file |
|---|---|
| Schema inventory and grains | `00_table_inventory.sql` |
| Multi-table joins (orders × products × customers) | `01_joins_orders_products_customers.sql` |
| Row-level transforms (`CASE`, `CAST`, dates, strings) | `02_row_level_functions.sql` |
| Aggregations and window functions | `03_aggregation_and_window_functions.sql` |
| Data quality and set operators | `04_data_quality_and_set_operators.sql` |
| Signature business insight SQL | `05_signature_insight_sql.sql` |

## How to verify (5 minutes)

```powershell
# From repository root
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
Get-Content docs/sql/00_table_inventory.sql | sqlite3 bakeops_evidence.db
```

Import all 11 CSV files from `exports/` per `docs/sql/README.md`, then:

```powershell
Get-Content docs/sql/05_signature_insight_sql.sql | sqlite3 bakeops_evidence.db
```

## Final acceptance criteria

| Check | Expected result |
|---|---|
| Staging tables created | 11 tables from `00_table_inventory.sql` |
| Inventory view | `v_table_inventory` lists fact, dimension, and gold layers |
| Row-level SQL | `02_row_level_functions.sql` executes; uses `CAST`, `COALESCE`, `strftime` |
| Window SQL | `03_aggregation_and_window_functions.sql` executes; uses `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `LAG` |
| Signature evidence string | `Birthday Classic 1 4 review` |
| Dashboard rank gap | `margin_rank_gap = 3` for Birthday Classic |
| Case study rank movement | `rank_movement = -3` for Birthday Classic |
| Workspace filter | Latest snapshot for `workspace_id = 1` |
| Scope boundary | No Django / CI / production DB changes in this phase |

## Expected signature row (current demo seed)

| Field | Expected |
|---|---|
| `cake_name` | Birthday Classic |
| `revenue_rank` | 1 |
| `waste_adjusted_margin_rank` | 4 |
| `action_flag` | review |
| `signature_evidence` | `Birthday Classic 1 4 review` |
| `margin_rank_gap` | 3 |
| `rank_movement` | -3 |

## Architecture alignment

```text
seed_demo_data → operational models
build_bakery_metrics → gold snapshots (ranks, margins, action flags)
export_bi_csv → CSV staging consumed by this SQL layer
```

SQL reads **exports**; it does not replace `build_bakery_metrics`. Rank columns in `product_performance_snapshot` remain the authoritative demo proof for the signature insight.

## Claim-safe statements

**Can claim:**

- Phase 1 SQL rehearses the same 11-file BI contract documented in `docs/LINEAGE.md`.
- Joins and quality checks operate on fact/dimension grains matching `bakeops/services/exports.py`.
- Signature insight SQL reproduces the **Birthday Classic 1 4 review** evidence used in tests and `docs/METRIC_GOVERNANCE.md`.
- `margin_rank_gap` and `rank_movement` are documented and consistent with the dashboard and case study respectively.

**Cannot claim:**

- This layer runs in production or replaces Django ORM queries on the app database.
- SQL alone builds gold metrics (build command still required).
- Results generalise beyond the seeded SweetCakes Bakery demo without re-exporting CSVs.

## File count checklist

- [x] `README.md`
- [x] `00_table_inventory.sql`
- [x] `01_joins_orders_products_customers.sql`
- [x] `02_row_level_functions.sql`
- [x] `03_aggregation_and_window_functions.sql`
- [x] `04_data_quality_and_set_operators.sql`
- [x] `05_signature_insight_sql.sql`
- [x] `PHASE_1_SQL_EVIDENCE_SUMMARY.md`

## Scope confirmation

No changes were made to: Django models, migrations, views, services, templates, dashboards, seed logic, CI configuration, or production database setup.
