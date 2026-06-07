CREATE DATABASE IF NOT EXISTS supply_chain_risk_intelligence;
USE supply_chain_risk_intelligence;

DROP TABLE IF EXISTS reorder_recommendations;
DROP TABLE IF EXISTS supplier_risk;
DROP TABLE IF EXISTS demand_forecast;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS suppliers;

CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    reliability_score DECIMAL(5,2),
    avg_lead_time_days INT,
    defect_rate DECIMAL(5,2)
);

CREATE TABLE warehouses (
    warehouse_id INT PRIMARY KEY AUTO_INCREMENT,
    warehouse_name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    capacity_units INT
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_price DECIMAL(10,2),
    reorder_level INT,
    safety_stock INT,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    warehouse_id INT,
    current_stock INT,
    reserved_stock INT,
    last_updated DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_region VARCHAR(50),
    order_date DATE,
    expected_delivery_date DATE,
    status VARCHAR(30)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    selling_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE shipments (
    shipment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    warehouse_id INT,
    shipment_date DATE,
    delivery_date DATE,
    carrier VARCHAR(50),
    shipment_status VARCHAR(30),
    shipping_cost DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

CREATE TABLE demand_forecast (
    forecast_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    forecast_month VARCHAR(20),
    predicted_demand INT,
    actual_demand INT,
    forecast_accuracy DECIMAL(5,2),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE supplier_risk (
    risk_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_id INT,
    risk_category VARCHAR(50),
    risk_score DECIMAL(5,2),
    risk_level VARCHAR(20),
    remarks TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE reorder_recommendations (
    recommendation_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    warehouse_id INT,
    current_stock INT,
    reorder_level INT,
    recommended_quantity INT,
    priority_level VARCHAR(20),
    recommendation_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);