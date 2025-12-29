import pandas as pd
import numpy as np

df = pd.read_csv("/Users/jein/env/ONINE_FOOD_DELIVERY_ANALYSIS.csv")


# Missing Values
df['Delivery_Time_Min'] = df['Delivery_Time_Min'].fillna(df['Delivery_Time_Min'].median())
df['Order_Value'] = df['Order_Value'].fillna(df['Order_Value'].median())
df['Payment_Mode'] = df['Payment_Mode'].fillna(df['Payment_Mode'].mode()[0])



# Outlier Capping (IQR)

for col in ['Delivery_Time_Min', 'Order_Value']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    df[col] = np.clip(df[col], Q1 - 1.5*IQR, Q3 + 1.5*IQR)


# Invalid Values

df['Delivery_Rating'] = df['Delivery_Rating'].clip(0, 5)
df['Restaurant_Rating'] = df['Restaurant_Rating'].clip(0, 5)
df = df[df['Profit_Margin'] >= 0]

df.loc[df['Order_Status'] == 'Cancelled',
       ['Delivery_Rating', 'Restaurant_Rating']] = np.nan

# Save cleaned data
df = df.to_csv("cleaned_data.csv", index=False)
