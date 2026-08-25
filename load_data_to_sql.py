"""
Automated Data Loader from Cleaned CSV to SQL Server
Database: BirdMonitoringDB
Table: dbo.Bird_Observations
"""

import os
import pyodbc
import pandas as pd
import numpy as np

CSV_PATH = os.path.join(os.path.dirname(__file__), 'bird_observations_cleaned.csv')

print(f"Reading cleaned dataset from: {CSV_PATH}")
df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"Loaded DataFrame shape: {df.shape[0]:,} rows, {df.shape[1]} columns")

# Connect to SQL Server
connection_strings = [
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=BirdMonitoringDB;Trusted_Connection=yes;TrustServerCertificate=yes;",
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=BirdMonitoringDB;Trusted_Connection=yes;TrustServerCertificate=yes;",
    "DRIVER={SQL Server};SERVER=localhost;DATABASE=BirdMonitoringDB;Trusted_Connection=yes;"
]

conn = None
for conn_str in connection_strings:
    try:
        conn = pyodbc.connect(conn_str)
        print(f"Connected to SQL Server successfully using: {conn_str.split(';')[0]}")
        break
    except Exception:
        continue

if conn is None:
    raise Exception("Could not connect to SQL Server. Ensure the instance is running.")

cursor = conn.cursor()
cursor.fast_executemany = True

cursor.execute("TRUNCATE TABLE dbo.Bird_Observations")
conn.commit()

# Prepare clean data tuples
cols = [
    'Admin_Unit_Code', 'Sub_Unit_Code', 'Site_Name', 'Plot_Name', 'Location_Type', 'Habitat',
    'Year', 'Date', 'Start_Time', 'End_Time', 'Month', 'Month_Name', 'Day', 'Day_Of_Week',
    'Observation_Hour', 'Observation_Duration_Min', 'Season',
    'Observer', 'Visit', 'Interval_Length', 'ID_Method', 'Distance', 'Distance_Category', 'Distance_Standardized',
    'Flyover_Observed', 'Sex', 'Sex_Standardized',
    'Common_Name', 'Scientific_Name', 'AcceptedTSN', 'Taxon_Code', 'AOU_Code',
    'PIF_Watchlist_Status', 'Regional_Stewardship_Status', 'Conservation_Priority',
    'Temperature', 'Humidity', 'Sky', 'Wind', 'Disturbance', 'Initial_Three_Min_Cnt',
    'Previously_Obs', 'Source_Sheet'
]

cleaned_rows = []
for _, row in df[cols].iterrows():
    row_dict = row.to_dict()
    
    # Cast specific types
    accepted_tsn = int(row_dict['AcceptedTSN']) if pd.notna(row_dict['AcceptedTSN']) else None
    taxon_code = int(row_dict['Taxon_Code']) if pd.notna(row_dict['Taxon_Code']) else None
    obs_hour = int(row_dict['Observation_Hour']) if pd.notna(row_dict['Observation_Hour']) else None
    obs_dur = float(row_dict['Observation_Duration_Min']) if pd.notna(row_dict['Observation_Duration_Min']) else None
    temp = float(row_dict['Temperature']) if pd.notna(row_dict['Temperature']) else 0.0
    hum = float(row_dict['Humidity']) if pd.notna(row_dict['Humidity']) else 0.0
    
    t = (
        str(row_dict['Admin_Unit_Code']) if pd.notna(row_dict['Admin_Unit_Code']) else None,
        str(row_dict['Sub_Unit_Code']) if pd.notna(row_dict['Sub_Unit_Code']) else None,
        str(row_dict['Site_Name']) if pd.notna(row_dict['Site_Name']) else None,
        str(row_dict['Plot_Name']),
        str(row_dict['Location_Type']),
        str(row_dict['Habitat']),
        int(row_dict['Year']),
        str(row_dict['Date']),
        str(row_dict['Start_Time']),
        str(row_dict['End_Time']),
        int(row_dict['Month']),
        str(row_dict['Month_Name']),
        int(row_dict['Day']),
        str(row_dict['Day_Of_Week']),
        obs_hour,
        obs_dur,
        str(row_dict['Season']),
        str(row_dict['Observer']),
        int(row_dict['Visit']),
        str(row_dict['Interval_Length']),
        str(row_dict['ID_Method']),
        str(row_dict['Distance']) if pd.notna(row_dict['Distance']) else None,
        str(row_dict['Distance_Category']),
        str(row_dict['Distance_Standardized']),
        bool(row_dict['Flyover_Observed']),
        str(row_dict['Sex']) if pd.notna(row_dict['Sex']) else None,
        str(row_dict['Sex_Standardized']),
        str(row_dict['Common_Name']),
        str(row_dict['Scientific_Name']),
        accepted_tsn,
        taxon_code,
        str(row_dict['AOU_Code']),
        bool(row_dict['PIF_Watchlist_Status']),
        bool(row_dict['Regional_Stewardship_Status']),
        str(row_dict['Conservation_Priority']),
        temp,
        hum,
        str(row_dict['Sky']),
        str(row_dict['Wind']),
        str(row_dict['Disturbance']),
        bool(row_dict['Initial_Three_Min_Cnt']),
        str(row_dict['Previously_Obs']) if pd.notna(row_dict['Previously_Obs']) else None,
        str(row_dict['Source_Sheet'])
    )
    cleaned_rows.append(t)

insert_sql = """
INSERT INTO dbo.Bird_Observations (
    Admin_Unit_Code, Sub_Unit_Code, Site_Name, Plot_Name, Location_Type, Habitat,
    [Year], [Date], Start_Time, End_Time, [Month], Month_Name, [Day], Day_Of_Week,
    Observation_Hour, Observation_Duration_Min, Season,
    Observer, Visit, Interval_Length, ID_Method, Distance, Distance_Category, Distance_Standardized,
    Flyover_Observed, Sex, Sex_Standardized,
    Common_Name, Scientific_Name, AcceptedTSN, Taxon_Code, AOU_Code,
    PIF_Watchlist_Status, Regional_Stewardship_Status, Conservation_Priority,
    Temperature, Humidity, Sky, Wind, Disturbance, Initial_Three_Min_Cnt,
    Previously_Obs, Source_Sheet
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

print(f"Inserting {len(cleaned_rows):,} rows into SQL Server dbo.Bird_Observations...")
cursor.executemany(insert_sql, cleaned_rows)
conn.commit()

cursor.execute("SELECT COUNT(*) FROM dbo.Bird_Observations")
cnt = cursor.fetchone()[0]
print(f"SUCCESS: Database BirdMonitoringDB.dbo.Bird_Observations has {cnt:,} records loaded.")

cursor.close()
conn.close()
