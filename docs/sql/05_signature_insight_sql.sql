-- DEPENDENCY NOTICE
-- This query reads from the gold-layer analytical snapshot (ProductPerformanceSnapshot).
-- Before running: seed demo data with `python manage.py seed_demo_data --reset`
-- then build metrics with `python manage.py build_bakery_metrics`.
-- Running against an empty snapshot will return zero rows.
-- BakeOps Phase 1 - Signature insight SQL
-- Business proof: top revenue product can weaken after waste-adjusted margin.
-- Demo expectation (current seed): Birthday Classic - revenue rank 1, margin rank 4, action review.
-- Dashboard gap: margin_rank_gap = 4 - 1 = 3 (positive means rank dropped after waste).
-- Case study movement: rank_movement = 1 - 4 = -3 (negative means margin rank weakened).
-- Source of truth for ranks: product_performance_snapshot (built by build_bakery_metrics).
-- Filter: workspace_id = 1 (SweetCakes Bakery demo), latest snapshot_date only.

-- ---------------------------------------------------------------------------
-- 1. Primary reviewer query - signature product rank movement
-- ---------------------------------------------------------------------------
SELECT
    cake_name,
    variant_label,
    CAST(revenue AS REAL) AS revenue,
    CAST(waste_cost AS REAL) AS waste_cost,
    CAST(waste_adjusted_margin AS REAL) AS waste_adjusted_margin,
    CAST(revenue_rank AS INTEGER) AS revenue_rank,
    CAST(waste_adjusted_margin_rank AS INTEGER) AS waste_adjusted_margin_rank,
    CAST(waste_adjusted_margin_rank AS INTEGER) - CAST(revenue_rank AS INTEGER) AS margin_rank_gap,
    CAST(revenue_rank AS INTEGER) - CAST(waste_adjusted_margin_rank AS INTEGER) AS rank_movement,
    CASE
        WHEN CAST(waste_adjusted_margin_rank AS INTEGER) > CAST(revenue_rank AS INTEGER) THEN 1
        ELSE 0
    END AS has_margin_rank_inversion,
    action_flag,
    action_reason
FROM product_performance_snapshot
WHERE workspace_id = 1
  AND cake_name = 'Birthday Classic'
  AND snapshot_date = (
      SELECT MAX(snapshot_date)
      FROM product_performance_snapshot
      WHERE workspace_id = 1
  );

-- ---------------------------------------------------------------------------
-- 2. All products - highlight rank inversion on latest snapshot
-- ---------------------------------------------------------------------------
SELECT
    cake_name,
    CAST(revenue_rank AS INTEGER) AS revenue_rank,
    CAST(waste_adjusted_margin_rank AS INTEGER) AS waste_adjusted_margin_rank,
    CAST(waste_adjusted_margin_rank AS INTEGER) - CAST(revenue_rank AS INTEGER) AS margin_rank_gap,
    CAST(revenue_rank AS INTEGER) - CAST(waste_adjusted_margin_rank AS INTEGER) AS rank_movement,
    CASE
        WHEN CAST(waste_adjusted_margin_rank AS INTEGER) > CAST(revenue_rank AS INTEGER) THEN 1
        ELSE 0
    END AS has_margin_rank_inversion,
    action_flag,
    CASE
        WHEN CAST(waste_adjusted_margin_rank AS INTEGER) > CAST(revenue_rank AS INTEGER)
            THEN 'margin_weaker_than_revenue_suggests'
        WHEN CAST(waste_adjusted_margin_rank AS INTEGER) < CAST(revenue_rank AS INTEGER)
            THEN 'margin_stronger_than_revenue_suggests'
        ELSE 'ranks_aligned'
    END AS rank_movement_label
FROM product_performance_snapshot
WHERE workspace_id = 1
  AND snapshot_date = (
      SELECT MAX(snapshot_date)
      FROM product_performance_snapshot
      WHERE workspace_id = 1
  )
ORDER BY CAST(revenue_rank AS INTEGER);

-- ---------------------------------------------------------------------------
-- 3. Supporting waste evidence for Birthday Classic (operational fact)
-- ---------------------------------------------------------------------------
SELECT
    waste_date,
    reason,
    CAST(quantity AS REAL) AS quantity,
    CAST(estimated_cost AS REAL) AS estimated_cost,
    notes
FROM fact_waste
WHERE workspace_id = 1
  AND cake_name = 'Birthday Classic'
ORDER BY CAST(estimated_cost AS REAL) DESC;

