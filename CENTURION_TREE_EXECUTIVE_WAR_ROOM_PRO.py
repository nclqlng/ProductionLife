"""
CENTURION TREE Executive Insights
Professional Performance Dashboard v5.1

Flexible Data Sources:
- MTD only (no target data)
- YTD only (full data)  
- Both MTD and YTD

Handles missing columns gracefully
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import base64

st.set_page_config(
    page_title="CENTURION TREE Executive Insights",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONFIGURATION
# ============================================================================

SUN_LIFE_GOLD = "#FDB913"
SUN_LIFE_DARK = "#2D2D2D"
SUN_LIFE_GREY = "#6B7280"
SUN_LIFE_LIGHT = "#F9FAFB"

COLORS = {
    "primary": SUN_LIFE_GOLD,
    "secondary": SUN_LIFE_DARK,
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "background": SUN_LIFE_LIGHT,
}

# ============================================================================
# STYLING
# ============================================================================

st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    .stApp { background: #F9FAFB; }
    
    .main-header {
        background: linear-gradient(135deg, #2D2D2D 0%, #1a1a2e 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        border-left: 6px solid #FDB913;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: transform 0.2s;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.10); }
    
    .health-score { font-size: 3rem; font-weight: 700; color: #2D2D2D; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #2D2D2D; }
    .metric-label { font-size: 0.85rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .alert-box {
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        border: 1px solid;
    }
    .alert-danger { background: #FEE2E2; border-color: #FECACA; color: #991B1B; }
    .alert-warning { background: #FEF3C7; border-color: #FDE68A; color: #92400E; }
    .alert-success { background: #D1FAE5; border-color: #A7F3D0; color: #065F46; }
    
    .alert-icon { font-size: 1.5rem; flex-shrink: 0; margin-top: 0.1rem; }
    .alert-content { flex: 1; }
    .alert-title { font-weight: 600; font-size: 1.05rem; }
    .alert-description { font-size: 0.95rem; opacity: 0.9; margin-top: 0.15rem; }
    .alert-explanation {
        font-size: 0.85rem;
        opacity: 0.8;
        margin-top: 0.25rem;
        padding-top: 0.25rem;
        border-top: 1px solid rgba(0,0,0,0.05);
    }
    
    .insight-box {
        background: white;
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #FDB913;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .insight-box-critical { border-left-color: #EF4444; }
    .insight-box-warning { border-left-color: #F59E0B; }
    .insight-box-success { border-left-color: #10B981; }
    
    .insight-title { font-weight: 600; color: #2D2D2D; font-size: 1.05rem; }
    .insight-content { color: #4B5563; line-height: 1.6; margin-top: 0.5rem; }
    
    .explanation {
        background: #F3F4F6;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #6B7280;
        margin-top: 0.5rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.1rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    .badge-success { background: #10B981; color: white; }
    .badge-warning { background: #F59E0B; color: white; }
    .badge-danger { background: #EF4444; color: white; }
    .badge-info { background: #3B82F6; color: white; }
    
    .component-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #E5E7EB;
    }
    .component-label { font-size: 0.8rem; color: #6B7280; }
    .component-value { font-size: 1.4rem; font-weight: 600; color: #2D2D2D; }
    .progress-bar { width: 100%; background: #E5E7EB; border-radius: 4px; height: 6px; margin-top: 0.5rem; }
    .progress-fill { background: #FDB913; border-radius: 4px; height: 6px; transition: width 0.3s ease; }
    
    .action-card {
        background: white;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border-left: 4px solid #6B7280;
    }
    .action-priority {
        padding: 0.1rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        color: white;
        margin-left: 0.5rem;
    }
    .action-priority-critical { background: #EF4444; }
    .action-priority-high { background: #F59E0B; }
    .action-priority-medium { background: #3B82F6; }
    .action-priority-low { background: #6B7280; }
    
    .divider { border-top: 1px solid #E5E7EB; margin: 1.5rem 0; }
    .gold-border { border-left: 4px solid #FDB913; padding-left: 1rem; }
    
    .material-icons {
        font-family: 'Material Icons';
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
    }
    .icon-sm { font-size: 18px; }
    .icon-md { font-size: 22px; }
    .icon-lg { font-size: 28px; }
    .icon-xl { font-size: 36px; }
    
    .icon-gold { color: #FDB913; }
    .icon-success { color: #10B981; }
    .icon-warning { color: #F59E0B; }
    .icon-danger { color: #EF4444; }
    .icon-info { color: #3B82F6; }
    .icon-dark { color: #2D2D2D; }
    .icon-grey { color: #6B7280; }
    
    .logo-text { font-size: 1.8rem; font-weight: 700; letter-spacing: 1px; }
    .logo-subtitle { font-size: 0.9rem; opacity: 0.8; letter-spacing: 2px; }
    
    .insight-content strong { color: #1F2937; }
    
    .data-source-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: #FDB913;
        color: #2D2D2D;
        margin-left: 0.5rem;
    }
    
    .data-note {
        background: #FEF3C7;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #92400E;
        margin: 0.5rem 0;
        border-left: 4px solid #F59E0B;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOGO HANDLING
# ============================================================================

def load_logo():
    try:
        with open("ctnbo-logo.png", "rb") as f:
            logo_data = f.read()
            logo_base64 = base64.b64encode(logo_data).decode()
            return f"data:image/png;base64,{logo_base64}"
    except:
        return None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clean_number(x):
    if pd.isna(x):
        return 0
    if isinstance(x, (int, float)):
        return float(x) if not pd.isna(x) else 0
    if isinstance(x, str):
        x = x.replace(",", "").replace("%", "").replace(" ", "")
        try:
            return float(x)
        except ValueError:
            return 0
    return 0

def safe_divide(a, b):
    if b == 0:
        return 0
    return a / b

def format_peso(value):
    if pd.isna(value) or value == 0:
        return "₱0"
    return f"₱{value:,.0f}"

def format_percent(value, decimals=1):
    if pd.isna(value):
        return "0%"
    return f"{value:.{decimals}f}%"

def get_percentile_rank(df, column, value):
    if df[column].count() == 0:
        return 0
    return (df[column] < value).sum() / df[column].count() * 100

def render_icon(icon_name, size="md", color="gold"):
    color_class = {
        "gold": "icon-gold", "success": "icon-success", "warning": "icon-warning",
        "danger": "icon-danger", "info": "icon-info", "dark": "icon-dark", "grey": "icon-grey"
    }.get(color, "icon-gold")
    size_class = {"sm": "icon-sm", "md": "icon-md", "lg": "icon-lg", "xl": "icon-xl"}.get(size, "icon-md")
    return f'<span class="material-icons {size_class} {color_class}">{icon_name}</span>'

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_ytd_report(file):
    try:
        raw = pd.read_excel(file, sheet_name="PER NBO", header=None)
    except Exception as e:
        st.error(f"Error loading YTD file: {e}")
        return pd.DataFrame()

    rows = []
    territory = None
    
    for idx, row in raw.iterrows():
        if len(row) < 10:
            continue
            
        name = row.iloc[0] if len(row) > 0 else None
        if pd.isna(name):
            continue
            
        name = str(name).strip()
        if not name or name.startswith('DECEMBER') or name.startswith('NBO NAME') or name.startswith('TOTAL'):
            continue
            
        if "TERRITORY" in name.upper():
            territory = name
            continue
            
        ac_val = clean_number(row.iloc[4]) if len(row) > 4 else 0
        lives_val = clean_number(row.iloc[3]) if len(row) > 3 else 0
        
        if ac_val == 0 and lives_val == 0:
            continue
        
        record = {
            "Territory": territory,
            "NBO": name,
            "Lives": clean_number(row.iloc[3]) if len(row) > 3 else 0,
            "AC": clean_number(row.iloc[4]) if len(row) > 4 else 0,
            "NSC": clean_number(row.iloc[5]) if len(row) > 5 else 0,
            "Lives_PY": clean_number(row.iloc[6]) if len(row) > 6 else 0,
            "AC_PY": clean_number(row.iloc[7]) if len(row) > 7 else 0,
            "NSC_PY": clean_number(row.iloc[8]) if len(row) > 8 else 0,
            "SSP": clean_number(row.iloc[12]) if len(row) > 12 else 0,
            "Target": clean_number(row.iloc[15]) if len(row) > 15 else None,
            "Pct_Target": clean_number(row.iloc[16]) if len(row) > 16 else None,
        }
        
        if record["Lives"] > 0 or record["AC"] > 0:
            rows.append(record)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    df["AC_Growth"] = df.apply(lambda x: safe_divide(x["AC"] - x["AC_PY"], x["AC_PY"]) * 100, axis=1)
    df["NSC_Growth"] = df.apply(lambda x: safe_divide(x["NSC"] - x["NSC_PY"], x["NSC_PY"]) * 100, axis=1)
    df["Lives_Growth"] = df.apply(lambda x: safe_divide(x["Lives"] - x["Lives_PY"], x["Lives_PY"]) * 100, axis=1)

    df["AC_Per_Life"] = df.apply(lambda x: safe_divide(x["AC"], x["Lives"]), axis=1)
    df["NSC_Per_Life"] = df.apply(lambda x: safe_divide(x["NSC"], x["Lives"]), axis=1)

    df["AC_Rank"] = df["AC"].rank(method="min", ascending=False).astype(int)
    df["NSC_Rank"] = df["NSC"].rank(method="min", ascending=False).astype(int)

    return df

@st.cache_data
def load_mtd_report(file):
    try:
        raw = pd.read_excel(file, sheet_name="PER NBO", header=None)
    except Exception as e:
        st.error(f"Error loading MTD file: {e}")
        return pd.DataFrame()

    rows = []
    territory = None
    
    for idx, row in raw.iterrows():
        if idx < 3:
            continue
            
        if len(row) < 10:
            continue
            
        # MTD has NBO in column B (index 1) or C (index 2)
        name = row.iloc[1] if len(row) > 1 else None
        if pd.isna(name):
            name = row.iloc[2] if len(row) > 2 else None
            
        if pd.isna(name):
            continue
            
        name = str(name).strip()
        if not name or name.startswith('NBO NAME'):
            continue
            
        if "TERRITORY" in name.upper():
            territory = name
            continue
        
        # MTD structure: Lives at col 3 (index 3), AC at col 4 (index 4), NSC at col 5 (index 5)
        # PY values at col 6, 7, 8 (indices 6, 7, 8)
        # SSP at col 12, 13 (indices 12, 13)
        
        record = {
            "Territory": territory,
            "NBO": name,
            "Lives": clean_number(row.iloc[3]) if len(row) > 3 else 0,
            "AC": clean_number(row.iloc[4]) if len(row) > 4 else 0,
            "NSC": clean_number(row.iloc[5]) if len(row) > 5 else 0,
            "Lives_PY": clean_number(row.iloc[6]) if len(row) > 6 else 0,
            "AC_PY": clean_number(row.iloc[7]) if len(row) > 7 else 0,
            "NSC_PY": clean_number(row.iloc[8]) if len(row) > 8 else 0,
            "SSP_Current": clean_number(row.iloc[12]) if len(row) > 12 else 0,
            "SSP_Prior": clean_number(row.iloc[13]) if len(row) > 13 else 0,
        }
        
        # MTD doesn't have Target or Pct_Target columns
        # We'll add them as None and handle later
        
        if record["Lives"] > 0 or record["AC"] > 0:
            rows.append(record)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    
    if not df.empty:
        df["AC_Growth"] = df.apply(lambda x: safe_divide(x["AC"] - x["AC_PY"], x["AC_PY"]) * 100, axis=1)
        df["NSC_Growth"] = df.apply(lambda x: safe_divide(x["NSC"] - x["NSC_PY"], x["NSC_PY"]) * 100, axis=1)
        df["Lives_Growth"] = df.apply(lambda x: safe_divide(x["Lives"] - x["Lives_PY"], x["Lives_PY"]) * 100, axis=1)
        df["SSP_Growth"] = df.apply(lambda x: safe_divide(x["SSP_Current"] - x["SSP_Prior"], x["SSP_Prior"]) * 100, axis=1)
        df["AC_Per_Life"] = df.apply(lambda x: safe_divide(x["AC"], x["Lives"]), axis=1)
        
        # Add rank columns for MTD as well
        df["AC_Rank"] = df["AC"].rank(method="min", ascending=False).astype(int)
        df["NSC_Rank"] = df["NSC"].rank(method="min", ascending=False).astype(int)

    return df

# ============================================================================
# CALCULATION ENGINE
# ============================================================================

def determine_verdict(health_score):
    if health_score >= 85:
        return {"label": "STRONG", "icon": "check_circle", "color": COLORS["success"], "description": "Exceptional performance across all metrics"}
    elif health_score >= 70:
        return {"label": "STABLE", "icon": "trending_up", "color": COLORS["warning"], "description": "Solid performance with some areas for improvement"}
    elif health_score >= 50:
        return {"label": "AT RISK", "icon": "warning", "color": COLORS["warning"], "description": "Underperforming in key metrics, requires attention"}
    else:
        return {"label": "CRITICAL", "icon": "error", "color": COLORS["danger"], "description": "Significant underperformance, immediate action needed"}

def calculate_health_score(row, df, has_target=False):
    """Calculate health score - handles missing target data for MTD"""
    ac_growth = row["AC_Growth"]
    ac_score = max(0, min(100, 50 + (ac_growth / 2)))
    
    nsc_growth = row["NSC_Growth"]
    nsc_score = max(0, min(100, 50 + (nsc_growth / 2)))
    
    # Handle target - if not available, use a default or skip
    if has_target and row.get("Pct_Target") is not None:
        target_pct = row.get("Pct_Target", 0) or 0
        target_score = min(target_pct, 100)
        target_weight = 0.25
    else:
        # MTD has no target - redistribute weight to other metrics
        target_score = 50  # Neutral score
        target_weight = 0
    
    company_avg = df["AC_Per_Life"].mean() if df["AC_Per_Life"].mean() > 0 else 1
    productivity_score = min((row["AC_Per_Life"] / company_avg) * 100, 150) if company_avg > 0 else 50
    
    total_nbos = df.shape[0]
    rank_score = ((total_nbos - row["AC_Rank"]) / total_nbos * 100) if total_nbos > 0 else 50
    
    momentum_score = 80 if (ac_growth > 0 and nsc_growth > 0) else 60 if (ac_growth > 0 or nsc_growth > 0) else 40
    
    # Adjust weights based on available data
    if has_target:
        weights = {"ac": 0.25, "nsc": 0.15, "target": 0.25, "productivity": 0.15, "rank": 0.10, "momentum": 0.10}
    else:
        # Redistribute target weight to other metrics
        weights = {"ac": 0.30, "nsc": 0.20, "target": 0, "productivity": 0.20, "rank": 0.15, "momentum": 0.15}
    
    health_score = (
        ac_score * weights["ac"] +
        nsc_score * weights["nsc"] +
        target_score * weights["target"] +
        productivity_score * weights["productivity"] +
        rank_score * weights["rank"] +
        momentum_score * weights["momentum"]
    )
    return max(0, min(100, health_score))

def calculate_health_score_components(row, df, has_target=False):
    ac_growth = row["AC_Growth"]
    ac_score = max(0, min(100, 50 + (ac_growth / 2)))
    
    nsc_growth = row["NSC_Growth"]
    nsc_score = max(0, min(100, 50 + (nsc_growth / 2)))
    
    if has_target and row.get("Pct_Target") is not None:
        target_pct = row.get("Pct_Target", 0) or 0
        target_score = min(target_pct, 100)
        target_weight = 0.25
        target_display = f"{target_pct:.1f}%"
    else:
        target_pct = None
        target_score = 50
        target_weight = 0
        target_display = "N/A (MTD)"
    
    company_avg = df["AC_Per_Life"].mean() if df["AC_Per_Life"].mean() > 0 else 1
    productivity_score = min((row["AC_Per_Life"] / company_avg) * 100, 150) if company_avg > 0 else 50
    
    total_nbos = df.shape[0]
    rank_score = ((total_nbos - row["AC_Rank"]) / total_nbos * 100) if total_nbos > 0 else 50
    
    momentum_score = 80 if (ac_growth > 0 and nsc_growth > 0) else 60 if (ac_growth > 0 or nsc_growth > 0) else 40
    
    if has_target:
        weights = {"ac": 0.25, "nsc": 0.15, "target": 0.25, "productivity": 0.15, "rank": 0.10, "momentum": 0.10}
    else:
        weights = {"ac": 0.30, "nsc": 0.20, "target": 0, "productivity": 0.20, "rank": 0.15, "momentum": 0.15}
    
    health_score = (
        ac_score * weights["ac"] +
        nsc_score * weights["nsc"] +
        target_score * weights["target"] +
        productivity_score * weights["productivity"] +
        rank_score * weights["rank"] +
        momentum_score * weights["momentum"]
    )
    health_score = max(0, min(100, health_score))
    
    components = {
        "AC Growth": {"score": ac_score, "weight": weights["ac"], "value": ac_growth, "display": f"{ac_growth:.1f}%"},
        "NSC Growth": {"score": nsc_score, "weight": weights["nsc"], "value": nsc_growth, "display": f"{nsc_growth:.1f}%"},
        "Target Attainment": {"score": target_score, "weight": weights["target"], "value": target_pct, "display": target_display},
        "Productivity": {"score": productivity_score, "weight": weights["productivity"], "value": row["AC_Per_Life"], "display": format_peso(row["AC_Per_Life"])},
        "Competitive Position": {"score": rank_score, "weight": weights["rank"], "value": row["AC_Rank"], "display": f"#{row['AC_Rank']}"},
        "Momentum": {"score": momentum_score, "weight": weights["momentum"], "value": "Positive" if ac_growth > 0 else "Negative", "display": "Positive" if ac_growth > 0 else "Negative"}
    }
    
    return {"score": health_score, "components": components}

def calculate_threat_metrics(row, df):
    above = df[df["AC_Rank"] < row["AC_Rank"]]
    below = df[df["AC_Rank"] > row["AC_Rank"]]
    
    threats = {}
    
    if not above.empty:
        threats["gap_to_next"] = above.iloc[0]["AC"] - row["AC"]
        threats["next_nbo"] = above.iloc[0]["NBO"]
        threats["next_ac"] = above.iloc[0]["AC"]
    else:
        threats["gap_to_next"] = 0
        threats["next_nbo"] = None
        
    if not below.empty:
        threats["gap_to_prev"] = row["AC"] - below.iloc[0]["AC"]
        threats["prev_nbo"] = below.iloc[0]["NBO"]
    else:
        threats["gap_to_prev"] = 0
        threats["prev_nbo"] = None
        
    if threats["gap_to_prev"] > 0:
        threat_pct = safe_divide(threats["gap_to_prev"], row["AC"]) * 100
        if threat_pct < 5:
            threats["threat_level"] = "HIGH"
            threats["threat_text"] = "Immediate threat - competitor is very close"
        elif threat_pct < 10:
            threats["threat_level"] = "MEDIUM"
            threats["threat_text"] = "Moderate threat - competitor is gaining"
        else:
            threats["threat_level"] = "LOW"
            threats["threat_text"] = "Low threat - comfortable lead"
    else:
        threats["threat_level"] = "NONE"
        threats["threat_text"] = "No immediate threat"
    
    if threats["gap_to_next"] > 0:
        threats["opportunity_value"] = threats["gap_to_next"]
        threats["opportunity_percent"] = safe_divide(threats["gap_to_next"], row["AC"]) * 100
    else:
        threats["opportunity_value"] = 0
        threats["opportunity_percent"] = 0
    
    top_10_avg = df.nlargest(10, "AC")["AC_Per_Life"].mean() if df.shape[0] >= 10 else df["AC_Per_Life"].max()
    threats["productivity_gap"] = max(top_10_avg - row["AC_Per_Life"], 0)
    threats["productivity_opportunity"] = threats["productivity_gap"] * row["Lives"]
    
    return threats

def calculate_forecast(row, has_target=False):
    if has_target and row.get("Target") is not None and row["Target"] > 0:
        target = row["Target"]
        target_attainment = safe_divide(row["AC"], target) * 100
        gap_to_target = max(target - (row["AC"] * 2), 0)  # Annualized projection
    else:
        target = row["AC"] * 2.5  # Estimate target as 2.5x current AC
        target_attainment = safe_divide(row["AC"], target) * 100
        gap_to_target = max(target - (row["AC"] * 2), 0)
    
    annual_projection = row["AC"] * 2
    
    return {
        "target": target,
        "target_attainment": target_attainment,
        "gap_to_target": gap_to_target,
        "annual_projection": annual_projection,
        "current_ac": row["AC"],
        "has_target": has_target and row.get("Target") is not None and row["Target"] > 0
    }

def calculate_revenue_leakage(row):
    leakage = {
        "ac_leakage": max(row["AC_PY"] - row["AC"], 0),
        "nsc_leakage": max(row["NSC_PY"] - row["NSC"], 0),
        "lives_leakage": max(row["Lives_PY"] - row["Lives"], 0),
    }
    
    recovery = {}
    for recovery_rate in [0.25, 0.50, 0.75]:
        recovery[f"{int(recovery_rate * 100)}%"] = {
            "ac": leakage["ac_leakage"] * recovery_rate,
            "nsc": leakage["nsc_leakage"] * recovery_rate,
            "lives": leakage["lives_leakage"] * recovery_rate,
        }
    
    return leakage, recovery

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_alert_box(verdict, health_score):
    if health_score < 50:
        alert_class, icon_name, icon_color = "alert-danger", "error", "danger"
    elif health_score < 70:
        alert_class, icon_name, icon_color = "alert-warning", "warning", "warning"
    else:
        alert_class, icon_name, icon_color = "alert-success", "check_circle", "success"
    
    st.markdown(f"""
    <div class="alert-box {alert_class}">
        <div class="alert-icon">{render_icon(icon_name, size="lg", color=icon_color)}</div>
        <div class="alert-content">
            <div class="alert-title">Verdict: {verdict['label']}</div>
            <div class="alert-description">{verdict['description']}</div>
            <div class="alert-explanation">
                {render_icon('info', size='sm', color='grey')}
                Health Score combines 6 metrics: AC Growth, NSC Growth, Target Attainment, Productivity, Competitive Rank, and Momentum
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_insight_card(icon_name, title, content, status="info", explanation=None):
    status_classes = {
        "strong": "insight-box-success", "stable": "insight-box",
        "risk": "insight-box-warning", "critical": "insight-box-critical", "info": "insight-box"
    }
    status_colors = {
        "strong": "success", "stable": "warning", "risk": "warning", "critical": "danger", "info": "info"
    }
    color = status_colors.get(status, "info")
    cls = status_classes.get(status, "insight-box")
    badge_class = {"strong": "badge-success", "stable": "badge-info", "risk": "badge-warning", "critical": "badge-danger", "info": "badge-info"}.get(status, "badge-info")
    
    html = f'<div class="{cls}">'
    html += f'<div>{render_icon(icon_name, size="md", color=color)}<span class="insight-title">{title}</span><span class="badge {badge_class}">{status.upper()}</span></div>'
    html += f'<div class="insight-content">{content}</div>'
    if explanation:
        html += f'<div class="explanation">{render_icon("info", size="sm", color="grey")} {explanation}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_data_note(has_target, data_source):
    """Show a note if target data is not available (MTD)"""
    if not has_target:
        st.markdown(f"""
        <div class="data-note">
            {render_icon('info', size='sm', color='warning')} 
            <strong>Note:</strong> This is {data_source} data. Target attainment information is only available in YTD files.
            The Health Score has been adjusted to exclude target data (weight redistributed to other metrics).
        </div>
        """, unsafe_allow_html=True)

