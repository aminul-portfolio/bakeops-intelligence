# When the best-seller is the fourth most profitable product

*A case study from BakeOps Intelligence — Aminul Islam*

In a four-product, 30-day snapshot of seeded bakery data, Birthday Classic was the highest-revenue product. By revenue rank, it was #1. By waste-adjusted margin rank, it was #4 — the largest negative rank movement in the catalogue.

That rank inversion is the central finding of BakeOps Intelligence. This document explains how the analysis is built, what the data shows, and where the work goes next.

## Why this question

Bakery operations software typically optimises for revenue. Dashboards show what sold most, which products moved fastest, which customers ordered most often. Revenue is observable. Waste is not — it lives in batch records, expiry logs, quality control notes, and the gap between produced quantity and allocated orders.

The hypothesis was simple: if waste is invisible in the revenue view, then revenue rankings can be misleading about which products contribute most to actual profit. To test it, I built a comparison between each product's revenue rank and its rank after waste cost is included.

## The data model

BakeOps separates operational data from analytical data. Operational tables capture events as they happen: `Order`, `OrderItem`, `ProductionBatch`, `WasteRecord`, `IngredientLot`, `Recipe`, `RecipeLine`. Analytical tables (`ProductPerformanceSnapshot`, `IngredientUsageSnapshot`, `DailyBakeryMetric`, and others) are gold-layer aggregations built deterministically by the `build_bakery_metrics` management command.

The separation matters. The dashboard is not the source of truth. The dashboard reads from the gold layer; the gold layer is built from operational records; operational records are immutable once written. Delete the snapshots, rebuild, and you get the same answer. If the answer ever changes, that's a bug in the build, not a bug in the dashboard.

For this analysis the relevant tables are:

- `OrderItem` — line-level sales, joined to `Cake` for product attribution and to `Order` for time and channel
- `WasteRecord` — cost-bearing waste events, optionally linked to a `Cake` and an `Ingredient`, with a categorical `reason` field
- `Recipe` and `RecipeLine` — ingredient quantities per cake, used to derive ingredient cost per unit produced
- `ProductPerformanceSnapshot` — one row per cake per snapshot date, with revenue, quantity, gross margin, waste cost, waste-adjusted margin, and four rank columns

The grain decision is deliberate. `ProductPerformanceSnapshot` is per-product, per-snapshot-date. Rank values are computed within the snapshot, so they are directly comparable across products in the same snapshot but must never be compared across snapshots without re-ranking. This is the kind of thing that becomes a quiet bug if you're not explicit about it.

## The metric

Waste-adjusted margin is simple in formula but precise in scope. Per cake, per period:

```
gross_margin            = sum(line_total) - sum(ingredient_cost_at_recipe_quantity)
waste_cost              = sum(waste_record.estimated_cost) where waste_record.cake = this cake
waste_adjusted_margin   = gross_margin - waste_cost
```

The rank inversion signal is then:

```
rank_movement = revenue_rank - waste_adjusted_margin_rank
```

A negative `rank_movement` means the product looks worse after waste is included than its revenue rank suggested. A positive `rank_movement` means the opposite — its profitability is stronger than revenue position implies. The size of the movement is the signal worth acting on; a movement of zero means revenue rank already tells the truth.

## The finding

In the 30-day snapshot of the seeded SweetCakes Bakery workspace:

| Product | Revenue | Rev Rank | Waste-Adjusted | Margin Rank | Movement | Action |
|---|---|---|---|---|---|---|
| Birthday Classic | £405.00 | #1 | £250.48 | #4 | −3 | Review |
| Wedding Rose | £190.00 | #2 | £134.94 | #2 | 0 | Stable |
| Luxury Chocolate | £76.00 | #3 | £50.02 | #3 | 0 | Stable |
| Lemon Poppy | £56.00 | #4 | £45.20 | #1 | +3 | Promote |

Birthday Classic carries £32.75 of waste cost, equal to 11.56% of its gross margin, driven largely by overproduction on large-party batches and a smaller contribution from decorative-icing quality issues. Lemon Poppy, the lowest-revenue product, has the strongest waste-adjusted margin rate (80.71% vs. Birthday Classic's 61.85%).

The two ends of the catalogue invert. The product that sells most needs profitability review. The product that sells least is the strongest profit contributor per pound of revenue.

## What this is not

This finding is on seeded demo data, not real bakery operations. The catalogue is four products. The waste record set has four events. With a real-world catalogue of fifty or a hundred SKUs, the rank-inversion signal would be richer but also noisier — small differences in waste cost would produce rank changes that aren't statistically meaningful, and the analysis would need a significance threshold below which a movement is treated as zero.

The analysis also assumes ingredient cost is fixed per recipe at snapshot time. In reality, ingredient prices drift; a more honest version would track historical ingredient unit cost and join on the date of each `OrderItem`. That work is not built yet.

There is no time-decay either. A waste event on day 1 of the snapshot is weighted identically to one on day 30. For a longer snapshot window this is wrong — recent waste is more actionable than old waste, and an acceleration in waste rate is itself a signal worth surfacing.

## What I'd build next

1. **Ingredient price drift.** Slowly-changing-dimension on `IngredientLot.unit_cost` (type-2 SCD), with `OrderItem` margin computed against the ingredient price effective on the order date.
2. **Time-aware waste weighting.** Exponential decay on waste events; a separate metric for recent waste acceleration vs. baseline waste rate.
3. **Per-occasion rank inversion.** Birthday Classic's waste signal is dominated by large-party batches. The same cake sold for everyday-treat occasions may have a different profile. Adding occasion as a dimension to `ProductPerformanceSnapshot` would surface this.
4. **Column-level contract tests.** The gold-layer build is currently tested by comparing aggregate output against expected values for the seeded dataset. A more general approach is contract tests at column granularity — type, range, referential integrity, null rules — running in CI on every metric build.

## Reproducing the analysis

The build is two management commands:

```
python manage.py seed_demo_data --reset
python manage.py build_bakery_metrics
```

The protected reviewer output verifies the finding survives a clean rebuild:

```
$ python manage.py shell -c "from bakeops.models import ProductPerformanceSnapshot; \
    p = ProductPerformanceSnapshot.objects.get(cake__name='Birthday Classic'); \
    print(p.cake.name, p.revenue_rank, p.waste_adjusted_margin_rank, p.action_flag)"
Birthday Classic 1 4 review
```

If that line ever changes, the analysis has changed. CI runs the rebuild and the verification on every commit. The full repository, including the metric build code, the seed data definitions, the test suite, and the BI export contract, is at [link to repo].

---

*BakeOps Intelligence is a portfolio project demonstrating analytics-engineering and data-engineering thinking on a bakery operations problem. It is not a live SaaS product, has no real customers, and runs on seeded demo data.*
