
# BakeOps Intelligence — Data Model Draft

## Sprint 2 Status

This document is a planning draft only. Real Django model fields will be implemented in the next model-building sprint.

## Architecture Boundary

| App | Responsibility |
|---|---|
| `cakes` | Existing customer-facing cake catalogue |
| `bakeops` | Analytics, operations, metrics, data quality, exports, and decision intelligence |

## Planned Model Groups

### 1. Workspace and Staff

- Workspace
- StaffMember

Purpose:
- Identify the bakery workspace.
- Support future multi-workspace separation.
- Keep operational analytics grouped under one bakery/business.

### 2. Catalog and Customer Context

- Customer
- LoyaltyAccount
- CakeReview
- OccasionType

Purpose:
- Capture customer behaviour, loyalty, reviews, and occasion-based demand.

### 3. Orders and Delivery

- DeliverySlot
- BakeryOrder
- BakeryOrderItem

Purpose:
- Capture paid orders, order value, item quantity, delivery demand, and collection pressure.

### 4. Ingredients and Stock

- Supplier
- Ingredient
- IngredientLot

Purpose:
- Track ingredient costs, stock levels, reorder risk, supplier source, and near-expiry risk.

### 5. Recipes, Production, Allocation, and Waste

- Recipe
- RecipeLine
- ProductionBatch
- ProductionBatchLine
- BatchAllocation
- WasteRecord

Purpose:
- Connect products to ingredient cost.
- Connect production output to order demand.
- Capture waste and its impact on profitability.

### 6. Gold-Layer Analytics

- DailyBakeryMetric
- ProductPerformanceSnapshot
- IngredientUsageSnapshot
- OccasionDemandSnapshot
- CustomerLoyaltySnapshot
- BakeryMetricRunLog
- DataQualityIssue

Purpose:
- Store trusted dashboard-ready metrics.
- Support BI exports.
- Surface data quality issues.
- Track metric build status.

## Key Relationship Plan

- Product snapshots will reference `cakes.Cake` and `cakes.CakeVariant`.
- Recipes will connect cake variants to ingredient lines.
- Production batches will produce cake variants.
- Batch allocations will connect production output to order items.
- Waste records will connect waste to ingredients, products, batches, and reasons.
- BakeryMetricRunLog will record build status, row counts, errors, and duration.
- DataQualityIssue will record trust issues visible in admin and dashboard.

## Signature V1 Insight

BakeOps must prove this core idea:

> A best-selling product can become weak after ingredient cost and waste are included.

Target demo scenario:

- Birthday Classic is revenue rank #1.
- Birthday Classic drops after waste-adjusted margin is calculated.
- Dashboard, exports, and recommendation cards must use the same waste-adjusted margin logic.

## Not In Sprint 2

- No real model fields yet.
- No migrations yet.
- No seeded data yet.
- No metric build command yet.
- No dashboard yet.
- No exports yet.
