# BakeOps Intelligence

BakeOps Intelligence is a bakery operations analytics platform built with Django.

It transforms bakery catalogue, customer, order, ingredient, recipe, production, waste, loyalty, and review data into dashboard-ready metrics and BI-ready CSV exports.

---

## Project Status

```text
V1 = Works
```

V1 is focused on one working analytics dashboard powered by seeded operational data and a metric build command.

---

## Core Purpose

BakeOps Intelligence is not just a bakery catalogue website.

The project separates the application into two layers:

| App | Purpose |
|---|---|
| `cakes` | Existing customer-facing cake catalogue |
| `bakeops` | Analytics, operations, metrics, data quality, exports, and decision intelligence |

---

## V1 Workflow

```text
seed_demo_data
→ operational bakery data
→ build_bakery_metrics
→ gold-layer snapshots
→ /analytics/ dashboard
→ export_bi_csv
→ BI-ready CSV files
```

---

## Key V1 Features

- Realistic seeded bakery operations dataset
- Workspace, customers, loyalty, occasions, orders, ingredients, recipes, production, allocation, and waste records
- Gold-layer analytics models
- Metric build command
- Data quality issue generation
- Bakery metric run logging
- `/analytics/` dashboard
- Product profitability table
- Revenue rank vs waste-adjusted margin rank
- Weekly action cards
- Ingredient risk panel
- Data quality panel
- BI-ready CSV exports

---

## Signature Insight

BakeOps proves the following business idea:

> A best-selling product can become weak after ingredient cost and waste are included.

In the seeded V1 demo:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | #1 | #4 | Review |

This shows that the highest-revenue product is not necessarily the strongest product after waste-adjusted profitability is calculated.

---

## Main Commands

### 1. Run Django checks

```powershell
python manage.py check
```

### 2. Seed demo data

```powershell
python manage.py seed_demo_data --reset
```

### 3. Build gold-layer metrics

```powershell
python manage.py build_bakery_metrics
```

### 4. Export BI-ready CSV files

```powershell
python manage.py export_bi_csv
```

### 5. Run tests

```powershell
python manage.py test bakeops
```

### 6. Run local server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/analytics/
```

---

## BI Export Files

The export command generates files into the `exports/` folder:

| File | Purpose |
|---|---|
| `fact_orders.csv` | Order-level fact table |
| `fact_order_items.csv` | Order item fact table |
| `fact_waste.csv` | Waste fact table |
| `fact_production_batches.csv` | Production batch line fact table |
| `dim_cake.csv` | Cake and variant dimension |
| `dim_ingredient.csv` | Ingredient dimension |
| `dim_customer.csv` | Customer and loyalty dimension |
| `dim_occasion.csv` | Occasion dimension |
| `dim_collection.csv` | Cake collection dimension |
| `daily_bakery_metrics.csv` | Daily KPI gold-layer export |
| `product_performance_snapshot.csv` | Product profitability gold-layer export |

Generated CSV files are intentionally ignored by Git.

---

## Data Model Layers

### Operational Layer

- Workspace
- StaffMember
- Customer
- LoyaltyAccount
- CakeReview
- OccasionType
- DeliverySlot
- BakeryOrder
- BakeryOrderItem
- Supplier
- Ingredient
- IngredientLot
- Recipe
- RecipeLine
- ProductionBatch
- ProductionBatchLine
- BatchAllocation
- WasteRecord

### Gold-Layer Analytics

- DailyBakeryMetric
- ProductPerformanceSnapshot
- IngredientUsageSnapshot
- OccasionDemandSnapshot
- CustomerLoyaltySnapshot
- BakeryMetricRunLog
- DataQualityIssue

---

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py runserver
```

---

## Environment Variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Then set your local `SECRET_KEY`.

---

## V1 Verification Checklist

```markdown
- [x] `python manage.py check` passes
- [x] `python manage.py migrate` works
- [x] `python manage.py seed_demo_data --reset` works
- [x] `python manage.py build_bakery_metrics` works
- [x] `python manage.py export_bi_csv` works
- [x] `/analytics/` dashboard loads
- [x] Waste-adjusted profitability is visible
- [x] Birthday Classic signature insight is visible
- [x] Data quality issues are visible
- [x] BakeryMetricRunLog is visible in admin
- [x] BI exports work
- [x] Dashboard metrics match export metrics
- [x] BakeOps tests pass
```

---

## Current Limitations

- V1 uses seeded demo data.
- V1 does not yet include file imports.
- V1 does not yet include external POS, Shopify, Square, or payment integrations.
- V1 does not yet include a full export centre UI.
- V1 does not yet include multi-tenant SaaS permissions.

---

## Next Versions

```text
V1 = Works
V2 = Trusted
V3 = Commercial
```

V2 will focus on deeper analytics pages, metric governance, data lineage, export contracts, and stronger documentation.

V3 will focus on SaaS readiness, imports, onboarding, workspace management, billing foundation, and commercial beta preparation.
