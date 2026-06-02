# BakeOps Phase 1 — SQL Evidence Layer

Reviewer-facing SQL only. This folder does **not** change Django models, migrations, services, dashboards, seed logic, CI, or production database setup.

## Purpose

Demonstrate Analytics Engineering and Data Engineering SQL skills against BakeOps **operational facts**, **dimensions**, and **gold-layer** exports produced by:

```powershell
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
```

All scripts target **SQLite 3.25+** (window functions required). Queries are written against CSV-backed staging tables that mirror the stable BI export contract in `bakeops/services/exports.py`.

## Scope boundary

| In scope | Out of scope |
|---|---|
| `docs/sql/*.sql` and this README | Django ORM, views, metric build code |
| Local SQLite rehearsal | Production PostgreSQL/SQLite app DB |
| Claims aligned to seeded demo exports | Live POS import or multi-tenant SaaS |

## Quick start

From the **repository root** (this project directory):

```powershell
# 1. Ensure exports exist (11 files, ~52 rows in current demo)
python manage.py export_bi_csv

# 2. Create a local evidence database
Get-Content docs/sql/00_table_inventory.sql | sqlite3 bakeops_evidence.db

# 3. Import CSVs (run inside sqlite3; paths relative to repository root)
sqlite3 bakeops_evidence.db
```

Inside the SQLite shell:

```sql
.mode csv
.import --skip 1 exports/fact_orders.csv fact_orders
.import --skip 1 exports/fact_order_items.csv fact_order_items
.import --skip 1 exports/fact_waste.csv fact_waste
.import --skip 1 exports/fact_production_batches.csv fact_production_batches
.import --skip 1 exports/dim_cake.csv dim_cake
.import --skip 1 exports/dim_ingredient.csv dim_ingredient
.import --skip 1 exports/dim_customer.csv dim_customer
.import --skip 1 exports/dim_occasion.csv dim_occasion
.import --skip 1 exports/dim_collection.csv dim_collection
.import --skip 1 exports/daily_bakery_metrics.csv daily_bakery_metrics
.import --skip 1 exports/product_performance_snapshot.csv product_performance_snapshot
SELECT * FROM v_table_inventory;
```

Run individual evidence scripts:

```powershell
Get-Content docs/sql/05_signature_insight_sql.sql | sqlite3 bakeops_evidence.db
```

**No `sqlite3` CLI?** Use Python 3.11+ with the standard library: load `00_table_inventory.sql` via `sqlite3.connect(...).executescript(...)`, import each CSV with `csv.DictReader`, then `executescript` each `.sql` file.

## File guide

| File | Skill focus |
|---|---|
| `00_table_inventory.sql` | Schema DDL, grains, keys, inventory view, idempotent drops |
| `01_joins_orders_products_customers.sql` | Star-style joins across facts and dimensions |
| `02_row_level_functions.sql` | `CASE`, `COALESCE`, `CAST`, `strftime`, string cleanup |
| `03_aggregation_and_window_functions.sql` | `GROUP BY`, `HAVING`, `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `LAG` |
| `04_data_quality_and_set_operators.sql` | Null/orphan checks, `UNION` / `EXCEPT` reconciliation |
| `05_signature_insight_sql.sql` | Revenue vs waste-adjusted margin ranks (demo proof) |
| `PHASE_1_SQL_EVIDENCE_SUMMARY.md` | Reviewer checklist and claim-safe evidence notes |

## Data layers (export contract)

```text
Facts:      fact_orders, fact_order_items, fact_waste, fact_production_batches
Dimensions: dim_cake, dim_ingredient, dim_customer, dim_occasion, dim_collection
Gold:       daily_bakery_metrics, product_performance_snapshot
```

Lineage reference: `docs/LINEAGE.md`, `docs/METRIC_GOVERNANCE.md`.

## Rank conventions (important)

| Metric | Formula | Birthday Classic (demo) | Meaning |
|---|---|---:|---|
| `margin_rank_gap` | `waste_adjusted_margin_rank - revenue_rank` | **3** | Matches dashboard/tests; positive = rank dropped after waste |
| `rank_movement` | `revenue_rank - waste_adjusted_margin_rank` | **-3** | Matches `docs/CASE_STUDY.md`; negative = margin rank weakened |

Gold-layer `revenue_rank` and `waste_adjusted_margin_rank` come from `build_bakery_metrics`; SQL reads them from `product_performance_snapshot`.

## CSV typing note

SQLite `.import` may store numeric export columns as TEXT. Evidence queries in `02`, `03`, and `05` use `CAST(... AS REAL)` / `CAST(... AS INTEGER)` before arithmetic.

## Final acceptance checklist

After seed, build, export, DDL, and CSV import:

- [ ] `SELECT * FROM v_table_inventory` returns **11** tables (~52 rows total on current seed)
- [ ] `02_row_level_functions.sql` runs without error (includes `CAST`, `strftime`, subquery `ORDER BY`)
- [ ] `03_aggregation_and_window_functions.sql` runs without error (includes `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `LAG`)
- [ ] `05_signature_insight_sql.sql` query 5 returns `Birthday Classic 1 4 review`
- [ ] Query 1 in `05` shows `margin_rank_gap = 3` and `rank_movement = -3` for Birthday Classic
- [ ] No claim of production warehouse, dbt, Snowflake, BigQuery, Airflow, or cloud orchestration

## Claim safety

- Demo workspace **SweetCakes Bakery** (`workspace_id = 1`) only; row counts change if seed data changes.
- Signature insight is defined in gold-layer snapshots built by `build_bakery_metrics`, not invented in SQL.
- SQL here **reads** exports; it does not replace the metric build pipeline.

## Expected demo anchors (current seed)

Use these only after a fresh seed + build + export; verify with queries if unsure:

| Evidence | Typical value |
|---|---|
| Paid orders | 6 |
| Export files | 11 |
| Export rows | ~52 |
| Signature product | Birthday Classic |
| Signature ranks | 1 (revenue) → 4 (waste-adjusted margin) |
| `margin_rank_gap` | 3 |
| `rank_movement` | -3 |
