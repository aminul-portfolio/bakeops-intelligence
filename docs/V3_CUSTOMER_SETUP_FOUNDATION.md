# BakeOps Intelligence — V3 Customer Setup Foundation

## Purpose

This document defines a realistic first-customer setup foundation for BakeOps Intelligence.

The goal is to explain how a bakery could eventually move from demo mode into a customer-specific setup without claiming that automated onboarding is already implemented.

---

## Customer Setup Position

BakeOps Intelligence V3 should be described as a commercial-ready product foundation, not a fully launched SaaS onboarding system.

The customer setup workflow is currently a planned operating model.

It is not yet an implemented automated feature.

---

## First Customer Profile

The realistic first customer is:

```text
A small or growing bakery with existing product, order, ingredient, waste, and customer records stored in spreadsheets, POS exports, order logs, or manual operational records.
```

The first customer likely needs:

- product profitability visibility
- waste-adjusted margin analysis
- ingredient stock and expiry risk visibility
- customer and loyalty reporting
- occasion demand analysis
- data quality issue review
- BI-ready exports
- practical action recommendations

They may not need:

- full enterprise multi-tenant SaaS
- complex role permissions on day one
- payment subscriptions on day one
- live POS integration on day one
- Shopify or Square API integration on day one

---

## Manual First-Customer Setup Model

A realistic early setup can be manual and controlled.

Suggested workflow:

```text
1. Create or identify the bakery workspace.
2. Collect sample customer/product/order/ingredient/waste records.
3. Map customer records to the BakeOps import contract.
4. Validate file structure and required columns.
5. Resolve missing references and duplicate records.
6. Load operational records through a future controlled import process.
7. Run the metric build command.
8. Review data quality issues.
9. Review analytics pages.
10. Export BI files if needed.
11. Document customer-specific setup notes.
```

This workflow is not fully automated yet.

It defines the operating model for future commercial onboarding.

---

## Setup Data Needed

A first customer setup should ideally collect:

| Data Area | Example Records | Priority |
|---|---|---:|
| Customers | customer name, contact, postcode, active status | High |
| Products | cake/product name, category, price, variant | High |
| Ingredients | ingredient name, unit, unit cost, reorder level | High |
| Orders | order date, customer, status, total value | High |
| Order items | product, quantity, unit price, line total | High |
| Waste records | waste date, product/ingredient, reason, estimated cost | High |
| Occasions | birthday, wedding, corporate, seasonal | Medium |
| Suppliers | supplier name, ingredient link | Medium |
| Ingredient lots | expiry date, quantity, received date | Medium |
| Recipes | product-to-ingredient mapping | Later |
| Production batches | batch date, product, quantity | Later |
| Batch allocations | batch-to-order relationships | Later |

---

## First Setup Should Prioritise

The first setup should prioritise data that proves business value quickly:

```text
customers
ingredients
orders
order_items
waste_records
```

This aligns with Sprint 2 import readiness.

These records can support:

- revenue visibility
- product ranking
- waste-adjusted margin
- customer value
- data quality checks
- BI exports

---

## Customer Setup Validation

Before customer data is accepted, BakeOps should validate:

```markdown
- [ ] required files are provided
- [ ] required columns exist
- [ ] dates are valid
- [ ] money values are valid
- [ ] quantities are valid
- [ ] product names can be mapped
- [ ] ingredient names can be mapped
- [ ] order references are unique
- [ ] order items link to valid orders
- [ ] duplicate business keys are detected
- [ ] rejected rows are reported
- [ ] warning rows are explained
```

This protects the trust model created in V2.

---

## Setup Output

A successful first-customer setup should produce:

| Output | Purpose |
|---|---|
| Workspace setup summary | Confirms target bakery context |
| Import validation summary | Shows accepted, rejected, and warning rows |
| Metric build run log | Confirms analytics were rebuilt |
| Data quality issue list | Shows operational trust gaps |
| Product performance snapshots | Shows revenue and margin ranking |
| Waste analysis | Shows margin impact of waste |
| Ingredient risk analysis | Shows stock/expiry concerns |
| BI export pack | Supports external reporting |
| Customer setup notes | Captures setup assumptions and limitations |

---

## Role-Aware Workflow Candidate

Role-aware workflows may be useful later, but should not be overbuilt in Sprint 3.

Potential future roles:

| Role | Possible Need |
|---|---|
| Owner | Revenue, margin, waste, action recommendations |
| Bakery manager | Production pressure, stock risk, operational issues |
| Finance/admin | BI exports, customer value, margin reporting |
| Staff/operator | Data correction, order/waste entry support |

Current V3 status:

```text
Role-aware workflow is a candidate, not implemented yet.
```

---

## Customer Setup Honesty Rules

Allowed wording:

```text
BakeOps defines a first-customer setup workflow.
```

```text
BakeOps can be prepared for customer-specific data onboarding.
```

```text
The current version uses seeded demo data.
```

```text
Import contracts and setup workflows are documented for future implementation.
```

Not allowed:

```text
BakeOps has automated customer onboarding.
```

```text
BakeOps provisions live customer accounts.
```

```text
BakeOps imports customer files today.
```

```text
BakeOps supports paid subscriptions.
```

```text
BakeOps is already used by real bakery customers.
```

---

## First-Customer Setup Checklist

```markdown
- [ ] Confirm bakery name and operating model
- [ ] Confirm product/cake catalogue
- [ ] Confirm ingredient list and units
- [ ] Confirm customer/order records available
- [ ] Confirm waste records available
- [ ] Map data to import contract
- [ ] Identify missing required fields
- [ ] Identify duplicate records
- [ ] Run future validation workflow
- [ ] Load operational records through a controlled future import process
- [ ] Run `build_bakery_metrics`
- [ ] Review `/analytics/data-quality/`
- [ ] Review `/analytics/products/`
- [ ] Review `/analytics/ingredients/`
- [ ] Review `/analytics/waste/`
- [ ] Generate BI exports
- [ ] Document assumptions and limitations
```

---

## Commercial Value of Setup Workflow

A clear setup workflow makes BakeOps more credible because it shows:

- the product is not just a static demo
- the seeded data maps to a future customer onboarding path
- customer data must be validated before analytics are trusted
- commercial readiness depends on evidence, not claims
- future import implementation has a controlled operating model

---

## Sprint 3 Boundary Confirmation

This document defines a customer setup foundation.

It does not implement:

- signup flow
- onboarding wizard
- workspace provisioning automation
- live customer import
- billing
- subscriptions
- customer account management
- multi-tenant SaaS permissions

Those may be future V3 or V4 candidates only if technically justified.
