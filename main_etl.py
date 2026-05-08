import pandas as pd
from sqlalchemy import create_engine

# 1. EXTRACTION
df_premium = pd.read_csv('data/subscribers_premium.csv')
df_free = pd.read_xml('data/subscribers_free.xml')
df_gold = pd.read_json('data/subscribers_gold.JSON')
df_engagement = pd.read_excel('data/user_engagement_details.xlsx')
# For .txt files, check if they are comma-separated or tab-separated
df_standard = pd.read_csv('data/subscribers_standard.txt') 

# 2. TRANSFORMATION (Business Rules)
# Fix Premium Data
df_premium['Age'] = df_premium['Age'].fillna(25)
df_premium['UserID'] = df_premium['UserID'].fillna(method='bfill')
df_premium['Location'] = df_premium['Location'].fillna(method='ffill')
df_premium = df_premium.dropna(subset=['Subscription']).dropna(axis=1)

# Fix Standard Data[cite: 1]
df_standard['Location'] = df_standard['Location'].str.strip().str.replace(r'\s+', ' ', regex=True)
df_standard['Subscription'] = df_standard['Subscription'].str.strip().str.upper()

# Engagement Metrics[cite: 1]
df_engagement['PlaybackStarted'] = pd.to_datetime(df_engagement['PlaybackStarted'])
df_engagement['Quarter'] = df_engagement['PlaybackStarted'].dt.quarter

# 3. LOADING (Outputs)
# Save to Excel for specific requirement[cite: 1]
seattle_sf = df_premium[df_premium['Location'].isin(['Seattle', 'San Francisco'])]
seattle_sf.to_excel('output/seattle_sf_users.xlsx', index=False)

# Load to MySQL[cite: 1, 2]
engine = create_engine('mysql+mysqlconnector://user:password@localhost/db_name')
df_engagement.to_sql('user_engagement_data', con=engine, if_exists='replace')