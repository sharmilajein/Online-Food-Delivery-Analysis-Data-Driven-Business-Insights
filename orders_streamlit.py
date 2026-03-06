import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    layout="wide"
)


st.title("🍔 Online Food Delivery – Enterprise Analytics Dashboard")
st.markdown("Real-time analytics from MySQL database")

# =====================================
# DATABASE CONNECTION
# =====================================
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
@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM food_orders", engine)

    # Safe datatype conversions
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    numeric_cols = ["Order_Value", "Final_Amount",
                    "Delivery_Time_Min", "Profit_Margin_Pct"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# =====================================
# SIDEBAR FILTERS
# =====================================
st.sidebar.header("🔎 Filters")

city = st.sidebar.multiselect(
    "City",
    df["City"].dropna().unique(),
    default=df["City"].dropna().unique()
)

cuisine = st.sidebar.multiselect(
    "Cuisine",
    df["Cuisine_Type"].dropna().unique(),
    default=df["Cuisine_Type"].dropna().unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order_Date"].min(), df["Order_Date"].max()]
)

filtered_df = df[
    (df["City"].isin(city)) &
    (df["Cuisine_Type"].isin(cuisine)) &
    (df["Order_Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order_Date"] <= pd.to_datetime(date_range[1]))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# =====================================
# TABS
# =====================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive KPI,s",
    "💰 Revenue",
    "🚚 Delivery",
    "⚙ Operations"
])

# =====================================
# TAB 1 – EXECUTIVE
# =====================================


with tab1:

    st.subheader("Executive KPIs")

    
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", f"{filtered_df.shape[0]:,}")
    col2.metric("Total Revenue", f"₹ {filtered_df['Final_Amount'].sum():,.0f}")
    col3.metric("Avg Order Value", f"₹ {filtered_df['Final_Amount'].mean():.2f}")
    col4.metric("Cancellation Rate",
                f"{(filtered_df['Order_Status']=='Cancelled').mean()*100:.2f}%")

    col5, col6 = st.columns(2)

    col5.metric("Avg Delivery Time",
                f"{filtered_df['Delivery_Time_Min'].mean():.2f} mins")
    col6.metric("Profit Margin %",
                f"{filtered_df['Profit_Margin_Pct'].mean():.2f}%")
   


    st.markdown("---")
    
    # ADVANCED QUERIES


    st.header("Advanced insights")


    query_options = {
        " Top-Spending Customers" : "SELECT Customer_ID,SUM(Final_Amount) AS Total_Spend FROM food_orders WHERE Order_Status = 'Completed' GROUP BY Customer_ID ORDER BY Total_Spend DESC LIMIT 10",
        "Age Group vs Order Value" : "SELECT Age_Group,AVG(Order_Value) AS Avg_Order_Value FROM food_orders GROUP BY Age_Group",
        "Weekday Order Patterns"        : "SELECT Day_Type,COUNT(*) AS Total_Orders,SUM(Final_Amount) AS Total_Revenue FROM food_orders GROUP BY Day_Type",
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
    df_new=pd.read_csv("/Users/jein/env/env/online_food_delivery/final_analytical_data.csv")
    st.subheader("📄 Filtered Data Preview")
    st.dataframe(df_new.head(23))

st.markdown("---")


# =====================================
# TAB 2 – REVENUE ANALYTICS
# =====================================
with tab2:
    
    st.subheader("Monthly Revenue Trend")

    filtered_df["Month"] = filtered_df["Order_Date"].dt.to_period("M")
    monthly = filtered_df.groupby("Month")["Final_Amount"].sum().reset_index()
    monthly["Month"] = monthly["Month"].astype(str)

    fig = px.line(monthly, x="Month", y="Final_Amount",
                  markers=True, template="plotly_white")
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.info("Insight: Revenue trend reveals seasonal patterns and peak demand cycles.")

    st.subheader("Revenue by City")

    city_rev = df_new.groupby("City")["Final_Amount"].sum().reset_index()
    fig_city = px.bar(city_rev, x="City", y="Final_Amount",
                      template="plotly_white")
    fig_city.update_layout(height=450)
    st.plotly_chart(fig_city, use_container_width=True)

    st.info("Insight: A few cities contribute majority of platform revenue.")

    st.subheader("Revenue by Cuisine")

    cuisine_rev = df_new.groupby("Cuisine_Type")["Final_Amount"].sum().reset_index()
    fig_cuisine = px.pie(cuisine_rev, values="Final_Amount",
                         names="Cuisine_Type", hole=0.4)
    st.plotly_chart(fig_cuisine, use_container_width=True)

    st.info("Insight: Popular cuisines dominate revenue share.")

    st.subheader("Weekend vs Weekday Revenue")

    weekend = df_new.groupby("Day_Type")["Final_Amount"].sum().reset_index()
    fig_weekend = px.bar(weekend, x="Day_Type", y="Final_Amount",
                         template="plotly_white")
    st.plotly_chart(fig_weekend, use_container_width=True)
    st.info("Insight: Weekday has high revenue")

# =====================================
# TAB 3 – DELIVERY PERFORMANCE
# =====================================
with tab3:

    st.subheader("Distance vs Delivery Time")

    safe_df = filtered_df.dropna(subset=["Distance_km", "Delivery_Time_Min"])

    fig_delivery = px.scatter(safe_df,
                              x="Distance_km",
                              y="Delivery_Time_Min",
                              opacity=0.4,
                              template="plotly_white")
    st.plotly_chart(fig_delivery, use_container_width=True)

    st.info("Insight: Delivery time increases with distance but operational inefficiencies may exist.")

    st.subheader("Delivery Performance Categories")

    perf = filtered_df["Delivery_Performance"].value_counts().reset_index()
    perf.columns = ["Category", "Count"]

    fig_perf = px.bar(perf, x="Category", y="Count",
                      template="plotly_white")
    st.plotly_chart(fig_perf, use_container_width=True)
    st.info("Insight:Helps identify delayed deliveries\nSupports delivery performance analysis")
    

# =====================================
# TAB 4 – OPERATIONS
# =====================================
with tab4:
   
    st.subheader("Cancellation Reasons")

    cancel_df = df_new[df_new["Order_Status"] == "Cancelled"]
    cancel_reason = cancel_df["Cancellation_Reason"].value_counts().reset_index()
    cancel_reason.columns = ["Reason", "Count"]

    fig_cancel = px.bar(cancel_reason, x="Reason", y="Count",
                        template="plotly_white")
    st.plotly_chart(fig_cancel, use_container_width=True)

    st.info("Insight: Majority cancellations occur due to delivery delays and peak-hour congestion.")
    

    st.subheader("Payment Mode Preference")

    payment = df_new["Payment_Mode"].value_counts().reset_index()
    payment.columns = ["Payment_Mode", "Count"]

    fig_payment = px.pie(payment, values="Count",
                         names="Payment_Mode", hole=0.4)
    st.plotly_chart(fig_payment, use_container_width=True)