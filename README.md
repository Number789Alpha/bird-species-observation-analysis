# 🦅 Bird Species Observation Analysis: Forest vs. Grassland Ecosystems
### An End-to-End Ecological Analytics Platform
**Google Colab / Python (Data Cleaning & EDA) $\rightarrow$ Microsoft SQL Server (Storage & Analytical Views) $\rightarrow$ Streamlit + Plotly (Interactive Dashboard)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌐 Live Interactive Dashboard
The interactive multi-page web application is deployed and publicly accessible 24/7 at:

🔗 **[https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/](https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/)**

---

## 📌 Project Overview
This project presents an end-to-end data analytics and ecological monitoring platform evaluating avian biodiversity across two major ecosystems (**Forest** and **Grassland**) in the **National Capital Region (NCR)**.

The analysis processes systematic avian point-count monitoring records collected across **11 National Park administrative units** during the **2018 Breeding Season** (May 7 – July 19, 2018).

```
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│   PHASE 1: DATA ENG.    │      │  PHASE 2: SQL DATABASE  │      │ PHASE 3: WEB DASHBOARD  │
│  Google Colab / Python  │ ───▶ │  Microsoft SQL Server   │ ───▶ │   Streamlit + Plotly    │
│ Cleaning, EDA & Metrics │      │ Views, Indexes & Procs  │      │ 8-Page Interactive App  │
└─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
```

---

## 🌟 Key Findings & Summary Metrics

| Metric | Forest Ecosystem | Grassland Ecosystem | Overall Dataset |
| :--- | :---: | :---: | :---: |
| **Total Observations** | 8,546 (50.05%) | 8,531 (49.95%) | **17,077 Records** |
| **Species Richness ($S$)** | **108 Species** | **107 Species** | **127 Unique Species** |
| **Shannon Diversity ($H'$)** | **3.578** | **3.704** | **3.921** |
| **Simpson Index ($1 - D$)** | **0.9597** | **0.9662** | **0.9715** |
| **Pielou's Evenness ($J'$)** | **0.7642** | **0.7926** | **0.8095** |
| **Surveyed Plots** | 408 Plots | 201 Plots | **609 Plots** |
| **Mean Temperature** | 21.87°C | 23.27°C | **22.57°C** |
| **Mean Relative Humidity** | 77.76% | 69.62% | **73.69%** |

### 🔬 Ecological Highlights:
- **Species Affinity:** **88 species** are generalists detected in both habitats. **20 species** are strict Forest-interior specialists (*e.g., Wood Thrush, Ovenbird, Red-eyed Vireo*), and **19 species** are strict Grassland specialists (*e.g., Grasshopper Sparrow, Eastern Meadowlark, Bobolink*).
- **Temporal Dawn Chorus:** Avian detection activity peaks sharply between **06:00 AM and 08:00 AM**, with **June** capturing maximal breeding song activity (10,218 records).
- **Detection Modality:** **Singing** is the dominant detection method (53.3%), followed by **Calling** (26.5%) and **Visual sightings** (20.2%).
- **Conservation Focus:** **2,429 observations** represent Partners in Flight (PIF) Watchlist species, and **2,933 observations** represent Regional Stewardship priorities.

---

## 📁 Repository Structure

```
bird-species-observation-analysis/
│
├── app.py                             # Multi-Page Streamlit + Plotly Web Dashboard
├── bird_observations_analysis.ipynb   # 15-Section Google Colab / Jupyter Notebook
├── bird_observations_cleaned.csv      # Standardized Cleaned Dataset (17,077 rows x 43 cols)
├── run_bird_pipeline.py               # Autonomous Python Data Processing & EDA Pipeline
├── load_data_to_sql.py                # Automated SQL Server Data Loader (pyodbc / fast_executemany)
├── requirements.txt                   # Python Dependencies for Local & Cloud Hosting
├── .gitignore                         # Git Ignore Configuration
├── README.md                          # Project Documentation & Architecture Guide
│
├── sql/                               # Production SQL Server Scripts
│   ├── 01_database_setup.sql          # DB, Table DDL & Non-Clustered Indexes
│   ├── 02_data_import.sql             # SSMS BULK INSERT Reference Script
│   ├── 03_analytical_views.sql        # Reusable Views (Habitat, Species, Hotspots, Conservation)
│   ├── 04_stored_procedures.sql       # Parameterized Stored Procedures for Dashboard Backend
│   └── 05_business_queries.sql        # 8 Core Business & Ecological SQL Queries
│
└── outputs/                           # Generated Analytical Reports & Visualizations
    ├── key_insights.md                # Structured Key Analytical Findings
    ├── data_quality_report.csv        # Pre vs Post-Cleaning Reconciliation
    ├── habitat_summary.csv            # Ecosystem Diversity & Microclimate Summary
    ├── species_summary.csv            # Species Frequencies & Habitat Affinity Catalog
    ├── admin_unit_diversity_summary.csv # Park-Level Biodiversity Leaderboard
    ├── monthly_temporal_summary.csv   # Monthly Survey Volumes & Richness
    ├── hourly_temporal_summary.csv    # Diurnal Dawn Chorus Profile
    ├── conservation_species_detail.csv# Watchlist & Regional Stewardship Catalog
    ├── interactive_charts/            # 8 Standalone Plotly Interactive HTML Charts
    └── figures/                       # High-Res Publication Figures (PNG)
```

