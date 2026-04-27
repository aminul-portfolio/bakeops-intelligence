# BakeOps Intelligence — V3 Final Hardening

## Purpose

This document defines the final V3 hardening checks for BakeOps Intelligence.

The goal is to confirm that V3 remains commercially credible, technically honest, test-verified, and ready for release documentation.

---

## V3 Final Position

```text
V1 = Works
V2 = Trusted
V3 = Commercial foundation
```

V3 has focused on commercial readiness, not fake commercial completion.

It improves the project through:

- commercial product positioning
- commercial scope boundaries
- import readiness assessment
- draft import contract
- demo setup workflow
- first-customer setup foundation
- premium commercial operations dashboard polish
- beta-readiness documentation
- deployment-readiness checklist
- packaging/pricing strategy
- commercial README polish
- final hardening evidence
- release checklist documentation

---

## V3 Hardening Principle

Final hardening must confirm:

```text
The project is stronger, clearer, and more commercially credible without pretending unbuilt features exist.
```

Sprint 7 should verify:

- tests pass
- Django checks pass
- signature insight still works
- V3 docs exist
- README references V3 docs
- CHANGELOG records V3 progress
- no accidental model/migration changes exist
- no fake production, billing, POS, Shopify, Square, or live customer claims were added

---

## Protected V2 Evidence

The following V2 evidence must remain protected:

```text
37 tests passing
8 trusted analytics pages
Birthday Classic 1 4 review
Revenue 727.00
Waste cost 37.99
Waste-adjusted margin 476.80
12 data quality issues
11 BI export files
52 exported rows
```

If any of these change in future work, the change must be intentional, explained, and verified.

---

## V3 Documentation Coverage

V3 should include:

```markdown
- [ ] `docs/V3_PRODUCT_STRATEGY.md`
- [ ] `docs/V3_COMMERCIAL_SCOPE.md`
- [ ] `docs/V3_IMPORT_READINESS.md`
- [ ] `docs/V3_IMPORT_CONTRACT.md`
- [ ] `docs/V3_DEMO_SETUP_WORKFLOW.md`
- [ ] `docs/V3_CUSTOMER_SETUP_FOUNDATION.md`
- [ ] `docs/V3_OPERATIONS_DASHBOARD_POLISH.md`
- [ ] `docs/V3_BETA_READINESS.md`
- [ ] `docs/V3_DEPLOYMENT_READINESS_CHECKLIST.md`
- [ ] `docs/V3_PACKAGING_PRICING_STRATEGY.md`
- [ ] `docs/V3_COMMERCIAL_README_POLISH.md`
- [ ] `docs/V3_FINAL_HARDENING.md`
- [ ] `docs/V3_RELEASE_CHECKLIST.md`
```

---

## Technical Verification Commands

Run:

```powershell
python manage.py check
python manage.py test bakeops
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
python manage.py export_bi_csv
```

Expected evidence:

```text
System check identified no issues (0 silenced).
Ran 37 tests
OK
BakeOps demo data seeded successfully.
BakeOps bakery metrics built successfully.
BakeOps BI CSV exports generated successfully.
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

---

## Route Verification

The following pages should return HTTP 200:

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

Django's test client uses the host `testserver`. If `testserver` is not in `ALLOWED_HOSTS`, route checks can return `400` even when the routes themselves are working. To avoid changing real settings only for this check, use `override_settings`.

Suggested route check command:

```powershell
python manage.py shell -c "from django.test import Client, override_settings; routes=['/analytics/','/analytics/products/','/analytics/ingredients/','/analytics/waste/','/analytics/occasions/','/analytics/customers/','/analytics/data-quality/','/analytics/exports/']; c=Client(); ctx=override_settings(ALLOWED_HOSTS=['testserver','localhost','127.0.0.1']); ctx.enable(); [print(r, c.get(r).status_code) for r in routes]; ctx.disable()"
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

## Final Commercial Honesty Check

V3 may claim:

```text
Commercial foundation
```

```text
Seeded operational demo data
```

```text
Trusted metric snapshots
```

```text
Import readiness documented
```

```text
Beta/deployment readiness documented
```

```text
Packaging/pricing strategy documented
```

V3 must not claim:

```text
Live customer usage
```

```text
Production deployment
```

```text
Paid subscriptions
```

```text
Stripe billing
```

```text
POS integration
```

```text
Shopify/Square integration
```

```text
Automated onboarding
```

unless those are genuinely implemented and verified.

---

## Final Hardening Acceptance Criteria

```markdown
- [ ] Django check passes
- [ ] 37 BakeOps tests pass
- [ ] Demo seed command works
- [ ] Metric build command works
- [ ] BI export command works
- [ ] Signature insight returns `Birthday Classic 1 4 review`
- [ ] All 8 trusted analytics routes return HTTP 200
- [ ] V3 documentation set is complete
- [ ] README references final V3 release docs
- [ ] CHANGELOG records Sprint 7
- [ ] No model files changed
- [ ] No migrations added
- [ ] No fake commercial claims added
- [ ] Git working tree is clean after commit
```

---

## Boundary Confirmation

This document does not implement new features.

It finalizes V3 hardening evidence and release readiness documentation.
