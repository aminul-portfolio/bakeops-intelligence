# BakeOps Intelligence - Reviewer Walkthrough

## Purpose

This walkthrough helps a reviewer run and validate BakeOps Intelligence locally.

BakeOps Intelligence is a bakery operations analytics platform built with Django. It transforms seeded bakery operations data into trusted analytics pages, data quality evidence, metric lineage documentation, and BI-ready CSV exports.

---

## Version Status

```text
V1 = Works
V2 = Trusted
V3 = Commercial foundation
```

V2 proves the platform is reliable, testable, explainable, and reviewer-ready.

V3 adds commercial-readiness documentation and product-positioning evidence, but it does not claim live SaaS usage, production deployment, billing, subscriptions, external POS integration, Shopify/Square integration, or real customer usage.

---

## Core Idea

BakeOps proves the following business idea:

```text
A best-selling bakery product can become weak after ingredient cost and waste are included.
```

The seeded demo proves this with:

```text
Birthday Classic 1 4 review
```

Meaning:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | 1 | 4 | review |

---

## Recommended Local Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
```

Then run the full verification sequence:

```powershell
python manage.py check
python manage.py test bakeops
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
python manage.py runserver
```

---

## Expected Command Results

### Django check

```powershell
python manage.py check
```

Expected:

```text
System check identified no issues (0 silenced).
```

### Test suite

```powershell
python manage.py test bakeops
```

Expected pattern:

```text
Found 37 test(s).
Ran 37 tests
OK
```

### Seed demo data

```powershell
python manage.py seed_demo_data --reset
```

Expected:

```text
BakeOps demo data seeded successfully.
Workspace: SweetCakes Bakery
Cakes: 4
Orders: 7
Ingredients: 8
Waste records: 4
```

### Build metrics

```powershell
python manage.py build_bakery_metrics
```

Expected:

```text
BakeOps bakery metrics built successfully.
Workspace: SweetCakes Bakery
Rows processed: 12
Metrics created: 1
Snapshots created: 21
Issues created: 12
```

### Export BI CSV pack

```powershell
python manage.py export_bi_csv
```

Expected:

```text
BakeOps BI CSV exports generated successfully.
Files generated: 11
Total rows exported: 52
```

---

## Pages to Review

After running:

```powershell
python manage.py runserver
```

Open these pages:

| Page | URL | What to Check |
|---|---|---|
| Main dashboard | `http://127.0.0.1:8000/analytics/` | Executive metrics, signature insight, data quality, export/governance visibility |
| Product profitability | `http://127.0.0.1:8000/analytics/products/` | Birthday Classic revenue rank #1 but waste-adjusted margin rank #4 |
| Ingredient risk | `http://127.0.0.1:8000/analytics/ingredients/` | Stock risk, reorder levels, near-expiry visibility |
| Waste analysis | `http://127.0.0.1:8000/analytics/waste/` | Waste cost and product waste impact |
| Occasion analytics | `http://127.0.0.1:8000/analytics/occasions/` | Birthday occasion demand signal |
| Customer analytics | `http://127.0.0.1:8000/analytics/customers/` | Maya Patel repeat-customer value |
| Data quality review | `http://127.0.0.1:8000/analytics/data-quality/` | 12 open data quality issues and suggested actions |
| Export centre | `http://127.0.0.1:8000/analytics/exports/` | 11-file BI export contract |

---

## Direct Route Verification

A reviewer can verify routes with:

```powershell
python manage.py shell -c "from django.urls import reverse; names=['analytics-dashboard','product-profitability','ingredient-risk','waste-analysis','occasion-analytics','customer-analytics','data-quality-review','export-centre']; [print(name, reverse('bakeops:'+name)) for name in names]"
```

Expected:

```text
analytics-dashboard /analytics/
product-profitability /analytics/products/
ingredient-risk /analytics/ingredients/
waste-analysis /analytics/waste/
occasion-analytics /analytics/occasions/
customer-analytics /analytics/customers/
data-quality-review /analytics/data-quality/
export-centre /analytics/exports/
```

---

## Direct Page Load Verification

```powershell
python manage.py shell -c "from django.test import Client, override_settings; c=Client(); paths=['/analytics/','/analytics/products/','/analytics/ingredients/','/analytics/waste/','/analytics/occasions/','/analytics/customers/','/analytics/data-quality/','/analytics/exports/'];
with override_settings(ALLOWED_HOSTS=['testserver','localhost','127.0.0.1']):
    [print(path, c.get(path).status_code) for path in paths]"
```

Expected:

