USE supply_chain_risk_intelligence;

-- ==========================================
-- 1. Critical Stockout Risks
-- ==========================================

SELECT *
FROM vw_inventory_intelligence
WHERE stock_status = 'Critical Stockout Risk'
ORDER BY available_stock ASC;

-- ==========================================
-- 2. Products Requiring Reorder
-- ==========================================

SELECT *
FROM vw_reorder_intelligence
WHERE reorder_priority <> 'No Reorder Needed'
ORDER BY recommended_reorder_quantity DESC;

-- ==========================================
-- 3. Top Inventory Value Products
-- ==========================================

SELECT
    product_name,
    category,
    SUM(inventory_value) AS total_inventory_value
FROM vw_inventory_intelligence
GROUP BY product_name, category
ORDER BY total_inventory_value DESC
LIMIT 20;

-- ==========================================
-- 4. High Risk Suppliers
-- ==========================================

SELECT
    supplier_name,
    country,
    reliability_score,
    risk_score,
    risk_level
FROM vw_supplier_scorecard
WHERE risk_level = 'High'
ORDER BY risk_score DESC;

-- ==========================================
-- 5. Best Performing Suppliers
-- ==========================================

SELECT
    supplier_name,
    reliability_score,
    defect_rate,
    supplier_status
FROM vw_supplier_scorecard
ORDER BY reliability_score DESC
LIMIT 20;

-- ==========================================
-- 6. Delayed Shipments
-- ==========================================

SELECT
    shipment_id,
    warehouse_name,
    carrier,
    delay_days,
    shipping_cost
FROM vw_shipment_analysis
WHERE delivery_status = 'Delayed'
ORDER BY delay_days DESC;

-- ==========================================
-- 7. Carrier Performance
-- ==========================================

SELECT
    carrier,
    COUNT(*) AS total_shipments,
    AVG(shipping_cost) AS avg_shipping_cost,
    AVG(delay_days) AS avg_delay
FROM vw_shipment_analysis
GROUP BY carrier
ORDER BY avg_delay ASC;

-- ==========================================
-- 8. Warehouse Utilization Ranking
-- ==========================================

SELECT
    warehouse_name,
    city,
    utilization_percentage,
    utilization_status,
    warehouse_inventory_value
FROM vw_warehouse_utilization
ORDER BY utilization_percentage DESC;

-- ==========================================
-- 9. Forecast Accuracy Analysis
-- ==========================================

SELECT
    product_name,
    category,
    forecast_accuracy,
    demand_gap,
    forecast_quality
FROM vw_demand_forecast_accuracy
ORDER BY forecast_accuracy DESC;

-- ==========================================
-- 10. Executive KPI Dashboard Query
-- ==========================================

SELECT
    (SELECT COUNT(*) FROM products) AS total_products,
    (SELECT COUNT(*) FROM suppliers) AS total_suppliers,
    (SELECT COUNT(*) FROM orders) AS total_orders,
    (SELECT COUNT(*) FROM shipments) AS total_shipments,
    (SELECT ROUND(SUM(inventory_value),2)
     FROM vw_inventory_intelligence) AS total_inventory_value;