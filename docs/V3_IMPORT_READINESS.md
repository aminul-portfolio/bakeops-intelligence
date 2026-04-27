# BakeOps Intelligence — V3 Import Readiness Assessment

## Purpose

This document assesses how BakeOps Intelligence can safely move from seeded demo data toward realistic bakery business data imports.

The goal is not to build import functionality immediately.

The goal is to define a safe import foundation before writing import code.

---

## Current Data Position

BakeOps Intelligence V2 already has a trusted seeded operational dataset.

The current data foundation includes:

- bakery workspace
- staff context
- customers
- loyalty accounts
- occasions
- delivery slots
- orders
- order items
- suppliers
- ingredients
- ingredient lots
- recipes
- recipe lines
- production batches
- production batch lines
- batch allocations
- waste records
- cake reviews
- gold-layer analytics snapshots
- metric build logs
- data quality issues
- BI-ready exports

This is enough to prove the analytics workflow.

V3 import readiness should define how a real bakery could eventually provide similar records safely.

---

## Commercial Import Problem

A bakery may already have useful data in spreadsheets, order systems, POS exports, production notes, waste logs, ingredient stock sheets, or customer lists.

However, importing data directly into analytics models without validation can damage trust.

The commercial import problem is:

```text
BakeOps needs a safe path from messy bakery business records to trusted operational models before analytics can be rebuilt.
```

---

## Import Design Principle

BakeOps should not import directly into dashboard metrics.

The correct flow is:

```text
source files
-> staging validation
-> operational records
-> metric build command
-> gold-layer snapshots
-> trusted analytics pages
-> BI-ready exports
```

This preserves the V2 trust model.

The dashboard should remain a consumer of trusted records, not the first place where imported data is transformed.

---

## Safe First Import Candidates

The safest first import candidates are lower-risk reference and operational tables.

| Import Area | Priority | Reason |
|---|---:|---|
| Customers | High | Useful, relatively stable, simple structure |
| Occasions | High | Small reference table, low risk |
| Ingredients | High | Needed for cost and stock visibility |
| Suppliers | Medium | Useful for ingredient traceability |
| Orders | Medium | Valuable, but requires careful customer/date/status validation |
| Order items | Medium | Valuable, but depends on valid orders, cakes, and variants |
| Waste records | Medium | Important for margin insight, but needs product/reason validation |
| Ingredient lots | Medium | Important for expiry/stock risk, but needs ingredient linkage |
| Recipes | Later | High business value but requires strong product and ingredient mapping |
| Production batches | Later | More complex due to batch allocation and production timing |
| Batch allocations | Later | Requires valid orders, products, and batches |
| Reviews | Later | Useful but not essential for first import readiness |

---

## Import Areas That Should Wait

These areas should not be the first V3 import build target:

| Area | Reason to Delay |
|---|---|
| Recipes | Requires accurate ingredient quantities and units |
| Production batches | Requires production workflow consistency |
| Batch allocations | Depends on orders, batches, and products |
| Ingredient lots | Needs expiry, stock, supplier, and unit consistency |
| External POS integration | Requires real API contract and test data |
| Shopify/Square integration | Requires real integration design |
| Payments | Not part of analytics import foundation |
| Subscriptions/billing | Commercial packaging concern, not import readiness |

---

## Required Validation Categories

Before any import is built, BakeOps should define validation checks.

### File-Level Validation

- file type is accepted
- required columns exist
- duplicate columns are rejected
- empty files are rejected
- encoding issues are detected
- row count is reported
- import date/time is recorded

### Row-Level Validation

- required values are present
- dates are valid
- numeric fields are valid
- money fields are non-negative where appropriate
- quantities are valid
- status values match allowed choices
- duplicate business keys are detected
- unknown references are reported

### Relationship Validation

- order item belongs to an existing order
- order belongs to an existing customer or guest rule
- ingredient lot belongs to an existing ingredient
- recipe line belongs to an existing recipe and ingredient
- waste record references a known product or ingredient where required
- production batch allocation references a valid order item

### Trust Validation

- imported records should not silently overwrite trusted records
- rejected rows should be reported
- partial imports should be clearly marked
- import summary should show created, skipped, rejected, and warning counts
- every import should be auditable

---

## First Import Workflow Candidate

The safest future workflow is:

```text
1. Upload source file
2. Validate schema
3. Preview detected rows
4. Show validation errors and warnings
5. Confirm import
6. Create/update operational records
7. Rebuild bakery metrics
8. Review data quality page
9. Review analytics pages
10. Export BI files if needed
```

This workflow should be implemented only after the file contracts are defined.

---

## Import Source Types

Potential source types:

| Source | V3 Status |
|---|---|
| CSV files | Best first candidate |
| Excel files | Good second candidate |
| Manual setup form | V3 candidate |
| POS export file | V4 candidate |
| Shopify API | V4+ candidate |
| Square API | V4+ candidate |
| Payment processor data | Out of scope for import readiness |

---

## Recommended First Import Scope

The safest first technical import scope later would be:

```text
customers.csv
ingredients.csv
orders.csv
order_items.csv
waste_records.csv
```

This gives enough data to rebuild useful analytics without forcing the full production workflow immediately.

---

## Import Readiness Risk Assessment

| Risk | Level | Mitigation |
|---|---|---|
| Incorrect product mapping | High | Require known cake/product keys before import |
| Bad money values | High | Validate decimal fields and reject invalid rows |
| Broken order/order item relationship | High | Import orders before order items |
| Missing customer data | Medium | Allow guest customer rules only if documented |
| Unit mismatch for ingredients | High | Define accepted units before import |
| Duplicate records | High | Use business keys and duplicate detection |
| Partial import confusion | Medium | Show summary and rejected-row report |
| Fake integration claims | High | Mark external integrations as planned only |

---

## Recommended V3 Decision

V3 Sprint 2 should not build import code yet.

It should produce:

```markdown
[x] Import readiness assessment
[x] Import contract design
[x] Clear first import candidates
[x] Validation categories
[x] Future import workflow
[x] Out-of-scope integration claims
```

This prepares the platform for commercial onboarding without damaging V2 trust.

---

## Sprint 2 Success Criteria

V3 Sprint 2 is complete when:

```markdown
- [ ] Import readiness document exists
- [ ] Import contract document exists
- [ ] README references the import readiness docs
- [ ] CHANGELOG records Sprint 2
- [ ] No model files changed
- [ ] No migrations added
- [ ] No import code added yet
- [ ] `python manage.py check` passes
- [ ] `python manage.py test bakeops` passes
- [ ] Signature insight still returns `Birthday Classic 1 4 review`
```