```text
/analytics/ 200
/analytics/products/ 200
/analytics/ingredients/ 200
/analytics/waste/ 200
/analytics/occasions/ 200
/analytics/customers/ 200
/analytics/data-quality/ 200
/analytics/exports/ 200
```

---

## Signature Insight Verification

Run:

```powershell
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
```

Expected:

```text
Birthday Classic 1 4 review
```

This confirms the key platform insight is stored in the database, not only displayed in the UI.

---

## Metric Evidence Verification

Run:

```powershell
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot, DataQualityIssue, DailyBakeryMetric; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); metric=DailyBakeryMetric.objects.order_by('-metric_date').first(); print('Signature:', p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag); print('Metric:', metric.metric_date, metric.revenue, metric.waste_cost, metric.waste_adjusted_margin); print('Data quality issues:', DataQualityIssue.objects.count()); print('Open issues:', DataQualityIssue.objects.filter(status=DataQualityIssue.STATUS_OPEN).count())"
```

Expected pattern:

```text
Signature: Birthday Classic 1 4 review
Metric: 2026-04-26 727.00 37.99 476.80
Data quality issues: 12
Open issues: 12
```

---

## Export Files

The BI export command generates:

| File | Rows | Columns |
|---|---:|---:|
| `fact_orders.csv` | 7 | 16 |
| `fact_order_items.csv` | 7 | 11 |
| `fact_waste.csv` | 4 | 14 |
| `fact_production_batches.csv` | 4 | 15 |
| `dim_cake.csv` | 4 | 13 |
| `dim_ingredient.csv` | 8 | 10 |
| `dim_customer.csv` | 5 | 10 |
| `dim_occasion.csv` | 4 | 5 |
| `dim_collection.csv` | 4 | 7 |
| `daily_bakery_metrics.csv` | 1 | 13 |
| `product_performance_snapshot.csv` | 4 | 20 |

Generated CSV files are written to:

```text
exports/
```

They are intentionally ignored by Git because they are reproducible.

---

## Reviewer Documents

| Document | Purpose |
|---|---|
| `README.md` | Main project overview and setup path |
| `docs/REVIEWER_WALKTHROUGH.md` | This reviewer validation guide |
| `docs/METRIC_GOVERNANCE.md` | Metric build process, gold-layer models, run logs, and verification |
| `docs/LINEAGE.md` | Data lineage from seeded operational data to analytics pages and BI exports |
| `docs/V2_RELEASE_CHECKLIST.md` | Final V2 release checklist |
| `docs/DATA_MODEL_DRAFT.md` | Data model draft |

---

## Final V2 Verification Evidence

The final V2 hardening check confirms the project is ready to present as:

```text
V2 = Trusted
```

Latest verified test output pattern:

```text
Found 37 test(s).
Ran 37 tests
OK
```

Latest verified signature insight:

```text
Birthday Classic 1 4 review
```

Latest verified V2 pages:

```text
/analytics/
/analytics/products/
/analytics/ingredients/
/analytics/waste/
/analytics/occasions/
/analytics/customers/
/analytics/data-quality/
/analytics/exports/
```

Final release checklist:

```text
docs/V2_RELEASE_CHECKLIST.md
```

The export centre page is available at:

```text
/analytics/exports/
```

---

## What V2 Proves

BakeOps Intelligence V2 proves:

```markdown
- [x] operational bakery data can be seeded
- [x] repeatable metric builds create stored reporting snapshots
- [x] the dashboard reads from stored metrics
- [x] product profitability can change after waste adjustment
- [x] ingredient stock and expiry risk are visible
- [x] waste impact is explainable
- [x] occasion and customer patterns are visible
- [x] data quality issues are exposed
- [x] BI exports are available and documented
- [x] metric governance and lineage are documented
- [x] tests verify major routes, views, commands, and export parity
```

---

## Current Limitations

BakeOps Intelligence currently uses seeded demo data and documented commercial-readiness workflows.

It does not yet include:

```markdown
- [ ] external POS imports
- [ ] Shopify, Square, Stripe, or payment integrations
- [ ] live production scheduling integrations
- [ ] automated customer onboarding flows
- [ ] multi-tenant SaaS account management
- [ ] billing or subscriptions
- [ ] production SaaS deployment
- [ ] real customer usage
```

These are future concerns and should not be claimed as implemented.

---

## Final Reviewer Summary

BakeOps Intelligence is a trusted bakery operations analytics platform with a V3 commercial foundation, not a live paid SaaS product.

It is reviewer-ready because the core insight can be verified through:

```text
seeded data -> metric build -> gold-layer snapshots -> analytics pages -> BI exports -> tests -> documentation
```