def render_executive_overview(row, df, health_score, verdict, data_source, has_target):
    logo_html = load_logo()
    if logo_html:
        st.markdown(f"""
        <div class="main-header">
            <div class="logo-container">
                <img src="{logo_html}" style="height:60px; width:auto;" />
                <div>
                    <div class="logo-text">CENTURION TREE</div>
                    <div class="logo-subtitle">Executive Insights • Performance Intelligence Platform</div>
                    <div style="opacity:0.6; font-size:0.85rem; margin-top:0.25rem;">
                        {render_icon('calendar_today', size='sm', color='grey')} {datetime.now().strftime("%B %d, %Y")}
                        <span class="data-source-badge">{data_source}</span>
                        {'' if has_target else '<span class="data-source-badge" style="background:#F59E0B;">MTD Only</span>'}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="main-header">
            <div style="display:flex; align-items:center; gap:1rem;">
                {render_icon('workspace_premium', size='xl', color='gold')}
                <div>
                    <div style="font-size:2rem;font-weight:700;">CENTURION TREE</div>
                    <div style="opacity:0.8;">Executive Insights • Performance Intelligence Platform</div>
                    <div style="opacity:0.6; font-size:0.85rem; margin-top:0.25rem;">
                        {render_icon('calendar_today', size='sm', color='grey')} {datetime.now().strftime("%B %d, %Y")}
                        <span class="data-source-badge">{data_source}</span>
                        {'' if has_target else '<span class="data-source-badge" style="background:#F59E0B;">MTD Only</span>'}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show note for MTD data
    render_data_note(has_target, data_source)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{render_icon('favorite', size='sm', color='gold')} Health Score</div>
            <div class="health-score">{health_score:.0f}</div>
            <div style="font-size:0.85rem; color: {COLORS['warning'] if health_score < 70 else COLORS['success']};">
                {render_icon('info', size='sm', color='warning' if health_score < 70 else 'success')} {verdict['label']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.metric("Annualized AC", format_peso(row["AC"]), delta=f"{row['AC_Growth']:.1f}%" if row.get("AC_Growth") else None)
    with col3:
        st.metric("Annualized NSC", format_peso(row["NSC"]), delta=f"{row['NSC_Growth']:.1f}%" if row.get("NSC_Growth") else None)
    with col4:
        st.metric("Lives", f"{row['Lives']:,.0f}", delta=f"{row['Lives_Growth']:.1f}%" if row.get("Lives_Growth") else None)
    with col5:
        pct_rank = row['AC_Rank']/df.shape[0]*100 if df.shape[0] > 0 else 0
        st.metric("AC Rank", f"#{row['AC_Rank']} of {df.shape[0]}", delta=f"Top {pct_rank:.0f}%" if df.shape[0] > 0 else "")
    with col6:
        if has_target and row.get("Pct_Target") is not None:
            target_pct = row.get("Pct_Target", 0) or 0
            st.metric("Target Attainment", f"{target_pct:.1f}%", delta="On Track" if target_pct > 80 else "Needs Attention" if target_pct > 50 else "Behind Target")
        else:
            st.metric("Target Attainment", "N/A", delta="MTD Data Only")

    render_alert_box(verdict, health_score)

def render_component_breakdown(health_data, has_target):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('assessment', size='lg', color='gold')}
        <h3 style="margin:0;">Health Score Components</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Each component contributes to the overall health score. Higher scores mean better performance.</p>
    """, unsafe_allow_html=True)
    
    components = health_data['components']
    cols = st.columns(3)
    
    for idx, (name, data) in enumerate(components.items()):
        with cols[idx % 3]:
            status = "strong" if data['score'] >= 70 else "stable" if data['score'] >= 50 else "risk"
            icon_map = {
                "AC Growth": "trending_up",
                "NSC Growth": "trending_up",
                "Target Attainment": "target",
                "Productivity": "speed",
                "Competitive Position": "emoji_events",
                "Momentum": "rocket"
            }
            icon_name = icon_map.get(name, "assessment")
            
            explanations = {
                "AC Growth": "How much your Annualized Commission has grown compared to last year",
                "NSC Growth": "How much your New Single Commission has grown compared to last year",
                "Target Attainment": "Percentage of your annual target you've achieved so far (N/A for MTD)",
                "Productivity": "How much AC you generate per life (efficiency measure)",
                "Competitive Position": "Your rank compared to other NBOs",
                "Momentum": "Whether you're trending in the right direction"
            }
            
            weight_display = f"Weight: {data['weight']*100:.0f}%" if data['weight'] > 0 else "Not applicable (MTD)"
            
            st.markdown(f"""
            <div class="component-card">
                <div class="component-label">
                    {render_icon(icon_name, size='sm', color=('success' if status=='strong' else 'warning' if status=='stable' else 'danger'))}
                    {name}
                    <span style="float:right; font-size:0.7rem; color:#6B7280;">
                        {weight_display}
                    </span>
                </div>
                <div class="component-value">{data['display']}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:{data['score']}%;"></div>
                </div>
                <div style="font-size:0.8rem; color:#6B7280; margin-top:0.25rem;">
                    Score: {data['score']:.0f}/100
                </div>
                <div style="font-size:0.75rem; color:#6B7280; margin-top:0.25rem; font-style:italic;">
                    {render_icon('info', size='sm', color='grey')} {explanations.get(name, '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_executive_briefing(row, health_score, verdict, threats, forecast, df, data_source, has_target):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('description', size='lg', color='gold')}
        <h3 style="margin:0;">Executive Briefing - {data_source}</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">What this data means for CENTURION TREE</p>
    """, unsafe_allow_html=True)
    
    # Show data source note
    if not has_target:
        st.markdown(f"""
        <div class="data-note">
            {render_icon('info', size='sm', color='warning')} 
            <strong>MTD Data:</strong> This analysis is based on Month-to-Date data. 
            Target attainment and some long-term performance metrics are only available in YTD data.
        </div>
        """, unsafe_allow_html=True)
    
    # Performance summary
    rank_pct = row['AC_Rank']/df.shape[0]*100 if df.shape[0] > 0 else 0
    st.markdown(f"""
    <div class="insight-box gold-border">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            {render_icon('analytics', size='md', color='gold')}
            <span class="insight-title">Performance Summary</span>
        </div>
        <div class="insight-content">
            <strong>Here's how CENTURION TREE is performing {data_source}:</strong><br><br>
            • Total Annualized Commission: <strong>{format_peso(row['AC'])}</strong>
            • Health Score: <strong>{health_score:.0f}/100</strong> - This is a {verdict['label'].lower()} position
            • Rank: <strong>#{row['AC_Rank']}</strong> out of <strong>{df.shape[0]}</strong> NBOs
            • You're in the <strong>top {rank_pct:.0f}%</strong> of performers
            {'' if has_target else '<br>• <em>Target data not available (MTD only)</em>'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Growth explanation
    if row["AC_Growth"] > 0:
        status, icon, title = "strong", "trending_up", f"Good News: AC is Growing at {row['AC_Growth']:.1f}%"
        content = f"""
        <strong>Your Annualized Commission is increasing.</strong><br><br>
        • Last year: <strong>{format_peso(row['AC_PY'])}</strong>
        • This {data_source}: <strong>{format_peso(row['AC'])}</strong>
        • You've gained <strong>{format_peso(row['AC'] - row['AC_PY'])}</strong> in AC
        • This is <strong>positive momentum</strong> - keep doing what's working!
        """
        explanation = f"AC Growth compares current period to last year. {row['AC_Growth']:.1f}% growth means you're acquiring more business or higher-value clients."
    else:
        status, icon, title = "risk", "trending_down", f"Alert: AC is Declining at {abs(row['AC_Growth']):.1f}%"
        content = f"""
        <strong>Your Annualized Commission is decreasing.</strong><br><br>
        • Last year: <strong>{format_peso(row['AC_PY'])}</strong>
        • This {data_source}: <strong>{format_peso(row['AC'])}</strong>
        • You've lost <strong>{format_peso(abs(row['AC_PY'] - row['AC']))}</strong> in AC
        • <strong>Action needed:</strong> Review what's changed and identify growth opportunities
        """
        explanation = f"AC Growth compares current period to last year. A decline of {abs(row['AC_Growth']):.1f}% needs attention. Focus on top-performing products and client segments."
    
    render_insight_card(icon, title, content, status, explanation)

    # Competitive position
    if threats.get("gap_to_next", 0) > 0:
        status, icon, title = "stable", "rocket", f"Opportunity: Move Up to #{row['AC_Rank'] - 1}"
        content = f"""
        <strong>You have a clear opportunity to improve your ranking.</strong><br><br>
        • Next NBO: <strong>{threats['next_nbo']}</strong> with {format_peso(threats['next_ac'])}
        • Gap to overtake them: <strong>{format_peso(threats['gap_to_next'])}</strong>
        • That's <strong>{threats['opportunity_percent']:.1f}%</strong> more AC than you have now
        • <strong>Suggestion:</strong> Focus on high-value clients and products to close this gap
        """
        explanation = f"The gap to {threats['next_nbo']} is the additional AC needed to move up one rank. Every ₱1 of AC counts toward closing this gap."
    else:
        status, icon, title = "strong", "emoji_events", "Top Performer - No Competitors Ahead"
        content = f"""
        <strong>Congratulations! You're the #1 performer.</strong><br><br>
        • No NBO has higher AC than you
        • Focus on maintaining your position
        • Keep growing to extend your lead
        """
        explanation = "Being rank #1 means you're the top performer. The focus should be on maintaining and extending this position."
    
    render_insight_card(icon, title, content, status, explanation)

    # Target performance - only if available
    if has_target and row.get("Pct_Target") is not None:
        target_pct = row.get("Pct_Target", 0) or 0
        if target_pct > 80:
            status, icon, title = "strong", "target", f"Target Performance: {target_pct:.1f}% - On Track!"
            content = f"""
            <strong>You're making good progress toward your annual target.</strong><br><br>
            • Target: <strong>{format_peso(forecast['target'])}</strong>
            • Achieved: <strong>{format_peso(row['AC'])}</strong>
            • That's <strong>{target_pct:.1f}%</strong> of your target
            • <strong>Keep it up!</strong> You're on track to exceed your target
            """
            explanation = f"Target attainment shows how much of your annual target you've achieved. {target_pct:.1f}% means you're ahead of schedule."
        elif target_pct > 50:
            status, icon, title = "stable", "target", f"Target Performance: {target_pct:.1f}% - Needs Acceleration"
            content = f"""
            <strong>You're making progress, but need to accelerate.</strong><br><br>
            • Target: <strong>{format_peso(forecast['target'])}</strong>
            • Achieved: <strong>{format_peso(row['AC'])}</strong>
            • Remaining: <strong>{format_peso(forecast['gap_to_target'])}</strong>
            • <strong>Suggestion:</strong> Increase sales activities and focus on high-value opportunities
            """
            explanation = f"Target attainment of {target_pct:.1f}% means you have {format_peso(forecast['gap_to_target'])} left to reach your target. Accelerate your efforts."
        else:
            status, icon, title = "critical", "error", f"Target Alert: {target_pct:.1f}% - Urgent Action Needed"
            content = f"""
            <strong>Target attainment is significantly behind schedule.</strong><br><br>
            • Target: <strong>{format_peso(forecast['target'])}</strong>
            • Achieved: <strong>{format_peso(row['AC'])}</strong>
            • Gap: <strong>{format_peso(forecast['gap_to_target'])}</strong>
            • <strong>Action required:</strong> Urgent review of sales strategy and target approach needed
            """
            explanation = f"Target attainment of {target_pct:.1f}% requires immediate intervention. Focus on high-value opportunities and accelerate sales activities."
        
        render_insight_card(icon, title, content, status, explanation)

def render_mtd_comparison(ytd_row, mtd_row, df):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('compare_arrows', size='lg', color='gold')}
        <h3 style="margin:0;">MTD vs YTD Comparison</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">How this month compares to your average month</p>
    """, unsafe_allow_html=True)
    
    # Calculate MTD vs YTD monthly average
    mtd_ac = mtd_row["AC"]
    mtd_nsc = mtd_row["NSC"]
    mtd_lives = mtd_row["Lives"]
    
    ytd_monthly_avg_ac = ytd_row["AC"] / 6
    ytd_monthly_avg_nsc = ytd_row["NSC"] / 6
    ytd_monthly_avg_lives = ytd_row["Lives"] / 6
    
    ac_diff_pct = safe_divide(mtd_ac - ytd_monthly_avg_ac, ytd_monthly_avg_ac) * 100
    nsc_diff_pct = safe_divide(mtd_nsc - ytd_monthly_avg_nsc, ytd_monthly_avg_nsc) * 100
    lives_diff_pct = safe_divide(mtd_lives - ytd_monthly_avg_lives, ytd_monthly_avg_lives) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if ac_diff_pct > 0:
            st.metric(
                label="AC - This Month vs Average",
                value=f"+{ac_diff_pct:.1f}%",
                delta=f"{format_peso(mtd_ac)} vs {format_peso(ytd_monthly_avg_ac)}",
                delta_color="normal"
            )
            st.markdown(f"""
            <div class="explanation">
                {render_icon('trending_up', size='sm', color='success')} 
                This month is performing <strong>{ac_diff_pct:.1f}% better</strong> than your average month.
                This is <strong>great momentum</strong>!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.metric(
                label="AC - This Month vs Average",
                value=f"{ac_diff_pct:.1f}%",
                delta=f"{format_peso(mtd_ac)} vs {format_peso(ytd_monthly_avg_ac)}",
                delta_color="inverse"
            )
            st.markdown(f"""
            <div class="explanation">
                {render_icon('trending_down', size='sm', color='danger')} 
                This month is performing <strong>{abs(ac_diff_pct):.1f}% lower</strong> than your average month.
                <strong>Action needed</strong> to improve performance.
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if nsc_diff_pct > 0:
            st.metric(
                label="NSC - This Month vs Average",
                value=f"+{nsc_diff_pct:.1f}%",
                delta=f"{format_peso(mtd_nsc)} vs {format_peso(ytd_monthly_avg_nsc)}",
                delta_color="normal"
            )
            st.markdown(f"""
            <div class="explanation">
                {render_icon('trending_up', size='sm', color='success')} 
                NSC is <strong>{nsc_diff_pct:.1f}% higher</strong> than your average month.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.metric(
                label="NSC - This Month vs Average",
                value=f"{nsc_diff_pct:.1f}%",
                delta=f"{format_peso(mtd_nsc)} vs {format_peso(ytd_monthly_avg_nsc)}",
                delta_color="inverse"
            )
            st.markdown(f"""
            <div class="explanation">
                {render_icon('trending_down', size='sm', color='danger')} 
                NSC is <strong>{abs(nsc_diff_pct):.1f}% lower</strong> than your average month.
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if lives_diff_pct > 0:
            st.metric(
                label="Lives - This Month vs Average",
                value=f"+{lives_diff_pct:.1f}%",
                delta=f"{mtd_lives:,.0f} vs {ytd_monthly_avg_lives:,.0f}",
                delta_color="normal"
            )
            st.markdown(f"""
            <div class="explanation">
                {render_icon('trending_up', size='sm', color='success')} 
                Lives are <strong>{lives_diff_pct:.1f}% higher</strong> than your average month.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.metric(
                label="Lives - This Month vs Average",
                value=f"{lives_diff_pct:.1f}%",
                delta=f"{mtd_lives:,.0f} vs {ytd_monthly_avg_lives:,.0f}",
                delta_color="inverse"
            )
            st.markdown(f"""
            <div class="explanation">
                {render_icon('trending_down', size='sm', color='danger')} 
                Lives are <strong>{abs(lives_diff_pct):.1f}% lower</strong> than your average month.
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### What This Means For You")
    
    positive_count = sum([ac_diff_pct > 0, nsc_diff_pct > 0, lives_diff_pct > 0])
    
    if positive_count == 3:
        st.success(f"""
        {render_icon('check_circle', size='md', color='success')} 
        **Excellent Month!** All metrics are above average.
        - Your AC, NSC, and Lives are all performing better than usual
        - This is a sign of **strong momentum**
        - Keep doing what you're doing, and consider documenting your successful strategies
        """)
    elif positive_count >= 2:
        st.info(f"""
        {render_icon('trending_up', size='md', color='info')} 
        **Good Month!** Most metrics are above average.
        - {positive_count} out of 3 metrics are performing better than usual
        - Focus on improving the metric(s) that are underperforming
        - You're on the right track
        """)
    else:
        st.warning(f"""
        {render_icon('warning', size='md', color='warning')} 
        **Needs Attention.** Most metrics are below average.
        - Only {positive_count} out of 3 metrics are above average
        - <strong>Action needed:</strong> Review what's changed this month
        - Consider accelerating sales activities and focusing on high-value opportunities
        """)

def render_threat_monitor(threats, row):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('shield', size='lg', color='gold')}
        <h3 style="margin:0;">Threat Monitor</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Competitive intelligence - who's ahead and who's behind</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if threats["gap_to_next"] > 0:
            st.info(f"""
            <strong>{render_icon('rocket', size='md', color='info')} Opportunity</strong><br><br>
            <strong>{threats['next_nbo']}</strong> is currently ahead of you.<br>
            • Their AC: {format_peso(threats['next_ac'])}<br>
            • Your AC: {format_peso(row['AC'])}<br>
            • Gap: {format_peso(threats['gap_to_next'])}<br><br>
            You need <strong>+{threats['opportunity_percent']:.1f}%</strong> more AC to overtake them.
            """)
        else:
            st.success(f"""
            <strong>{render_icon('emoji_events', size='md', color='success')} Top Position</strong><br><br>
            You are the <strong>#1 performer</strong> among all NBOs.<br>
            No one is ahead of you. Keep up the great work!
            """)
    
    with col2:
        if threats["gap_to_prev"] > 0:
            threat_pct = safe_divide(threats["gap_to_prev"], row["AC"]) * 100
            if threat_pct < 5:
                st.warning(f"""
                <strong>{render_icon('warning', size='md', color='warning')} HIGH Threat</strong><br><br>
                <strong>{threats['prev_nbo']}</strong> is very close behind you.<br>
                • Their AC: {format_peso(row['AC'] - threats['gap_to_prev'])}<br>
                • Your AC: {format_peso(row['AC'])}<br>
                • Gap: {format_peso(threats['gap_to_prev'])}<br>
                • That's only <strong>{threat_pct:.1f}%</strong> of your AC<br><br>
                <strong>Action needed:</strong> Accelerate growth to maintain your position.
                """)
            elif threat_pct < 10:
                st.info(f"""
                <strong>{render_icon('trending_up', size='md', color='info')} Medium Threat</strong><br><br>
                <strong>{threats['prev_nbo']}</strong> is gaining on you.<br>
                • Gap: {format_peso(threats['gap_to_prev'])}<br>
                • That's {threat_pct:.1f}% of your AC<br><br>
                Keep growing to stay ahead.
                """)
            else:
                st.success(f"""
                <strong>{render_icon('shield', size='md', color='success')} Low Threat</strong><br><br>
                <strong>{threats['prev_nbo']}</strong> is behind you with a comfortable lead.<br>
                • Gap: {format_peso(threats['gap_to_prev'])}<br>
                • That's {threat_pct:.1f}% of your AC<br><br>
                You have a <strong>comfortable buffer</strong>. Maintain your performance.
                """)
        else:
            st.info(f"""
            <strong>{render_icon('shield', size='md', color='info')} No Immediate Threats</strong><br><br>
            There are no NBOs close behind you in the rankings.
            Focus on growing your AC to move up further.
            """)

def render_forecast_center(forecast, row, has_target):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('trending_up', size='lg', color='gold')}
        <h3 style="margin:0;">Forecast Center</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Projected performance based on current trends</p>
    """, unsafe_allow_html=True)
    
    if not has_target:
        st.markdown(f"""
        <div class="data-note">
            {render_icon('info', size='sm', color='warning')} 
            <strong>Note:</strong> Target data is only available in YTD files. 
            The target shown below is estimated based on current AC.
        </div>
        """, unsafe_allow_html=True)
    
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "indicator"}, {"type": "bar"}]],
                        subplot_titles=("Target Progress", "Annual Projection Scenarios"))
    
    fig.add_trace(go.Indicator(mode="gauge+number+delta", value=forecast["target_attainment"],
                               domain={"x": [0, 1], "y": [0, 1]}, delta={"reference": 100},
                               gauge={"axis": {"range": [0, 150]}, "bar": {"color": SUN_LIFE_GOLD},
                                      "steps": [{"range": [0, 50], "color": "red"},
                                               {"range": [50, 80], "color": "yellow"},
                                               {"range": [80, 150], "color": "green"}],
                                      "threshold": {"line": {"color": "black", "width": 4},
                                                   "thickness": 0.75, "value": 100}}),
                  row=1, col=1)
    
    current_ac = forecast["current_ac"]
    scenarios = {"Worst Case": current_ac * 1.8, "Expected": current_ac * 2.2, "Best Case": current_ac * 2.5}
    fig.add_trace(go.Bar(x=list(scenarios.keys()), y=list(scenarios.values()),
                         text=[format_peso(v) for v in scenarios.values()], textposition="auto",
                         marker_color=[COLORS["danger"], SUN_LIFE_GOLD, COLORS["success"]]),
                  row=1, col=2)
    
    fig.update_layout(height=350, showlegend=False, template="plotly_white", margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Current Daily Pace**\n\n{format_peso(forecast['annual_projection'] / 365)} per day")
    with col2:
        st.info(f"**Annual Projection**\n\n{format_peso(forecast['annual_projection'])}")
    with col3:
        if forecast["gap_to_target"] > 0:
            st.warning(f"**Gap to Target**\n\n{format_peso(forecast['gap_to_target'])}")
        else:
            st.success("**Target Achieved**\n\n✅ On track to meet or exceed target")

def render_productivity_benchmark(row, df):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('speed', size='lg', color='gold')}
        <h3 style="margin:0;">Productivity Benchmark</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">How efficient you are compared to others</p>
    """, unsafe_allow_html=True)
    
    company_avg = df["AC_Per_Life"].mean() if df["AC_Per_Life"].mean() > 0 else 0
    top_10_avg = df.nlargest(10, "AC")["AC_Per_Life"].mean() if df.shape[0] >= 10 else df["AC_Per_Life"].max()
    top_3_avg = df.nlargest(3, "AC")["AC_Per_Life"].mean() if df.shape[0] >= 3 else df["AC_Per_Life"].max()
    percentile = get_percentile_rank(df, "AC_Per_Life", row["AC_Per_Life"])
    
    benchmark_data = pd.DataFrame({
        "Category": ["You", "Company Avg", "Top 10 Avg", "Top 3 Avg"],
        "AC Per Life": [row["AC_Per_Life"], company_avg, top_10_avg, top_3_avg]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=benchmark_data["Category"], y=benchmark_data["AC Per Life"],
                         text=[format_peso(v) for v in benchmark_data["AC Per Life"]], textposition="auto",
                         marker_color=[SUN_LIFE_GOLD, "#6B7280", "#3B82F6", "#10B981"]))
    fig.update_layout(title="AC Per Life Comparison", height=350, template="plotly_white",
                      margin=dict(l=0, r=0, t=50, b=0), yaxis_title="AC Per Life")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Productivity Rank", f"{percentile:.0f}th percentile", delta=f"of {df.shape[0]} NBOs")
    with col2:
        if row["AC_Per_Life"] >= top_10_avg:
            st.success(f"🏆 You're above the Top 10 average! {format_peso(row['AC_Per_Life'])} vs {format_peso(top_10_avg)}")
        elif row["AC_Per_Life"] >= company_avg:
            st.info(f"📊 You're above company average: {format_peso(row['AC_Per_Life'])} vs {format_peso(company_avg)}")
        else:
            st.warning(f"⚠️ You're below company average: {format_peso(row['AC_Per_Life'])} vs {format_peso(company_avg)}")

