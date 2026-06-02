-- BakeOps Phase 1 — Table inventory and staging DDL (SQLite)
-- Run once to create empty staging tables, then import CSVs per docs/sql/README.md
-- Re-run safe: drops prior staging objects before recreate.

PRAGMA foreign_keys = OFF;

DROP VIEW IF EXISTS v_table_inventory;
DROP VIEW IF EXISTS v_staging_table_catalog;
DROP TABLE IF EXISTS product_performance_snapshot;
DROP TABLE IF EXISTS daily_bakery_metrics;
DROP TABLE IF EXISTS dim_collection;
DROP TABLE IF EXISTS dim_occasion;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_ingredient;
DROP TABLE IF EXISTS dim_cake;
DROP TABLE IF EXISTS fact_production_batches;
DROP TABLE IF EXISTS fact_waste;
DROP TABLE IF EXISTS fact_order_items;
DROP TABLE IF EXISTS fact_orders;

-- ---------------------------------------------------------------------------
-- FACT TABLES (event / transaction grain)
-- ---------------------------------------------------------------------------

-- Grain: one row per bakery order header
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id                 INTEGER PRIMARY KEY,
    workspace_id             INTEGER NOT NULL,
    workspace_name           TEXT NOT NULL,
    order_number             TEXT NOT NULL,
    customer_id              TEXT,          -- empty string when unknown in export
    occasion_id              TEXT,
    delivery_slot_id         TEXT,
    order_date               TEXT NOT NULL, -- ISO date YYYY-MM-DD
    required_date            TEXT,
    status                   TEXT NOT NULL,
    channel                  TEXT NOT NULL,
    subtotal                 REAL NOT NULL,
    discount_amount          REAL NOT NULL,
    total_amount             REAL NOT NULL,
    loyalty_points_earned    INTEGER NOT NULL,
    loyalty_points_redeemed  INTEGER NOT NULL
);

-- Grain: one row per order line (cake variant sold)
CREATE TABLE IF NOT EXISTS fact_order_items (
    order_item_id   INTEGER PRIMARY KEY,
    order_id        INTEGER NOT NULL,
    order_number    TEXT NOT NULL,
    workspace_id    INTEGER NOT NULL,
    cake_id         INTEGER NOT NULL,
    cake_name       TEXT NOT NULL,
    variant_id      TEXT,
    variant_label   TEXT,
    quantity        INTEGER NOT NULL,
    unit_price      REAL NOT NULL,
    line_total      REAL NOT NULL
);

-- Grain: one row per waste event
CREATE TABLE IF NOT EXISTS fact_waste (
    waste_id          INTEGER PRIMARY KEY,
    workspace_id      INTEGER NOT NULL,
    waste_date        TEXT NOT NULL,
    reason            TEXT NOT NULL,
    ingredient_id     TEXT,
    ingredient_name   TEXT,
    cake_id           TEXT,
    cake_name         TEXT,
    variant_id        TEXT,
    variant_label     TEXT,
    batch_line_id     TEXT,
    quantity          REAL NOT NULL,
    estimated_cost    REAL NOT NULL,
    notes             TEXT
);

-- Grain: one row per production batch line (output by recipe/cake)
CREATE TABLE IF NOT EXISTS fact_production_batches (
    production_batch_id       INTEGER NOT NULL,
    production_batch_line_id  INTEGER PRIMARY KEY,
    workspace_id              INTEGER NOT NULL,
    batch_code                TEXT NOT NULL,
    production_date           TEXT NOT NULL,
    status                    TEXT NOT NULL,
    recipe_id                 INTEGER NOT NULL,
    recipe_name               TEXT NOT NULL,
    cake_id                   INTEGER NOT NULL,
    cake_name                 TEXT NOT NULL,
    variant_id                TEXT,
    variant_label             TEXT,
    planned_quantity          REAL NOT NULL,
    produced_quantity         REAL NOT NULL,
    failed_quantity           REAL NOT NULL
);

-- ---------------------------------------------------------------------------
-- DIMENSION TABLES (descriptive grain)
-- ---------------------------------------------------------------------------

-- Grain: one row per cake variant (catalog slice for demo cakes)
CREATE TABLE IF NOT EXISTS dim_cake (
    cake_id              INTEGER NOT NULL,
    cake_name            TEXT NOT NULL,
    slug                 TEXT NOT NULL,
    code                 TEXT NOT NULL,
    category             TEXT NOT NULL,
    occasion_type        TEXT NOT NULL,
    is_active            TEXT NOT NULL,  -- CSV: True/False
    variant_id           INTEGER PRIMARY KEY,
    variant_label        TEXT NOT NULL,
    serves_min           INTEGER NOT NULL,
    serves_max           INTEGER NOT NULL,
    price                REAL NOT NULL,
    is_default_variant   TEXT NOT NULL
);

