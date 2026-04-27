# BakeOps Intelligence — V3 Import Contract Draft

## Purpose

This document defines a draft import contract for future BakeOps Intelligence imports.

It is a design document only.

No import parser, upload screen, or database import workflow is implemented yet.

---

## Import Contract Principle

BakeOps imports should create or update operational records first.

Analytics should then be rebuilt using the existing metric build command.

The import contract should protect this flow:

```text
import source
-> validated operational records
-> build_bakery_metrics
-> analytics snapshots
-> trusted pages
-> export_bi_csv
```

---

## Recommended First Import Files

The safest first import bundle is:

```text
customers.csv
ingredients.csv
orders.csv
order_items.csv
waste_records.csv
```

This supports commercially useful analytics without requiring the full production batch model immediately.

---

## File 1 — `customers.csv`

### Purpose

Creates or updates bakery customer records.

### Required Columns

| Column | Type | Required | Notes |
|---|---|---:|---|
| customer_ref | text | Yes | Stable external customer identifier |
| full_name | text | Yes | Customer display name |
| email | text | No | Should be unique when provided |
| phone | text | No | Optional contact number |
| postcode | text | No | Useful for delivery/customer analysis |
| is_active | boolean | No | Defaults to true |

### Validation Rules

- `customer_ref` must not be blank.
- `full_name` must not be blank.
- `email` must be valid if provided.
- duplicate `customer_ref` rows should be rejected or merged by explicit rule.
- customer imports should not delete existing customers.

---

## File 2 — `ingredients.csv`

### Purpose

Creates or updates ingredient master records.

### Required Columns

| Column | Type | Required | Notes |
|---|---|---:|---|
| ingredient_ref | text | Yes | Stable external ingredient identifier |
| ingredient_name | text | Yes | Ingredient display name |
| category | text | No | Example: dairy, flour, fruit, decoration |
| unit | text | Yes | Example: kg, g, litre, unit |
| unit_cost | decimal | Yes | Cost per unit |
| reorder_level | decimal | No | Minimum stock threshold |
| is_active | boolean | No | Defaults to true |

### Validation Rules

- `ingredient_ref` must not be blank.
- `ingredient_name` must not be blank.
- `unit` must be one of the accepted unit values.
- `unit_cost` must be zero or positive.
- `reorder_level` must be zero or positive when provided.
- duplicate ingredient names should be flagged for review.

---

## File 3 — `orders.csv`

### Purpose

Creates order-level records.

### Required Columns

| Column | Type | Required | Notes |
|---|---|---:|---|
| order_ref | text | Yes | Stable external order identifier |
| customer_ref | text | No | Links to `customers.csv`; blank may mean guest |
| order_date | date | Yes | Date order was placed |
| required_date | date | No | Delivery/collection date |
| status | text | Yes | Must match allowed order statuses |
| channel | text | No | Example: phone, website, shop, social |
| subtotal | decimal | Yes | Pre-discount value |
| discount_amount | decimal | No | Defaults to 0 |
| total_amount | decimal | Yes | Final order value |
| occasion_name | text | No | Example: Birthday, Wedding, Corporate |

### Validation Rules

- `order_ref` must not be blank.
- `order_date` must be valid.
- `required_date` cannot be earlier than `order_date` unless explicitly allowed.
- `status` must match accepted values.
- `subtotal`, `discount_amount`, and `total_amount` must be valid decimal values.
- `discount_amount` cannot be negative.
- `total_amount` cannot be negative.
- unknown `customer_ref` values should be reported.
- duplicate `order_ref` values should not silently create duplicate orders.

---

## File 4 — `order_items.csv`

### Purpose

Creates order item records linked to orders and products.

### Required Columns

| Column | Type | Required | Notes |
|---|---|---:|---|
| order_ref | text | Yes | Must match `orders.csv` or existing order |
| product_name | text | Yes | Must map to known cake/product |
| variant_name | text | No | Optional product variant |
| quantity | decimal | Yes | Number of items |
| unit_price | decimal | Yes | Price per item |
| line_total | decimal | Yes | Quantity × unit price, after line adjustment if used |

