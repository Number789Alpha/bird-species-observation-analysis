# 🦅 BIRD SPECIES OBSERVATION ANALYSIS: ECOSYSTEM COMPARISON & BIODIVERSITY MONITORING
## Comprehensive End-to-End Project Summary Report & Technical Documentation

**Author & Lead Analyst:** Vidit ([@Number789Alpha](https://github.com/Number789Alpha))  
**Project Scope:** Forest vs. Grassland Ecosystems | National Capital Region (NCR) National Parks  
**Temporal Scope:** 2018 Avian Breeding Season (May 7 – July 19, 2018)  
**Live Public Dashboard:** [https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/](https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/)  
**GitHub Repository:** [https://github.com/Number789Alpha/bird-species-observation-analysis](https://github.com/Number789Alpha/bird-species-observation-analysis)  

---

## 1. EXECUTIVE SUMMARY & PROJECT CHARTER

### 1.1 Project Objective & Problem Statement
Understanding the distribution, diversity, and behavioral ecology of avian populations across differing ecosystem types is critical for informing biodiversity conservation, land-use planning, and ecosystem management. Avian species serve as sensitive bio-indicators whose population structures, detection frequencies, and vocalization patterns reflect underlying microclimate variations, vegetation structure, and anthropogenic disturbances.

This project delivers an end-to-end data analytics, statistical modeling, and interactive web platform that evaluates avian observational data across two distinct ecosystems:
1. **Forest Ecosystem:** Multi-layered canopy, dense understory, lower solar radiation, higher relative humidity.
2. **Grassland Ecosystem:** Open meadows, herbaceous vegetation, high direct solar exposure, elevated ambient temperatures.

The primary objective is to quantify habitat specialization, temporal activity windows, spatial biodiversity hotspots, microclimate influences, and conservation priorities across **11 National Park administrative units** in the National Capital Region.

### 1.2 Multi-Tier Architectural Pipeline
The project is built across three production-grade engineering tiers:
- **Tier 1 — Data Engineering & Exploratory Data Analysis (Google Colab / Python):** Raw workbook inspection, sheet consolidation, schema harmonization, point-count deduplication auditing, feature engineering, and statistical diversity modeling.
- **Tier 2 — Enterprise Relational Storage & Analytical Modeling (Microsoft SQL Server / SSMS):** Relational schema implementation (`BirdMonitoringDB`), primary key and non-clustered index creation, 6 analytical reporting views, 3 parameterized stored procedures, and 8 production business queries.
- **Tier 3 — Interactive Analytics & Presentation (Streamlit + Plotly):** Multi-page interactive web application featuring 8 analytical modules, dual SQL/CSV data connectors, dynamic filters, and real-time Plotly charts deployed to the public cloud.

---

## 2. RAW DATASET ARCHITECTURE & INGESTION ANALYSIS (PHASE 1)

### 2.1 Raw Source Workbooks
The raw observational data was provided in two Microsoft Excel workbooks containing 11 separate administrative unit sheets corresponding to National Park Service properties:
- `Bird_Monitoring_Data_FOREST.XLSX` (Total Size: ~955 KB)
- `Bird_Monitoring_Data_GRASSLAND.XLSX` (Total Size: ~958 KB)

### 2.2 Sheet-by-Sheet Dimensional Audit
| Administrative Unit Code | Park Name / Description | Forest Rows | Forest Cols | Grassland Rows | Grassland Cols | Grassland Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **ANTI** | Antietam National Battlefield | 333 | 29 | 3,588 | 29 | Active |
| **CATO** | Catoctin Mountain Park | 805 | 29 | 0 | 29 | Empty |
| **CHOH** | Chesapeake and Ohio Canal NHP | 2,202 | 29 | 0 | 29 | Empty |
| **GWMP** | George Washington Memorial Parkway | 386 | 29 | 0 | 29 | Empty |
| **HAFE** | Harpers Ferry National Historical Park | 422 | 29 | 117 | 29 | Active |
| **MANA** | Manassas National Battlefield Park | 465 | 29 | 1,811 | 29 | Active |
| **MONO** | Monocacy National Battlefield | 370 | 29 | 3,015 | 29 | Active |
| **NACE** | National Capital Parks - East | 684 | 29 | 0 | 29 | Empty |
| **PRWI** | Prince William Forest Park | 2,463 | 29 | 0 | 29 | Empty |
| **ROCR** | Rock Creek Park | 289 | 29 | 0 | 29 | Empty |
| **WOTR** | Wolf Trap National Park | 127 | 29 | 0 | 29 | Empty |
| **TOTALS** | **11 Administrative Units** | **8,546** | **29** | **8,531** | **29** | **17,077 Records** |

### 2.3 Raw Schema Discrepancy Analysis
A programmatic comparison of column schemas revealed that while the core 27 observational columns were identical, structural differences existed:
1. **Taxonomic Identifier Naming:** Forest recorded the NPS Taxon Code under `NPSTaxonCode`, whereas Grassland recorded the exact equivalent taxonomic integer under `TaxonCode`.
2. **Forest-Only Column:** `Site_Name` was populated in Forest sheets but was entirely omitted in Grassland sheets.
3. **Grassland-Only Column:** `Previously_Obs` was recorded in Grassland sheets but was absent in Forest sheets.

---

## 3. DATA CLEANING, HARMONIZATION & QUALITY ASSURANCE (PHASES 2–4)

### 3.1 Point-Count Survey Deduplication Audit
In ecological point-count methodology (National Park Service standard protocol), an observer conducts a 10-minute point count at a specific GPS plot. When multiple individuals of the same species (*e.g., 3 Common Grackles*) are recorded in the same interval, distance band, and plot, they legitimately share session attributes.
- **Forest Workbook:** Contained **0 exact duplicate rows**.
- **Grassland Workbook:** Contained **1,705 identical-attribute rows** representing multi-individual bird detections.
- **Data Engineering Decision:** To preserve biological abundance and accurate population counts, all 17,077 observational records were preserved while generating a dedicated duplicate audit table.

### 3.2 Missing Value Analysis & Remediation Strategy
- `Sub_Unit_Code`: Missing in 95.77% of rows (retained as valid `NULL` where sub-units do not exist).
- `Sex`: Missing / unrecorded in 30.35% of rows. In avian field surveys, sexually monomorphic species cannot be visually or acoustically sexed; missing values were mapped to explicit category `'Undetermined'`.
- `Distance`: Missing in 8.70% of rows (predominantly high flyover observations); standardized to `'Not Recorded / Flyover'`.
- `Site_Name` & `Previously_Obs`: Maintained as legitimate `NULL` values representing habitat-specific collection protocols without fabricating synthetic data.

### 3.3 Data Type Conversions & Standardizations
- **Dates & Times:** `Date` converted to `datetime64[ns]`. `Start_Time` and `End_Time` standardized to formatted strings (`HH:MM:SS`).
- **Numericals:** `Temperature` and `Humidity` cast to high-precision floating-point values.
- **Taxonomic Identifiers:** `AcceptedTSN` and `Taxon_Code` cast to nullable 64-bit integers (`Int64`).
- **Booleans:** `Flyover_Observed`, `PIF_Watchlist_Status`, `Regional_Stewardship_Status`, and `Initial_Three_Min_Cnt` cast to strict booleans.

### 3.4 Outlier & Physical Plausibility Assessment
- **Temperature:** Range: 11.0°C to 37.3°C ($	ext{Mean} = 22.57^\circ	ext{C}, 	ext{Median} = 22.30^\circ	ext{C}, 	ext{IQR} = 5.50^\circ	ext{C}$).
- **Humidity:** Range: 7.3% to 98.8% ($	ext{Mean} = 73.69\%, 	ext{Median} = 75.80\%, 	ext{IQR} = 15.50\%$).
- **Conclusion:** All extreme values represent valid diurnal weather fluctuations during the mid-Atlantic summer breeding season and were retained without arbitrary trimming.

---

## 4. FEATURE ENGINEERING & DERIVED METRICS (PHASE 5)

1. **`Month` & `Month_Name`:** Derived from `Date` (May, June, July).
2. **`Day` & `Day_Of_Week`:** Day of the month and categorical weekday.
3. **`Observation_Hour`:** Integer hour extracted from `Start_Time` (05:00 to 11:00 AM) to evaluate diurnal chorus patterns.
4. **`Observation_Duration_Min`:** Exact survey duration calculated between `Start_Time` and `End_Time` ($	ext{Median} = 10.0	ext{ minutes}$).
5. **`Season`:** Ecological breeding phase classification (`Spring (Early Breeding)` for May; `Summer (Peak Breeding)` for June/July).
6. **`Distance_Category`:** Segmented distance bands (`Near (<= 50m)`, `Far (50 - 100m)`, `Very Far (> 100m)`, `Flyover / Unrecorded`).
7. **`Conservation_Priority`:** Four-tier classification combining Partners in Flight (PIF) Watchlist status and Regional Stewardship status (`High Priority (Watchlist & Stewardship)`, `PIF Watchlist Only`, `Regional Stewardship Only`, `Standard / Secure`).

---

## 5. DATA QUALITY VALIDATION & RECONCILIATION AUDIT (PHASE 6)

| Validation Parameter | Raw Source State | Cleaned Dataset State | Status |
| :--- | :---: | :---: | :---: |
| **Total Record Count** | 17,077 Rows | **17,077 Rows** | 100.0% Verified (0 Loss) |
| **Forest Record Count** | 8,546 Rows | **8,546 Rows** | 100.0% Verified |
| **Grassland Record Count** | 8,531 Rows | **8,531 Rows** | 100.0% Verified |
| **Total Features / Columns** | 29 (Forest) / 29 (Grassland) | **43 Standardized Columns** | Schema Unified & Enriched |
| **Unique Common Names** | 126 Names | **126 Common Names** | Verified |
| **Unique Scientific Names** | 127 Taxa | **127 Scientific Taxa** | Verified |
| **Unique Parks (Admin Units)** | 11 Units | **11 Units** | Verified |
| **Unique Survey Plots** | 609 Plots | **609 Plots** | Verified |
| **Unique Observers** | 3 Observers | **3 Observers** | Verified |
| **Temporal Horizon** | May 7 – July 19, 2018 | **May 7 – July 19, 2018** | Single-Year Breeding Season |

---

## 6. EXPLORATORY DATA ANALYSIS (EDA) & ECOLOGICAL FINDINGS (PHASE 7)

### 6.1 Mathematical Ecological Diversity Modeling (Phase 8)
| Ecosystem Habitat | Observations | Richness ($S$) | Shannon Index ($H'$) | Simpson Index ($1-D$) | Pielou Evenness ($J'$) | Mean Temp (°C) | Mean Humidity (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Forest** | 8,546 | **108** | **3.5780** | **0.9597** | **0.7642** | 21.87°C | 77.76% |
| **Grassland** | 8,531 | **107** | **3.7037** | **0.9662** | **0.7926** | 23.27°C | 69.62% |
| **Overall Landscape** | **17,077** | **127** | **3.9214** | **0.9715** | **0.8095** | **22.57°C** | **73.69%** |

### 6.2 Top 10 Most Frequently Observed Avian Species
1. **American Robin** (*Turdus migratorius*) — 1,061 observations (358 Forest, 703 Grassland)
2. **Red-eyed Vireo** (*Vireo olivaceus*) — 972 observations (903 Forest, 69 Grassland)
3. **Northern Cardinal** (*Cardinalis cardinalis*) — 969 observations (413 Forest, 556 Grassland)
4. **Eastern Towhee** (*Pipilo erythrophthalmus*) — 873 observations (351 Forest, 522 Grassland)
5. **Indigo Bunting** (*Passerina cyanea*) — 823 observations (236 Forest, 587 Grassland)
6. **Wood Thrush** (*Hylocichla mustelina*) — 809 observations (774 Forest, 35 Grassland)
7. **Tufted Titmouse** (*Baeolophus bicolor*) — 722 observations (561 Forest, 161 Grassland)
8. **Song Sparrow** (*Melospiza melodia*) — 689 observations (76 Forest, 613 Grassland)
9. **Red-bellied Woodpecker** (*Melanerpes carolinus*) — 658 observations (453 Forest, 205 Grassland)
10. **Common Grackle** (*Quiscalus quiscula*) — 602 observations (108 Forest, 494 Grassland)

### 6.3 Species Specialization & Community Dynamics
- **Shared Generalists (88 Species):** Ubiquitous species occupying both ecosystems (*e.g., American Robin, Northern Cardinal, Red-eyed Vireo*).
- **Forest-Only Specialists (20 Species):** Canopy and forest-interior obligates (*e.g., Wood Thrush, Ovenbird, Pileated Woodpecker, Scarlet Tanager, Black-and-white Warbler*).
- **Grassland-Only Specialists (19 Species):** Open-field and meadow obligates (*e.g., Grasshopper Sparrow, Eastern Meadowlark, Bobolink, Dickcissel, Horned Lark*).

### 6.4 Temporal & Diurnal Dynamics
- **Seasonal Breakdown:** May (5,596 obs, 32.8%), June (6,596 obs, 38.6% - peak breeding activity), July (4,885 obs, 28.6%).
- **Diurnal Dawn Chorus:** Detections concentrated between 06:00 AM and 08:00 AM (8,804 records, 51.6% of total).

### 6.5 Detection Modality & Distance
- **Singing:** 9,103 observations (53.3%).
- **Calling:** 4,528 observations (26.5%).
- **Visual Sightings:** 3,444 observations (20.2%).
- **Distance Bands:** Near <= 50m (51.3%), Far 50-100m (40.0%), Flyover (8.7%).

---

## 7. CONSERVATION & AT-RISK POPULATION ANALYSIS

| Conservation Priority Category | Total Observations | Unique Species Count | Survey Plots Recorded | Key Indicator Species |
| :--- | :---: | :---: | :---: | :--- |
| **High Priority (Watchlist & Stewardship)** | **367** | **4** | **225** | Wood Thrush, Prairie Warbler, Grasshopper Sparrow, Kentucky Warbler |
| **PIF Watchlist Only** | **11** | **3** | **11** | Cerulean Warbler, Golden-winged Warbler, Blue-winged Warbler |
| **Regional Stewardship Only** | **3,618** | **20** | **598** | Eastern Towhee, Eastern Wood-Pewee, Field Sparrow, Scarlet Tanager |
| **Standard / Secure** | **13,081** | **100** | **609** | American Robin, Northern Cardinal, Red-eyed Vireo |

---

## 8. MICROSOFT SQL SERVER RELATIONAL ARCHITECTURE (PHASE 12)

- **Database Engine:** Microsoft SQL Server (`BirdMonitoringDB`) | Table: `dbo.Bird_Observations` (17,077 rows).
- **Indexing:** 5 Non-Clustered Indexes on `Habitat`, `Common_Name`, `Admin_Unit_Code`, `Date`, and `Conservation_Priority`.
- **Views:** `vw_Habitat_Summary`, `vw_Species_Distribution`, `vw_Temporal_Trends`, `vw_Spatial_Hotspots`, `vw_Conservation_Priorities`, `vw_Behavior_Detection`.
- **Stored Procedures:** `sp_GetSpeciesByHabitat`, `sp_GetParkConservationReport`, `sp_GetTopBiodiversityPlots`.

---

## 9. STREAMLIT + PLOTLY WEB APPLICATION ARCHITECTURE (PHASE 3)

The interactive web dashboard is publicly accessible at:  
👉 **[https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/](https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/)**

### Analytical Modules (8 Pages):
1. **📊 Executive Overview:** KPI metrics, ecosystem share donut chart, top 10 species bar chart, and weekly timeline.
2. **🌿 Habitat & Ecosystems:** Forest vs. Grassland diversity indices ($S, H', 1-D, J'$) and microclimate boxplots.
3. **🐦 Species & Biodiversity:** Dynamic species profile card, park presence, and species x park heatmap.
4. **⏱️ Temporal Dynamics:** Monthly trends, diurnal dawn chorus curve, and repeat visit comparisons.
5. **📍 Spatial Hotspots:** Park diversity leaderboard, top 15 hotspot plots, and plot inspection lookup.
6. **⛅ Environmental & Behavior:** Microclimate scatter plots, sky condition impacts, and distance bands.
7. **🛡️ Conservation Center:** PIF Watchlist and Regional Stewardship catalog with risk classifications.
8. **💾 Data Explorer & SQL Console:** Live filtered data viewer, CSV download, and interactive SQL query sandbox.

---

## 10. STRATEGIC RECOMMENDATIONS & POLICY GUIDANCE

1. **Forest Interior Protection:** Mature interior forests in Prince William Forest Park (`PRWI`) and C&O Canal (`CHOH`) must be protected from canopy fragmentation to safeguard Wood Thrush nesting territories.
2. **Grassland Mowing Regimes:** Implementing delayed mowing schedules until mid-July at Antietam (`ANTI`) and Monocacy (`MONO`) will protect ground-nesting Grasshopper Sparrows and Eastern Meadowlarks.
3. **Eco-Tourism Development:** High-richness plots (`ANTI-0105`, `MONO-0057`, `CHOH-0812`) should be incorporated into guided eco-tourism birding trails.
4. **Standardized Monitoring Expansion:** Expanding Grassland point counts to units currently lacking grassland data (`CATO`, `GWMP`, `PRWI`) will provide a complete landscape-level monitoring network.
