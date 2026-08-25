-- =========================================================
-- SQL Server Table DDL for Bird Species Observation Analysis
-- Target Database: BirdMonitoringDB
-- =========================================================

CREATE TABLE Bird_Observations_Cleaned (
    Observation_ID INT IDENTITY(1,1) PRIMARY KEY,
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
    Observation_Duration_Min DECIMAL(6,2) NULL,
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
    Temperature DECIMAL(5,2) NOT NULL,
    Humidity DECIMAL(5,2) NOT NULL,
    Sky VARCHAR(50) NOT NULL,
    Wind VARCHAR(100) NOT NULL,
    Disturbance VARCHAR(50) NOT NULL,
    Initial_Three_Min_Cnt BIT NOT NULL,
    Previously_Obs VARCHAR(20) NULL,
    Source_Sheet VARCHAR(20) NOT NULL,
    Created_At DATETIME DEFAULT GETDATE()
);

-- Indexing for Fast Querying in SQL / Streamlit Dashboard
CREATE INDEX IX_BirdObs_Habitat ON Bird_Observations_Cleaned(Habitat);
CREATE INDEX IX_BirdObs_Species ON Bird_Observations_Cleaned(Common_Name);
CREATE INDEX IX_BirdObs_AdminUnit ON Bird_Observations_Cleaned(Admin_Unit_Code);
CREATE INDEX IX_BirdObs_Date ON Bird_Observations_Cleaned([Date]);
CREATE INDEX IX_BirdObs_Conservation ON Bird_Observations_Cleaned(Conservation_Priority);