-- Grain: one row per ingredient master
CREATE TABLE IF NOT EXISTS dim_ingredient (
    ingredient_id            INTEGER PRIMARY KEY,
    workspace_id             INTEGER NOT NULL,
    ingredient_name          TEXT NOT NULL,
    supplier_id              TEXT,
    supplier_name            TEXT,
    unit                     TEXT NOT NULL,
    cost_per_unit            REAL NOT NULL,
    current_stock_quantity   REAL NOT NULL,
    reorder_level_quantity   REAL NOT NULL,
    is_active                TEXT NOT NULL
);

-- Grain: one row per customer
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id               INTEGER PRIMARY KEY,
    workspace_id              INTEGER NOT NULL,
    full_name                 TEXT NOT NULL,
    email                     TEXT,
    phone                     TEXT,
    postcode                  TEXT,
    is_repeat_customer        TEXT NOT NULL,
    points_balance            INTEGER NOT NULL,
    lifetime_points_earned    INTEGER NOT NULL,
    lifetime_points_redeemed  INTEGER NOT NULL
);

-- Grain: one row per occasion type
CREATE TABLE IF NOT EXISTS dim_occasion (
    occasion_id    INTEGER PRIMARY KEY,
    workspace_id   INTEGER NOT NULL,
    occasion_name  TEXT NOT NULL,
    description    TEXT,
    is_active      TEXT NOT NULL
);

-- Grain: one row per catalogue collection (cakes app)
CREATE TABLE IF NOT EXISTS dim_collection (
    collection_id  INTEGER PRIMARY KEY,
    key            TEXT NOT NULL,
    label          TEXT NOT NULL,
    icon           TEXT,
    description    TEXT,
    is_active      TEXT NOT NULL,
    sort_order     INTEGER NOT NULL
);

-- ---------------------------------------------------------------------------
-- GOLD LAYER (metric snapshots — dashboard / BI truth for aggregates)
-- ---------------------------------------------------------------------------

-- Grain: one row per workspace per metric_date
CREATE TABLE IF NOT EXISTS daily_bakery_metrics (
    metric_id                      INTEGER PRIMARY KEY,
    workspace_id                   INTEGER NOT NULL,
    metric_date                    TEXT NOT NULL,
    revenue                        REAL NOT NULL,
    paid_orders                    INTEGER NOT NULL,
    average_order_value            REAL NOT NULL,
    total_items_sold               INTEGER NOT NULL,
    ingredient_cost                REAL NOT NULL,
    gross_margin                   REAL NOT NULL,
    gross_margin_percent           REAL NOT NULL,
    waste_cost                     REAL NOT NULL,
    waste_adjusted_margin          REAL NOT NULL,
    waste_adjusted_margin_percent  REAL NOT NULL
);

