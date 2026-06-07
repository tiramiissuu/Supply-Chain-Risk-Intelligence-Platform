import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="230623",
        database="supply_chain_risk_intelligence"
    )