def render_revenue_leakage(leakage, recovery, row):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('money_off', size='lg', color='gold')}
        <h3 style="margin:0;">Revenue Leakage</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Opportunities to recover lost revenue</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if leakage["ac_leakage"] > 0:
            st.error(f"""
            <strong>{render_icon('warning', size='md', color='danger')} AC Leakage Detected</strong><br><br>
            • You've lost {format_peso(leakage['ac_leakage'])} in AC compared to last year<br>
            • That's {safe_divide(leakage['ac_leakage'], row['AC_PY']) * 100:.1f}% of last year's total<br><br>
            <strong>Recovery Scenarios:</strong>
            """)
            rec_df = pd.DataFrame({
                "Recovery Rate": list(recovery.keys()),
                "Recovered AC": [format_peso(r["ac"]) for r in recovery.values()]
            })
            st.dataframe(rec_df, hide_index=True, use_container_width=True)
        else:
            st.success(f"""
            <strong>{render_icon('check_circle', size='md', color='success')} No AC Leakage</strong><br><br>
            Your AC has increased or remained stable compared to last year.
            Current: {format_peso(row['AC'])} vs Last Year: {format_peso(row['AC_PY'])}
            """)
    
    with col2:
        if leakage["lives_leakage"] > 0:
            st.warning(f"""
            <strong>{render_icon('groups', size='md', color='warning')} Lives Leakage Detected</strong><br><br>
            • You've lost {leakage['lives_leakage']:,.0f} lives compared to last year<br>
            • That's {safe_divide(leakage['lives_leakage'], row['Lives_PY']) * 100:.1f}% of last year's total<br>
            • <strong>Action needed:</strong> Focus on client retention and acquisition
            """)
        else:
            st.success(f"""
            <strong>{render_icon('check_circle', size='md', color='success')} No Lives Leakage</strong><br><br>
            Your lives have increased or remained stable.
            Current: {row['Lives']:,.0f} vs Last Year: {row['Lives_PY']:,.0f}
            """)