-- ---------------------------------------------------------------------------
-- 4. Reconcile product revenue (facts) vs snapshot revenue (gold)
-- ---------------------------------------------------------------------------
WITH fact_product AS (
    SELECT
        oi.cake_name,
        SUM(CAST(oi.line_total AS REAL)) AS operational_revenue,
        SUM(CAST(oi.quantity AS INTEGER)) AS operational_units
    FROM fact_order_items AS oi
    INNER JOIN fact_orders AS o
        ON o.order_id = oi.order_id
       AND o.status = 'paid'
    WHERE oi.cake_name = 'Birthday Classic'
    GROUP BY oi.cake_name
),
gold_product AS (
    SELECT
        cake_name,
        CAST(revenue AS REAL) AS snapshot_revenue,
        CAST(quantity_sold AS INTEGER) AS quantity_sold,
        CAST(waste_cost AS REAL) AS waste_cost,
        CAST(waste_adjusted_margin AS REAL) AS waste_adjusted_margin,
        CAST(revenue_rank AS INTEGER) AS revenue_rank,
        CAST(waste_adjusted_margin_rank AS INTEGER) AS waste_adjusted_margin_rank
    FROM product_performance_snapshot
    WHERE workspace_id = 1
      AND cake_name = 'Birthday Classic'
      AND snapshot_date = (
          SELECT MAX(snapshot_date)
          FROM product_performance_snapshot
          WHERE workspace_id = 1
      )
)
SELECT
    f.cake_name,
    f.operational_revenue,
    g.snapshot_revenue,
    ROUND(g.snapshot_revenue - f.operational_revenue, 2) AS revenue_delta,
    f.operational_units,
    g.quantity_sold,
    g.waste_cost,
    g.waste_adjusted_margin,
    g.revenue_rank,
    g.waste_adjusted_margin_rank,
    g.waste_adjusted_margin_rank - g.revenue_rank AS margin_rank_gap,
    g.revenue_rank - g.waste_adjusted_margin_rank AS rank_movement,
    CASE WHEN g.waste_adjusted_margin_rank > g.revenue_rank THEN 1 ELSE 0 END AS has_margin_rank_inversion
FROM fact_product AS f
INNER JOIN gold_product AS g
    ON g.cake_name = f.cake_name;

-- ---------------------------------------------------------------------------
-- 5. Compact evidence string (matches dashboard test convention)
-- ---------------------------------------------------------------------------
SELECT
    cake_name
    || ' '
    || CAST(CAST(revenue_rank AS INTEGER) AS TEXT)
    || ' '
    || CAST(CAST(waste_adjusted_margin_rank AS INTEGER) AS TEXT)
    || ' '
    || action_flag AS signature_evidence
FROM product_performance_snapshot
WHERE workspace_id = 1
  AND cake_name = 'Birthday Classic'
  AND snapshot_date = (
      SELECT MAX(snapshot_date)
      FROM product_performance_snapshot
      WHERE workspace_id = 1
  );

-- ---------------------------------------------------------------------------
-- 6. Acceptance assertion - signature_evidence + rank proof (demo seed)
-- ---------------------------------------------------------------------------
WITH latest_signature AS (
    SELECT
        cake_name,
        CAST(revenue_rank AS INTEGER) AS revenue_rank,
        CAST(waste_adjusted_margin_rank AS INTEGER) AS waste_adjusted_margin_rank,
        action_flag,
        CAST(waste_adjusted_margin_rank AS INTEGER) - CAST(revenue_rank AS INTEGER) AS margin_rank_gap,
        CAST(revenue_rank AS INTEGER) - CAST(waste_adjusted_margin_rank AS INTEGER) AS rank_movement,
        cake_name
            || ' '
            || CAST(CAST(revenue_rank AS INTEGER) AS TEXT)
            || ' '
            || CAST(CAST(waste_adjusted_margin_rank AS INTEGER) AS TEXT)
            || ' '
            || action_flag AS signature_evidence
    FROM product_performance_snapshot
    WHERE workspace_id = 1
      AND cake_name = 'Birthday Classic'
      AND snapshot_date = (
          SELECT MAX(snapshot_date)
          FROM product_performance_snapshot
          WHERE workspace_id = 1
      )
)
SELECT
    cake_name,
    revenue_rank,
    waste_adjusted_margin_rank,
    action_flag,
    margin_rank_gap,
    rank_movement,
    signature_evidence,
    CASE
        WHEN signature_evidence = 'Birthday Classic 1 4 review'
         AND revenue_rank = 1
         AND waste_adjusted_margin_rank = 4
         AND action_flag = 'review'
         AND margin_rank_gap = 3
         AND rank_movement = -3
            THEN 'PASS'
        ELSE 'FAIL'
    END AS acceptance_result
FROM latest_signature;

