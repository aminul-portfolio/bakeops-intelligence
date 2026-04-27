# BakeOps Intelligence — V3 Product Strategy

## Version Position

```text
V1 = Works
V2 = Trusted
V3 = Commercial
```

BakeOps Intelligence V3 is the commercial-readiness phase.

V1 proved that a working bakery analytics dashboard could be built from seeded operational data.

V2 proved that the analytics layer could be trusted through stored gold-layer metrics, repeatable metric builds, data quality visibility, metric governance, lineage documentation, BI-ready exports, tests, and reviewer verification.

V3 should now turn that trusted analytics foundation into a commercially credible product direction without pretending that unbuilt features already exist.

---

## Commercial Definition

BakeOps Intelligence is a bakery operations intelligence platform for small and growing bakery businesses that need clearer visibility into product profitability, waste impact, ingredient risk, customer value, occasion demand, operational trust issues, and BI-ready reporting outputs.

It is not a generic bakery website.

It is not only a product catalogue.

It is not a fake SaaS product.

It is a decision-intelligence layer that converts bakery operational records into practical business insight.

---

## First Realistic User

The first realistic user is:

```text
An owner-operator, bakery manager, or operations lead at a small bakery that already takes customer orders and wants better visibility into revenue, ingredient cost, waste, stock pressure, customer value, and product profitability.
```

This user may not need a complex enterprise platform first.

They need clear answers to practical questions:

- Which products generate revenue?
- Which products stay profitable after ingredient cost and waste?
- Which products need review?
- Which ingredients create stock or expiry risk?
- Which waste patterns are reducing margin?
- Which occasions drive demand?
- Which customers show repeat value?
- Which records need correction before decisions can be trusted?
- Which data can be exported for reporting or BI tools?

---

## Core Commercial Problem

Bakery owners often know which products sell well, but they may not clearly know which products remain strong after ingredient cost, production waste, stock pressure, and operational data quality issues are considered.

BakeOps Intelligence addresses this problem by connecting operational bakery records to stored analytics outputs.

The core commercial problem is:

```text
Revenue alone can mislead bakery decisions when ingredient cost, waste, production records, stock risk, and data quality issues are not visible.
```

---

## Signature Commercial Insight

The V2 proof point remains central to V3:

```text
Birthday Classic 1 4 review
```

Meaning:

| Product | Revenue Rank | Waste-adjusted Margin Rank | Action |
|---|---:|---:|---|
| Birthday Classic | 1 | 4 | review |

This proves the central business idea:

```text
A best-selling bakery product can become weak after ingredient cost and waste are included.
```

This insight should remain protected throughout V3.

---

## What Is Already Implemented

V2 already includes:

- customer-facing `cakes` catalogue app
- separate `bakeops` analytics app
- realistic seeded bakery operations dataset
- workspace and staff context
- customers and loyalty records
- occasions and delivery slots
- orders and order items
- suppliers, ingredients, and ingredient lots
- recipes and recipe lines
- production batches and batch allocations
- waste records
- cake reviews
- gold-layer metric snapshots
- repeatable metric build command
- metric build run logging
- data quality issue generation
- product profitability page
- ingredient risk page
- waste analysis page
- occasion analytics page
- customer analytics page
- data quality review page
- export centre
- BI-ready CSV export pack
- metric governance documentation
- lineage documentation
- reviewer walkthrough
- V2 release checklist
- automated tests for key commands, services, views, and export parity

---

## What Is Not Implemented Yet

The following are not implemented yet and must not be presented as live features:

| Area | Current Status |
|---|---|
| File import workflow | Not implemented yet |
| Customer onboarding flow | Not implemented yet |
| Commercial workspace setup | V3 candidate |
| External POS integration | Not implemented yet |
| Shopify integration | Not implemented yet |
| Square integration | Not implemented yet |
| Stripe/payment integration | Not implemented yet |
| Billing/subscriptions | Not implemented yet |
| Multi-tenant SaaS permissions | Not implemented yet |
| Production deployment | Unknown unless separately verified |
| Real customer data | Not included |
| Live business usage | Not claimed |

---

## V3 Commercial Direction

V3 should focus on commercially credible foundations rather than exaggerated SaaS claims.

Recommended V3 direction:

1. Define commercial product positioning.
2. Assess import readiness before building import features.
3. Design a safe import workflow for realistic bakery records.
4. Improve demo/customer setup clarity.
5. Strengthen commercial dashboard language and operating workflow.
6. Add beta-readiness and deployment documentation.
7. Explain packaging/pricing only as product strategy, not as implemented billing.
8. Finalize V3 release evidence through tests, verification commands, and clean Git history.

---

## V3 Product Boundary

V3 should build or document foundations that make BakeOps commercially understandable.

V3 should not attempt to become a full enterprise SaaS product unless the code genuinely supports that claim.

The safest commercial boundary is:

```text
Commercial-ready product foundation for bakery operations intelligence.
```

This means the platform can be explained, reviewed, demoed, and extended toward commercial usage, but it should not claim to already support paid live customers, automated payment plans, external POS syncing, or production-grade multi-tenant SaaS operations.

---

## Commercial Credibility Evidence From V2

V3 commercial positioning is supported by V2 evidence:

| Evidence | Why It Matters Commercially |
|---|---|
| 37 passing tests | Shows the analytics layer has regression protection |
| 8 trusted analytics routes | Shows meaningful product surface area |
| Metric build command | Shows repeatable analytics generation |
| BakeryMetricRunLog | Shows metric build auditability |
| DataQualityIssue records | Shows the platform does not hide trust problems |
| 11-file BI export pack | Shows reporting and external analysis readiness |
| Signature insight | Shows business value beyond simple revenue tracking |
| Governance docs | Shows methodology is explainable |
| Lineage docs | Shows data flow is inspectable |
| Clean release checklist | Shows controlled delivery discipline |

---

## Out of Scope for V3 Sprint 1

This sprint does not include:

- model changes
- migrations
- new analytics calculations
- import UI
- billing UI
- login/role refactor
- external integrations
- deployment setup
- pricing pages
- subscription logic
- fake customer claims
- fake live data claims

---

## V3 Sprint 1 Success Criteria

V3 Sprint 1 is complete when:

```markdown
- [ ] Commercial product definition is documented
- [ ] First realistic user is documented
- [ ] Commercial problem is documented
- [ ] Implemented vs not implemented status is clear
- [ ] V2 commercial evidence is documented
- [ ] Out-of-scope items are documented
- [ ] README points to the V3 strategy and scope docs
- [ ] Changelog records the Sprint 1 documentation update
- [ ] Existing tests still pass
- [ ] Signature insight still verifies
- [ ] Git working tree is clean after commit
```
