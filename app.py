"""
Bird Species Observation Analysis - Interactive Streamlit Dashboard
Technologies: Streamlit, Plotly, Pandas, SQLAlchemy / PyODBC
Author: Antigravity AI Data Engineering & Ecological Analytics
"""

import os
import sys
import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# -----------------------------------------------------------------------------
# 1. STREAMLIT APP CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Bird Species Observation Analysis Dashboard",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics, glassmorphism cards, and premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 6px;
        color: #ffffff;
    }
    
    .main-header p {
        font-size: 1.05rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    
    .kpi-sub {
        font-size: 0.8rem;
        color: #10b981;
        margin-top: 2px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .status-badge-forest {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .status-badge-grassland {
        background-color: #ffedd5;
        color: #9a3412;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING (SQL Server with CSV Fallback)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_data():
    """Load cleaned bird observations dataset from SQL Server or CSV fallback."""
    data_loaded_from = "CSV"
    df = None
    
    # Try SQL Server first
    try:
        import pyodbc
        conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=BirdMonitoringDB;Trusted_Connection=yes;TrustServerCertificate=yes;"
        conn = pyodbc.connect(conn_str, timeout=3)
        query = "SELECT * FROM dbo.Bird_Observations"
        df = pd.read_sql(query, conn)
        conn.close()
        data_loaded_from = "SQL Server (BirdMonitoringDB)"
    except Exception:
        pass
    
    # Fallback to CSV
    if df is None:
        csv_path = os.path.join(os.path.dirname(__file__), 'bird_observations_cleaned.csv')
        df = pd.read_csv(csv_path, low_memory=False)
        data_loaded_from = "Cleaned CSV Dataset"
        
    df['Date'] = pd.to_datetime(df['Date'])
    return df, data_loaded_from

df_raw, data_source = load_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & GLOBAL FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1444464666168-49d633b86797?w=600&auto=format&fit=crop&q=80", use_container_width=True)
    st.title("🦅 Navigation")
    
    page = st.radio(
        "Select Dashboard View:",
        [
            "📊 Executive Overview",
            "🌿 Habitat & Ecosystems",
            "🐦 Species & Biodiversity",
            "⏱️ Temporal & Diurnal Dynamics",
            "📍 Spatial & Hotspot Explorer",
            "⛅ Environmental & Behavior",
            "🛡️ Conservation & At-Risk Center",
            "💾 Data Explorer & SQL Console"
        ],
        index=0
    )
    
    st.markdown("---")
    st.subheader("🔍 Global Filters")
    
    # Habitat Filter
    habitat_filter = st.selectbox("Ecosystem / Habitat:", ["All Habitats", "Forest", "Grassland"])
    
    # Admin Unit Filter
    all_admin_units = sorted(df_raw['Admin_Unit_Code'].dropna().unique())
    selected_admin_units = st.multiselect("Parks / Admin Units:", all_admin_units, default=all_admin_units)
    
    # Date Range Filter
    min_date = df_raw['Date'].min().date()
    max_date = df_raw['Date'].max().date()
    date_range = st.date_input("Observation Date Range:", (min_date, max_date), min_value=min_date, max_value=max_date)
    
    # Conservation Filter
    all_priorities = sorted(df_raw['Conservation_Priority'].dropna().unique())
    selected_priorities = st.multiselect("Conservation Status:", all_priorities, default=all_priorities)
    
    st.markdown("---")
    st.caption(f"**Connected Source:** {data_source}")
    st.caption("National Park Service Avian Monitoring — NCR (2018)")

# -----------------------------------------------------------------------------
# 4. FILTER APPLICATION
# -----------------------------------------------------------------------------
df = df_raw.copy()

if habitat_filter != "All Habitats":
    df = df[df['Habitat'] == habitat_filter]

if selected_admin_units:
    df = df[df['Admin_Unit_Code'].isin(selected_admin_units)]

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_d, end_d = date_range
    df = df[(df['Date'].dt.date >= start_d) & (df['Date'].dt.date <= end_d)]

if selected_priorities:
    df = df[df['Conservation_Priority'].isin(selected_priorities)]

# -----------------------------------------------------------------------------
# 5. DIVERSITY CALCULATION HELPER
# -----------------------------------------------------------------------------
def calculate_diversity_metrics(data_df):
    counts = data_df['Common_Name'].value_counts()
    n = counts.sum()
    if n == 0:
        return {'S': 0, 'H': 0.0, 'D': 0.0, 'J': 0.0}
    p = counts / n
    S = len(counts)
    H = -np.sum(p * np.log(p))
    D = 1.0 - np.sum(p**2)
    J = H / np.log(S) if S > 1 else 0
    return {'S': S, 'H': round(H, 4), 'D': round(D, 4), 'J': round(J, 4)}

# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if page == "📊 Executive Overview":
    st.markdown("""
    <div class="main-header">
        <h1>🦅 Bird Species Observation Analysis</h1>
        <p>Comprehensive Ecological Monitoring & Biodiversity Insights Across Forest & Grassland Ecosystems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Row
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Observations</div>
            <div class="kpi-value">{len(df):,}</div>
            <div class="kpi-sub">Filtered Records</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Unique Species</div>
            <div class="kpi-value">{df['Common_Name'].nunique()}</div>
            <div class="kpi-sub">Across Ecosystems</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Surveyed Plots</div>
            <div class="kpi-value">{df['Plot_Name'].nunique()}</div>
            <div class="kpi-sub">Point-Count Sites</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Parks / Units</div>
            <div class="kpi-value">{df['Admin_Unit_Code'].nunique()}</div>
            <div class="kpi-sub">National Capital Parks</div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        pif_cnt = df['PIF_Watchlist_Status'].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Watchlist Birds</div>
            <div class="kpi-value">{pif_cnt:,}</div>
            <div class="kpi-sub" style="color: #ef4444;">PIF High Concern</div>
        </div>
        """, unsafe_allow_html=True)
    with k6:
        avg_t = df['Temperature'].mean()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Temperature</div>
            <div class="kpi-value">{avg_t:.1f}°C</div>
            <div class="kpi-sub">Breeding Season</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 1: Ecosystem Share & Top 10 Species
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Ecosystem Breakdown")
        hab_cnts = df['Habitat'].value_counts().reset_index()
        hab_cnts.columns = ['Habitat', 'Count']
        fig_pie = px.pie(
            hab_cnts, 
            names='Habitat', 
            values='Count', 
            hole=0.45,
            color='Habitat',
            color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Top 10 Most Common Species")
        top10 = df['Common_Name'].value_counts().head(10).reset_index()
        top10.columns = ['Species', 'Observations']
        fig_top = px.bar(
            top10, 
            x='Observations', 
            y='Species', 
            orientation='h',
            text='Observations',
            color='Observations',
            color_continuous_scale='Viridis'
        )
        fig_top.update_layout(yaxis=dict(autorange="reversed"), margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig_top, use_container_width=True)
        
    # Row 2: Temporal Timeline & Spatial Bar
    c3, c4 = st.columns([2, 1])
    with c3:
        st.subheader("Weekly Observation Timeline (2018 Breeding Season)")
        weekly_df = df.set_index('Date').resample('W-MON')['Common_Name'].count().reset_index()
        weekly_df.columns = ['Week', 'Observations']
        fig_time = px.area(
            weekly_df, 
            x='Week', 
            y='Observations',
            title='Weekly Survey Count Progression',
            color_discrete_sequence=['#3b82f6']
        )
        fig_time.update_layout(margin=dict(t=30, b=20, l=20, r=20), height=320)
        st.plotly_chart(fig_time, use_container_width=True)
        
    with c4:
        st.subheader("Observations by Park")
        park_df = df['Admin_Unit_Code'].value_counts().reset_index()
        park_df.columns = ['Park', 'Count']
        fig_park = px.bar(
            park_df, 
            x='Park', 
            y='Count', 
            color='Park',
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_park.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=320)
        st.plotly_chart(fig_park, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 2: HABITAT & ECOSYSTEM COMPARISON
# -----------------------------------------------------------------------------
elif page == "🌿 Habitat & Ecosystems":
    st.header("🌿 Ecosystem Comparison: Forest vs. Grassland")
    st.markdown("Direct head-to-head ecological comparison of species richness, diversity indices, and microclimate characteristics.")
    
    # Calculate diversity metrics for both habitats
    f_df = df[df['Habitat'] == 'Forest']
    g_df = df[df['Habitat'] == 'Grassland']
    
    f_div = calculate_diversity_metrics(f_df)
    g_div = calculate_diversity_metrics(g_df)
    
    # Metrics Cards
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        st.metric("Forest Observations", f"{len(f_df):,}", f"{len(f_df)/max(1,len(df))*100:.1f}% Share")
    with h2:
        st.metric("Grassland Observations", f"{len(g_df):,}", f"{len(g_df)/max(1,len(df))*100:.1f}% Share")
    with h3:
        st.metric("Forest Richness S", f"{f_div['S']} Species", f"Shannon H': {f_div['H']}")
    with h4:
        st.metric("Grassland Richness S", f"{g_div['S']} Species", f"Shannon H': {g_div['H']}")
        
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Diversity & Metrics Table", "🌡️ Microclimate Comparison", "🔄 Species Overlap & Affinity"])
    
    with tab1:
        div_table = pd.DataFrame([
            {
                "Ecosystem": "Forest",
                "Total Observations": len(f_df),
                "Unique Species (S)": f_div['S'],
                "Shannon Diversity (H')": f_div['H'],
                "Simpson Index (1-D)": f_div['D'],
                "Pielou's Evenness (J')": f_div['J'],
                "Surveyed Plots": f_df['Plot_Name'].nunique(),
                "Mean Temp (°C)": round(f_df['Temperature'].mean(), 2),
                "Mean Humidity (%)": round(f_df['Humidity'].mean(), 2)
            },
            {
                "Ecosystem": "Grassland",
                "Total Observations": len(g_df),
                "Unique Species (S)": g_div['S'],
                "Shannon Diversity (H')": g_div['H'],
                "Simpson Index (1-D)": g_div['D'],
                "Pielou's Evenness (J')": g_div['J'],
                "Surveyed Plots": g_df['Plot_Name'].nunique(),
                "Mean Temp (°C)": round(g_df['Temperature'].mean(), 2),
                "Mean Humidity (%)": round(g_df['Humidity'].mean(), 2)
            }
        ])
        st.dataframe(div_table, use_container_width=True)
        
        st.info("""
        **Ecological Index Interpretation:**
        - **Species Richness ($S$):** Total count of unique avian species detected.
        - **Shannon-Wiener ($H'$):** Combines richness and abundance evenness. Higher values signify more diverse communities.
        - **Simpson ($1-D$):** Probability that two randomly selected individuals belong to different species.
        - **Pielou's Evenness ($J'$):** Measures how evenly observations are distributed across species ($0$ to $1$).
        """)
        
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig_temp = px.box(
                df, 
                x='Habitat', 
                y='Temperature', 
                color='Habitat',
                points="outliers",
                title='Temperature Distribution by Habitat (°C)',
                color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
            )
            st.plotly_chart(fig_temp, use_container_width=True)
        with c2:
            fig_hum = px.box(
                df, 
                x='Habitat', 
                y='Humidity', 
                color='Habitat',
                points="outliers",
                title='Relative Humidity Distribution by Habitat (%)',
                color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
            )
            st.plotly_chart(fig_hum, use_container_width=True)
            
    with tab3:
        # Calculate overlap
        f_species = set(f_df['Common_Name'].unique())
        g_species = set(g_df['Common_Name'].unique())
        shared = f_species.intersection(g_species)
        f_only = f_species - g_species
        g_only = g_species - f_species
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("🌲 Forest-Only Species", f"{len(f_only)} Species")
        col_b.metric("🤝 Shared Generalists", f"{len(shared)} Species")
        col_c.metric("🌾 Grassland-Only Species", f"{len(g_only)} Species")
        
        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("🌲 Top Forest-Only Specialists")
            f_only_counts = f_df[f_df['Common_Name'].isin(f_only)]['Common_Name'].value_counts().head(10).reset_index()
            f_only_counts.columns = ['Species', 'Forest Observations']
            st.dataframe(f_only_counts, use_container_width=True)
            
        with c_right:
            st.subheader("🌾 Top Grassland-Only Specialists")
            g_only_counts = g_df[g_df['Common_Name'].isin(g_only)]['Common_Name'].value_counts().head(10).reset_index()
            g_only_counts.columns = ['Species', 'Grassland Observations']
            st.dataframe(g_only_counts, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 3: SPECIES & BIODIVERSITY EXPLORER
# -----------------------------------------------------------------------------
elif page == "🐦 Species & Biodiversity":
    st.header("🐦 Species Biodiversity & Profile Explorer")
    
    # Species Lookup
    species_list = sorted(df['Common_Name'].unique())
    selected_species = st.selectbox("🔍 Select Species to Inspect:", species_list, index=0)
    
    sp_df = df[df['Common_Name'] == selected_species]
    
    # Profile Card
    st.markdown(f"""
    <div style="background: #f8fafc; border-left: 5px solid #3b82f6; padding: 18px 24px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="margin: 0; color: #1e293b;">{selected_species} (<em>{sp_df['Scientific_Name'].iloc[0]}</em>)</h2>
        <p style="margin-top: 6px; color: #64748b; font-size: 0.95rem;">
            <strong>AOU Code:</strong> {sp_df['AOU_Code'].iloc[0]} | 
            <strong>Accepted TSN:</strong> {sp_df['AcceptedTSN'].iloc[0]} | 
            <strong>Conservation Status:</strong> {sp_df['Conservation_Priority'].iloc[0]}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Sightings", f"{len(sp_df):,}")
    m2.metric("Forest Sightings", f"{(sp_df['Habitat']=='Forest').sum():,}")
    m3.metric("Grassland Sightings", f"{(sp_df['Habitat']=='Grassland').sum():,}")
    m4.metric("Parks Present", f"{sp_df['Admin_Unit_Code'].nunique()} / {df['Admin_Unit_Code'].nunique()}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Park Presence Distribution")
        sp_park = sp_df.groupby(['Admin_Unit_Code', 'Habitat']).size().reset_index(name='Count')
        fig_sp_park = px.bar(
            sp_park, 
            x='Admin_Unit_Code', 
            y='Count', 
            color='Habitat',
            title=f"{selected_species} Counts Across Parks",
            color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
        )
        st.plotly_chart(fig_sp_park, use_container_width=True)
        
    with col2:
        st.subheader("Detection Methods")
        sp_id = sp_df['ID_Method'].value_counts().reset_index()
        sp_id.columns = ['Method', 'Count']
        fig_sp_id = px.pie(sp_id, names='Method', values='Count', title=f"Identification Methods for {selected_species}")
        st.plotly_chart(fig_sp_id, use_container_width=True)
        
    # Species Cross-Tab Heatmap
    st.subheader("Top 25 Species × Administrative Unit Cross-Tabulation")
    top25_species = df['Common_Name'].value_counts().head(25).index
    cross_tab = pd.crosstab(df[df['Common_Name'].isin(top25_species)]['Common_Name'], df['Admin_Unit_Code'])
    fig_heat = px.imshow(cross_tab, color_continuous_scale='YlGnBu', aspect="auto")
    fig_heat.update_layout(height=600)
    st.plotly_chart(fig_heat, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 4: TEMPORAL & DIURNAL DYNAMICS
# -----------------------------------------------------------------------------
elif page == "⏱️ Temporal & Diurnal Dynamics":
    st.header("⏱️ Temporal Dynamics & Diurnal Activity Windows")
    st.markdown("Avian point-count frequency analyzed across months, diurnal hours, and repeat sampling visits (2018 Breeding Season).")
    
    t1, t2 = st.columns(2)
    with t1:
        st.subheader("Monthly Observation Volume")
        month_df = df.groupby(['Month_Name', 'Habitat']).size().reset_index(name='Observations')
        fig_m = px.bar(
            month_df, 
            x='Month_Name', 
            y='Observations', 
            color='Habitat', 
            barmode='group',
            category_orders={"Month_Name": ["May", "June", "July"]},
            color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
        )
        st.plotly_chart(fig_m, use_container_width=True)
        
    with t2:
        st.subheader("Diurnal Hourly Activity Curve (Dawn Chorus)")
        hour_df = df[df['Observation_Hour'].notna()].groupby(['Observation_Hour', 'Habitat']).size().reset_index(name='Observations')
        fig_h = px.line(
            hour_df, 
            x='Observation_Hour', 
            y='Observations', 
            color='Habitat', 
            markers=True,
            title='Avian Activity by Hour of Day',
            color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
        )
        st.plotly_chart(fig_h, use_container_width=True)
        
    st.markdown("---")
    
    # Visit Dynamics
    st.subheader("Visit Dynamics (Visit 1 vs. Visit 2)")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        visit_df = df.groupby(['Visit', 'Habitat']).agg(
            Observations=('Common_Name', 'count'),
            Unique_Species=('Common_Name', 'nunique')
        ).reset_index()
        fig_v = px.bar(
            visit_df, 
            x='Visit', 
            y='Observations', 
            color='Habitat', 
            barmode='group',
            color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
        )
        st.plotly_chart(fig_v, use_container_width=True)
    with v_col2:
        st.write("""
        **Sampling Visit Insights:**
        - **Repeat Surveys:** Point counts were conducted in two systematic waves (**Visit 1** in early breeding season, **Visit 2** in peak summer).
        - **Turnover:** High consistency in species detection was observed between visits, with peak song activity captured during June surveys.
        """)
        st.dataframe(visit_df, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 5: SPATIAL & HOTSPOT EXPLORER
# -----------------------------------------------------------------------------
elif page == "📍 Spatial & Hotspot Explorer":
    st.header("📍 Spatial Hotspots & Administrative Unit Biodiversity")
    st.markdown("Plot-level species richness and administrative park leaderboards.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Park Diversity Leaderboard")
        admin_summary = df.groupby('Admin_Unit_Code').agg(
            Total_Observations=('Common_Name', 'count'),
            Species_Richness=('Common_Name', 'nunique'),
            Plots_Count=('Plot_Name', 'nunique')
        ).reset_index().sort_values(by='Total_Observations', ascending=False)
        
        fig_adm = px.bar(
            admin_summary, 
            x='Admin_Unit_Code', 
            y='Total_Observations',
            color='Species_Richness',
            color_continuous_scale='Viridis',
            title='Observations & Species Richness per Park'
        )
        st.plotly_chart(fig_adm, use_container_width=True)
        
    with col2:
        st.subheader("Top 15 Biodiversity Hotspot Plots")
        plot_summary = df.groupby(['Plot_Name', 'Admin_Unit_Code', 'Habitat']).agg(
            Observations=('Common_Name', 'count'),
            Species_Richness=('Common_Name', 'nunique'),
            Watchlist_Count=('PIF_Watchlist_Status', 'sum')
        ).reset_index().sort_values(by=['Species_Richness', 'Observations'], ascending=False).head(15)
        
        st.dataframe(plot_summary, use_container_width=True)
        
    # Plot Detail Lookup
    st.subheader("🔍 Plot-Level Inspection")
    selected_plot = st.selectbox("Select a Plot to Inspect:", sorted(df['Plot_Name'].unique()))
    plot_records = df[df['Plot_Name'] == selected_plot]
    
    st.write(f"**Plot:** `{selected_plot}` | **Park:** `{plot_records['Admin_Unit_Code'].iloc[0]}` | **Habitat:** `{plot_records['Habitat'].iloc[0]}` | **Observations:** `{len(plot_records)}` | **Species:** `{plot_records['Common_Name'].nunique()}`")
    st.dataframe(
        plot_records[['Date', 'Start_Time', 'Common_Name', 'Scientific_Name', 'ID_Method', 'Distance_Standardized', 'Conservation_Priority']].reset_index(drop=True),
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# PAGE 6: ENVIRONMENTAL & BEHAVIORAL ANALYSIS
# -----------------------------------------------------------------------------
elif page == "⛅ Environmental & Behavior":
    st.header("⛅ Environmental Conditions & Avian Behavior")
    st.markdown("Analysis of temperature, humidity, sky conditions, wind speed, detection modality, and flyover behavior.")
    
    e1, e2 = st.columns(2)
    with e1:
        st.subheader("Microclimate: Temperature vs. Humidity")
        sample_df = df.sample(min(1500, len(df)), random_state=42)
        fig_scatter = px.scatter(
            sample_df, 
            x='Temperature', 
            y='Humidity', 
            color='Habitat',
            opacity=0.6,
            marginal_x='box',
            marginal_y='box',
            color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with e2:
        st.subheader("Identification Method by Habitat")
        id_df = df.groupby(['ID_Method', 'Habitat']).size().reset_index(name='Count')
        fig_id = px.bar(
            id_df, 
            x='ID_Method', 
            y='Count', 
            color='Habitat', 
            barmode='group',
            color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
        )
        st.plotly_chart(fig_id, use_container_width=True)
        
    st.markdown("---")
    
    e3, e4 = st.columns(2)
    with e3:
        st.subheader("Sky Condition & Count Volume")
        sky_df = df['Sky'].value_counts().reset_index()
        sky_df.columns = ['Sky_Condition', 'Count']
        fig_sky = px.bar(sky_df, x='Sky_Condition', y='Count', color='Sky_Condition', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_sky.update_layout(showlegend=False)
        st.plotly_chart(fig_sky, use_container_width=True)
        
    with e4:
        st.subheader("Distance Category Breakdown")
        dist_df = df['Distance_Category'].value_counts().reset_index()
        dist_df.columns = ['Distance_Band', 'Observations']
        fig_dist = px.pie(dist_df, names='Distance_Band', values='Observations', hole=0.4)
        st.plotly_chart(fig_dist, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 7: CONSERVATION & AT-RISK SPECIES CENTER
# -----------------------------------------------------------------------------
elif page == "🛡️ Conservation & At-Risk Center":
    st.header("🛡️ Conservation Priorities & Vulnerable Avian Populations")
    st.markdown("Actionable monitoring of Partners in Flight (PIF) Watchlist and Regional Stewardship bird species.")
    
    pif_total = df['PIF_Watchlist_Status'].sum()
    reg_total = df['Regional_Stewardship_Status'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("PIF Watchlist Observations", f"{pif_total:,}", "At-Risk Species")
    c2.metric("Regional Stewardship Observations", f"{reg_total:,}", "High Regional Priority")
    c3.metric("Secure / Standard Observations", f"{(len(df) - pif_total - reg_total):,}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Priority Breakdown Chart
    cons_df = df.groupby(['Conservation_Priority', 'Habitat']).size().reset_index(name='Observations')
    fig_cons = px.bar(
        cons_df, 
        x='Conservation_Priority', 
        y='Observations', 
        color='Habitat',
        barmode='group',
        title='Observation Counts by Conservation Classification',
        color_discrete_map={'Forest': '#2ca02c', 'Grassland': '#ff7f0e'}
    )
    st.plotly_chart(fig_cons, use_container_width=True)
    
    # Table of At-Risk Species
    st.subheader("Priority Species Catalog")
    at_risk_species = df[df['PIF_Watchlist_Status'] | df['Regional_Stewardship_Status']].groupby(
        ['Common_Name', 'Scientific_Name', 'AOU_Code', 'Conservation_Priority']
    ).agg(
        Total_Observations=('Habitat', 'count'),
        Forest_Observations=('Habitat', lambda x: (x == 'Forest').sum()),
        Grassland_Observations=('Habitat', lambda x: (x == 'Grassland').sum()),
        Parks_Recorded=('Admin_Unit_Code', 'nunique')
    ).reset_index().sort_values(by='Total_Observations', ascending=False)
    
    st.dataframe(at_risk_species, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 8: DATA EXPLORER & SQL CONSOLE
# -----------------------------------------------------------------------------
elif page == "💾 Data Explorer & SQL Console":
    st.header("💾 Data Explorer & SQL Query Console")
    st.markdown("Filter, inspect, export cleaned records, or execute SQL queries against `BirdMonitoringDB`.")
    
    tab1, tab2 = st.tabs(["📋 Filtered Data Viewer", "⚡ SQL Query Console"])
    
    with tab1:
        st.dataframe(df.head(500), use_container_width=True)
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_export,
            file_name="bird_observations_filtered.csv",
            mime="text/csv"
        )
        
    with tab2:
        st.subheader("SQL Query Sandbox")
        default_query = """SELECT TOP 10 
    Common_Name, 
    Habitat, 
    COUNT(*) AS Sighting_Count, 
    AVG(Temperature) AS Avg_Temp
FROM dbo.Bird_Observations
GROUP BY Common_Name, Habitat
ORDER BY Sighting_Count DESC;"""
        
        user_query = st.text_area("Write SQL Query:", value=default_query, height=150)
        
        if st.button("🚀 Run SQL Query"):
            try:
                import pyodbc
                conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=BirdMonitoringDB;Trusted_Connection=yes;TrustServerCertificate=yes;"
                conn = pyodbc.connect(conn_str, timeout=3)
                result_df = pd.read_sql(user_query, conn)
                conn.close()
                st.success(f"Query returned {len(result_df)} rows.")
                st.dataframe(result_df, use_container_width=True)
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
                st.info("Ensure the SQL Server instance `localhost` and database `BirdMonitoringDB` are active.")
