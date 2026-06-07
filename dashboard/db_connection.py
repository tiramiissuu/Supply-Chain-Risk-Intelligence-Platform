import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="supply_chain_risk_intelligence"
    )