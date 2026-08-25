-- ============================================================================
-- SCRIPT 02: DATA IMPORT VIA BULK INSERT (SSMS / SQL SERVER)
-- Project: Bird Species Observation Analysis
-- Database: BirdMonitoringDB
-- ============================================================================

USE BirdMonitoringDB;
GO

-- Optional: Truncate before loading if reloading data
-- TRUNCATE TABLE dbo.Bird_Observations;

/*
NOTE: If using BULK INSERT directly in SSMS, ensure the SQL Server service account
has read permissions to the file path below. Alternatively, run the Python loader:
`python load_data_to_sql.py`
*/

PRINT 'To load via SSMS BULK INSERT, uncomment and run the block below with your absolute path:';

/*
BULK INSERT dbo.Bird_Observations
FROM 'C:\Users\WELCOME\Desktop\LABMENTIX Project 3\bird_observations_cleaned.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK,
    KEEPNULLS
);
GO
*/
