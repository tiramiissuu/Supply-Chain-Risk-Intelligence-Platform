from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

output_file = "database/02_sample_data.sql"

with open(output_file, "w", encoding="utf-8") as f:

    f.write("USE supply_chain_risk_intelligence;\n\n")

    # -------------------------
    # SUPPLIERS
    # -------------------------

    supplier_count = 50

    for i in range(1, supplier_count + 1):
        name = fake.company().replace("'", "")
        country = fake.country().replace("'", "")
        reliability = round(random.uniform(60, 99), 2)
        lead_time = random.randint(2, 30)
        defect_rate = round(random.uniform(0.5, 10), 2)

        f.write(
            f"INSERT INTO suppliers "
            f"(supplier_name,country,reliability_score,avg_lead_time_days,defect_rate) "
            f"VALUES "
            f"('{name}','{country}',{reliability},{lead_time},{defect_rate});\n"
        )

    f.write("\n")

    # -------------------------
    # WAREHOUSES
    # -------------------------

    warehouse_count = 20

    for i in range(1, warehouse_count + 1):
        warehouse = f"Warehouse_{i}"
        city = fake.city().replace("'", "")
        capacity = random.randint(5000, 50000)

        f.write(
            f"INSERT INTO warehouses "
            f"(warehouse_name,city,capacity_units) "
            f"VALUES "
            f"('{warehouse}','{city}',{capacity});\n"
        )

    f.write("\n")

    # -------------------------
    # PRODUCTS
    # -------------------------

    categories = [
        "Electronics",
        "Medical",
        "Automotive",
        "Food",
        "Industrial",
        "Consumer Goods"
    ]

    product_count = 500

    for i in range(1, product_count + 1):

        product_name = f"Product_{i}"

        category = random.choice(categories)

        unit_price = round(random.uniform(10, 5000), 2)

        reorder_level = random.randint(50, 300)

        safety_stock = random.randint(20, reorder_level)

        supplier_id = random.randint(1, supplier_count)

        f.write(
            f"INSERT INTO products "
            f"(product_name,category,unit_price,reorder_level,safety_stock,supplier_id) "
            f"VALUES "
            f"('{product_name}','{category}',{unit_price},{reorder_level},{safety_stock},{supplier_id});\n"
        )

    f.write("\n")

    # -------------------------
    # INVENTORY
    # -------------------------

    inventory_count = 5000

    for i in range(inventory_count):

        product_id = random.randint(1, product_count)

        warehouse_id = random.randint(1, warehouse_count)

        stock = random.randint(0, 2000)

        reserved = random.randint(0, min(stock, 500))

        date = fake.date_between(
            start_date="-90d",
            end_date="today"
        )

        f.write(
            f"INSERT INTO inventory "
            f"(product_id,warehouse_id,current_stock,reserved_stock,last_updated) "
            f"VALUES "
            f"({product_id},{warehouse_id},{stock},{reserved},'{date}');\n"
        )

    f.write("\n")

    # -------------------------
    # ORDERS
    # -------------------------

    regions = [
        "North",
        "South",
        "East",
        "West",
        "Central"
    ]

    order_count = 10000

    for i in range(1, order_count + 1):

        order_date = fake.date_between(
            start_date="-365d",
            end_date="today"
        )

        expected = order_date + timedelta(
            days=random.randint(2, 10)
        )

        status = random.choice([
            "Delivered",
            "Shipped",
            "Processing"
        ])

        region = random.choice(regions)

        f.write(
            f"INSERT INTO orders "
            f"(customer_region,order_date,expected_delivery_date,status) "
            f"VALUES "
            f"('{region}','{order_date}','{expected}','{status}');\n"
        )

    f.write("\n")

    # -------------------------
    # ORDER ITEMS
    # -------------------------

    order_item_count = 25000

    for i in range(order_item_count):

        order_id = random.randint(1, order_count)

        product_id = random.randint(1, product_count)

        quantity = random.randint(1, 50)

        price = round(
            random.uniform(10, 5000),
            2
        )

        f.write(
            f"INSERT INTO order_items "
            f"(order_id,product_id,quantity,selling_price) "
            f"VALUES "
            f"({order_id},{product_id},{quantity},{price});\n"
        )

    f.write("\n")

    # -------------------------
    # SHIPMENTS
    # -------------------------

    carriers = [
        "DHL",
        "FedEx",
        "UPS",
        "BlueDart",
        "Delhivery"
    ]

    shipment_count = 10000

    for i in range(1, shipment_count + 1):

        order_id = random.randint(1, order_count)

        warehouse_id = random.randint(1, warehouse_count)

        ship_date = fake.date_between(
            start_date="-365d",
            end_date="today"
        )

        delivery = ship_date + timedelta(
            days=random.randint(1, 15)
        )

        cost = round(
            random.uniform(50, 2000),
            2
        )

        carrier = random.choice(carriers)

        status = random.choice([
            "Delivered",
            "In Transit",
            "Delayed"
        ])

        f.write(
            f"INSERT INTO shipments "
            f"(order_id,warehouse_id,shipment_date,delivery_date,carrier,shipment_status,shipping_cost) "
            f"VALUES "
            f"({order_id},{warehouse_id},'{ship_date}','{delivery}','{carrier}','{status}',{cost});\n"
        )

    f.write("\n")

    # -------------------------
    # DEMAND FORECAST
    # -------------------------

    for i in range(2000):

        product_id = random.randint(1, product_count)

        predicted = random.randint(100, 5000)

        actual = random.randint(100, 5000)

        accuracy = round(
            (1 - abs(predicted - actual) / max(predicted, actual)) * 100,
            2
        )

        month = random.choice([
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ])

        f.write(
            f"INSERT INTO demand_forecast "
            f"(product_id,forecast_month,predicted_demand,actual_demand,forecast_accuracy) "
            f"VALUES "
            f"({product_id},'{month}',{predicted},{actual},{accuracy});\n"
        )

    f.write("\n")

    # -------------------------
    # SUPPLIER RISK
    # -------------------------

    for supplier_id in range(1, supplier_count + 1):

        score = round(
            random.uniform(10, 100),
            2
        )

        if score >= 75:
            level = "High"
        elif score >= 40:
            level = "Medium"
        else:
            level = "Low"

        category = random.choice([
            "Financial",
            "Operational",
            "Geopolitical",
            "Quality"
        ])

        f.write(
            f"INSERT INTO supplier_risk "
            f"(supplier_id,risk_category,risk_score,risk_level,remarks) "
            f"VALUES "
            f"({supplier_id},'{category}',{score},'{level}','Auto Generated');\n"
        )

print("Data generation completed successfully.")