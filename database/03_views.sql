USE supply_chain_risk_intelligence;

CREATE OR REPLACE VIEW vw_inventory_intelligence AS
SELECT
    i.inventory_id,
    p.product_id,
    p.product_name,
    p.category,
    w.warehouse_id,
    w.warehouse_name,
    i.current_stock,
    i.reserved_stock,
    (i.current_stock - i.reserved_stock) AS available_stock,
    p.reorder_level,
    p.safety_stock,
    p.unit_price,
    ROUND(i.current_stock * p.unit_price, 2) AS inventory_value,
    CASE
        WHEN (i.current_stock - i.reserved_stock) <= p.safety_stock THEN 'Critical Stockout Risk'
        WHEN (i.current_stock - i.reserved_stock) <= p.reorder_level THEN 'Reorder Required'
        ELSE 'Healthy Stock'
    END AS stock_status
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN warehouses w ON i.warehouse_id = w.warehouse_id;


CREATE OR REPLACE VIEW vw_supplier_scorecard AS
SELECT
    s.supplier_id,
    s.supplier_name,
    s.country,
    s.reliability_score,
    s.avg_lead_time_days,
    s.defect_rate,
    sr.risk_category,
    sr.risk_score,
    sr.risk_level,
    CASE
        WHEN s.reliability_score >= 85 AND sr.risk_score < 40 THEN 'Preferred Supplier'
        WHEN s.reliability_score >= 70 AND sr.risk_score < 70 THEN 'Moderate Supplier'
        ELSE 'High Risk Supplier'
    END AS supplier_status
FROM suppliers s
LEFT JOIN supplier_risk sr ON s.supplier_id = sr.supplier_id;


CREATE OR REPLACE VIEW vw_shipment_analysis AS
SELECT
    sh.shipment_id,
    o.order_id,
    o.customer_region,
    sh.warehouse_id,
    w.warehouse_name,
    sh.carrier,
    sh.shipment_date,
    sh.delivery_date,
    o.expected_delivery_date,
    DATEDIFF(sh.delivery_date, o.expected_delivery_date) AS delay_days,
    sh.shipping_cost,
    CASE
        WHEN sh.delivery_date > o.expected_delivery_date THEN 'Delayed'
        ELSE 'On Time'
    END AS delivery_status
FROM shipments sh
JOIN orders o ON sh.order_id = o.order_id
JOIN warehouses w ON sh.warehouse_id = w.warehouse_id;


CREATE OR REPLACE VIEW vw_warehouse_utilization AS
SELECT
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    w.capacity_units,
    SUM(i.current_stock) AS total_stock,
    ROUND((SUM(i.current_stock) / w.capacity_units) * 100, 2) AS utilization_percentage,
    ROUND(SUM(i.current_stock * p.unit_price), 2) AS warehouse_inventory_value,
    CASE
        WHEN ROUND((SUM(i.current_stock) / w.capacity_units) * 100, 2) >= 90 THEN 'Overutilized'
        WHEN ROUND((SUM(i.current_stock) / w.capacity_units) * 100, 2) >= 70 THEN 'Highly Utilized'
        WHEN ROUND((SUM(i.current_stock) / w.capacity_units) * 100, 2) >= 40 THEN 'Moderately Utilized'
        ELSE 'Underutilized'
    END AS utilization_status
FROM warehouses w
JOIN inventory i ON w.warehouse_id = i.warehouse_id
JOIN products p ON i.product_id = p.product_id
GROUP BY w.warehouse_id, w.warehouse_name, w.city, w.capacity_units;


CREATE OR REPLACE VIEW vw_demand_forecast_accuracy AS
SELECT
    df.forecast_id,
    p.product_id,
    p.product_name,
    p.category,
    df.forecast_month,
    df.predicted_demand,
    df.actual_demand,
    df.forecast_accuracy,
    ABS(df.predicted_demand - df.actual_demand) AS demand_gap,
    CASE
        WHEN df.forecast_accuracy >= 85 THEN 'High Accuracy'
        WHEN df.forecast_accuracy >= 70 THEN 'Medium Accuracy'
        ELSE 'Low Accuracy'
    END AS forecast_quality
FROM demand_forecast df
JOIN products p ON df.product_id = p.product_id;


CREATE OR REPLACE VIEW vw_reorder_intelligence AS
SELECT
    i.inventory_id,
    p.product_id,
    p.product_name,
    p.category,
    w.warehouse_id,
    w.warehouse_name,
    i.current_stock,
    i.reserved_stock,
    (i.current_stock - i.reserved_stock) AS available_stock,
    p.reorder_level,
    p.safety_stock,
    CASE
        WHEN (i.current_stock - i.reserved_stock) <= p.safety_stock
            THEN (p.reorder_level * 2) - (i.current_stock - i.reserved_stock)
        WHEN (i.current_stock - i.reserved_stock) <= p.reorder_level
            THEN p.reorder_level - (i.current_stock - i.reserved_stock)
        ELSE 0
    END AS recommended_reorder_quantity,
    CASE
        WHEN (i.current_stock - i.reserved_stock) <= p.safety_stock THEN 'High Priority'
        WHEN (i.current_stock - i.reserved_stock) <= p.reorder_level THEN 'Medium Priority'
        ELSE 'No Reorder Needed'
    END AS reorder_priority
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN warehouses w ON i.warehouse_id = w.warehouse_id;