def render_competitive_position(row, df):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('emoji_events', size='lg', color='gold')}
        <h3 style="margin:0;">Competitive Position</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Where you stand among all NBOs</p>
    """, unsafe_allow_html=True)
    
    top_n = min(15, df.shape[0])
    ladder_data = df.nsmallest(top_n, "AC_Rank")[["NBO", "AC", "AC_Rank"]].copy()
    ladder_data["Color"] = ladder_data["NBO"].apply(
        lambda x: SUN_LIFE_GOLD if "CENTURION" in str(x).upper() else "#6B7280")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(y=ladder_data["NBO"], x=ladder_data["AC"], orientation="h",
                         marker_color=ladder_data["Color"],
                         text=[format_peso(v) for v in ladder_data["AC"]], textposition="outside",
                         hovertemplate="%{y}<br>AC: %{text}<br>Rank: %{customdata}<extra></extra>",
                         customdata=ladder_data["AC_Rank"]))
    fig.update_layout(title="AC Rank Ladder (Top 15)", xaxis_title="Annualized AC", yaxis_title="NBO",
                      height=400, template="plotly_white", margin=dict(l=0, r=50, t=50, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    row_rank = row["AC_Rank"]
    total = df.shape[0]
    ahead = row_rank - 1
    behind = total - row_rank
    
    st.markdown(f"""
    <div class="insight-box gold-border">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            {render_icon('analytics', size='md', color='gold')}
            <span class="insight-title">Your Position</span>
        </div>
        <div class="insight-content">
            <strong>Rank #{row_rank} of {total} NBOs</strong><br><br>
            • <strong>{ahead}</strong> NBOs are ahead of you<br>
            • <strong>{behind}</strong> NBOs are behind you<br>
            • You're in the <strong>top {row_rank/total*100:.0f}%</strong> of performers<br><br>
            {f'<strong>Next target:</strong> Overtake #{row_rank - 1} (need +{format_peso(df.nsmallest(row_rank, "AC_Rank").iloc[-2]["AC"] - row["AC"])})' if row_rank > 1 else '<strong>🏆 You\'re the #1 performer!</strong>'}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_management_actions(row, threats, forecast, health_score, data_source, has_target):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('task_alt', size='lg', color='gold')}
        <h3 style="margin:0;">Action Center - {data_source}</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Prioritized actions based on your performance</p>
    """, unsafe_allow_html=True)
    
    actions = []
    
    if health_score < 60:
        actions.append({
            "priority": "CRITICAL",
            "action": "🚨 Immediate Performance Review Needed",
            "details": f"Your health score is {health_score:.0f}/100, which is below 60. This requires urgent attention. Schedule a comprehensive review of all performance drivers."
        })
    
    if row.get("AC_Growth", 0) < 0:
        actions.append({
            "priority": "HIGH",
            "action": "📉 Reverse AC Decline",
            "details": f"AC is down {abs(row['AC_Growth']):.1f}%. Focus on your top-performing products and client segments. Consider reaching out to high-value clients."
        })
    
    if threats.get("threat_level") in ["HIGH", "MEDIUM"]:
        actions.append({
            "priority": "HIGH",
            "action": f"🛡️ Defend Position from {threats['prev_nbo']}",
            "details": f"Competitor is only {format_peso(threats['gap_to_prev'])} behind. Increase productivity and accelerate growth to maintain your lead."
        })
    
    if threats.get("opportunity_value", 0) > 0:
        actions.append({
            "priority": "HIGH",
            "action": f"🎯 Overtake {threats['next_nbo']}",
            "details": f"Need +{threats['opportunity_percent']:.1f}% growth to pass {threats['next_nbo']}. Focus on competitive advantages and key opportunities."
        })
    
    if has_target and forecast.get("gap_to_target", 0) > 0:
        actions.append({
            "priority": "MEDIUM",
            "action": "📊 Accelerate Target Attainment",
            "details": f"Gap to target: {format_peso(forecast['gap_to_target'])}. Increase sales activities and focus on high-value opportunities."
        })
    
    if threats.get("productivity_gap", 0) > 0:
        actions.append({
            "priority": "MEDIUM",
            "action": "⚡ Improve AC per Life",
            "details": f"Gap: {format_peso(threats['productivity_gap'])} per life. Opportunity: {format_peso(threats['productivity_opportunity'])}."
        })
    
    if len(actions) == 0:
        actions.append({
            "priority": "LOW",
            "action": "✅ Maintain Current Performance",
            "details": "All metrics are performing well. Continue monitoring and optimizing your strategies."
        })
    
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    actions.sort(key=lambda x: priority_order.get(x["priority"], 99))
    
    for action in actions:
        priority_class = f"action-priority-{action['priority'].lower()}"
        color = "#EF4444" if action["priority"] == "CRITICAL" else "#F59E0B" if action["priority"] == "HIGH" else "#3B82F6" if action["priority"] == "MEDIUM" else "#6B7280"
        st.markdown(f"""
        <div class="action-card" style="border-left-color: {color};">
            <div>
                <span class="insight-title">{action['action']}</span>
                <span class="action-priority {priority_class}">{action['priority']}</span>
            </div>
            <div style="color:#4B5563; font-size:0.9rem; margin-top:0.25rem;">
                {action['details']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    with st.sidebar:
        logo_html = load_logo()
        if logo_html:
            st.image(logo_html, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align:center; padding:1rem 0;">
                <span class="material-icons" style="font-size:3rem; color:#FDB913;">workspace_premium</span>
                <div style="font-weight:700; font-size:1.2rem; margin-top:0.5rem;">CENTURION TREE</div>
                <div style="color:#6B7280; font-size:0.85rem;">Executive Insights</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Data Sources")
        st.markdown("*Upload one or both files*")
        ytd_file = st.file_uploader("Upload YTD File", type=["xlsx"], key="ytd")
        mtd_file = st.file_uploader("Upload MTD File", type=["xlsx"], key="mtd")
        
        st.markdown("---")
        
        with st.expander("How Metrics Work"):
            st.markdown("""
            **Health Score** (0-100)
            - AC Growth: How much AC grew vs last year
            - NSC Growth: How much NSC grew vs last year  
            - Target Attainment: % of annual target achieved (YTD only)
            - Productivity: AC per Life
            - Competitive Rank: Your position vs others
            - Momentum: Are you trending in the right direction?
            
            **Note:** When only MTD data is available, target-related metrics are excluded and weights are redistributed.
            """)
        
        st.caption("Powered by Sun Life Data Analytics")
        
        # Show active data sources
        if ytd_file and mtd_file:
            st.success("✅ YTD + MTD loaded")
        elif ytd_file:
            st.info("📊 YTD only loaded")
        elif mtd_file:
            st.info("📊 MTD only loaded")

    # Determine which data sources are available
    ytd_df = None
    mtd_df = None
    centurion_ytd = None
    centurion_mtd = None
    data_source = ""
    has_target = False

    if ytd_file:
        ytd_df = load_ytd_report(ytd_file)
        if not ytd_df.empty:
            centurion_ytd = ytd_df[ytd_df["NBO"].astype(str).str.contains("CENTURION", case=False, na=False)]
    
    if mtd_file:
        mtd_df = load_mtd_report(mtd_file)
        if not mtd_df.empty:
            centurion_mtd = mtd_df[mtd_df["NBO"].astype(str).str.contains("CENTURION", case=False, na=False)]

    # Check if we have data - prioritize YTD if available
    if ytd_df is not None and not ytd_df.empty and centurion_ytd is not None and not centurion_ytd.empty:
        row = centurion_ytd.iloc[0]
        df = ytd_df
        data_source = "YTD"
        has_target = True
    elif mtd_df is not None and not mtd_df.empty and centurion_mtd is not None and not centurion_mtd.empty:
        row = centurion_mtd.iloc[0]
        df = mtd_df
        data_source = "MTD"
        has_target = False
    else:
        st.info("👈 Please upload a YTD or MTD Excel file to begin")
        st.markdown("""
        ### Getting Started
        1. Upload a **YTD file** for year-to-date analysis (includes target data)
        2. Upload a **MTD file** for month-to-date analysis (no target data)  
        3. Upload **both** for comprehensive comparison
        
        ### What You'll See
        - **Health Score** - Overall performance metric
        - **Executive Briefing** - Plain English insights
        - **Threat Monitor** - Competitive intelligence
        - **Forecast Center** - Performance projections
        - **Action Center** - Prioritized next steps
        """)
        return

    # Calculate all metrics - pass has_target flag
    health_score = calculate_health_score(row, df, has_target)
    health_data = calculate_health_score_components(row, df, has_target)
    verdict = determine_verdict(health_score)
    threats = calculate_threat_metrics(row, df)
    forecast = calculate_forecast(row, has_target)
    leakage, recovery = calculate_revenue_leakage(row)

    # Render everything
    render_executive_overview(row, df, health_score, verdict, data_source, has_target)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    render_component_breakdown(health_data, has_target)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Create tabs
    tabs = st.tabs([
        "📋 Briefing",
        "📈 Forecast", 
        "🛡️ Threats",
        "📊 Productivity",
        "💰 Revenue",
        "🏆 Position",
        "🎯 Actions"
    ])
    
    with tabs[0]:
        render_executive_briefing(row, health_score, verdict, threats, forecast, df, data_source, has_target)
    
    with tabs[1]:
        render_forecast_center(forecast, row, has_target)
    
    with tabs[2]:
        render_threat_monitor(threats, row)
    
    with tabs[3]:
        render_productivity_benchmark(row, df)
    
    with tabs[4]:
        render_revenue_leakage(leakage, recovery, row)
    
    with tabs[5]:
        render_competitive_position(row, df)
    
    with tabs[6]:
        render_management_actions(row, threats, forecast, health_score, data_source, has_target)
    
    # MTD Comparison - only if both files are loaded
    if ytd_file and mtd_file and ytd_df is not None and mtd_df is not None:
        if centurion_ytd is not None and not centurion_ytd.empty and centurion_mtd is not None and not centurion_mtd.empty:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            render_mtd_comparison(centurion_ytd.iloc[0], centurion_mtd.iloc[0], ytd_df)

if __name__ == "__main__":
    main()