-- Grain: one row per workspace per snapshot_date per cake variant
CREATE TABLE IF NOT EXISTS product_performance_snapshot (
    snapshot_id                      INTEGER PRIMARY KEY,
    workspace_id                     INTEGER NOT NULL,
    snapshot_date                    TEXT NOT NULL,
    cake_id                          INTEGER NOT NULL,
    cake_name                        TEXT NOT NULL,
    variant_id                       TEXT,
    variant_label                    TEXT,
    revenue                          REAL NOT NULL,
    quantity_sold                    INTEGER NOT NULL,
    paid_order_count                 INTEGER NOT NULL,
    ingredient_cost                  REAL NOT NULL,
    gross_margin                     REAL NOT NULL,
    gross_margin_percent             REAL NOT NULL,
    waste_cost                       REAL NOT NULL,
    waste_adjusted_margin            REAL NOT NULL,
    waste_adjusted_margin_percent    REAL NOT NULL,
    revenue_rank                     INTEGER NOT NULL,
    waste_adjusted_margin_rank       INTEGER NOT NULL,
    action_flag                      TEXT NOT NULL,
    action_reason                    TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- STATIC STAGING CATALOG (pre-import — documents BI export contract)
-- ---------------------------------------------------------------------------

CREATE VIEW IF NOT EXISTS v_staging_table_catalog AS
SELECT 'fact_orders' AS table_name, 'fact' AS layer,
       'order header' AS grain_description, 16 AS expected_column_count,
       'order_id' AS primary_key_column
UNION ALL SELECT 'fact_order_items', 'fact', 'order line item', 11, 'order_item_id'
UNION ALL SELECT 'fact_waste', 'fact', 'waste event', 14, 'waste_id'
UNION ALL SELECT 'fact_production_batches', 'fact', 'production batch line', 15, 'production_batch_line_id'
UNION ALL SELECT 'dim_cake', 'dimension', 'cake variant', 13, 'variant_id'
UNION ALL SELECT 'dim_ingredient', 'dimension', 'ingredient master', 10, 'ingredient_id'
UNION ALL SELECT 'dim_customer', 'dimension', 'customer profile', 10, 'customer_id'
UNION ALL SELECT 'dim_occasion', 'dimension', 'occasion type', 5, 'occasion_id'
UNION ALL SELECT 'dim_collection', 'dimension', 'cake collection', 7, 'collection_id'
UNION ALL SELECT 'daily_bakery_metrics', 'gold', 'workspace daily KPI', 13, 'metric_id'
UNION ALL SELECT 'product_performance_snapshot', 'gold', 'product snapshot by date', 20, 'snapshot_id'
ORDER BY layer, table_name;

-- ---------------------------------------------------------------------------
-- INVENTORY VIEW (post-import row counts)
-- ---------------------------------------------------------------------------

CREATE VIEW IF NOT EXISTS v_table_inventory AS
SELECT 'fact_orders' AS table_name, 'fact' AS layer, COUNT(*) AS row_count FROM fact_orders
UNION ALL SELECT 'fact_order_items', 'fact', COUNT(*) FROM fact_order_items
UNION ALL SELECT 'fact_waste', 'fact', COUNT(*) FROM fact_waste
UNION ALL SELECT 'fact_production_batches', 'fact', COUNT(*) FROM fact_production_batches
UNION ALL SELECT 'dim_cake', 'dimension', COUNT(*) FROM dim_cake
UNION ALL SELECT 'dim_ingredient', 'dimension', COUNT(*) FROM dim_ingredient
UNION ALL SELECT 'dim_customer', 'dimension', COUNT(*) FROM dim_customer
UNION ALL SELECT 'dim_occasion', 'dimension', COUNT(*) FROM dim_occasion
UNION ALL SELECT 'dim_collection', 'dimension', COUNT(*) FROM dim_collection
UNION ALL SELECT 'daily_bakery_metrics', 'gold', COUNT(*) FROM daily_bakery_metrics
UNION ALL SELECT 'product_performance_snapshot', 'gold', COUNT(*) FROM product_performance_snapshot
ORDER BY layer, table_name;

-- Relationship map (logical — not enforced FKs on CSV staging):
--   fact_orders.customer_id      -> dim_customer.customer_id
--   fact_orders.occasion_id      -> dim_occasion.occasion_id
--   fact_order_items.order_id    -> fact_orders.order_id
--   fact_order_items.cake_id     -> dim_cake.cake_id (variant_id -> dim_cake.variant_id)
--   fact_waste.cake_id           -> dim_cake.cake_id
--   fact_waste.ingredient_id     -> dim_ingredient.ingredient_id
--   product_performance_snapshot -> dim_cake (cake_id, variant_id)

-- Suggested join indexes (optional; CSV staging is small in the demo).
CREATE INDEX IF NOT EXISTS idx_fact_order_items_order_id ON fact_order_items (order_id);
CREATE INDEX IF NOT EXISTS idx_fact_order_items_cake_id ON fact_order_items (cake_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_id ON fact_orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_product_snapshot_cake_id ON product_performance_snapshot (cake_id);

-- ---------------------------------------------------------------------------
-- TABLE INVENTORY QUERIES (executable verification)
-- ---------------------------------------------------------------------------

-- Export contract: expect 11 BI export tables before CSV import
SELECT COUNT(*) AS export_table_count
FROM v_staging_table_catalog;

SELECT *
FROM v_staging_table_catalog
ORDER BY layer, table_name;

-- Post-import row counts (expect ~52 total rows on current demo seed)
SELECT *
FROM v_table_inventory;

SELECT SUM(row_count) AS total_staged_rows
FROM v_table_inventory;

-- Column inventory for signature gold table (expect 20 columns)
SELECT
    cid AS ordinal_position,
    name AS column_name,
    type AS column_type,
    NOT "notnull" AS allows_null
FROM pragma_table_info('product_performance_snapshot')
ORDER BY cid;

-- ============================================================
-- SQLite schema inspection for key analytical evidence tables
-- These statements are intentionally executable, not comments.
-- ============================================================

PRAGMA table_info(fact_orders);
PRAGMA table_info(fact_order_items);
PRAGMA table_info(product_performance_snapshot);