---

## 🚀 Quickstart & Local Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Number789Alpha/bird-species-observation-analysis.git
cd bird-species-observation-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit Dashboard Locally
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 💻 Technical Implementation Details

### Phase 1 — Google Colab & Data Engineering
- **11 Administrative Unit Sheets:** (`ANTI`, `CATO`, `CHOH`, `GWMP`, `HAFE`, `MANA`, `MONO`, `NACE`, `PRWI`, `ROCR`, `WOTR`).
- **Schema Harmonization:** Standardized `NPSTaxonCode` (Forest) and `TaxonCode` (Grassland) into `Taxon_Code`. Preserved `Site_Name` and `Previously_Obs` without data fabrication.
- **Feature Engineering:** Derived `Month`, `Month_Name`, `Day`, `Day_Of_Week`, `Observation_Hour`, `Observation_Duration_Min`, `Season`, `Distance_Category`, `Distance_Standardized`, `Sex_Standardized`, and `Conservation_Priority`.
- **Zero Record Loss:** 17,077 raw rows successfully cleaned and reconciled.

### Phase 2 — Microsoft SQL Server Database
- **Database:** `BirdMonitoringDB` | **Table:** `dbo.Bird_Observations`
- **Performance Indexing:** Non-clustered indexes on `Habitat`, `Common_Name`, `Admin_Unit_Code`, `Date`, and `Conservation_Priority`.
- **Analytical Views:**
  - `vw_Habitat_Summary`: Ecosystem level metrics & shares.
  - `vw_Species_Distribution`: Species counts, park occurrences, and habitat affinity.
  - `vw_Temporal_Trends`: Monthly & hourly survey dynamics.
  - `vw_Spatial_Hotspots`: Park and plot biodiversity rankings.
  - `vw_Conservation_Priorities`: Priority at-risk species monitoring.

### Phase 3 — Streamlit Web Dashboard
The web app features **8 dedicated analytical modules**:
1. **📊 Executive Overview:** Real-time KPI cards, ecosystem shares, top 10 species, and weekly timeline.
2. **🌿 Habitat & Ecosystems:** Forest vs. Grassland diversity indices ($S, H', 1-D, J'$) and microclimate boxplots.
3. **🐦 Species & Biodiversity:** Dynamic species profile card, park presence, and species $\times$ park heatmap.
4. **⏱️ Temporal Dynamics:** Monthly trends, diurnal dawn chorus curve, and repeat visit comparisons.
5. **📍 Spatial Hotspots:** Park diversity leaderboard, top 15 hotspot plots, and plot inspection lookup.
6. **⛅ Environmental & Behavior:** Microclimate scatter plots, sky condition impacts, and distance bands.
7. **🛡️ Conservation Center:** PIF Watchlist and Regional Stewardship catalog with risk classifications.
8. **💾 Data Explorer & SQL Console:** Live filtered data viewer, CSV download, and interactive SQL query sandbox.

---

## 👥 Authors & Acknowledgments
- **Developer:** Vidit ([@Number789Alpha](https://github.com/Number789Alpha))
- **Live App:** [https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/](https://bird-species-observation-analysis-5adppp8jrh6xjqws3uwfey.streamlit.app/)
- **Data Source:** National Park Service (NPS) Avian Point Count Monitoring Program — National Capital Region.
- **Frameworks:** Python, Pandas, Plotly, Streamlit, Microsoft SQL Server, Google Colab.
