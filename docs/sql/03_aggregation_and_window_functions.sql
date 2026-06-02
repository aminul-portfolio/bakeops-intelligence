-- BakeOps Phase 1 — Aggregation and window functions (SQLite 3.25+)
-- CAST aggregates when reading CSV-backed staging tables.

-- ---------------------------------------------------------------------------
-- 1. Product revenue from operational facts (compare to gold snapshots)
-- ---------------------------------------------------------------------------
SELECT
    oi.cake_id,
    oi.cake_name,
    SUM(CAST(oi.quantity AS INTEGER)) AS units_sold,
    SUM(CAST(oi.line_total AS REAL)) AS revenue,
    COUNT(DISTINCT oi.order_id) AS distinct_orders
FROM fact_order_items AS oi
INNER JOIN fact_orders AS o
    ON o.order_id = oi.order_id
   AND o.status = 'paid'
GROUP BY oi.cake_id, oi.cake_name
HAVING SUM(CAST(oi.line_total AS REAL)) > 0
ORDER BY revenue DESC;

-- ---------------------------------------------------------------------------
-- 2. Window ranking — RANK and DENSE_RANK from operational facts
-- ---------------------------------------------------------------------------
WITH product_revenue AS (
    SELECT
        oi.cake_id,
        oi.cake_name,
        SUM(CAST(oi.line_total AS REAL)) AS revenue
    FROM fact_order_items AS oi
    INNER JOIN fact_orders AS o
        ON o.order_id = oi.order_id
       AND o.status = 'paid'
    GROUP BY oi.cake_id, oi.cake_name
)
SELECT
    cake_name,
    revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank_operational,
    DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_dense_rank_operational,
    ROUND(100.0 * revenue / SUM(revenue) OVER (), 2) AS revenue_share_pct
FROM product_revenue
ORDER BY revenue_rank_operational;

-- ---------------------------------------------------------------------------
-- 3. Gold-layer window — margin_rank_gap (dashboard) and rank_movement (case study)
-- ---------------------------------------------------------------------------
SELECT
    cake_name,
    CAST(revenue AS REAL) AS revenue,
    CAST(waste_adjusted_margin AS REAL) AS waste_adjusted_margin,
    CAST(revenue_rank AS INTEGER) AS revenue_rank,
    CAST(waste_adjusted_margin_rank AS INTEGER) AS waste_adjusted_margin_rank,
    CAST(waste_adjusted_margin_rank AS INTEGER) - CAST(revenue_rank AS INTEGER) AS margin_rank_gap,
    CAST(revenue_rank AS INTEGER) - CAST(waste_adjusted_margin_rank AS INTEGER) AS rank_movement,
    action_flag,
    SUM(CAST(revenue AS REAL)) OVER () AS workspace_revenue,
    ROUND(
        100.0 * CAST(waste_adjusted_margin AS REAL)
        / NULLIF(SUM(CAST(waste_adjusted_margin AS REAL)) OVER (), 0),
        2
    ) AS margin_share_pct
FROM product_performance_snapshot
WHERE workspace_id = 1
  AND snapshot_date = (
      SELECT MAX(snapshot_date)
      FROM product_performance_snapshot
      WHERE workspace_id = 1
  )
ORDER BY CAST(revenue_rank AS INTEGER);

-- ---------------------------------------------------------------------------
-- 4. ROW_NUMBER and running waste cost by date
-- ---------------------------------------------------------------------------
SELECT
    waste_date,
    reason,
    CAST(estimated_cost AS REAL) AS estimated_cost,
    ROW_NUMBER() OVER (
        PARTITION BY waste_date
        ORDER BY CAST(estimated_cost AS REAL) DESC, waste_id
    ) AS waste_rank_within_day,
    SUM(CAST(estimated_cost AS REAL)) OVER (
        ORDER BY waste_date, waste_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_waste_cost
FROM fact_waste
ORDER BY waste_date, waste_id;

-- ---------------------------------------------------------------------------
-- 5. Production yield rate by batch line
-- ---------------------------------------------------------------------------
SELECT
    batch_code,
    cake_name,
    CAST(planned_quantity AS REAL) AS planned_quantity,
    CAST(produced_quantity AS REAL) AS produced_quantity,
    CAST(failed_quantity AS REAL) AS failed_quantity,
    ROUND(
        100.0 * CAST(produced_quantity AS REAL) / NULLIF(CAST(planned_quantity AS REAL), 0),
        2
    ) AS yield_pct,
    AVG(CAST(produced_quantity AS REAL)) OVER (
        PARTITION BY cake_id
    ) AS avg_produced_per_cake
FROM fact_production_batches
ORDER BY batch_code, cake_name;

-- ---------------------------------------------------------------------------
-- 6. Daily KPI from gold layer with LAG period comparison
-- ---------------------------------------------------------------------------
SELECT
    metric_date,
    CAST(revenue AS REAL) AS revenue,
    CAST(paid_orders AS INTEGER) AS paid_orders,
    CAST(average_order_value AS REAL) AS average_order_value,
    CAST(waste_cost AS REAL) AS waste_cost,
    CAST(waste_adjusted_margin AS REAL) AS waste_adjusted_margin,
    LAG(CAST(revenue AS REAL)) OVER (ORDER BY metric_date) AS prior_day_revenue,
    CAST(revenue AS REAL)
        - COALESCE(LAG(CAST(revenue AS REAL)) OVER (ORDER BY metric_date), CAST(revenue AS REAL))
        AS revenue_day_change
FROM daily_bakery_metrics
WHERE workspace_id = 1
ORDER BY metric_date;
