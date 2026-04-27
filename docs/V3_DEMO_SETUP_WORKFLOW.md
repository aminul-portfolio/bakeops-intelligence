# BakeOps Intelligence — V3 Demo Setup Workflow

## Purpose

This document explains how the BakeOps Intelligence demo should be prepared, verified, and presented.

The goal is to make the project easier to review and demo without pretending the product has automated customer onboarding, live customer data, or production deployment.

---

## Demo Position

BakeOps Intelligence currently uses a controlled seeded demo dataset.

The seeded demo is not fake commercial usage.

It is a repeatable demonstration dataset used to prove the platform workflow:

```text
seed_demo_data
-> operational bakery records
-> build_bakery_metrics
-> gold-layer snapshots
-> trusted analytics pages
-> export_bi_csv
-> BI-ready exports
```

The demo should be described as:

```text
A realistic seeded bakery operations dataset for reviewer and product demonstration.
```

It should not be described as:

```text
Live customer data
Real business usage
Production bakery account
Automated commercial onboarding
POS-integrated data
```

---

## Demo User

The demo represents a realistic small bakery scenario.

The intended demo viewer is:

```text
A reviewer, hiring manager, product evaluator, or potential first bakery operator who wants to understand how BakeOps converts bakery records into operational insight.
```

The demo should help them understand:

- which products sell well
- which products remain profitable after waste
- where ingredients create stock or expiry risk
- how waste affects margin
- which occasions drive demand
- which customers show loyalty value
- which data issues need review
- how metrics can be exported for BI tools

---

## Demo Setup Commands

From a clean local environment, the recommended demo setup is:

```powershell
python manage.py check
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/analytics/
```

Recommended review path:

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

---

## Demo Verification Commands

Before presenting the demo, run:

```powershell
python manage.py check
python manage.py test bakeops
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; p=ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
```

Expected key output:

```text
Birthday Classic 1 4 review
```

This confirms the signature insight is preserved.

---

## Demo Storyline

The recommended demo storyline is:

```text
1. Start with the main analytics dashboard.
2. Explain that BakeOps is not just a cake catalogue.
3. Show that operational records feed a metric build pipeline.
4. Open product profitability.
5. Highlight Birthday Classic as revenue rank #1 but waste-adjusted margin rank #4.
6. Explain why this creates a review action.
7. Open ingredient risk.
8. Show how stock and expiry pressure affect operations.
9. Open waste analysis.
10. Show how waste cost reduces business confidence.
11. Open data quality.
12. Explain that BakeOps surfaces trust issues instead of hiding them.
13. Open exports.
14. Show how outputs can support BI/reporting workflows.
```

---

## Signature Demo Moment

The signature commercial proof point is:

```text
Birthday Classic 1 4 review
```

Meaning:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | 1 | 4 | review |

This proves:

```text
A best-selling bakery product can become weak after ingredient cost and waste are included.
```

The demo should preserve this insight across V3.

---

## Demo Readiness Checklist

Before using the demo, verify:

```markdown
- [ ] `python manage.py check` passes
- [ ] `python manage.py test bakeops` passes
- [ ] `python manage.py seed_demo_data --reset` works
- [ ] `python manage.py build_bakery_metrics` works
- [ ] `python manage.py export_bi_csv` works
- [ ] `/analytics/` loads
- [ ] `/analytics/products/` loads
- [ ] `/analytics/ingredients/` loads
- [ ] `/analytics/waste/` loads
- [ ] `/analytics/occasions/` loads
- [ ] `/analytics/customers/` loads
- [ ] `/analytics/data-quality/` loads
- [ ] `/analytics/exports/` loads
- [ ] `Birthday Classic 1 4 review` verifies
- [ ] BI export pack generates 11 files
- [ ] Data quality issues are visible
```

---

## Demo Claims Allowed

Safe claims:

```text
BakeOps uses seeded bakery operations data for a repeatable demo.
```

```text
BakeOps builds trusted analytics snapshots from operational records.
```

```text
BakeOps demonstrates product profitability, ingredient risk, waste impact, customer value, data quality, and BI export workflows.
```

```text
BakeOps is in V3 commercial-readiness planning.
```

```text
Import workflow and customer onboarding are planned but not implemented yet.
```

---

## Demo Claims Not Allowed

Do not claim:

```text
BakeOps is used by live bakery customers.
```

```text
BakeOps imports real customer files today.
```

```text
BakeOps is integrated with POS, Shopify, or Square.
```

```text
BakeOps has automated customer onboarding.
```

```text
BakeOps has billing or subscription management.
```

```text
BakeOps is production-deployed unless that deployment is separately verified.
```

---

## Demo-to-Customer Bridge

The seeded demo is useful because it models the kind of operational records a real bakery would eventually provide.

The bridge from demo to customer setup is:

```text
Seeded demo records
-> define required operational data
-> define import contracts
-> validate customer files
-> create operational records
-> rebuild trusted metrics
-> review analytics and data quality
```

This means the demo is not a dead-end sample.

It is a controlled proof of the future customer workflow.

---

## Sprint 3 Boundary Confirmation

This document defines the demo setup workflow.

It does not implement:

- customer onboarding
- upload screens
- workspace provisioning automation
- billing
- subscriptions
- external integrations
- live customer data import

It keeps V3 commercially honest.
