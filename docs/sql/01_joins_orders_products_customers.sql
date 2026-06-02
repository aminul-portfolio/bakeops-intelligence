-- BakeOps Phase 1 — Joins: orders, products (cakes), customers, occasions
-- Prerequisites: 00_table_inventory.sql + CSV import (see README.md)

-- ---------------------------------------------------------------------------
-- 1. Order line detail (star join: items -> order -> customer -> cake -> occasion)
-- ---------------------------------------------------------------------------
SELECT
    o.order_number,
    o.order_date,
    o.status,
    o.channel,
    c.full_name AS customer_name,
    c.is_repeat_customer,
    occ.occasion_name,
    oi.cake_name,
    oi.variant_label,
    oi.quantity,
    oi.unit_price,
    oi.line_total
FROM fact_order_items AS oi
INNER JOIN fact_orders AS o
    ON o.order_id = oi.order_id
LEFT JOIN dim_customer AS c
    ON c.customer_id = CAST(NULLIF(o.customer_id, '') AS INTEGER)
LEFT JOIN dim_occasion AS occ
    ON occ.occasion_id = CAST(NULLIF(o.occasion_id, '') AS INTEGER)
LEFT JOIN dim_cake AS cake
    ON cake.cake_id = oi.cake_id
   AND cake.variant_id = CAST(NULLIF(oi.variant_id, '') AS INTEGER)
WHERE o.status = 'paid'
ORDER BY o.order_date, o.order_number, oi.cake_name;

-- ---------------------------------------------------------------------------
-- 2. Customer revenue roll-up from joined facts (operational layer)
-- ---------------------------------------------------------------------------
SELECT
    c.customer_id,
    c.full_name,
    c.is_repeat_customer,
    COUNT(DISTINCT o.order_id) AS paid_order_count,
    SUM(oi.line_total) AS item_revenue,
    SUM(oi.quantity) AS units_purchased
FROM dim_customer AS c
INNER JOIN fact_orders AS o
    ON CAST(NULLIF(o.customer_id, '') AS INTEGER) = c.customer_id
   AND o.status = 'paid'
INNER JOIN fact_order_items AS oi
    ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.full_name, c.is_repeat_customer
ORDER BY item_revenue DESC, c.full_name;

-- ---------------------------------------------------------------------------
-- 3. Product catalogue join — list price vs realised unit price on lines
-- ---------------------------------------------------------------------------
SELECT
    oi.order_number,
    oi.cake_name,
    oi.variant_label,
    oi.unit_price AS charged_unit_price,
    cake.price AS catalogue_list_price,
    ROUND(oi.unit_price - cake.price, 2) AS price_delta,
    oi.line_total
FROM fact_order_items AS oi
INNER JOIN dim_cake AS cake
    ON cake.cake_id = oi.cake_id
   AND cake.variant_id = CAST(NULLIF(oi.variant_id, '') AS INTEGER)
ORDER BY oi.order_number, oi.cake_name;

-- ---------------------------------------------------------------------------
-- 4. Occasion demand via order headers (before gold-layer snapshots)
-- ---------------------------------------------------------------------------
SELECT
    occ.occasion_name,
    COUNT(DISTINCT o.order_id) AS paid_orders,
    SUM(o.total_amount) AS order_header_revenue,
    SUM(oi.quantity) AS units_sold
FROM fact_orders AS o
INNER JOIN dim_occasion AS occ
    ON occ.occasion_id = CAST(NULLIF(o.occasion_id, '') AS INTEGER)
INNER JOIN fact_order_items AS oi
    ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY occ.occasion_name
ORDER BY order_header_revenue DESC;

-- ---------------------------------------------------------------------------
-- 5. Waste attributed to products sold on orders (cake-level join path)
-- ---------------------------------------------------------------------------
SELECT
    oi.cake_name,
    oi.variant_label,
    w.reason,
    w.waste_date,
    w.quantity AS waste_quantity,
    w.estimated_cost AS waste_cost,
    oi.order_number
FROM fact_waste AS w
INNER JOIN dim_cake AS cake
    ON cake.cake_id = CAST(NULLIF(w.cake_id, '') AS INTEGER)
INNER JOIN fact_order_items AS oi
    ON oi.cake_id = cake.cake_id
   AND CAST(NULLIF(oi.variant_id, '') AS INTEGER) = cake.variant_id
WHERE w.cake_id <> ''
ORDER BY w.estimated_cost DESC, oi.cake_name;
