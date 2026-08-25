-- ============================================================================
-- SCRIPT 01: DATABASE CREATION & SCHEMA DEFINITION
-- Project: Bird Species Observation Analysis
-- Target Engine: Microsoft SQL Server 2019 / 2022 / Azure SQL
-- Database: BirdMonitoringDB
-- ============================================================================

USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'BirdMonitoringDB')
BEGIN
    CREATE DATABASE BirdMonitoringDB;
    PRINT 'Database [BirdMonitoringDB] created successfully.';
END
GO

USE BirdMonitoringDB;
GO

IF OBJECT_ID(N'dbo.Bird_Observations', N'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.Bird_Observations;
    PRINT 'Existing table [dbo.Bird_Observations] dropped.';
END
GO

CREATE TABLE dbo.Bird_Observations (
    Observation_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,
    Admin_Unit_Code VARCHAR(10) NOT NULL,
    Sub_Unit_Code VARCHAR(50) NULL,
    Site_Name VARCHAR(100) NULL,
    Plot_Name VARCHAR(50) NOT NULL,
    Location_Type VARCHAR(50) NOT NULL,
    Habitat VARCHAR(20) NOT NULL,
    [Year] INT NOT NULL,
    [Date] DATE NOT NULL,
    Start_Time VARCHAR(8) NOT NULL,
    End_Time VARCHAR(8) NOT NULL,
    [Month] INT NOT NULL,
    Month_Name VARCHAR(20) NOT NULL,
    [Day] INT NOT NULL,
    Day_Of_Week VARCHAR(20) NOT NULL,
    Observation_Hour INT NULL,
    Observation_Duration_Min FLOAT NULL,
    Season VARCHAR(50) NOT NULL,
    Observer VARCHAR(50) NOT NULL,
    Visit INT NOT NULL,
    Interval_Length VARCHAR(20) NOT NULL,
    ID_Method VARCHAR(50) NOT NULL,
    Distance VARCHAR(50) NULL,
    Distance_Category VARCHAR(50) NOT NULL,
    Distance_Standardized VARCHAR(50) NOT NULL,
    Flyover_Observed BIT NOT NULL,
    Sex VARCHAR(20) NULL,
    Sex_Standardized VARCHAR(20) NOT NULL,
    Common_Name VARCHAR(100) NOT NULL,
    Scientific_Name VARCHAR(100) NOT NULL,
    AcceptedTSN BIGINT NULL,
    Taxon_Code BIGINT NULL,
    AOU_Code VARCHAR(10) NOT NULL,
    PIF_Watchlist_Status BIT NOT NULL,
    Regional_Stewardship_Status BIT NOT NULL,
    Conservation_Priority VARCHAR(100) NOT NULL,
    Temperature FLOAT NOT NULL,
    Humidity FLOAT NOT NULL,
    Sky VARCHAR(50) NOT NULL,
    Wind VARCHAR(100) NOT NULL,
    Disturbance VARCHAR(50) NOT NULL,
    Initial_Three_Min_Cnt BIT NOT NULL,
    Previously_Obs VARCHAR(20) NULL,
    Source_Sheet VARCHAR(20) NOT NULL,
    Created_At DATETIME DEFAULT GETDATE()
);
GO

CREATE NONCLUSTERED INDEX IX_BirdObs_Habitat 
    ON dbo.Bird_Observations (Habitat) 
    INCLUDE (Common_Name, Admin_Unit_Code, [Date]);

CREATE NONCLUSTERED INDEX IX_BirdObs_CommonName 
    ON dbo.Bird_Observations (Common_Name) 
    INCLUDE (Habitat, Scientific_Name, AOU_Code);

CREATE NONCLUSTERED INDEX IX_BirdObs_AdminUnit 
    ON dbo.Bird_Observations (Admin_Unit_Code) 
    INCLUDE (Plot_Name, Habitat, Common_Name);

CREATE NONCLUSTERED INDEX IX_BirdObs_Date_Month 
    ON dbo.Bird_Observations ([Date], [Month], Observation_Hour);

CREATE NONCLUSTERED INDEX IX_BirdObs_Conservation 
    ON dbo.Bird_Observations (Conservation_Priority, PIF_Watchlist_Status, Regional_Stewardship_Status) 
    INCLUDE (Common_Name, Habitat, Admin_Unit_Code);

PRINT 'Table [dbo.Bird_Observations] and indexes created successfully.';
GO
