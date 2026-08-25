-- ============================================================================
-- SCRIPT 03: ANALYTICAL SQL VIEWS
-- Project: Bird Species Observation Analysis
-- Database: BirdMonitoringDB
-- ============================================================================

USE BirdMonitoringDB;
GO

-- 1. View: Habitat Ecosystem Summary
IF OBJECT_ID(N'dbo.vw_Habitat_Summary', N'V') IS NOT NULL DROP VIEW dbo.vw_Habitat_Summary;
GO
CREATE VIEW dbo.vw_Habitat_Summary AS
SELECT 
    Habitat,
    COUNT(*) AS Total_Observations,
    COUNT(DISTINCT Common_Name) AS Unique_Species_Count,
    COUNT(DISTINCT Plot_Name) AS Unique_Plots_Count,
    COUNT(DISTINCT Admin_Unit_Code) AS Unique_Parks_Count,
    ROUND(AVG(Temperature), 2) AS Avg_Temperature_C,
    ROUND(AVG(Humidity), 2) AS Avg_Humidity_Pct,
    ROUND(CAST(COUNT(*) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM dbo.Bird_Observations), 2) AS Pct_Of_Total_Obs
FROM dbo.Bird_Observations
GROUP BY Habitat;
GO

-- 2. View: Species Distribution and Habitat Affinity
IF OBJECT_ID(N'dbo.vw_Species_Distribution', N'V') IS NOT NULL DROP VIEW dbo.vw_Species_Distribution;
GO
CREATE VIEW dbo.vw_Species_Distribution AS
SELECT 
    Common_Name,
    Scientific_Name,
    AOU_Code,
    COUNT(*) AS Total_Observations,
    SUM(CASE WHEN Habitat = 'Forest' THEN 1 ELSE 0 END) AS Forest_Observations,
    SUM(CASE WHEN Habitat = 'Grassland' THEN 1 ELSE 0 END) AS Grassland_Observations,
    COUNT(DISTINCT Plot_Name) AS Total_Plots_Recorded,
    COUNT(DISTINCT Admin_Unit_Code) AS Total_Parks_Recorded,
    MAX(CAST(PIF_Watchlist_Status AS INT)) AS Is_PIF_Watchlist,
    MAX(CAST(Regional_Stewardship_Status AS INT)) AS Is_Regional_Stewardship,
    CASE 
        WHEN SUM(CASE WHEN Habitat = 'Forest' THEN 1 ELSE 0 END) > 0 
         AND SUM(CASE WHEN Habitat = 'Grassland' THEN 1 ELSE 0 END) = 0 THEN 'Forest Only'
        WHEN SUM(CASE WHEN Habitat = 'Forest' THEN 1 ELSE 0 END) = 0 
         AND SUM(CASE WHEN Habitat = 'Grassland' THEN 1 ELSE 0 END) > 0 THEN 'Grassland Only'
        ELSE 'Both Habitats'
    END AS Habitat_Affinity
FROM dbo.Bird_Observations
GROUP BY Common_Name, Scientific_Name, AOU_Code;
GO

-- 3. View: Temporal Activity Summary (Monthly & Hourly)
IF OBJECT_ID(N'dbo.vw_Temporal_Trends', N'V') IS NOT NULL DROP VIEW dbo.vw_Temporal_Trends;
GO
CREATE VIEW dbo.vw_Temporal_Trends AS
SELECT 
    [Month],
    Month_Name,
    Observation_Hour,
    Habitat,
    COUNT(*) AS Observation_Count,
    COUNT(DISTINCT Common_Name) AS Species_Richness,
    ROUND(AVG(Temperature), 2) AS Avg_Temperature,
    ROUND(AVG(Humidity), 2) AS Avg_Humidity
FROM dbo.Bird_Observations
GROUP BY [Month], Month_Name, Observation_Hour, Habitat;
GO

-- 4. View: Administrative Unit & Plot Spatial Hotspots
IF OBJECT_ID(N'dbo.vw_Spatial_Hotspots', N'V') IS NOT NULL DROP VIEW dbo.vw_Spatial_Hotspots;
GO
CREATE VIEW dbo.vw_Spatial_Hotspots AS
SELECT 
    Admin_Unit_Code,
    Plot_Name,
    Location_Type,
    Habitat,
    COUNT(*) AS Total_Observations,
    COUNT(DISTINCT Common_Name) AS Species_Richness,
    SUM(CAST(PIF_Watchlist_Status AS INT)) AS Watchlist_Observations,
    SUM(CAST(Regional_Stewardship_Status AS INT)) AS Stewardship_Observations,
    ROUND(AVG(Temperature), 2) AS Avg_Temperature_C
FROM dbo.Bird_Observations
GROUP BY Admin_Unit_Code, Plot_Name, Location_Type, Habitat;
GO

-- 5. View: Conservation Priorities
IF OBJECT_ID(N'dbo.vw_Conservation_Priorities', N'V') IS NOT NULL DROP VIEW dbo.vw_Conservation_Priorities;
GO
CREATE VIEW dbo.vw_Conservation_Priorities AS
SELECT 
    Conservation_Priority,
    Habitat,
    Admin_Unit_Code,
    Common_Name,
    Scientific_Name,
    COUNT(*) AS Observation_Count,
    COUNT(DISTINCT Plot_Name) AS Plots_Recorded
FROM dbo.Bird_Observations
WHERE Conservation_Priority <> 'Standard / Secure'
GROUP BY Conservation_Priority, Habitat, Admin_Unit_Code, Common_Name, Scientific_Name;
GO

-- 6. View: Detection Modality and Behavioral Analysis
IF OBJECT_ID(N'dbo.vw_Behavior_Detection', N'V') IS NOT NULL DROP VIEW dbo.vw_Behavior_Detection;
GO
CREATE VIEW dbo.vw_Behavior_Detection AS
SELECT 
    ID_Method,
    Distance_Category,
    Flyover_Observed,
    Habitat,
    COUNT(*) AS Total_Observations,
    COUNT(DISTINCT Common_Name) AS Distinct_Species
FROM dbo.Bird_Observations
GROUP BY ID_Method, Distance_Category, Flyover_Observed, Habitat;
GO

PRINT 'Analytical Views created successfully.';
GO
