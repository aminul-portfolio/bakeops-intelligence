# BakeOps Intelligence - V2 Release Checklist

## Release Name

```text
BakeOps Intelligence V2 = Trusted
```

## Purpose

This checklist verifies that BakeOps Intelligence V2 is ready to be presented as a trusted analytics and decision-support portfolio project.

V2 does not claim to be a commercial SaaS product yet. It focuses on trust, metric lineage, deeper analytics pages, data quality visibility, export contracts, documentation, and reviewer evidence.

---

## Version Scope

```text
V1 = Works
V2 = Trusted
V3 = Commercial
```

V2 is complete when the platform can prove:

```markdown
- [x] operational bakery data can be seeded
- [x] gold-layer metrics can be built
- [x] analytics pages read from stored data
- [x] data quality issues are visible
- [x] BI exports are available
- [x] metric governance is documented
- [x] lineage is documented
- [x] tests pass
- [x] generated files are not accidentally committed
```

---

## Core Commands Verified

| Command | Expected Result | Status |
|---|---|---|
| `python manage.py check` | Django system check passes | Passed |
| `python manage.py test bakeops` | BakeOps tests pass | Passed |
| `python manage.py seed_demo_data --reset` | Demo bakery data is recreated | Passed |
| `python manage.py build_bakery_metrics` | Gold-layer metrics are built | Passed |
| `python manage.py export_bi_csv` | BI CSV export pack is generated | Passed |

Latest verified test result:

```text
Found 37 test(s).
Ran 37 tests
OK
```

Latest verified export result:

```text
Files generated: 11
Total rows exported: 52
```

---

## V2 Routes Verified

| Page | URL | Status |
|---|---|---|
| Main analytics dashboard | `/analytics/` | Verified |
| Product profitability | `/analytics/products/` | Verified |
| Ingredient risk | `/analytics/ingredients/` | Verified |
| Waste analysis | `/analytics/waste/` | Verified |
| Occasion analytics | `/analytics/occasions/` | Verified |
| Customer analytics | `/analytics/customers/` | Verified |
| Data quality review | `/analytics/data-quality/` | Verified |
| Export centre | `/analytics/exports/` | Verified |

Expected route output:

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

## Page Load Verification

All V2 pages should return HTTP 200:

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

BakeOps Intelligence proves:

```text
A best-selling bakery product can become weak after ingredient cost and waste are included.
```

Verified database output:

```text
Birthday Classic 1 4 review
```

Meaning:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | 1 | 4 | review |

This confirms that Birthday Classic sells the most, but waste-adjusted profitability reveals it needs review.

---

## Metric Evidence Verified

Latest metric evidence:

| Metric | Value |
|---|---:|
| Revenue | 727.00 |
| Waste cost | 37.99 |
| Waste-adjusted margin | 476.80 |
| Data quality issues | 12 |
| Open issues | 12 |

---

## V2 Trusted Analytics Pages

| Sprint | Page | URL | Evidence |
|---|---|---|---|
| Sprint 1 | Product profitability | `/analytics/products/` | Birthday Classic margin-rank inversion |
| Sprint 2 | Ingredient risk | `/analytics/ingredients/` | Stock risk and near-expiry visibility |
| Sprint 3 | Waste analysis | `/analytics/waste/` | Waste impact on margin |
| Sprint 4 | Occasion analytics | `/analytics/occasions/` | Birthday occasion demand signal |
| Sprint 4 | Customer analytics | `/analytics/customers/` | Maya Patel repeat-customer value |
| Sprint 5 | Data quality review | `/analytics/data-quality/` | 12 open data quality issues |
| Sprint 6 | Export centre | `/analytics/exports/` | 11-file BI export contract |
| Sprint 7 | Governance and lineage docs | `docs/` | Metric governance and lineage documented |

---

## BI Export Contract Verified

The export command generates 11 files:

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

Generated CSV files are ignored by Git and should not be committed.

---

## Documentation Verified

| Document | Purpose | Status |
|---|---|---|
| `README.md` | Main project overview and verification path | Updated |
| `docs/REVIEWER_WALKTHROUGH.md` | Reviewer walkthrough | Updated |
| `docs/DATA_MODEL_DRAFT.md` | Data model draft | Present |
| `docs/METRIC_GOVERNANCE.md` | Metric build, governance, run logging, verification | Created |
| `docs/LINEAGE.md` | Data lineage from seed to exports | Created |
| `docs/V2_RELEASE_CHECKLIST.md` | Final V2 release checklist | Created |

---

## Git Hygiene Checklist

Before final V2 commit:

```markdown
- [ ] `git status` reviewed
- [ ] no generated CSV exports staged
- [ ] no `.env` staged
- [ ] no `.venv/` staged
- [ ] no `db.sqlite3` staged
- [ ] no `__pycache__/` staged
- [ ] no model changes
- [ ] no migration changes
- [ ] no `cakes` app changes
- [ ] final tests passed
```

Expected safe ignored files include:

```text
.env
.venv/
db.sqlite3
exports/*.csv
media/
__pycache__/
```

---

## Current Limitations

V2 is a trusted analytics demo. It does not yet include:

```markdown
- [ ] external POS imports
- [ ] Shopify, Square, Stripe, or payment integrations
- [ ] live production scheduling integrations
- [ ] user onboarding flows
- [ ] multi-tenant SaaS permissions
- [ ] billing or subscriptions
- [ ] commercial workspace setup
```

These are V3 concerns.

---

## Final V2 Release Decision

BakeOps Intelligence V2 can be marked as complete when:

```markdown
- [x] all tests pass
- [x] all routes resolve
- [x] all pages return HTTP 200
- [x] signature insight verifies from the database
- [x] data quality evidence verifies from the database
- [x] export pack generates successfully
- [x] governance docs exist
- [x] lineage docs exist
- [x] generated files are ignored
- [x] Git working tree is clean after final commit
```

## Release Summary

BakeOps Intelligence V2 is ready to be positioned as:

```text
A trusted bakery operations analytics platform that turns operational data into inspectable metrics, data quality evidence, BI-ready exports, and decision-support pages.
```