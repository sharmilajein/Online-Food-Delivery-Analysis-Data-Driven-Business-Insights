import pandas as pd
import numpy as np
import mysql.connector
import streamlit as st
# import pandas as pd
from sqlalchemy import create_engine


df = pd.read_csv("/Users/jein/env/final_analytical_data.csv")

print(f"Dataframe has {len(df.columns)} columns")
# Convert Order date Format
df['Order_Date'] = df['Order_Date'].astype(str).str.replace(r'[^0-9/-]','', regex=True)
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format = 'mixed', errors='coerce')
df['Order_Date']  = df['Order_Date'].dt.strftime('%Y-%m-%d') 

df = df.replace({np.nan: None, 'NaT': None, '': None})
# df = df.replace({'': None})
# df['Order_Date'] = pd.to_datetime(df['Order_Date'], format = 'mixed', errors='coerce').dt.strftime('%Y-%m-&d')
data = [tuple(row) for row in df.values]

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root12345",
    database="food_delivery_db"
)

cursor = conn.cursor()

insert_query = """
INSERT INTO food_orders (
    `Order_ID`, `Customer_ID`, `Customer_Age`, `Customer_Gender`,
    `City`, `Area`, `Restaurant_ID`, `Restaurant_Name`, `Cuisine_Type`,
    `Order_Date`, `Order_Time`, `Delivery_Time_Min`, `Distance_km`, `Order_Value`,`Discount_Applied`,
    `Final_Amount`, `Payment_Mode` ,`Order_Status`, `Cancellation_Reason`,`Delivery_Partner_ID`,`Delivery_Rating`, `Restaurant_Rating`,
    `Order_Day`, `Peak_Hour` ,`Profit_Margin`, `Day_type` ,`Profit_Margin_Pct`, `Delivery_Performance`, `Age_Group`
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s ,%s)
"""

data = [tuple(row) for row in df.values]

cursor.executemany(insert_query, data)
conn.commit()

print(f"{cursor.rowcount} records inserted successfully")

cursor.close()
conn.close()


