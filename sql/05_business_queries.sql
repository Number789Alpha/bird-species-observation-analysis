-- ============================================================================
-- SCRIPT 05: CORE BUSINESS & ECOLOGICAL ANALYTICAL QUERIES
-- Project: Bird Species Observation Analysis
-- Database: BirdMonitoringDB
-- ============================================================================

USE BirdMonitoringDB;
GO

-- ----------------------------------------------------------------------------
-- QUERY 1: OVERALL DATASET KPI SUMMARY
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS Total_Observations,
    COUNT(DISTINCT Common_Name) AS Total_Species,
    COUNT(DISTINCT Admin_Unit_Code) AS Total_Parks,
    COUNT(DISTINCT Plot_Name) AS Total_Plots,
    COUNT(DISTINCT Observer) AS Total_Observers,
    MIN([Date]) AS Earliest_Date,
    MAX([Date]) AS Latest_Date
FROM dbo.Bird_Observations;

-- ----------------------------------------------------------------------------
-- QUERY 2: HABITAT ECOSYSTEM COMPARISON (FOREST VS GRASSLAND)
-- ----------------------------------------------------------------------------
SELECT 
    Habitat,
    COUNT(*) AS Observation_Count,
    COUNT(DISTINCT Common_Name) AS Species_Richness,
    COUNT(DISTINCT Plot_Name) AS Plots_Surveyed,
    COUNT(DISTINCT Admin_Unit_Code) AS Parks_Covered,
    ROUND(AVG(Temperature), 2) AS Mean_Temperature_C,
    ROUND(AVG(Humidity), 2) AS Mean_Humidity_Pct,
    ROUND(CAST(COUNT(*) AS FLOAT) * 100.0 / (SELECT COUNT(*) FROM dbo.Bird_Observations), 2) AS Habitat_Share_Pct
FROM dbo.Bird_Observations
GROUP BY Habitat;

-- ----------------------------------------------------------------------------
-- QUERY 3: TOP 20 MOST FREQUENTLY OBSERVED BIRD SPECIES
-- ----------------------------------------------------------------------------
SELECT TOP 20
    Common_Name,
    Scientific_Name,
    AOU_Code,
    Habitat_Affinity,
    Total_Observations,
    Forest_Observations,
    Grassland_Observations,
    Total_Plots_Recorded,
    Is_PIF_Watchlist
FROM dbo.vw_Species_Distribution
ORDER BY Total_Observations DESC;

-- ----------------------------------------------------------------------------
-- QUERY 4: HABITAT SPECIALISTS (FOREST-ONLY VS GRASSLAND-ONLY SPECIES)
-- ----------------------------------------------------------------------------
-- 4A. Forest-Only Species
SELECT 
    Common_Name,
    Scientific_Name,
    AOU_Code,
    Total_Observations AS Forest_Obs_Count,
    Total_Plots_Recorded,
    Is_PIF_Watchlist
FROM dbo.vw_Species_Distribution
WHERE Habitat_Affinity = 'Forest Only'
ORDER BY Total_Observations DESC;

-- 4B. Grassland-Only Species
SELECT 
    Common_Name,
    Scientific_Name,
    AOU_Code,
    Total_Observations AS Grassland_Obs_Count,
    Total_Plots_Recorded,
    Is_PIF_Watchlist
FROM dbo.vw_Species_Distribution
WHERE Habitat_Affinity = 'Grassland Only'
ORDER BY Total_Observations DESC;

-- ----------------------------------------------------------------------------
-- QUERY 5: TEMPORAL DISTRIBUTION (MONTHLY & DIURNAL HOURLY PATTERNS)
-- ----------------------------------------------------------------------------
-- 5A. Monthly Trends
SELECT 
    [Month],
    Month_Name,
    COUNT(*) AS Total_Observations,
    SUM(CASE WHEN Habitat = 'Forest' THEN 1 ELSE 0 END) AS Forest_Obs,
    SUM(CASE WHEN Habitat = 'Grassland' THEN 1 ELSE 0 END) AS Grassland_Obs,
    COUNT(DISTINCT Common_Name) AS Monthly_Species_Richness
FROM dbo.Bird_Observations
GROUP BY [Month], Month_Name
ORDER BY [Month];

-- 5B. Hourly Activity Profile
SELECT 
    Observation_Hour,
    COUNT(*) AS Observations,
    COUNT(DISTINCT Common_Name) AS Species_Detected,
    ROUND(AVG(Temperature), 1) AS Avg_Temp_C
FROM dbo.Bird_Observations
WHERE Observation_Hour IS NOT NULL
GROUP BY Observation_Hour
ORDER BY Observation_Hour;

-- ----------------------------------------------------------------------------
-- QUERY 6: SPATIAL HOTSPOT RANKING BY ADMINISTRATIVE UNIT & PLOT
-- ----------------------------------------------------------------------------
-- Top 10 High-Density Plots (Using DENSE_RANK)
WITH PlotRankings AS (
    SELECT 
        Plot_Name,
        Admin_Unit_Code,
        Habitat,
        COUNT(*) AS Total_Observations,
        COUNT(DISTINCT Common_Name) AS Species_Richness,
        SUM(CAST(PIF_Watchlist_Status AS INT)) AS Watchlist_Observations,
        DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT Common_Name) DESC, COUNT(*) DESC) AS Biodiversity_Rank
    FROM dbo.Bird_Observations
    GROUP BY Plot_Name, Admin_Unit_Code, Habitat
)
SELECT * 
FROM PlotRankings 
WHERE Biodiversity_Rank <= 10
ORDER BY Biodiversity_Rank;

-- ----------------------------------------------------------------------------
-- QUERY 7: ENVIRONMENTAL CORRELATIONS & DETECTION MODES
-- ----------------------------------------------------------------------------
-- Detection Method Breakdown by Sky Condition
SELECT 
    Sky,
    ID_Method,
    COUNT(*) AS Observation_Count,
    ROUND(AVG(Temperature), 1) AS Avg_Temperature,
    ROUND(AVG(Humidity), 1) AS Avg_Humidity
FROM dbo.Bird_Observations
GROUP BY Sky, ID_Method
ORDER BY Sky, Observation_Count DESC;

-- ----------------------------------------------------------------------------
-- QUERY 8: CONSERVATION PRIORITIES & VULNERABLE SPECIES SUMMARY
-- ----------------------------------------------------------------------------
SELECT 
    Conservation_Priority,
    Habitat,
    COUNT(*) AS Observation_Count,
    COUNT(DISTINCT Common_Name) AS Species_Count,
    COUNT(DISTINCT Plot_Name) AS Plots_With_At_Risk_Birds
FROM dbo.Bird_Observations
GROUP BY Conservation_Priority, Habitat
ORDER BY Observation_Count DESC;
GO
