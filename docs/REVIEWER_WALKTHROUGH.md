# BakeOps Intelligence — Reviewer Walkthrough

## Purpose

BakeOps Intelligence is a bakery operations analytics platform.

It is designed to show how operational bakery data can be transformed into dashboard-ready metrics, data quality signals, and BI-ready exports.

---

## Quick Start

```powershell
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/analytics/
```

---

## What To Look For

### 1. KPI Cards

The dashboard shows:

- Revenue
- Average order value
- Gross margin
- Waste-adjusted margin

These values come from `DailyBakeryMetric`.

---

### 2. Signature Insight

Look for:

```text
Birthday Classic
Revenue rank #1
Waste-adjusted margin rank #4
Action: Review
```

This is the main V1 proof point.

The product sells strongly, but after ingredient cost and waste are included, it becomes weaker from a profitability perspective.

---

### 3. Product Profitability Table

This table comes from `ProductPerformanceSnapshot`.

It shows:

- Revenue
- Ingredient cost
- Waste cost
- Waste-adjusted margin
- Revenue rank
- Waste-adjusted margin rank
- Action flag

---

### 4. Ingredient Risk

This panel comes from `IngredientUsageSnapshot`.

It highlights ingredients below reorder level or affected by stock/expiry risk.

---

### 5. Data Quality Issues

This panel comes from `DataQualityIssue`.

It shows trust issues that should be reviewed before relying on metrics.

---

### 6. Last Build Status

This panel comes from `BakeryMetricRunLog`.

It confirms the latest metric build status, rows processed, snapshots created, and issues generated.

---

### 7. BI Exports

Run:

```powershell
python manage.py export_bi_csv
```

Check:

```text
exports/
```

The export pack includes fact tables, dimension tables, and gold-layer analytics exports.

---

## Verification Commands

```powershell
python manage.py check
python manage.py test bakeops
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
```

---

## Expected Export Count

```text
11 CSV files
```

---

## Expected Core Scenario

```text
Birthday Classic is revenue rank #1 but waste-adjusted margin rank #4.
```

---

## Interpretation

This proves BakeOps is not simply showing sales data.

It is connecting:

```text
orders + recipes + ingredient costs + production + waste
```

into:

```text
decision-ready profitability insight
```

---

## Reviewer Notes

- V1 uses seeded demo data only.
- The dashboard should be reviewed after running `seed_demo_data --reset` and `build_bakery_metrics`.
- The export pack is generated locally and should not be committed to Git.
- The `/analytics/` dashboard is the main V1 surface.
- The Django admin can be used to inspect operational records, gold-layer snapshot records, metric run logs, and data quality issues.

---

## V1 Review Path

```text
1. Run migrations
2. Seed demo data
3. Build bakery metrics
4. Open /analytics/
5. Verify Birthday Classic signature insight
6. Generate BI exports
7. Run BakeOps tests
```

---

## Evidence of Analytics Engineering

BakeOps demonstrates:

- Source operational modelling
- Transformation logic through management commands and services
- Gold-layer reporting models
- Dashboard-ready metric snapshots
- Data quality issue generation
- Run logging
- BI-ready export design
- Dashboard/export parity checks
