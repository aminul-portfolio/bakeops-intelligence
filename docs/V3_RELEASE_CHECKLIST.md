# BakeOps Intelligence — V3 Release Checklist

## Release Position

```text
V3 = Commercial foundation
```

BakeOps Intelligence V3 is complete when the project has a commercially credible product foundation with clear boundaries, verified analytics, release documentation, and no fake commercial claims.

---

## V3 Sprint Completion Record

```markdown
- [x] V3 Sprint 1 — Commercial positioning and product boundary
- [x] V3 Sprint 2 — Import readiness assessment and safe import design
- [x] V3 Sprint 3 — Demo/customer setup workflow foundation
- [x] V3 Sprint 4 — Commercial operations dashboard polish
- [x] V3 Sprint 5 — Beta-readiness documentation and deployment checklist
- [x] V3 Sprint 6 — Packaging/pricing strategy and commercial README polish
- [ ] V3 Sprint 7 — Final hardening, tests, and release checklist
```

---

## V3 Release Evidence

Before final V3 release, confirm:

```markdown
- [ ] `python manage.py check` passes
- [ ] `python manage.py test bakeops` passes
- [ ] `python manage.py seed_demo_data --reset` works
- [ ] `python manage.py build_bakery_metrics` works
- [ ] `python manage.py export_bi_csv` works
- [ ] `Birthday Classic 1 4 review` verifies
- [ ] all 8 V2/V3 analytics routes return HTTP 200
- [ ] README is updated
- [ ] CHANGELOG is updated
- [ ] V3 documentation set is complete
- [ ] working tree is clean after commit
```

---

## Expected Technical Evidence

Expected test evidence:

```text
Ran 37 tests
OK
```

Expected signature insight:

```text
Birthday Classic 1 4 review
```

Expected route evidence:

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

Expected BI export evidence:

```text
Files generated: 11
Total rows exported: 52
```

---

## V3 Documentation Checklist

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

## Implemented Capabilities

BakeOps V3 can honestly present these as implemented or documented:

| Capability | Status |
|---|---|
| Trusted analytics pages | Implemented |
| Gold-layer metric build | Implemented |
| Metric run logging | Implemented |
| Data quality issues | Implemented |
| BI-ready exports | Implemented |
| Signature insight | Implemented |
| Commercial product positioning | Documented |
| Commercial scope boundary | Documented |
| Import readiness | Documented |
| Import contract | Draft documented |
| Demo setup workflow | Documented |
| Customer setup foundation | Documented |
| Commercial dashboard polish | Implemented |
| Beta-readiness checklist | Documented |
| Deployment-readiness checklist | Documented |
| Packaging/pricing strategy | Documented |
| Commercial README polish | Documented |
| Final hardening evidence | Documented |
| Release checklist | Documented |

---

## Not Implemented Yet

The following must remain clearly marked as not implemented:

| Capability | Status |
|---|---|
| Import UI | Not implemented yet |
| CSV/Excel parser | Not implemented yet |
| Automated customer onboarding | Not implemented yet |
| Production deployment | Not claimed yet |
| Billing/subscriptions | Not implemented yet |
| Stripe/payment integration | Not implemented yet |
| POS integration | Not implemented yet |
| Shopify/Square integration | Not implemented yet |
| Real customer usage | Not claimed |
| Multi-tenant SaaS account management | Not implemented yet |

---

## Final V3 Release Statement

Safe release wording:

```text
BakeOps Intelligence V3 is a commercial foundation for bakery operations intelligence. It demonstrates how bakery operational records can be transformed into trusted analytics pages, waste-adjusted profitability insights, ingredient risk signals, data quality checks, action recommendations, and BI-ready exports.
```

Do not say:

```text
BakeOps is a live paid SaaS product.
```

```text
BakeOps is production deployed.
```

```text
BakeOps has real customer usage.
```

```text
BakeOps supports live POS/Shopify/Square integration.
```

```text
BakeOps has billing or subscriptions.
```

---

## Final Git Evidence

Final V3 Sprint 7 commit message should be:

```text
V3 Sprint 7: finalize commercial release hardening
```

Final expected Git state:

```text
nothing to commit, working tree clean
```

---

## Release Completion

V3 is complete only after:

```markdown
- [ ] all verification commands pass
- [ ] final V3 docs are committed
- [ ] Git working tree is clean
- [ ] latest commit is the Sprint 7 release commit
```
