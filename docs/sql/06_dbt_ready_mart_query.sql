-- BakeOps Phase 2 - dbt-ready mart query
-- This file is a SQL bridge to the future bakeops-dbt project.
--
-- PURPOSE
-- This query mirrors the structure of the planned bakeops-dbt
-- mart_product_performance model. Each CTE here maps to a future
-- dbt staging, intermediate, or mart model.
--
-- DEPENDENCY NOTICE
-- Run the BakeOps demo seed, metric build, and BI export before using this query:
--   python manage.py seed_demo_data --reset
--   python manage.py build_bakery_metrics
--   python manage.py export_bi_csv
--
-- GRAIN
-- Final output grain: one row per cake/product in workspace_id = 1
-- using the latest product performance snapshot.

WITH stg_orders AS (
    -- Future dbt model: models/staging/stg_orders.sql
    -- Purpose: paid orders scoped to the SweetCakes demo workspace.
    SELECT
        order_id,
        workspace_id,
        order_date,
        status
    FROM fact_orders
    WHERE workspace_id = 1
      AND LOWER(TRIM(status)) = 'paid'
),

stg_order_items AS (
    -- Future dbt model: models/staging/stg_order_items.sql
    -- Purpose: cleaned order item values for product-level revenue analysis.
    SELECT
        order_id,
        cake_id,
        TRIM(cake_name) AS cake_name,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(line_total AS REAL) AS line_total
    FROM fact_order_items
),

int_product_revenue AS (
    -- Future dbt model: models/intermediate/int_product_revenue.sql
    -- Grain: one row per cake_id from paid order activity.
    SELECT
        oi.cake_id,
        oi.cake_name,
        SUM(oi.quantity) AS units_sold,
        SUM(oi.line_total) AS operational_revenue,
        COUNT(DISTINCT oi.order_id) AS distinct_orders
    FROM stg_order_items AS oi
    INNER JOIN stg_orders AS o
        ON o.order_id = oi.order_id
    GROUP BY
        oi.cake_id,
        oi.cake_name
),

latest_snapshot AS (
    -- Future dbt model pattern: latest snapshot filter.
    -- Purpose: select the latest product performance snapshot for workspace_id = 1.
    SELECT
        MAX(snapshot_date) AS snapshot_date
    FROM product_performance_snapshot
    WHERE workspace_id = 1
),

int_product_margins AS (
    -- Future dbt model: models/intermediate/int_product_margins.sql
    -- Grain: one row per cake_id with operational revenue and gold-layer margin evidence.
    SELECT
        ipr.cake_id,
        ipr.cake_name,
        ipr.units_sold,
        ipr.operational_revenue,
        ipr.distinct_orders,
        CAST(pps.revenue AS REAL) AS snapshot_revenue,
        CAST(pps.waste_cost AS REAL) AS waste_cost,
        CAST(pps.gross_margin AS REAL) AS gross_margin,
        CAST(pps.waste_adjusted_margin AS REAL) AS waste_adjusted_margin,
        CAST(pps.revenue_rank AS INTEGER) AS revenue_rank,
        CAST(pps.waste_adjusted_margin_rank AS INTEGER) AS waste_adjusted_margin_rank,
        pps.action_flag,
        pps.action_reason
    FROM int_product_revenue AS ipr
    LEFT JOIN product_performance_snapshot AS pps
        ON pps.cake_id = ipr.cake_id
       AND pps.workspace_id = 1
       AND pps.snapshot_date = (SELECT snapshot_date FROM latest_snapshot)
)

-- Future dbt model: models/marts/mart_product_performance.sql
-- Final mart-style output for product performance and rank inversion analysis.
SELECT
    cake_id,
    cake_name,
    units_sold,
    distinct_orders,
    operational_revenue,
    snapshot_revenue,
    gross_margin,
    waste_cost,
    waste_adjusted_margin,
    revenue_rank,
    waste_adjusted_margin_rank,
    waste_adjusted_margin_rank - revenue_rank AS margin_rank_gap,
    revenue_rank - waste_adjusted_margin_rank AS rank_movement,
    CASE
        WHEN waste_adjusted_margin_rank > revenue_rank THEN 'margin_weaker_than_revenue_suggests'
        WHEN waste_adjusted_margin_rank < revenue_rank THEN 'margin_stronger_than_revenue_suggests'
        ELSE 'ranks_aligned'
    END AS rank_movement_label,
    CASE
        WHEN waste_adjusted_margin_rank > revenue_rank THEN 1
        ELSE 0
    END AS has_rank_inversion,
    action_flag,
    action_reason
FROM int_product_margins
ORDER BY revenue_rank;
