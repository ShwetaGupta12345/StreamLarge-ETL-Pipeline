import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. EXTRACTION
df_premium = pd.read_csv('data/subscribers_premium.csv')
df_free = pd.read_xml('data/subscribers_free.xml')
df_gold = pd.read_json('data/subscribers_gold.JSON')
df_engagement = pd.read_excel('data/user_engagement_details.xlsx')
df_standard = pd.read_csv('data/subscribers_standard.txt') 

# 2. TRANSFORMATION (Business Rules)
df_premium['Age'] = df_premium['Age'].fillna(25)
df_premium['UserID'] = df_premium['UserID'].bfill()
df_premium['Location'] = df_premium['Location'].ffill()
df_premium = df_premium.dropna(subset=['Subscription']).dropna(axis=1)

df_standard['Location'] = df_standard['Location'].str.strip().str.replace(r'\s+', ' ', regex=True)
df_standard['Subscription'] = df_standard['Subscription'].str.strip().str.upper()

df_engagement['PlaybackStarted'] = pd.to_datetime(df_engagement['PlaybackStarted'])
df_engagement['Quarter'] = df_engagement['PlaybackStarted'].dt.quarter

# 3. LOADING (Outputs)
os.makedirs('output', exist_ok=True)

seattle_sf = df_premium[df_premium['Location'].isin(['Seattle', 'San Francisco'])]
seattle_sf.to_excel('output/seattle_sf_users.xlsx', index=False)

# Load to MySQL using environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')
df_engagement.to_sql('user_engagement_data', con=engine, if_exists='replace')
print("ETL process completed successfully!")