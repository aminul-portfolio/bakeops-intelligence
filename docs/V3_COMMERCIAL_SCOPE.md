# BakeOps Intelligence — V3 Commercial Scope

## Purpose

This document defines the commercial boundary for BakeOps Intelligence V3.

The goal is to make the project commercially credible without overclaiming features that are not implemented.

---

## Commercial Scope Statement

BakeOps Intelligence V3 is a commercial-readiness foundation for bakery operations intelligence.

It is intended to help bakery owners and operators understand product profitability, waste impact, ingredient risk, customer value, occasion demand, operational data quality, and BI-ready reporting outputs.

V3 should make the product easier to explain, demo, evaluate, and extend toward commercial usage.

It should not pretend to be a fully launched SaaS business.

---

## Current Product Truth

The current project has a trusted V2 analytics foundation.

It can:

- seed realistic bakery demo data
- build gold-layer analytics metrics
- log metric build runs
- generate product performance snapshots
- surface ingredient risk
- analyse waste impact
- review occasion demand
- summarise customer loyalty value
- show data quality issues
- export BI-ready CSV files
- verify outputs through tests and commands

The current project does not yet support:

- uploaded customer files
- external POS data syncing
- Shopify or Square integrations
- payment collection
- subscriptions
- commercial account provisioning
- production deployment claims
- real customer onboarding
- live customer usage evidence

---

## Scope Categories

### Implemented

These can be described as built and working:

| Capability | Status |
|---|---|
| Seeded bakery operations data | Implemented |
| Metric build pipeline | Implemented |
| Gold-layer snapshots | Implemented |
| Data quality issues | Implemented |
| Metric build logs | Implemented |
| Trusted analytics pages | Implemented |
| BI CSV exports | Implemented |
| Reviewer walkthrough | Implemented |
| Metric governance documentation | Implemented |
| Lineage documentation | Implemented |
| Test coverage | Implemented |

---

### V3 Candidate

These are reasonable V3 candidates if implemented carefully:

| Capability | Reason |
|---|---|
| Commercial positioning docs | Clarifies product value |
| Commercial scope docs | Prevents overclaiming |
| Import readiness assessment | Prepares realistic data onboarding |
| Import file contract design | Defines expected file structure before building import code |
| Demo setup workflow | Helps reviewers and potential users understand setup |
| Customer setup notes | Explains first-user journey without fake onboarding |
| Beta-readiness checklist | Makes commercial gaps visible |
| Deployment readiness checklist | Separates local demo from production readiness |
| Commercial README polish | Improves product communication |

---

### V4 Candidate

These should likely wait until after V3 unless there is a strong technical reason:

| Capability | Reason to Delay |
|---|---|
| Real import UI | Needs import contract first |
| Role-aware permissions | Needs clear user model and workflow requirement |
| Multi-workspace commercial workflows | Needs careful permission and data isolation design |
| Production deployment | Needs deployment target and environment strategy |
| Payment integration | Not needed before product workflow is validated |
| Subscription plans | Strategy can be documented before code |
| External POS integration | Requires real API/data contract |
| Shopify/Square integration | Requires real integration design and test strategy |

---

### Out of Scope Unless Built Honestly

These must not be claimed unless genuinely implemented and verified:

| Claim | Allowed Wording |
|---|---|
| Live POS integration | Planned / not implemented yet |
| Shopify integration | Planned / not implemented yet |
| Square integration | Planned / not implemented yet |
| Stripe payments | Planned / not implemented yet |
| SaaS subscriptions | Planned / not implemented yet |
| Live customer usage | Not claimed |
| Production deployment | Unknown unless verified |
| Multi-tenant SaaS | Not claimed unless implemented |
| Automated onboarding | Planned / not implemented yet |

---

## Safe Commercial Wording

Use wording like:

```text
Commercial-ready product foundation
```

```text
Commercial-readiness phase
```

```text
Designed to support future import and onboarding workflows
```

```text
Prepared for beta-readiness review
```

```text
V3 candidate
```

```text
Not implemented yet
```

```text
Planned commercial extension
```

---

## Wording to Avoid

Avoid wording like:

```text
Live SaaS platform
```

```text
Integrated with Shopify/Square/POS
```

```text
Accepts payments
```

```text
Used by real bakeries
```

```text
Production-ready multi-tenant platform
```

```text
Automated commercial onboarding
```

```text
Subscription-ready billing system
```

unless those features are genuinely implemented, tested, and documented.

---

## Recommended V3 Sprint Structure

Use seven sprints:

| Sprint | Theme | Boundary |
|---|---|---|
| V3 Sprint 1 | Commercial positioning and product boundary | Documentation only |
| V3 Sprint 2 | Import readiness assessment and safe import design | Assess before building |
| V3 Sprint 3 | Demo/customer setup workflow foundation | Clarify onboarding path |
| V3 Sprint 4 | Commercial operations dashboard polish | Improve value explanation |
| V3 Sprint 5 | Beta-readiness documentation and deployment checklist | Document commercial gaps |
| V3 Sprint 6 | Packaging/pricing evidence and commercial README polish | Strategy only unless built |
| V3 Sprint 7 | Final V3 hardening, tests, and release checklist | Verify and close |

---

## Sprint 1 Acceptance Criteria

V3 Sprint 1 is complete only when:

```markdown
- [ ] `docs/V3_PRODUCT_STRATEGY.md` exists
- [ ] `docs/V3_COMMERCIAL_SCOPE.md` exists
- [ ] README references both V3 documents
- [ ] README keeps V2 evidence intact
- [ ] CHANGELOG records the Sprint 1 update
- [ ] No model files changed
- [ ] No migrations added
- [ ] No fake commercial claims added
- [ ] `python manage.py check` passes
- [ ] `python manage.py test bakeops` passes
- [ ] Signature insight still returns `Birthday Classic 1 4 review`
```

---

## Protected V2 Evidence

The following V2 evidence must remain protected during V3:

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

If future V3 work changes these numbers, the change must be intentional, explained, and verified.

---

## Final Scope Rule

The product can be commercially positioned before it is commercially launched.

Therefore, V3 should focus on making BakeOps Intelligence:

```text
understandable
credible
demo-ready
beta-aware
commercially scoped
technically honest
```

not artificially complete.
