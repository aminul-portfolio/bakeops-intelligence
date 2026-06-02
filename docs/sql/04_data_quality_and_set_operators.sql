-- BakeOps Phase 1 — Data quality checks and set operators
-- Aligns with BakeOps DataQualityIssue themes; runs on CSV staging only.

-- ---------------------------------------------------------------------------
-- 1. Null / blank foreign keys on paid orders
-- ---------------------------------------------------------------------------
SELECT
    order_id,
    order_number,
    customer_id,
    occasion_id,
    delivery_slot_id,
    'missing_customer' AS issue_type
FROM fact_orders
WHERE status = 'paid'
  AND (customer_id IS NULL OR TRIM(customer_id) = '')

UNION ALL

SELECT
    order_id,
    order_number,
    customer_id,
    occasion_id,
    delivery_slot_id,
    'missing_occasion'
FROM fact_orders
WHERE status = 'paid'
  AND (occasion_id IS NULL OR TRIM(occasion_id) = '');

-- ---------------------------------------------------------------------------
-- 2. Line total reconciliation (quantity * unit_price vs line_total)
-- ---------------------------------------------------------------------------
SELECT
    order_item_id,
    order_number,
    cake_name,
    quantity,
    unit_price,
    line_total,
    ROUND(quantity * unit_price, 2) AS expected_line_total,
    ROUND(line_total - (quantity * unit_price), 2) AS line_total_delta
FROM fact_order_items
WHERE ABS(line_total - (quantity * unit_price)) >= 0.01
ORDER BY ABS(line_total_delta) DESC;

-- ---------------------------------------------------------------------------
-- 3. Orphan order items (set difference: items NOT IN orders)
-- ---------------------------------------------------------------------------
SELECT oi.order_item_id, oi.order_id, oi.order_number
FROM fact_order_items AS oi
WHERE oi.order_id NOT IN (SELECT order_id FROM fact_orders);

-- ---------------------------------------------------------------------------
-- 4. DISTINCT cake_ids across facts (UNION — catalog coverage)
-- ---------------------------------------------------------------------------
SELECT cake_id, 'order_items' AS source_table
FROM fact_order_items
UNION
SELECT CAST(NULLIF(cake_id, '') AS INTEGER), 'waste'
FROM fact_waste
WHERE cake_id <> ''
UNION
SELECT cake_id, 'production_batches'
FROM fact_production_batches
ORDER BY cake_id;

-- ---------------------------------------------------------------------------
-- 5. Cakes sold but missing from dim_cake (EXCEPT)
-- ---------------------------------------------------------------------------
SELECT DISTINCT cake_id
FROM fact_order_items
EXCEPT
SELECT DISTINCT cake_id
FROM dim_cake;

-- ---------------------------------------------------------------------------
-- 6. Customers referenced on orders but missing from dim_customer (EXCEPT)
-- ---------------------------------------------------------------------------
SELECT DISTINCT CAST(NULLIF(customer_id, '') AS INTEGER) AS customer_id
FROM fact_orders
WHERE TRIM(customer_id) <> ''
EXCEPT
SELECT customer_id
FROM dim_customer;

-- ---------------------------------------------------------------------------
-- 7. Duplicate natural keys (GROUP BY / HAVING)
-- ---------------------------------------------------------------------------
SELECT
    order_number,
    COUNT(*) AS row_count
FROM fact_orders
GROUP BY order_number
HAVING COUNT(*) > 1;

-- ---------------------------------------------------------------------------
-- 8. Gold vs operational revenue sanity (single snapshot date)
-- ---------------------------------------------------------------------------
WITH operational AS (
    SELECT SUM(oi.line_total) AS revenue
    FROM fact_order_items AS oi
    INNER JOIN fact_orders AS o
        ON o.order_id = oi.order_id
       AND o.status = 'paid'
),
gold AS (
    SELECT revenue
    FROM daily_bakery_metrics
    ORDER BY metric_date DESC
    LIMIT 1
)
SELECT
    operational.revenue AS operational_line_revenue,
    gold.revenue AS gold_daily_revenue,
    ROUND(gold.revenue - operational.revenue, 2) AS revenue_delta
FROM operational, gold;

-- ---------------------------------------------------------------------------
-- 9. Products flagged for review in gold layer
-- ---------------------------------------------------------------------------
SELECT
    snapshot_id,
    cake_name,
    revenue_rank,
    waste_adjusted_margin_rank,
    action_flag,
    action_reason
FROM product_performance_snapshot
WHERE action_flag = 'review'
ORDER BY revenue_rank;
