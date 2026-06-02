-- BakeOps Phase 1 — Row-level functions (SQLite)
-- CASE, COALESCE, CAST, date math, string functions
-- Note: CSV import may load numbers as TEXT; CAST before arithmetic where needed.

-- ---------------------------------------------------------------------------
-- 1. Channel grouping for reporting slices
-- ---------------------------------------------------------------------------
SELECT
    order_number,
    channel,
    CASE channel
        WHEN 'website' THEN 'Digital'
        WHEN 'phone' THEN 'Digital'
        WHEN 'in_store' THEN 'Walk-in'
        ELSE 'Other'
    END AS channel_group,
    CAST(total_amount AS REAL) AS total_amount
FROM fact_orders
WHERE status = 'paid'
ORDER BY order_date;

-- ---------------------------------------------------------------------------
-- 2. Fulfilment lead time (days between order and required date)
-- ---------------------------------------------------------------------------
SELECT
    order_number,
    order_date,
    date(order_date) AS order_day,
    strftime('%Y-%m', order_date) AS order_month,
    COALESCE(NULLIF(required_date, ''), order_date) AS fulfilment_target,
    CAST(
        julianday(COALESCE(NULLIF(required_date, ''), order_date))
        - julianday(order_date) AS INTEGER
    ) AS lead_time_days
FROM fact_orders
ORDER BY lead_time_days DESC, order_number;

-- ---------------------------------------------------------------------------
-- 3. Loyalty net points on the order row (CAST after CSV import)
-- ---------------------------------------------------------------------------
SELECT
    order_number,
    customer_id,
    CAST(loyalty_points_earned AS INTEGER) AS loyalty_points_earned,
    CAST(loyalty_points_redeemed AS INTEGER) AS loyalty_points_redeemed,
    CAST(loyalty_points_earned AS INTEGER) - CAST(loyalty_points_redeemed AS INTEGER) AS net_points,
    CASE
        WHEN CAST(loyalty_points_redeemed AS INTEGER) > 0
         AND CAST(loyalty_points_earned AS INTEGER) > 0 THEN 'earn_and_redeem'
        WHEN CAST(loyalty_points_redeemed AS INTEGER) > 0 THEN 'redeem_only'
        WHEN CAST(loyalty_points_earned AS INTEGER) > 0 THEN 'earn_only'
        ELSE 'no_loyalty_activity'
    END AS loyalty_activity_type
FROM fact_orders
WHERE status = 'paid';

-- ---------------------------------------------------------------------------
-- 4. Line economics — margin proxy from price and quantity
-- ---------------------------------------------------------------------------
SELECT
    order_item_id,
    cake_name,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(unit_price AS REAL) AS unit_price,
    CAST(line_total AS REAL) AS line_total,
    ROUND(CAST(line_total AS REAL) / NULLIF(CAST(quantity AS INTEGER), 0), 2) AS implied_unit_price,
    CASE
        WHEN ABS(
            CAST(line_total AS REAL)
            - (CAST(quantity AS INTEGER) * CAST(unit_price AS REAL))
        ) < 0.01 THEN 'balanced'
        ELSE 'check_line_math'
    END AS line_math_flag
FROM fact_order_items;

-- ---------------------------------------------------------------------------
-- 5. Ingredient stock signal (row-level risk label; subquery for ORDER BY)
-- ---------------------------------------------------------------------------
SELECT
    ingredient_name,
    current_stock_quantity,
    reorder_level_quantity,
    unit,
    cost_per_unit,
    stock_signal
FROM (
    SELECT
        ingredient_name,
        CAST(current_stock_quantity AS REAL) AS current_stock_quantity,
        CAST(reorder_level_quantity AS REAL) AS reorder_level_quantity,
        unit,
        ROUND(CAST(cost_per_unit AS REAL), 4) AS cost_per_unit,
        CASE
            WHEN CAST(current_stock_quantity AS REAL) <= 0 THEN 'out_of_stock'
            WHEN CAST(current_stock_quantity AS REAL)
                 < CAST(reorder_level_quantity AS REAL) THEN 'below_reorder'
            WHEN CAST(current_stock_quantity AS REAL)
                 = CAST(reorder_level_quantity AS REAL) THEN 'at_reorder'
            ELSE 'adequate'
        END AS stock_signal
    FROM dim_ingredient
    WHERE is_active IN ('True', '1')
) AS ingredient_signals
ORDER BY
    CASE stock_signal
        WHEN 'out_of_stock' THEN 1
        WHEN 'below_reorder' THEN 2
        WHEN 'at_reorder' THEN 3
        ELSE 4
    END,
    ingredient_name;

-- ---------------------------------------------------------------------------
-- 6. Normalise boolean CSV fields and string cleanup
-- ---------------------------------------------------------------------------
SELECT
    customer_id,
    full_name,
    CASE WHEN is_repeat_customer IN ('True', 'true', '1') THEN 1 ELSE 0 END AS is_repeat_customer_flag,
    COALESCE(NULLIF(TRIM(email), ''), 'unknown') AS email_clean,
    LOWER(COALESCE(NULLIF(TRIM(email), ''), 'unknown')) AS email_lower,
    SUBSTR(COALESCE(NULLIF(TRIM(email), ''), 'unknown'), 1, 3) AS email_prefix,
    REPLACE(COALESCE(NULLIF(TRIM(email), ''), 'unknown'), '@', ' [at] ') AS email_display_safe,
    UPPER(COALESCE(NULLIF(TRIM(postcode), ''), 'N/A')) AS postcode_display,
    LENGTH(COALESCE(NULLIF(TRIM(phone), ''), '')) AS phone_length
FROM dim_customer
ORDER BY full_name;
