DROP DATABASE food_delivery_db;
CREATE DATABASE food_delivery_db;
USE food_delivery_db;
CREATE TABLE food_orders (
    Order_ID VARCHAR(20) PRIMARY KEY,
    Customer_ID VARCHAR(20) ,
    Customer_Age INT,
    Customer_Gender VARCHAR(10),
    City VARCHAR(50),
    Area VARCHAR(50),
    Restaurant_ID VARCHAR(30),
    Restaurant_Name VARCHAR(100),
    Cuisine_Type VARCHAR(50),
    Order_Date DATE,
    Order_Time TIME,
  --   Order_DateTime datetime,
    Delivery_Time_Min INT,
    Distance_km DECIMAL(6,2),
    Order_Value DECIMAL(10,2),
    Discount_Applied DECIMAL(10,2),
    Final_Amount DECIMAL(10,2),
    Payment_Mode VARCHAR(20),
    Order_Status Varchar(20),
    Cancellation_Reason VARCHAR(100),
    Delivery_Partner_ID  VARCHAR(20),
    Delivery_Rating DECIMAL(3,2),
    Restaurant_Rating DECIMAL(3,2),
	Order_Day VARCHAR(15),
    Peak_Hour BOOLEAN,
    Profit_Margin DECIMAL(10,2),
    Day_Type VARCHAR(10),
    Profit_Margin_Pct DECIMAL(6,2),
    Delivery_Performance VARCHAR(15),
    Age_Group VARCHAR(10)
    
   
    
    
);

select * from food_orders;
 -- Customer & Order Analysis
--     Top-Spending Customers
SELECT Customer_ID,SUM(Final_Amount) AS Total_Spend
FROM food_orders
WHERE Order_Status = 'Completed'
GROUP BY Customer_ID
ORDER BY Total_Spend DESC
LIMIT 10;
-- Age Group vs Order Value
SELECT Age_Group,AVG(Order_Value) AS Avg_Order_Value
FROM food_orders
GROUP BY Age_Group;
-- Weekend vs Weekday Order Patterns
SELECT Day_Type,COUNT(*) AS Total_Orders,SUM(Final_Amount) AS Total_Revenue
FROM food_orders
GROUP BY Day_Type;
-- Revenue & Profit Analysis
-- Monthly Revenue Trends
SELECT Order_Date, AS Month,SUM(Final_Amount) AS Monthly_Revenue
FROM food_orders
WHERE Order_Status = 'Completed'
GROUP BY Month
ORDER BY Month;
-- Impact of Discounts on Profit
SELECT
    CASE
        WHEN Discount_Applied > 0 THEN 'Discounted'
        ELSE 'No Discount'
    END AS Discount_Type,
    AVG(Profit_Margin_Pct) AS Avg_Profit_Margin
FROM food_orders
GROUP BY Discount_Type;
-- High-Revenue Cities and Cuisine
SELECT City,
       Cuisine_Type,
       SUM(Final_Amount) AS Revenue
FROM food_orders
GROUP BY City, Cuisine_Type
ORDER BY Revenue DESC
LIMIT 10;

-- Delivery Performance
--  Average Delivery Time by City
SELECT City,
       AVG(Delivery_Time_Min) AS Avg_Delivery_Time
FROM food_orders
WHERE Order_Status = 'Completed'
GROUP BY City;
-- Distance vs Delivery Delay
SELECT Distance_km,AVG(Delivery_Time_Min) AS Avg_Delivery_Time
FROM food_orders
GROUP BY Distance_km
ORDER BY Distance_km;

-- Delivery Rating vs Delivery Time
SELECT Delivery_Performance,AVG(Delivery_Rating) AS Avg_Rating
FROM food_orders
GROUP BY Delivery_Performance;

-- Restaurant Performance
-- Top-Rated Restaurants
SELECT Restaurant_Name,AVG(Restaurant_Rating) AS Avg_Rating
FROM food_orders
GROUP BY Restaurant_Name
ORDER BY Avg_Rating DESC
LIMIT 10;

-- Cancellation Rate by Restaurant
SELECT Restaurant_Name,COUNT(CASE WHEN Order_Status='Cancelled' THEN 1 END) /COUNT(*) * 100 AS Cancellation_Rate
FROM food_orders
GROUP BY Restaurant_Name;
-- Cuisine-wise Performance
SELECT Cuisine_Type,COUNT(*) AS Total_Orders,SUM(Final_Amount) AS Revenue,AVG(Restaurant_Rating) AS Avg_Rating
FROM food_orders
GROUP BY Cuisine_Type;

-- Operational Insights
-- Payment Mode Preferences
SELECT Payment_Mode,COUNT(*) AS Usage_Count
FROM food_orders
GROUP BY Payment_Mode
ORDER BY Usage_Count DESC;
-- Cancellation Reason Analysis
SELECT Cancellation_Reason,COUNT(*) AS Cancellation_Count
FROM food_orders
WHERE Order_Status = 'Cancelled'
GROUP BY Cancellation_Reason
ORDER BY Cancellation_Count DESC;




































