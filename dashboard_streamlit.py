import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


# PAGE CONFIG
st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    layout="wide"
)

st.title("🍔 Online Food Delivery – Business KPI Dashboard")
st.markdown("Real-time analytics from MySQL database")


# MYSQL CONNECTION

engine = create_engine(
    "mysql+pymysql://root:root12345@localhost/food_delivery_db"
)
# FETCH SQL

def run_query(sql: str):
    try:
        df = pd.read_sql(sql, engine)
        return df
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
        return pd.DataFrame()
# Load Data
@st.cache_data
def load_data():
    query = "SELECT * FROM food_orders"
    return pd.read_sql(query, engine)

df = load_data()

# FILTERS
st.sidebar.header("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    options=df['City'].unique(),
    default=df['City'].unique()
)

cuisine_filter = st.sidebar.multiselect(
    "Select Cuisine",
    options=df['Cuisine_Type'].unique(),
    default=df['Cuisine_Type'].unique()
)

status_filter = st.sidebar.multiselect(
    "Order Status",
    options=df['Order_Status'].unique(),
    default=df['Order_Status'].unique()
)

filtered_df = df[
    (df['City'].isin(city_filter)) &
    (df['Cuisine_Type'].isin(cuisine_filter)) &
    (df['Order_Status'].isin(status_filter))
]


# KPI CALCULATIONS

total_orders = filtered_df.shape[0]

total_revenue = filtered_df.loc[
    filtered_df['Order_Status'] == 'Completed',
    'Final_Amount'
].sum()

avg_order_value = filtered_df.loc[
    filtered_df['Order_Status'] == 'Completed',
    'Final_Amount'
].mean()

avg_delivery_time = filtered_df.loc[
    filtered_df['Order_Status'] == 'Completed',
    'Delivery_Time_Min'
].mean()

cancellation_rate = (
    filtered_df['Order_Status'].eq('Cancelled').mean() * 100
)

avg_delivery_rating = filtered_df['Delivery_Rating'].mean()

profit_margin_pct = filtered_df.loc[
    filtered_df['Order_Status'] == 'Completed',
    'Profit_Margin_Pct'
].mean()


# KPI DISPLAY

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
col3.metric("Avg Order Value", f"₹ {avg_order_value:.2f}")
col4.metric("Avg Delivery Time", f"{avg_delivery_time:.2f} mins")

col5, col6, col7 = st.columns(3)

col5.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
col6.metric("Avg Delivery Rating", f"{avg_delivery_rating:.2f}")
col7.metric("Profit Margin %", f"{profit_margin_pct:.2f}%")


# ADVANCED QUERIES


st.header("Advanced insights")


query_options = {
    " Top-Spending Customers" : "SELECT Customer_ID,SUM(Final_Amount) AS Total_Spend FROM food_orders WHERE Order_Status = 'Completed' GROUP BY Customer_ID ORDER BY Total_Spend DESC LIMIT 10",
    "Age Group vs Order Value" : "SELECT Age_Group,AVG(Order_Value) AS Avg_Order_Value FROM food_orders GROUP BY Age_Group",
    "Weekend vs Weekday Order Patterns": "SELECT Day_Type,COUNT(*) AS Total_Orders,SUM(Final_Amount) AS Total_Revenue FROM food_orders GROUP BY Day_Type",
    "Monthly Revenue Trends" : "SELECT Order_Date, AS Month,SUM(Final_Amount) AS Monthly_Revenue FROM food_orders WHERE Order_Status = 'Completed' GROUP BY Month ORDER BY Month",
    "Impact of Discounts on Profit" : "SELECT CASE WHEN Discount_Applied > 0 THEN 'Discounted' ELSE 'No Discount'END AS Discount_Type,AVG(Profit_Margin_Pct) AS Avg_Profit_Margin FROM food_orders GROUP BY Discount_Type",
    "High-Revenue Cities and Cuisine" : "SELECT City,Cuisine_Type,SUM(Final_Amount) AS Revenue FROM food_orders GROUP BY City Cuisine_Type ORDER BY Revenue DESC LIMIT 10",
    "Average Delivery Time by City"   : "SELECT City,AVG(Delivery_Time_Min) AS Avg_Delivery_Time FROM food_orders WHERE Order_Status = 'Completed' GROUP BY City",
    "Distance vs Delivery Delay"      : "SELECT Distance_km,AVG(Delivery_Time_Min) AS Avg_Delivery_Time FROM food_orders GROUP BY Distance_km ORDER BY Distance_km",
    "Delivery Rating vs Delivery Time": "SELECT Delivery_Performance,AVG(Delivery_Rating) AS Avg_Rating FROM food_orders GROUP BY Delivery_Performance",
    "Top-Rated Restaurants"           : "SELECT Restaurant_Name,AVG(Restaurant_Rating) AS Avg_Rating FROM food_orders GROUP BY Restaurant_Name ORDER BY Avg_Rating DESC LIMIT 10",
    "Cancellation Rate by Restaurant" : "SELECT Restaurant_Name,COUNT(CASE WHEN Order_Status='Cancelled' THEN 1 END) /COUNT(*) * 100 AS Cancellation_Rate FROM food_orders GROUP BY Restaurant_Name",
    "Cuisine-wise Performance"        : "SELECT Cuisine_Type,COUNT(*) AS Total_Orders,SUM(Final_Amount) AS Revenue,AVG(Restaurant_Rating) AS Avg_Rating FROM food_orders GROUP BY Cuisine_Type",
    "Payment Mode Preferences"        : "SELECT Payment_Mode,COUNT(*) AS Usage_Count FROM food_orders GROUP BY Payment_Mode ORDER BY Usage_Count DESC",
    "Cancellation Reason Analysis"    : "SELECT Cancellation_Reason,COUNT(*) AS Cancellation_Count FROM food_orders WHERE Order_Status = 'Cancelled'GROUP BY Cancellation_Reason ORDER BY Cancellation_Count DESC",
    
}

selected_query = st.selectbox("Choose a Query", list(query_options.keys()))

if st.button("Run Query"):
    sql = query_options[selected_query]
    result = run_query(sql)

    if result.empty:
        st.warning("No records found.")
    else:
        st.success("Query executed successfully.")
        st.dataframe(result)





# DATA PREVIEW

st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered_df.head(100))

st.markdown("---")
st.markdown("✅ **Data Source:** MySQL | **Built with:** Streamlit & Python")
