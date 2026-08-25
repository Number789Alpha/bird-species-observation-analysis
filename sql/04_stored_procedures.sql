-- ============================================================================
-- SCRIPT 04: PARAMETERIZED STORED PROCEDURES
-- Project: Bird Species Observation Analysis
-- Database: BirdMonitoringDB
-- ============================================================================

USE BirdMonitoringDB;
GO

-- 1. Procedure: Get Species Breakdown by Habitat
IF OBJECT_ID(N'dbo.sp_GetSpeciesByHabitat', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_GetSpeciesByHabitat;
GO
CREATE PROCEDURE dbo.sp_GetSpeciesByHabitat
    @HabitatFilter VARCHAR(20) = 'ALL',
    @TopN INT = 20
AS
BEGIN
    SET NOCOUNT ON;
    
    IF @HabitatFilter = 'ALL'
    BEGIN
        SELECT TOP (@TopN)
            Common_Name,
            Scientific_Name,
            AOU_Code,
            Habitat_Affinity,
            Total_Observations,
            Forest_Observations,
            Grassland_Observations,
            Total_Plots_Recorded,
            Is_PIF_Watchlist,
            Is_Regional_Stewardship
        FROM dbo.vw_Species_Distribution
        ORDER BY Total_Observations DESC;
    END
    ELSE
    BEGIN
        SELECT TOP (@TopN)
            Common_Name,
            Scientific_Name,
            AOU_Code,
            Habitat_Affinity,
            CASE WHEN @HabitatFilter = 'Forest' THEN Forest_Observations ELSE Grassland_Observations END AS Habitat_Specific_Observations,
            Total_Observations,
            Total_Plots_Recorded,
            Is_PIF_Watchlist,
            Is_Regional_Stewardship
        FROM dbo.vw_Species_Distribution
        WHERE (@HabitatFilter = 'Forest' AND Forest_Observations > 0)
           OR (@HabitatFilter = 'Grassland' AND Grassland_Observations > 0)
        ORDER BY CASE WHEN @HabitatFilter = 'Forest' THEN Forest_Observations ELSE Grassland_Observations END DESC;
    END
END;
GO

-- 2. Procedure: Get Park Conservation & At-Risk Species Summary
IF OBJECT_ID(N'dbo.sp_GetParkConservationReport', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_GetParkConservationReport;
GO
CREATE PROCEDURE dbo.sp_GetParkConservationReport
    @AdminUnitCode VARCHAR(10) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        Admin_Unit_Code,
        Habitat,
        Conservation_Priority,
        Common_Name,
        Scientific_Name,
        COUNT(*) AS Total_Observations,
        COUNT(DISTINCT Plot_Name) AS Active_Plots
    FROM dbo.Bird_Observations
    WHERE (@AdminUnitCode IS NULL OR Admin_Unit_Code = @AdminUnitCode)
      AND Conservation_Priority <> 'Standard / Secure'
    GROUP BY Admin_Unit_Code, Habitat, Conservation_Priority, Common_Name, Scientific_Name
    ORDER BY Admin_Unit_Code, Total_Observations DESC;
END;
GO

-- 3. Procedure: Get Top Biodiversity Plots
IF OBJECT_ID(N'dbo.sp_GetTopBiodiversityPlots', N'P') IS NOT NULL DROP PROCEDURE dbo.sp_GetTopBiodiversityPlots;
GO
CREATE PROCEDURE dbo.sp_GetTopBiodiversityPlots
    @TopN INT = 15,
    @MinObservations INT = 20
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP (@TopN)
        Plot_Name,
        Admin_Unit_Code,
        Habitat,
        COUNT(*) AS Total_Observations,
        COUNT(DISTINCT Common_Name) AS Species_Richness,
        SUM(CAST(PIF_Watchlist_Status AS INT)) AS Watchlist_Count,
        ROUND(AVG(Temperature), 1) AS Avg_Temp_C,
        ROUND(AVG(Humidity), 1) AS Avg_Humidity_Pct
    FROM dbo.Bird_Observations
    GROUP BY Plot_Name, Admin_Unit_Code, Habitat
    HAVING COUNT(*) >= @MinObservations
    ORDER BY Species_Richness DESC, Total_Observations DESC;
END;
GO

PRINT 'Stored Procedures created successfully.';
GO