### Validation Rules

- `order_ref` must exist.
- `product_name` must map to a known cake.
- `variant_name` must map to a known variant when provided.
- `quantity` must be greater than zero.
- `unit_price` cannot be negative.
- `line_total` cannot be negative.
- line total mismatches should be warnings or rejections depending on tolerance.
- order items should be imported after orders.

---

## File 5 — `waste_records.csv`

### Purpose

Creates waste records used for waste-adjusted profitability and operational review.

### Required Columns

| Column | Type | Required | Notes |
|---|---|---:|---|
| waste_ref | text | Yes | Stable waste record identifier |
| waste_date | date | Yes | Date waste occurred |
| waste_type | text | Yes | Example: expired, damaged, overproduction |
| product_name | text | No | Product affected, if applicable |
| ingredient_name | text | No | Ingredient affected, if applicable |
| quantity | decimal | Yes | Wasted quantity |
| unit | text | Yes | Unit of waste |
| estimated_cost | decimal | Yes | Estimated waste cost |
| reason | text | No | Free-text explanation |

### Validation Rules

- `waste_ref` must not be blank.
- `waste_date` must be valid.
- `waste_type` must match accepted values.
- either `product_name` or `ingredient_name` should be provided where possible.
- `quantity` must be greater than zero.
- `estimated_cost` cannot be negative.
- unknown product or ingredient names should be reported.
- waste records should not be silently ignored.

---

## Optional Later Import Files

These are useful, but should not be first unless the earlier contracts are stable:

```text
suppliers.csv
ingredient_lots.csv
recipes.csv
recipe_lines.csv
production_batches.csv
production_batch_lines.csv
batch_allocations.csv
cake_reviews.csv
delivery_slots.csv
loyalty_accounts.csv
```

---

## Import Result Summary Contract

Every future import should produce a summary like:

| Field | Meaning |
|---|---|
| import_name | Name of the import run |
| workspace | Target workspace |
| source_file | Uploaded file name |
| started_at | Import start time |
| finished_at | Import finish time |
| status | success, partial, failed |
| rows_received | Total rows read |
| rows_created | New records created |
| rows_updated | Existing records updated |
| rows_skipped | Rows skipped by rule |
| rows_rejected | Rows rejected due to errors |
| warnings_count | Non-blocking issues |
| errors_count | Blocking issues |

---

## Rejected Row Report Contract

Rejected rows should include:

| Field | Meaning |
|---|---|
| file_name | Source file |
| row_number | Original row number |
| business_key | Customer/order/product/waste reference |
| field_name | Field causing issue |
| rejected_value | Original invalid value |
| severity | warning or error |
| message | Human-readable explanation |
| suggested_fix | Practical correction |

---

## Import Safety Rules

- Imports should never bypass validation.
- Imports should never write directly into gold-layer analytics tables.
- Imports should never delete existing records by default.
- Imports should never silently overwrite trusted records.
- Imports should never claim POS, Shopify, or Square integration unless those integrations are genuinely built.
- Imports should always preserve the metric rebuild workflow.
- Imports should always report warnings and rejected rows.

---

## Future Technical Implementation Notes

A safe later implementation could include:

```text
bakeops/services/imports/
bakeops/services/imports/contracts.py
bakeops/services/imports/validators.py
bakeops/services/imports/parsers.py
bakeops/services/imports/results.py
bakeops/management/commands/validate_import_file.py
bakeops/management/commands/import_bakery_file.py
```

These are not implemented in Sprint 2.

They are design candidates for a later sprint only.

---

## Sprint 2 Boundary Confirmation

This document is a contract draft.

It does not claim:

- CSV import is implemented
- Excel import is implemented
- upload UI is implemented
- POS integration is implemented
- Shopify/Square integration is implemented
- customer onboarding automation is implemented

It prepares the platform for safe import design.
