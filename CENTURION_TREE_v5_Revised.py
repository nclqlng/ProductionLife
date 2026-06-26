"""
CENTURION TREE Executive Insights
Professional Performance Dashboard v5.0

Flexible Data Sources:
- MTD only
- YTD only  
- Both MTD and YTD

Built for Sun Life - Clear, Actionable, Insightful
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

    /* Ranking table styling */
    .ranking-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    .ranking-table th {
        background: #2D2D2D;
        color: white;
        padding: 0.75rem 0.5rem;
        text-align: left;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    .ranking-table td {
        padding: 0.6rem 0.5rem;
        border-bottom: 1px solid #E5E7EB;
    }
    .ranking-table tr:hover {
        background: #F3F4F6;
    }
    .ranking-table .centurion-row {
        background: #FDB913 !important;
        font-weight: 600;
    }
    .ranking-table .centurion-row:hover {
        background: #E5A800 !important;
    }
    .ranking-table .rank-number {
        font-weight: 600;
        color: #2D2D2D;
    }
    .ranking-table .centurion-rank {
        color: #1a1a2e;
    }
    
    .leaderboard-container {
        max-height: 600px;
        overflow-y: auto;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    .leaderboard-container::-webkit-scrollbar {
        width: 8px;
    }
    .leaderboard-container::-webkit-scrollbar-track {
        background: #F1F1F1;
        border-radius: 4px;
    }
    .leaderboard-container::-webkit-scrollbar-thumb {
        background: #FDB913;
        border-radius: 4px;
    }
    
    .gold-highlight {
        background: #FDB913 !important;
        font-weight: 600;
        color: #1a1a2e;
    }
    
    .rank-badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #E5E7EB;
        color: #2D2D2D;
    }
    .rank-badge-gold {
        background: #FDB913;
        color: #1a1a2e;
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
    if b is None or pd.isna(b) or b == 0:
        return 0
    if a is None or pd.isna(a):
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

def render_callout(title, body, style="info"):
    cls = {"success": "alert-success", "warning": "alert-warning", "danger": "alert-danger"}.get(style, "insight-box")
    icon = {"success": "check_circle", "warning": "warning", "danger": "error"}.get(style, "info")
    color = {"success": "success", "warning": "warning", "danger": "danger"}.get(style, "info")
    st.markdown(f"""
    <div class="alert-box {cls}">
        <div class="alert-icon">{render_icon(icon, size='md', color=color)}</div>
        <div class="alert-content">
            <div class="alert-title">{title}</div>
            <div class="alert-description">{body}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

NAME_COLUMNS = (0, 2)
METRIC_COLUMNS = {
    "Lives": 3, "AC": 4, "NSC": 5,
    "Lives_PY": 6, "AC_PY": 7, "NSC_PY": 8,
    "SSP": 12,
    "Target": 13, "Pct_Target": 14,
}
SHEET2_COLUMNS = {
    "Lives": 1, "AC": 2, "NSC": 3,
    "Lives_PY": 4, "AC_PY": 5, "NSC_PY": 6,
    "SSP": 10,
}
HEADER_ROWS = 3

# ============================================================================
# OFFICIAL NBO VALIDATION
# ============================================================================

NBO_TERRITORY_MAP = {
    "JACARANDA":"METRO NORTH TERRITORY","MANGO":"METRO NORTH TERRITORY",
    "MULBERRY":"METRO NORTH TERRITORY","PASSION":"METRO NORTH TERRITORY",
    "WISTERIA TREE":"METRO NORTH TERRITORY","BLUEWOOD":"METRO NORTH TERRITORY",
    "JARRAH":"METRO NORTH TERRITORY","MUSTARD TREE":"METRO NORTH TERRITORY",
    "MYRTLE":"METRO NORTH TERRITORY","STAR MAGNOLIA":"METRO NORTH TERRITORY",
    "GENESIS":"METRO NORTH TERRITORY","GREEN FIR":"METRO NORTH TERRITORY",
    "KARRI":"METRO NORTH TERRITORY","MAJESTY":"METRO NORTH TERRITORY",
    "OSMANTHUS":"METRO NORTH TERRITORY","RED SYCAMORE":"METRO NORTH TERRITORY",
    "BAOBAB":"METRO NORTH TERRITORY","CYPRESS":"METRO NORTH TERRITORY",
    "DIAMOND TREE":"METRO NORTH TERRITORY","MENARA TREE":"METRO NORTH TERRITORY",
    "RED SPRUCE":"METRO NORTH TERRITORY","REDWOOD":"METRO NORTH TERRITORY",
    "GOPHERWOOD":"METRO NORTH TERRITORY","HEATHER":"METRO NORTH TERRITORY",
    "HYPERION TREE":"METRO NORTH TERRITORY","IRON OAK":"METRO NORTH TERRITORY",
    "MILLENNIUM DRAGON":"METRO NORTH TERRITORY","TREE OF LIFE":"METRO NORTH TERRITORY",
    "BAMBOO":"METRO NORTH TERRITORY","CHESTNUT":"METRO NORTH TERRITORY",
    "DAU":"METRO NORTH TERRITORY","GRANDIS TREE":"METRO NORTH TERRITORY",
    "RAINBOW TREE":"METRO NORTH TERRITORY","ROSEWOOD":"METRO NORTH TERRITORY",
    "CANNONBALL":"METRO SOUTH TERRITORY","IVY":"METRO SOUTH TERRITORY",
    "KOA":"METRO SOUTH TERRITORY","MULAWIN":"METRO SOUTH TERRITORY",
    "RAVENS TOWER":"METRO SOUTH TERRITORY","SEQUOIA":"METRO SOUTH TERRITORY",
    "ALMOND":"METRO SOUTH TERRITORY","CEDAR":"METRO SOUTH TERRITORY",
    "COPAIBA":"METRO SOUTH TERRITORY","CRIMSON QUEEN":"METRO SOUTH TERRITORY",
    "LAURELWOOD":"METRO SOUTH TERRITORY","ROWAN":"METRO SOUTH TERRITORY",
    "EMPRESS":"METRO SOUTH TERRITORY","EUCALYPTUS":"METRO SOUTH TERRITORY",
    "GENUS PINE":"METRO SOUTH TERRITORY","NEEM TREE":"METRO SOUTH TERRITORY",
    "ROYAL POINCIANA":"METRO SOUTH TERRITORY","SAKURA":"METRO SOUTH TERRITORY",
    "CACAO":"METRO SOUTH TERRITORY","GOLDENRAIN":"METRO SOUTH TERRITORY",
    "JOSHUA TREE":"METRO SOUTH TERRITORY","MOLAVE":"METRO SOUTH TERRITORY",
    "TINDALO":"METRO SOUTH TERRITORY","ALEXANDER PALM":"METRO SOUTH TERRITORY",
    "ATLAS PALM":"METRO SOUTH TERRITORY","PHOENIX PALM":"METRO SOUTH TERRITORY",
    "ROYAL PALM":"METRO SOUTH TERRITORY","WALT PALM":"METRO SOUTH TERRITORY",
    "CENTURION TREE":"METRO SOUTH TERRITORY","KHAYA":"METRO SOUTH TERRITORY",
    "OAKWOOD":"METRO SOUTH TERRITORY","QUEBRACHO":"METRO SOUTH TERRITORY",
    "WILLOW TREE":"METRO SOUTH TERRITORY",
    "CANARYWOOD":"LUZON TERRITORY","CHERRY TREE":"LUZON TERRITORY",
    "DRAGONWOOD":"LUZON TERRITORY","GOLDEN SHOWER TREE":"LUZON TERRITORY",
    "MAGNOLIA WOODS":"LUZON TERRITORY","MAGNUS ALMACIGA":"LUZON TERRITORY",
    "MORINGA TREE":"LUZON TERRITORY","OLIVE":"LUZON TERRITORY",
    "SHERMAN":"LUZON TERRITORY","BAYWOOD":"LUZON TERRITORY",
    "COCONUT":"LUZON TERRITORY","COFFEE TREE":"LUZON TERRITORY",
    "CRESPON DE MIRTO":"LUZON TERRITORY","EXCELSA":"LUZON TERRITORY",
    "HONEY TREE":"LUZON TERRITORY","LIBERICA":"LUZON TERRITORY",
    "LIME TREE":"LUZON TERRITORY","MIRACLE TREE":"LUZON TERRITORY",
    "ACACIA":"VISMIN TERRITORY","ANGEL OAK":"VISMIN TERRITORY",
    "BRISTLECONE":"VISMIN TERRITORY","CINNAMON":"VISMIN TERRITORY",
    "CORINTHIAN":"VISMIN TERRITORY","GOLDEN ASPEN":"VISMIN TERRITORY",
    "JACKFRUIT":"VISMIN TERRITORY","KINGWOOD":"VISMIN TERRITORY",
    "APPLE":"VISMIN TERRITORY","DURIAN":"VISMIN TERRITORY",
    "GRAND ELM":"VISMIN TERRITORY","IRONWOOD":"VISMIN TERRITORY",
    "MANGROVE":"VISMIN TERRITORY","NARRA":"VISMIN TERRITORY",
    "NETTLE":"VISMIN TERRITORY",
}

VALID_NBOS = set(NBO_TERRITORY_MAP.keys())

def _is_valid_nbo(name):
    return _nbo_key(name) in VALID_NBOS

def _looks_like_nbo_name(value):
    if pd.isna(value) or isinstance(value, (int, float, np.integer, np.floating)):
        return False
    name = str(value).strip()
    if len(name) < 3 or not any(c.isalpha() for c in name):
        return False
    upper = name.upper()
    if upper in ("NBO", "AC", "NSC", "LIVES", "SUBMITTED LIVES"):
        return False
    if upper.startswith(("SINGLE PAY", "NBO NAME", "TOTAL", "DECEMBER", "TERRITORY", "METRO NORTH")):
        return False
    try:
        float(name.replace(",", "").replace("₱", ""))
        return False
    except ValueError:
        return True

def _is_centurion_name(name):
    return "CENTURION" in str(name).upper()

def _parse_nbo_name(row):
    for col in NAME_COLUMNS:
        if len(row) > col and _looks_like_nbo_name(row.iloc[col]):
            return str(row.iloc[col]).strip()
    for col in range(min(8, len(row))):
        if pd.isna(row.iloc[col]):
            continue
        text = str(row.iloc[col]).strip()
        if _is_centurion_name(text):
            return text
    return None

def _nbo_key(name):
    key = str(name).upper().strip()
    for suffix in (" NEW BUSINESS OFFICE", " NBO", " OFFICE"):
        key = key.replace(suffix, "")
    return key.strip()

def _build_record(row, name, territory, report_type, target_col=None, pct_col=None):
    record = {
        "Territory": territory,
        "NBO": name,
        "Lives": clean_number(row.iloc[METRIC_COLUMNS["Lives"]]) if len(row) > METRIC_COLUMNS["Lives"] else 0,
        "AC": clean_number(row.iloc[METRIC_COLUMNS["AC"]]) if len(row) > METRIC_COLUMNS["AC"] else 0,
        "NSC": clean_number(row.iloc[METRIC_COLUMNS["NSC"]]) if len(row) > METRIC_COLUMNS["NSC"] else 0,
        "Lives_PY": clean_number(row.iloc[METRIC_COLUMNS["Lives_PY"]]) if len(row) > METRIC_COLUMNS["Lives_PY"] else 0,
        "AC_PY": clean_number(row.iloc[METRIC_COLUMNS["AC_PY"]]) if len(row) > METRIC_COLUMNS["AC_PY"] else 0,
        "NSC_PY": clean_number(row.iloc[METRIC_COLUMNS["NSC_PY"]]) if len(row) > METRIC_COLUMNS["NSC_PY"] else 0,
        "SSP": clean_number(row.iloc[METRIC_COLUMNS["SSP"]]) if len(row) > METRIC_COLUMNS["SSP"] else 0,
        "SSP_PY": 0,
    }
    if report_type == "YTD":
        t_col = target_col if target_col is not None else METRIC_COLUMNS["Target"]
        p_col = pct_col if pct_col is not None else METRIC_COLUMNS["Pct_Target"]
        if len(row) > t_col:
            record["Target"] = clean_number(row.iloc[t_col])
        if len(row) > p_col:
            record["Pct_Target"] = _parse_pct_target(row.iloc[p_col])
    return record

def _load_sheet2_lookup(file):
    lookup = {}
    try:
        xl = pd.ExcelFile(file)
        if "Sheet2" not in xl.sheet_names:
            return lookup
        raw = pd.read_excel(file, sheet_name="Sheet2", header=None)
    except Exception:
        return lookup

    start_row = 2
    for idx in range(min(5, len(raw))):
        cell = str(raw.iloc[idx, 0]).strip().upper() if pd.notna(raw.iloc[idx, 0]) else ""
        if "NBO NAME" in cell:
            start_row = idx + 1
            break

    cols = SHEET2_COLUMNS
    for idx in range(start_row, len(raw)):
        row = raw.iloc[idx]
        if len(row) < 7 or pd.isna(row.iloc[0]):
            continue
        name = str(row.iloc[0]).strip()
        if "TERRITORY" in name.upper() or not _looks_like_nbo_name(name):
            continue
        lookup[_nbo_key(name)] = {
            "Lives": clean_number(row.iloc[cols["Lives"]]),
            "AC": clean_number(row.iloc[cols["AC"]]),
            "NSC": clean_number(row.iloc[cols["NSC"]]),
            "SSP": clean_number(row.iloc[cols["SSP"]]) if len(row) > cols["SSP"] else 0,
        }
        if len(row) > 11:
            tgt = clean_number(row.iloc[11])
            if tgt > 0:
                lookup[_nbo_key(name)]["Target"] = tgt
        if len(row) > 12:
            pct = _parse_pct_target(row.iloc[12])
            if pct > 0:
                lookup[_nbo_key(name)]["Pct_Target"] = pct
    return lookup

def _supplement_record(record, sheet2_lookup, source_lookup, report_type):
    key = _nbo_key(record["NBO"])

    if record["AC"] == 0 and record["Lives"] == 0:
        if key in sheet2_lookup:
            src = sheet2_lookup[key]
        elif record["NBO"].upper() in source_lookup:
            src = source_lookup[record["NBO"].upper()]
        else:
            src = None
        if src:
            record["Lives"] = src.get("Lives", record["Lives"])
            record["AC"] = src.get("AC", record["AC"])
            record["NSC"] = src.get("NSC", record["NSC"])
            if record.get("SSP", 0) == 0 and src.get("SSP"):
                record["SSP"] = src["SSP"]

    if report_type == "YTD":
        s2 = sheet2_lookup.get(key, {})
        if clean_number(record.get("Pct_Target", 0)) == 0 and clean_number(s2.get("Pct_Target", 0)) > 0:
            if clean_number(record.get("Target", 0)) == 0:
                record["Target"] = clean_number(s2.get("Target", 0))
            record["Pct_Target"] = clean_number(s2["Pct_Target"])
        elif clean_number(record.get("Target", 0)) == 0 and clean_number(s2.get("Target", 0)) > 0:
            record["Target"] = clean_number(s2["Target"])
    return record

def _load_source_mtd_lookup(file):
    lookup = {}
    try:
        raw = pd.read_excel(file, sheet_name="SOURCE", header=None)
    except Exception:
        return lookup
    for idx in range(2, len(raw)):
        row = raw.iloc[idx]
        if len(row) < 6:
            continue
        name = None
        for col in (0, 1):
            if len(row) > col and _looks_like_nbo_name(row.iloc[col]):
                name = str(row.iloc[col]).strip().upper()
                break
        if not name:
            continue
        lookup[name] = {
            "Lives": clean_number(row.iloc[3]),
            "AC": clean_number(row.iloc[4]),
            "NSC": clean_number(row.iloc[5]),
        }
        if len(row) > 6:
            lookup[name]["SSP"] = clean_number(row.iloc[6])
    return lookup

def _apply_source_mtd_fallback(rows, lookup):
    for record in rows:
        _supplement_record(record, {}, lookup, "MTD")
    return rows

def _detect_ytd_target_columns(raw):
    target_col = pct_col = None
    for hi in (1, 0, 2):
        if hi >= len(raw):
            continue
        for j, val in enumerate(raw.iloc[hi]):
            if pd.isna(val):
                continue
            text = str(val).upper().replace("\n", " ")
            if "ANNUAL" in text and "LIFE AC" in text and "TARGET" in text:
                target_col = j
            elif "% TO TARGET" in text or (text.strip().startswith("%") and "TARGET" in text):
                pct_col = j
        if target_col is not None and pct_col is not None:
            return target_col, pct_col
    return None, None

def _parse_pct_target(value):
    pct = clean_number(value)
    if pct <= 0:
        return 0
    return pct * 100 if pct <= 1.5 else pct

# ============================================================================
# RANKING CALCULATIONS (NEW FRAMEWORK)
# ============================================================================

def calculate_competitive_rankings(df, report_type):
    """
    Calculate all competitive rankings for each NBO.
    Preserves existing Health Score logic.
    """
    if df.empty:
        return df
    
    df = df.copy()
    total_nbos = df.shape[0]
    
    # Calculate Growth Score (average of growth percentages)
    df["Growth_Score"] = (
        df["AC_Growth"].fillna(0) + 
        df["NSC_Growth"].fillna(0) + 
        df["Lives_Growth"].fillna(0)
    ) / 3
    
    # Calculate Growth Rank (highest score = Rank #1) - using min method for ties
    df["Growth_Rank"] = df["Growth_Score"].rank(method="min", ascending=False).astype(int)
    
    # AC Rank - using min method for ties
    df["AC_Rank"] = df["AC"].rank(method="min", ascending=False).astype(int)
    
    # NSC Rank - using min method for ties
    df["NSC_Rank"] = df["NSC"].rank(method="min", ascending=False).astype(int)
    
    # Lives Rank - using min method for ties
    df["Lives_Rank"] = df["Lives"].rank(method="min", ascending=False).astype(int)
    
    # Target Rank (% to Target - only for YTD)
    if report_type == "YTD" and "Pct_Target" in df.columns:
        df["Target_Rank"] = df["Pct_Target"].rank(method="min", ascending=False).astype(int)
    else:
        df["Target_Rank"] = None
    
    # Calculate Overall Competitive Score and Rank
    if report_type == "YTD":
        # YTD Weighting: AC=25%, NSC=20%, Lives=15%, Growth=20%, Target=20%
        df["Competitive_Score"] = (
            df["AC_Rank"] * 0.25 +
            df["NSC_Rank"] * 0.20 +
            df["Lives_Rank"] * 0.15 +
            df["Growth_Rank"] * 0.20 +
            df["Target_Rank"].fillna(total_nbos) * 0.20
        )
    else:
        # MTD Weighting: AC=35%, NSC=25%, Lives=20%, Growth=20%
        df["Competitive_Score"] = (
            df["AC_Rank"] * 0.35 +
            df["NSC_Rank"] * 0.25 +
            df["Lives_Rank"] * 0.20 +
            df["Growth_Rank"] * 0.20
        )
    
    # Competitive Rank (lowest score = Rank #1) - using min method for ties
    df["Competitive_Rank"] = df["Competitive_Score"].rank(method="min", ascending=True).astype(int)
    
    # Calculate percentile for Competitive Rank
    df["Competitive_Percentile"] = (
        (total_nbos - df["Competitive_Rank"] + 1) / total_nbos * 100
    ).round(1)
    
    return df

def enrich_dataframe(df, report_type):
    if df.empty:
        return df

    df = df.copy()
    df["AC_Growth"] = df.apply(lambda x: safe_divide(x["AC"] - x["AC_PY"], x["AC_PY"]) * 100, axis=1)
    df["NSC_Growth"] = df.apply(lambda x: safe_divide(x["NSC"] - x["NSC_PY"], x["NSC_PY"]) * 100, axis=1)
    df["Lives_Growth"] = df.apply(lambda x: safe_divide(x["Lives"] - x["Lives_PY"], x["Lives_PY"]) * 100, axis=1)
    df["AC_Per_Life"] = df.apply(lambda x: safe_divide(x["AC"], x["Lives"]), axis=1)
    df["NSC_Per_Life"] = df.apply(lambda x: safe_divide(x["NSC"], x["Lives"]), axis=1)
    df["NSC_Multiple"] = df.apply(lambda x: safe_divide(x["NSC"], x["AC"]), axis=1)
    
    # Legacy rank columns (preserved for compatibility)
    df["AC_Rank_Legacy"] = df["AC"].rank(method="min", ascending=False).astype(int)
    df["NSC_Rank_Legacy"] = df["NSC"].rank(method="min", ascending=False).astype(int)
    df["Lives_Rank_Legacy"] = df["Lives"].rank(method="min", ascending=False).astype(int)
    df["Territory_AC_Rank"] = df.groupby("Territory")["AC"].rank(method="min", ascending=False).astype(int)
    df["Territory_NSC_Rank"] = df.groupby("Territory")["NSC"].rank(method="min", ascending=False).astype(int)
    df["Territory_Lives_Rank"] = df.groupby("Territory")["Lives"].rank(method="min", ascending=False).astype(int)
    df["Report_Type"] = report_type

    if "SSP" in df.columns:
        df["SSP_Growth"] = df.apply(
            lambda x: safe_divide(x["SSP"] - x.get("SSP_PY", 0), x.get("SSP_PY", 0)) * 100, axis=1
        )

    if "Target" not in df.columns:
        df["Target"] = None
    if "Pct_Target" not in df.columns:
        df["Pct_Target"] = None

    # Calculate competitive rankings using new framework
    df = calculate_competitive_rankings(df, report_type)
    
    return df

@st.cache_data
def load_production_report(file, report_type, _parser_version=10):
    try:
        raw = pd.read_excel(file, sheet_name="PER NBO", header=None)
    except Exception as e:
        st.error(f"Error loading {report_type} file: {e}")
        return pd.DataFrame()

    target_col, pct_col = (None, None)
    if report_type == "YTD":
        target_col, pct_col = _detect_ytd_target_columns(raw)

    sheet2_lookup = _load_sheet2_lookup(file)
    source_lookup = _load_source_mtd_lookup(file)
    rows = []
    territory = None

    for idx, row in raw.iterrows():
        if idx < HEADER_ROWS or len(row) < 9:
            continue

        name = _parse_nbo_name(row)
        if not name:
            continue

        if "TERRITORY" in name.upper() and not _is_centurion_name(name):
            territory = name
            continue

        normalized_name = _nbo_key(name)

        if normalized_name not in VALID_NBOS:
            continue

        record = _build_record(
            row,
            name,
            NBO_TERRITORY_MAP[normalized_name],
            report_type,
            target_col,
            pct_col,
        )
        record = _supplement_record(record, sheet2_lookup, source_lookup, report_type)
        rows.append(record)

    if not rows:
        return pd.DataFrame()

    return enrich_dataframe(pd.DataFrame(rows), report_type)

def find_centurion(df):
    if df is None or df.empty:
        return pd.DataFrame()
    names = df["NBO"].astype(str).str.upper().str.strip()
    mask = names.str.contains("CENTURION", case=False, na=False)
    return df[mask]

def format_nbo_sample(df, limit=8):
    if df is None or df.empty:
        return "none"
    sample = df["NBO"].astype(str).head(limit).tolist()
    suffix = f" … and {len(df) - limit} more" if len(df) > limit else ""
    return ", ".join(sample) + suffix

def has_target_data(row):
    target = row.get("Target")
    pct = row.get("Pct_Target")
    return (target is not None and clean_number(target) > 0) or (pct is not None and clean_number(pct) > 0)

def get_period_labels(data_source):
    if data_source == "MTD":
        return {
            "period": "this month",
            "period_short": "MTD",
            "ac_label": "Monthly Life AC",
            "nsc_label": "Annualized Production Value",
            "lives_label": "Lives (This Month)",
            "py_label": "same month last year",
            "growth_context": "vs same month last year",
            "rank_context": "among all NBOs this month",
        }
    return {
        "period": "year to date",
        "period_short": "YTD",
        "ac_label": "Year-to-Date Life AC",
        "nsc_label": "Annualized Production Value (YTD)",
        "lives_label": "Lives (YTD)",
        "py_label": "prior year to date",
        "growth_context": "vs prior year to date",
        "rank_context": "among all NBOs year to date",
    }

@st.cache_data
def load_ytd_report(file, _parser_version=10):
    return load_production_report(file, "YTD", _parser_version=_parser_version)

@st.cache_data
def load_mtd_report(file, _parser_version=10):
    return load_production_report(file, "MTD", _parser_version=_parser_version)

# ============================================================================
# CALCULATION ENGINE (Health Score - UNCHANGED)
# ============================================================================

def determine_verdict(health_score):
    if health_score >= 85:
        return {"label": "STRONG", "icon": "check_circle", "color": COLORS["success"], "description": "Performance is excellent — keep current strategy"}
    elif health_score >= 70:
        return {"label": "STABLE", "icon": "trending_up", "color": COLORS["warning"], "description": "Solid results with room to improve in a few areas"}
    elif health_score >= 50:
        return {"label": "AT RISK", "icon": "warning", "color": COLORS["warning"], "description": "Below expectations — review growth and competitive position"}
    else:
        return {"label": "CRITICAL", "icon": "error", "color": COLORS["danger"], "description": "Well below target — immediate leadership review recommended"}

def _health_score_weights(include_target=None):
    return {
        "nsc": 0.40,
        "ac": 0.20,
        "lives": 0.20,
        "rank": 0.10,
        "momentum": 0.10,
    }

def calculate_health_score(row, df, include_target=None):
    if include_target is None:
        include_target = has_target_data(row)

    ac_growth = row["AC_Growth"]
    ac_score = max(0, min(100, 50 + (ac_growth / 2)))
    
    nsc_growth = row["NSC_Growth"]
    nsc_score = max(0, min(100, 50 + (nsc_growth / 2)))
    
    lives_growth = row["Lives_Growth"]
    lives_score = max(0, min(100, 50 + (lives_growth / 2)))
    target_pct = clean_number(row.get("Pct_Target", 0))
    target_score = min(target_pct, 100) if include_target else 50
    
    company_avg = df["AC_Per_Life"].mean() if df["AC_Per_Life"].mean() > 0 else 1
    case_size_score = min((row["AC_Per_Life"] / company_avg) * 100, 150) if company_avg > 0 else 50
    
    total_nbos = df.shape[0]
    rank_score = ((total_nbos - row["AC_Rank"]) / total_nbos * 100) if total_nbos > 0 else 50
    
    momentum_score = 80 if (ac_growth > 0 and nsc_growth > 0) else 60 if (ac_growth > 0 or nsc_growth > 0) else 40
    
    weights = _health_score_weights(include_target)
    health_score = (
        ac_score * weights["ac"] +
        nsc_score * weights["nsc"] +
        rank_score * weights["rank"] +
        momentum_score * weights["momentum"]
    )
    return max(0, min(100, health_score))

def calculate_health_score_components(row, df, include_target=None):
    if include_target is None:
        include_target = has_target_data(row)

    ac_growth = row["AC_Growth"]
    ac_score = max(0, min(100, 50 + (ac_growth / 2)))
    
    nsc_growth = row["NSC_Growth"]
    nsc_score = max(0, min(100, 50 + (nsc_growth / 2)))
    
    lives_growth = row["Lives_Growth"]
    lives_score = max(0, min(100, 50 + (lives_growth / 2)))
    target_pct = clean_number(row.get("Pct_Target", 0))
    target_score = min(target_pct, 100) if include_target else 50
    
    company_avg = df["AC_Per_Life"].mean() if df["AC_Per_Life"].mean() > 0 else 1
    case_size_score = min((row["AC_Per_Life"] / company_avg) * 100, 150) if company_avg > 0 else 50
    
    total_nbos = df.shape[0]
    rank_score = ((total_nbos - row["AC_Rank"]) / total_nbos * 100) if total_nbos > 0 else 50
    
    momentum_score = 80 if (ac_growth > 0 and nsc_growth > 0) else 60 if (ac_growth > 0 or nsc_growth > 0) else 40
    
    weights = _health_score_weights(include_target)
    health_score = (
        ac_score * weights["ac"] +
        nsc_score * weights["nsc"] +
        rank_score * weights["rank"] +
        momentum_score * weights["momentum"]
    )
    health_score = max(0, min(100, health_score))

    target_display = f"{target_pct:.1f}%" if include_target else "N/A (MTD report)"
    target_note = "" if include_target else "Target data comes from YTD reports only"
    
    return {
        "score": health_score,
        "include_target": include_target,
        "components": {
            "AC Growth": {"score": ac_score, "weight": weights["ac"], "value": ac_growth, "display": f"{ac_growth:.1f}%"},
            "NSC Growth": {"score": nsc_score, "weight": weights["nsc"], "value": nsc_growth, "display": f"{nsc_growth:.1f}%"},
            "Target Attainment": {"score": target_score, "weight": 0, "value": target_pct, "display": target_display, "note": target_note},
            "Case Size": {"score": case_size_score, "weight": 0, "value": row["AC_Per_Life"], "display": format_peso(row["AC_Per_Life"])},
            "Lives Growth": {"score": lives_score, "weight": weights["lives"], "value": lives_growth, "display": f"{lives_growth:.1f}%"},
            "Competitive Position": {
                "score": rank_score,
                "weight": weights["rank"],
                "value": row["AC_Rank"],
                "display": f"AC #{row['AC_Rank']}<br>NSC #{row['NSC_Rank']}<br>Lives #{row['Lives_Rank']}"
            },
            "Momentum": {"score": momentum_score, "weight": weights["momentum"], "value": "Positive" if ac_growth > 0 else "Negative", "display": "Positive" if ac_growth > 0 else "Negative"}
        }
    }

# ============================================================================
# THREAT METRICS (UPDATED to use Competitive_Rank)
# ============================================================================

def calculate_threat_metrics(row, df):
    """Calculate threat metrics using Competitive_Rank instead of AC_Rank"""
    df_sorted = df.sort_values("Competitive_Rank")
    
    # Find position of CENTURION TREE in sorted list
    centurion_pos = df_sorted[df_sorted["NBO"].str.contains("CENTURION", case=False, na=False)].index
    
    if len(centurion_pos) > 0:
        centurion_idx = df_sorted.index.get_loc(centurion_pos[0])
        
        # Get NBO above (better rank, lower number)
        if centurion_idx > 0:
            above = df_sorted.iloc[centurion_idx - 1]
            gap_to_next = above["AC"] - row["AC"]
            next_nbo = above["NBO"]
            next_ac = above["AC"]
        else:
            gap_to_next = 0
            next_nbo = None
            next_ac = 0
        
        # Get NBO below (worse rank, higher number)
        if centurion_idx < len(df_sorted) - 1:
            below = df_sorted.iloc[centurion_idx + 1]
            gap_to_prev = row["AC"] - below["AC"]
            prev_nbo = below["NBO"]
        else:
            gap_to_prev = 0
            prev_nbo = None
    else:
        gap_to_next = 0
        next_nbo = None
        next_ac = 0
        gap_to_prev = 0
        prev_nbo = None
    
    threats = {
        "gap_to_next": gap_to_next,
        "next_nbo": next_nbo,
        "next_ac": next_ac,
        "gap_to_prev": gap_to_prev,
        "prev_nbo": prev_nbo,
    }
    
    if gap_to_prev > 0:
        threat_pct = safe_divide(gap_to_prev, row["AC"]) * 100
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
    
    if gap_to_next > 0:
        threats["opportunity_value"] = gap_to_next
        threats["opportunity_percent"] = safe_divide(gap_to_next, row["AC"]) * 100
    else:
        threats["opportunity_value"] = 0
        threats["opportunity_percent"] = 0
    
    top_10_avg = df.nlargest(10, "AC")["AC_Per_Life"].mean() if df.shape[0] >= 10 else df["AC_Per_Life"].max()
    threats["productivity_gap"] = max(top_10_avg - row["AC_Per_Life"], 0)
    threats["productivity_opportunity"] = threats["productivity_gap"] * row["Lives"]
    
    return threats

def calculate_forecast(row, historical_growth_rates=None):
    ac = clean_number(row.get("AC", 0))
    has_target = has_target_data(row)
    target = clean_number(row.get("Target")) if has_target else 0

    if has_target and target == 0 and clean_number(row.get("Pct_Target", 0)) > 0:
        target = safe_divide(ac, clean_number(row.get("Pct_Target", 0)) / 100)

    is_mtd = str(row.get("Report_Type", "")).upper() == "MTD"
    annual_projection = ac * 12 if is_mtd else ac * 2

    if historical_growth_rates and len(historical_growth_rates) > 0:
        avg_growth = np.mean(historical_growth_rates)
        std_growth = np.std(historical_growth_rates)
    else:
        avg_growth = 0.10
        std_growth = 0.05

    worst_multiplier = max(0.5, 1 + avg_growth - std_growth)
    expected_multiplier = 1 + avg_growth
    best_multiplier = 1 + avg_growth + std_growth

    scenarios = {
        "Worst Case": ac * worst_multiplier,
        "Expected": ac * expected_multiplier,
        "Best Case": ac * best_multiplier
    }

    if has_target and target > 0:
        pct = clean_number(row.get("Pct_Target", 0))
        target_attainment = pct if pct > 0 else safe_divide(ac, target) * 100
        gap_to_target = max(target - annual_projection, 0)
    else:
        target_attainment = 0
        gap_to_target = 0

    return {
        "target": target,
        "has_target": has_target,
        "target_attainment": target_attainment,
        "gap_to_target": gap_to_target,
        "annual_projection": annual_projection,
        "current_ac": ac,
        "scenarios": scenarios,
        "forecast_methodology": "Run-rate annualization with historical-growth-based scenarios"
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

def render_alert_box(verdict, health_score, data_source, include_target=False):
    labels = get_period_labels(data_source)
    if health_score < 50:
        alert_class, icon_name, icon_color = "alert-danger", "error", "danger"
    elif health_score < 70:
        alert_class, icon_name, icon_color = "alert-warning", "warning", "warning"
    else:
        alert_class, icon_name, icon_color = "alert-success", "check_circle", "success"

    score_note = (
        "Growth, productivity, rank, momentum, and SSP target attainment for this month."
        if data_source == "MTD" and include_target
        else "Growth, productivity, rank, and momentum for this month."
        if data_source == "MTD"
        else "Growth, target progress, productivity, rank, and momentum for the year so far."
    )
    
    st.markdown(f"""
    <div class="alert-box {alert_class}">
        <div class="alert-icon">{render_icon(icon_name, size="lg", color=icon_color)}</div>
        <div class="alert-content">
            <div class="alert-title">Bottom Line: {verdict['label']}</div>
            <div class="alert-description">{verdict['description']} ({labels['period_short']} view)</div>
            <div class="alert-explanation">
                {render_icon('info', size='sm', color='grey')}
                Health Score ({health_score:.0f}/100) for {labels['period']}: {score_note}
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

def render_executive_overview(row, df, health_score, verdict, data_source):
    labels = get_period_labels(data_source)
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
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
        st.metric(labels["ac_label"], format_peso(row["AC"]), delta=f"{row['AC_Growth']:.1f}% {labels['growth_context']}")
    with col3:
        st.metric(labels["nsc_label"], format_peso(row["NSC"]), delta=f"{row['NSC_Growth']:.1f}% {labels['growth_context']}")
    with col4:
        st.metric(labels["lives_label"], f"{row['Lives']:,.0f}", delta=f"{row.get('Lives_Growth', 0):.1f}% {labels['growth_context']}")
    with col5:
        # Updated to show Competitive Rank
        pct_rank = row.get('Competitive_Percentile', 0)
        st.markdown(f"""
        <div style="font-size:0.85rem;color:#6B7280;">
            Competitive Position
        </div>
        <div style="font-size:1.1rem;font-weight:600;line-height:1.4;">
            Overall #{row['Competitive_Rank']}<br>
            AC #{row['AC_Rank']}<br>
            NSC #{row['NSC_Rank']}
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"Top {pct_rank:.0f}% {labels['rank_context']}")

    with col6:
        if data_source == "YTD" and has_target_data(row):
            target_pct = clean_number(row.get("Pct_Target", 0))
            st.metric("Target Attainment", f"{target_pct:.1f}%", delta="On Track" if target_pct > 80 else "Needs Attention" if target_pct > 50 else "Behind Target")
        else:
            st.metric("SSP", format_peso(row.get("SSP", 0)), delta=f"{row.get('SSP_Growth', 0):.1f}% vs PY" if row.get("SSP_Growth") is not None else None)

    render_alert_box(verdict, health_score, data_source, include_target=has_target_data(row))

def render_component_breakdown(health_data, data_source):
    labels = get_period_labels(data_source)
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('assessment', size='lg', color='gold')}
        <h3 style="margin:0;">What Drives Your Score ({labels['period_short']})</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">
        Each bar shows how you score on one factor. Higher is better. Weights show how much each factor counts toward your Health Score.
    </p>
    """, unsafe_allow_html=True)
    
    components = health_data['components']
    cols = st.columns(3)
    for idx, (name, data) in enumerate(components.items()):
        if data.get("weight", 0) == 0:
            continue
        with cols[idx % 3]:
            status = "strong" if data['score'] >= 70 else "stable" if data['score'] >= 50 else "risk"
            icon_map = {
                "AC Growth": "trending_up",
                "NSC Growth": "trending_up",
                "Target Attainment": "target",
                "Case Size": "speed",
                "Competitive Position": "emoji_events",
                "Momentum": "rocket"
            }
            icon_name = icon_map.get(name, "assessment")
            
            period_word = labels["period"]
            explanations = {
                "AC Growth": f"How much Life AC grew {labels['growth_context']} ({period_word})",
                "NSC Growth": f"How much new business commission grew {labels['growth_context']}",
                "Target Attainment": "How much of your annual sales target you have reached (YTD reports only)",
                "Case Size": "Average Life AC generated per client. Higher values indicate larger-value cases. Not included in Health Score.",
                "Competitive Position": f"Your rank {labels['rank_context']} (#1 is best)",
                "Momentum": "Whether both AC and new business are moving in the right direction"
            }
            extra_note = f"<br><em>{data['note']}</em>" if data.get("note") else ""
            
            st.markdown(f"""
            <div class="component-card">
                <div class="component-label">
                    {render_icon(icon_name, size='sm', color=('success' if status=='strong' else 'warning' if status=='stable' else 'danger'))}
                    {name}
                    <span style="float:right; font-size:0.7rem; color:#6B7280;">
                        Weight: {data['weight']*100:.0f}%
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
                    {render_icon('info', size='sm', color='grey')} {explanations.get(name, '')}{extra_note}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_executive_briefing(row, health_score, verdict, threats, forecast, df, data_source):
    labels = get_period_labels(data_source)
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('description', size='lg', color='gold')}
        <h3 style="margin:0;">Executive Briefing — {labels['period_short']}</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">
        Plain-language summary for leadership. All numbers are for <strong>{labels['period']}</strong>.
    </p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="explanation" style="margin-bottom:1rem;">
        {render_icon('menu_book', size='sm', color='grey')}
        <strong>Quick glossary:</strong>
        <strong>Life AC</strong> = commission from life insurance production ·
        <strong>Life NSC</strong> = commission from new policies ·
        <strong>Lives</strong> = number of clients ·
        <strong>Overall Rank</strong> = weighted competitive position (#1 is best)
    </div>
    """, unsafe_allow_html=True)
    
    rank_pct = row.get('Competitive_Percentile', 0)
    ac_change = row['AC'] - row['AC_PY']
    change_word = "up" if ac_change >= 0 else "down"

    st.markdown(f"""
    <div class="insight-box gold-border">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            {render_icon('analytics', size='md', color='gold')}
            <span class="insight-title">The Headline ({labels['period_short']})</span>
        </div>
        <div class="insight-content">
            CENTURION TREE is <strong>{verdict['label'].lower()}</strong> with a Health Score of <strong>{health_score:.0f}/100</strong>.<br><br>
            • <strong>{labels['ac_label']}:</strong> {format_peso(row['AC'])} ({change_word} {format_peso(abs(ac_change))} vs {labels['py_label']})<br>
            • <strong>{labels['nsc_label']}:</strong> {format_peso(row['NSC'])}<br>
            • <strong>{labels['lives_label']}:</strong> {row['Lives']:,.0f}<br>
            • <strong>Overall Competitive Rank:</strong> #{row['Competitive_Rank']} of {df.shape[0]} NBOs — top {rank_pct:.0f}%<br>
            • <strong>AC Rank:</strong> #{row['AC_Rank']} · <strong>NSC Rank:</strong> #{row['NSC_Rank']} · <strong>Lives Rank:</strong> #{row['Lives_Rank']}<br>
            • <strong>Growth Rank:</strong> #{row['Growth_Rank']} · <strong>Target Rank:</strong> #{row['Target_Rank'] if row.get('Target_Rank') else 'N/A'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if row["AC_Growth"] > 0:
        status, icon, title = "strong", "trending_up", f"Life AC is up {row['AC_Growth']:.1f}% {labels['growth_context']}"
        content = f"""
        <strong>Revenue from life production is growing.</strong><br><br>
        • {labels['py_label'].title()}: <strong>{format_peso(row['AC_PY'])}</strong><br>
        • {labels['period_short']} now: <strong>{format_peso(row['AC'])}</strong><br>
        • Net gain: <strong>{format_peso(row['AC'] - row['AC_PY'])}</strong><br><br>
        <strong>What this means:</strong> Current activity is beating last year's pace for this same period. Protect what's working.
        """
        explanation = f"A positive {row['AC_Growth']:.1f}% means you are producing more Life AC than at this point last year."
    else:
        status, icon, title = "risk", "trending_down", f"Life AC is down {abs(row['AC_Growth']):.1f}% {labels['growth_context']}"
        content = f"""
        <strong>Revenue from life production is below last year.</strong><br><br>
        • {labels['py_label'].title()}: <strong>{format_peso(row['AC_PY'])}</strong><br>
        • {labels['period_short']} now: <strong>{format_peso(row['AC'])}</strong><br>
        • Shortfall: <strong>{format_peso(abs(row['AC_PY'] - row['AC']))}</strong><br><br>
        <strong>What to do:</strong> Review pipeline, advisor activity, and top client segments. Prioritize actions that close the gap fastest.
        """
        explanation = f"A decline of {abs(row['AC_Growth']):.1f}% means less Life AC than the same period last year — this needs a clear recovery plan."
    
    render_insight_card(icon, title, content, status, explanation)

    if row["NSC_Growth"] > 0:
        nsc_status, nsc_icon, nsc_title = "strong", "add_circle", f"New business is up {row['NSC_Growth']:.1f}%"
        nsc_content = f"""
        <strong>New policy sales are contributing more than last year.</strong><br>
        Life NSC: <strong>{format_peso(row['NSC'])}</strong> vs {format_peso(row['NSC_PY'])} last year.
        """
    else:
        nsc_status, nsc_icon, nsc_title = "risk", "remove_circle", f"New business is down {abs(row['NSC_Growth']):.1f}%"
        nsc_content = f"""
        <strong>Fewer new policies are being sold than last year.</strong><br>
        Life NSC: <strong>{format_peso(row['NSC'])}</strong> vs {format_peso(row['NSC_PY'])} last year.
        Focus on prospecting and new business campaigns.
        """
    render_insight_card(nsc_icon, nsc_title, nsc_content, nsc_status,
                        "Life NSC measures commission from newly issued business — it signals future growth.")

    # Updated threat insight using Competitive Rank
    if threats.get("gap_to_next", 0) > 0 and threats.get("next_nbo"):
        status, icon, title = "stable", "rocket", f"One rank away: Overall #{row['Competitive_Rank'] - 1}"
        content = f"""
        <strong>You can move up one overall rank with focused effort.</strong><br><br>
        • NBO ahead of you: <strong>{threats['next_nbo']}</strong><br>
        • You need: <strong>{format_peso(threats['gap_to_next'])}</strong> more Life AC ({threats['opportunity_percent']:.1f}% increase) to move from Overall Rank #{row['Competitive_Rank']} to #{row['Competitive_Rank'] - 1}<br><br>
        <strong>What to do:</strong> Target high-value cases and advisors closest to closing.
        """
        explanation = "Closing this gap moves CENTURION TREE up one position in the overall competitive ranking."
    else:
        status, icon, title = "strong", "emoji_events", "You hold the #1 overall rank"
        content = f"""
        <strong>No other NBO has a better overall competitive ranking.</strong><br><br>
        Protect your lead by maintaining advisor activity and client retention.
        """
        explanation = "Overall Competitive Rank #1 means you lead the field for this reporting period."
    
    render_insight_card(icon, title, content, status, explanation)

    if has_target_data(row):
        target_pct = clean_number(row.get("Pct_Target", 0))
        if target_pct > 80:
            status, icon, title = "strong", "target", f"Annual target: {target_pct:.1f}% reached — on track"
            content = f"""
            <strong>You are on pace to hit your annual target.</strong><br><br>
            • Target: <strong>{format_peso(forecast['target'])}</strong><br>
            • Achieved (YTD): <strong>{format_peso(row['AC'])}</strong><br>
            • Progress: <strong>{target_pct:.1f}%</strong>
            """
            explanation = "Target attainment compares year-to-date Life AC against your full-year goal."
        elif target_pct > 50:
            status, icon, title = "stable", "target", f"Annual target: {target_pct:.1f}% — need to speed up"
            content = f"""
            <strong>Progress is OK but not fast enough for the year-end goal.</strong><br><br>
            • Target: <strong>{format_peso(forecast['target'])}</strong><br>
            • Achieved: <strong>{format_peso(row['AC'])}</strong><br>
            • Still needed: <strong>{format_peso(forecast['gap_to_target'])}</strong>
            """
            explanation = f"At {target_pct:.1f}%, you need {format_peso(forecast['gap_to_target'])} more Life AC to reach target."
        else:
            status, icon, title = "critical", "error", f"Annual target: only {target_pct:.1f}% — urgent action"
            content = f"""
            <strong>Significantly behind the annual target.</strong><br><br>
            • Target: <strong>{format_peso(forecast['target'])}</strong><br>
            • Achieved: <strong>{format_peso(row['AC'])}</strong><br>
            • Gap: <strong>{format_peso(forecast['gap_to_target'])}</strong><br><br>
            Schedule an immediate sales review and recovery plan.
            """
            explanation = "Low target attainment requires a structured catch-up plan with weekly tracking."
        render_insight_card(icon, title, content, status, explanation)
    elif data_source == "MTD" and not has_target_data(row):
        render_insight_card(
            "calendar_month", "Monthly snapshot — no annual target in this file",
            f"""<strong>This MTD report shows {labels['period']} performance only.</strong><br><br>
            Upload a <strong>YTD file</strong> to see annual target progress, or use the rank and growth insights above to guide this month's priorities.""",
            "info",
            "MTD files do not include annual targets. The dashboard still scores growth, rank, productivity, and momentum from MTD data alone."
        )

def render_mtd_comparison(ytd_row, mtd_row, df):
    months = max(datetime.now().month, 1)
    month_name = datetime.now().strftime("%B")

    mtd_ac, mtd_nsc, mtd_lives = mtd_row["AC"], mtd_row["NSC"], mtd_row["Lives"]
    avg_ac = ytd_row["AC"] / months
    avg_nsc = ytd_row["NSC"] / months
    avg_lives = ytd_row["Lives"] / months

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('compare_arrows', size='lg', color='gold')}
        <h3 style="margin:0;">This Month vs YTD Monthly Pace</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">
        Compares your <strong>MTD file</strong> (this month's production) against your
        <strong>YTD monthly average</strong> (YTD totals ÷ {months} months through {month_name}).
    </p>
    """, unsafe_allow_html=True)

    metrics = [
        ("Life AC", mtd_ac, avg_ac, format_peso),
        ("Life NSC", mtd_nsc, avg_nsc, format_peso),
        ("Lives", mtd_lives, avg_lives, lambda v: f"{v:,.0f}"),
    ]

    cols = st.columns(3)
    results = []
    for col, (label, mtd_val, avg_val, fmt) in zip(cols, metrics):
        diff_pct = safe_divide(mtd_val - avg_val, avg_val) * 100
        results.append(diff_pct)
        with col:
            st.metric(
                f"{label} — MTD vs Avg",
                f"{diff_pct:+.1f}%",
                f"{fmt(mtd_val)} this month vs {fmt(avg_val)} avg",
                delta_color="normal" if diff_pct >= 0 else "inverse",
            )
            if diff_pct >= 0:
                render_callout(
                    f"{label} is ahead of pace",
                    f"You are <strong>{diff_pct:.1f}% above</strong> your {month_name} YTD monthly average. Keep this momentum.",
                    "success" if diff_pct >= 5 else "info",
                )
            else:
                render_callout(
                    f"{label} is behind pace",
                    f"You are <strong>{abs(diff_pct):.1f}% below</strong> your YTD monthly average "
                    f"({fmt(mtd_val)} vs {fmt(avg_val)}). Focus advisor activity to close the gap.",
                    "warning" if diff_pct > -20 else "danger",
                )

    st.markdown("### What This Means")
    ahead = sum(v >= 0 for v in results)

    if ahead == 3:
        render_callout(
            "Strong month across the board",
            "Life AC, Life NSC, and Lives are all running above your YTD monthly pace. Document what is working and replicate it next month.",
            "success",
        )
    elif ahead >= 2:
        render_callout(
            "Mostly on track",
            f"{ahead} of 3 metrics are above your YTD monthly average. Review the lagging metric with your team this week.",
            "info",
        )
    elif ahead == 1:
        render_callout(
            "Mixed month — action needed",
            "Only one metric is above your YTD monthly pace. Prioritize pipeline reviews and high-value case closing to recover.",
            "warning",
        )
    else:
        render_callout(
            "Below pace on all metrics",
            "This month's production is below your YTD monthly average on Life AC, NSC, and Lives. Schedule an immediate review of advisor activity, pipeline, and conversion.",
            "danger",
        )

def render_threat_monitor(threats, row):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('shield', size='lg', color='gold')}
        <h3 style="margin:0;">Threat Monitor</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Competitive intelligence - who's ahead and who's behind overall</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if threats["gap_to_next"] > 0 and threats.get("next_nbo"):
            render_callout(
                "Opportunity to move up",
                f"<strong>{threats['next_nbo']}</strong> is ahead of you in the overall ranking. "
                f"You need <strong>{format_peso(threats['gap_to_next'])}</strong> more Life AC "
                f"({threats['opportunity_percent']:.1f}% increase) to move from Overall Rank #{row['Competitive_Rank']} to #{row['Competitive_Rank'] - 1}.",
                "info",
            )
        else:
            render_callout(
                "You hold the top spot",
                "No other NBO has a better overall competitive ranking. Focus on maintaining and extending your lead.",
                "success",
            )
    
    with col2:
        if threats["gap_to_prev"] > 0 and threats.get("prev_nbo"):
            threat_pct = safe_divide(threats["gap_to_prev"], row["AC"]) * 100
            if threat_pct < 5:
                render_callout(
                    "High threat — competitor very close",
                    f"<strong>{threats['prev_nbo']}</strong> is only {format_peso(threats['gap_to_prev'])} "
                    f"({threat_pct:.1f}%) behind you overall. Accelerate growth to protect your rank.",
                    "warning",
                )
            elif threat_pct < 10:
                render_callout(
                    "Moderate threat",
                    f"<strong>{threats['prev_nbo']}</strong> is {format_peso(threats['gap_to_prev'])} "
                    f"({threat_pct:.1f}%) behind. Keep production steady to stay ahead.",
                    "info",
                )
            else:
                render_callout(
                    "Low threat — comfortable lead",
                    f"<strong>{threats['prev_nbo']}</strong> is {format_peso(threats['gap_to_prev'])} behind. "
                    "You have a comfortable buffer.",
                    "success",
                )
        else:
            render_callout(
                "No immediate threat from behind",
                "No NBO is close behind you in the overall rankings. Focus on closing the gap to the next rank up.",
                "info",
            )

def render_forecast_center(forecast, row, data_source="YTD"):
    labels = get_period_labels(data_source)
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('trending_up', size='lg', color='gold')}
        <h3 style="margin:0;">Forecast Center — {labels['period_short']}</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">Projected performance based on current {labels['period']} trends</p>
    """, unsafe_allow_html=True)

    current_ac = forecast["current_ac"]
    has_target = forecast.get("has_target", False)

    if has_target:
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
        scenarios = forecast.get("scenarios", {"Worst Case": current_ac, "Expected": current_ac, "Best Case": current_ac})
        fig.add_trace(go.Bar(x=list(scenarios.keys()), y=list(scenarios.values()),
                             text=[format_peso(v) for v in scenarios.values()], textposition="auto",
                             marker_color=[COLORS["danger"], SUN_LIFE_GOLD, COLORS["success"]]),
                      row=1, col=2)
        fig.update_layout(height=350, showlegend=False, template="plotly_white", margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "Annual target progress is available in **YTD reports** only. "
            f"Below is a monthly run-rate view based on {labels['period']} Life AC."
        )
        scenarios = {
            "Current Month": current_ac,
            "3-Month Pace": current_ac * 3,
            "Annualized (×12)": current_ac * 12,
        }
        fig = go.Figure(go.Bar(
            x=list(scenarios.keys()), y=list(scenarios.values()),
            text=[format_peso(v) for v in scenarios.values()], textposition="auto",
            marker_color=[SUN_LIFE_GOLD, COLORS["info"], COLORS["success"]],
        ))
        fig.update_layout(title=f"{labels['period_short']} Run-Rate Scenarios", height=350, template="plotly_white",
                          margin=dict(l=0, r=0, t=50, b=0), yaxis_title="Life AC")
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if data_source == "MTD":
            st.info(f"**This Month (Life AC)**\n\n{format_peso(current_ac)}")
        else:
            st.info(f"**Current Daily Pace**\n\n{format_peso(forecast['annual_projection'] / 365)} per day")
    with col2:
        label = "Annualized (×12)" if data_source == "MTD" else "Annual Projection"
        st.info(f"**{label}**\n\n{format_peso(forecast['annual_projection'])}")
    with col3:
        if has_target:
            if forecast["gap_to_target"] > 0:
                st.warning(f"**Gap to Target**\n\n{format_peso(forecast['gap_to_target'])}")
            else:
                st.success("**Target Achieved**\n\n✅ On track to meet or exceed target")
        else:
            st.info("**Annual Target**\n\nUpload YTD file to track target progress")

def render_productivity_benchmark(row, df):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('speed', size='lg', color='gold')}
        <h3 style="margin:0;">Case Size Benchmark</h3>
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
        st.metric("Your Case Size Rank", f"{percentile:.0f}th percentile", delta=f"of {df.shape[0]} NBOs")
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
            render_callout(
                "Life AC below last year",
                f"You are down {format_peso(leakage['ac_leakage'])} vs the same period last year "
                f"({safe_divide(leakage['ac_leakage'], row['AC_PY']) * 100:.1f}% of prior-year Life AC). "
                "Recovery scenarios below show what partial recovery would look like.",
                "danger",
            )
            rec_df = pd.DataFrame({
                "Recovery Rate": list(recovery.keys()),
                "Recovered AC": [format_peso(r["ac"]) for r in recovery.values()]
            })
            st.dataframe(rec_df, hide_index=True, use_container_width=True)
        else:
            render_callout(
                "No Life AC leakage",
                f"Life AC is stable or up vs last year. "
                f"Current: {format_peso(row['AC'])} · Prior year same period: {format_peso(row['AC_PY'])}",
                "success",
            )
    
    with col2:
        if leakage["lives_leakage"] > 0:
            render_callout(
                "Lives below last year",
                f"You are down {leakage['lives_leakage']:,.0f} lives "
                f"({safe_divide(leakage['lives_leakage'], row['Lives_PY']) * 100:.1f}% vs prior year). "
                "Focus on retention and new business prospecting.",
                "warning",
            )
        else:
            render_callout(
                "No lives leakage",
                f"Lives are stable or up vs last year. "
                f"Current: {row['Lives']:,.0f} · Prior year: {row['Lives_PY']:,.0f}",
                "success",
            )

def render_competitive_position(row, df):
    """Updated to show all six ranks with Overall Competitive Rank as primary"""
    total = df.shape[0]

    comp_rank = int(row["Competitive_Rank"])
    ac_rank = int(row["AC_Rank"])
    nsc_rank = int(row["NSC_Rank"])
    lives_rank = int(row["Lives_Rank"])
    growth_rank = int(row["Growth_Rank"])
    target_rank = int(row["Target_Rank"]) if row.get("Target_Rank") and pd.notna(row["Target_Rank"]) else None

    comp_pct = row.get("Competitive_Percentile", 0)

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        {render_icon('emoji_events', size='lg', color='gold')}
        <h3 style="margin:0;">Competitive Position</h3>
    </div>
    <p style="color:#6B7280; margin-bottom:1rem;">All rankings among {total} NBOs</p>
    """, unsafe_allow_html=True)
    
    # Show all six ranks in a 3x2 grid
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        st.metric("🏆 Overall", f"#{comp_rank}", f"Top {comp_pct:.0f}%")
    with col2:
        st.metric("💰 AC", f"#{ac_rank}", f"of {total} NBOs")
    with col3:
        st.metric("📈 NSC", f"#{nsc_rank}", f"of {total} NBOs")
    with col4:
        st.metric("👥 Lives", f"#{lives_rank}", f"of {total} NBOs")
    with col5:
        st.metric("🚀 Growth", f"#{growth_rank}", f"of {total} NBOs")
    with col6:
        target_display = f"#{target_rank}" if target_rank else "N/A"
        st.metric("🎯 Target", target_display, f"of {total} NBOs" if target_rank else "YTD only")
    
    # Position Summary
    st.markdown(f"""
    <div class="insight-box gold-border" style="margin-top:1rem;">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            {render_icon('analytics', size='md', color='gold')}
            <span class="insight-title">Position Summary</span>
        </div>
        <div class="insight-content">
            <strong>🏆 Overall Competitive Rank:</strong> #{comp_rank} of {total} NBOs · Top {comp_pct:.0f}%<br>
            <strong>💰 AC Rank:</strong> #{ac_rank} of {total} NBOs<br>
            <strong>📈 NSC Rank:</strong> #{nsc_rank} of {total} NBOs<br>
            <strong>👥 Lives Rank:</strong> #{lives_rank} of {total} NBOs<br>
            <strong>🚀 Growth Rank:</strong> #{growth_rank} of {total} NBOs<br>
            <strong>🎯 Target Rank:</strong> {f'#{target_rank} of {total} NBOs' if target_rank else 'N/A (YTD only)'}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_rankings_page(df, report_type, centurion_row):
    """New Rankings page with all leaderboards - COMPLETELY FIXED DISPLAY"""
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
        {render_icon('leaderboard', size='xl', color='gold')}
        <h2 style="margin:0;">🏆 Rankings Leaderboard</h2>
        <span class="data-source-badge">{report_type}</span>
    </div>
    <p style="color:#6B7280; margin-bottom:1.5rem;">
        Complete rankings of all {len(df)} NBOs. CENTURION TREE is highlighted in gold.
    </p>
    """, unsafe_allow_html=True)
    
    # Create tabs for each ranking type
    tabs = st.tabs([
        "🏆 Overall Rankings",
        "💰 AC Rankings", 
        "📈 NSC Rankings",
        "👥 Lives Rankings",
        "🚀 Growth Rankings",
        "🎯 % to Target Rankings"
    ])
    
    # Create a completely clean DataFrame with ONLY the data we need
    # This avoids any pandas metadata contamination
    clean_data = []
    
    for idx, row in df.iterrows():
        # Get clean values
        nbo = str(row["NBO"])
        ac = float(row["AC"]) if pd.notna(row["AC"]) else 0
        nsc = float(row["NSC"]) if pd.notna(row["NSC"]) else 0
        lives = float(row["Lives"]) if pd.notna(row["Lives"]) else 0
        
        # Get ranks
        comp_rank = int(row["Competitive_Rank"]) if pd.notna(row["Competitive_Rank"]) else 0
        ac_rank = int(row["AC_Rank"]) if pd.notna(row["AC_Rank"]) else 0
        nsc_rank = int(row["NSC_Rank"]) if pd.notna(row["NSC_Rank"]) else 0
        lives_rank = int(row["Lives_Rank"]) if pd.notna(row["Lives_Rank"]) else 0
        growth_rank = int(row["Growth_Rank"]) if pd.notna(row["Growth_Rank"]) else 0
        
        # Target data
        pct_target = float(row["Pct_Target"]) if pd.notna(row.get("Pct_Target")) and row.get("Pct_Target") is not None else 0
        target_rank = int(row["Target_Rank"]) if pd.notna(row.get("Target_Rank")) and row.get("Target_Rank") is not None else 0
        
        # Add star to CENTURION
        if "CENTURION" in nbo.upper():
            nbo_display = f"⭐ {nbo}"
        else:
            nbo_display = nbo
        
        clean_data.append({
            "NBO": nbo,
            "NBO_Display": nbo_display,
            "AC": ac,
            "NSC": nsc,
            "Lives": lives,
            "Competitive_Rank": comp_rank,
            "AC_Rank": ac_rank,
            "NSC_Rank": nsc_rank,
            "Lives_Rank": lives_rank,
            "Growth_Rank": growth_rank,
            "Pct_Target": pct_target,
            "Target_Rank": target_rank,
            "is_centurion": "CENTURION" in nbo.upper()
        })
    
    clean_df = pd.DataFrame(clean_data)
    
    # Overall Rankings
    with tabs[0]:
        st.subheader("Overall Competitive Rankings")
        st.caption(f"Sorted by Overall Competitive Rank — {len(clean_df)} NBOs")
        sorted_df = clean_df.sort_values("Competitive_Rank")
        _render_ranking_table_safe(sorted_df, "Competitive_Rank", report_type)
    
    # AC Rankings
    with tabs[1]:
        st.subheader("AC Rankings")
        st.caption(f"Sorted by Life AC — {len(clean_df)} NBOs")
        sorted_df = clean_df.sort_values("AC_Rank")
        _render_ranking_table_safe(sorted_df, "AC_Rank", report_type)
    
    # NSC Rankings
    with tabs[2]:
        st.subheader("NSC Rankings")
        st.caption(f"Sorted by Life NSC — {len(clean_df)} NBOs")
        sorted_df = clean_df.sort_values("NSC_Rank")
        _render_ranking_table_safe(sorted_df, "NSC_Rank", report_type)
    
    # Lives Rankings
    with tabs[3]:
        st.subheader("Lives Rankings")
        st.caption(f"Sorted by Lives — {len(clean_df)} NBOs")
        sorted_df = clean_df.sort_values("Lives_Rank")
        _render_ranking_table_safe(sorted_df, "Lives_Rank", report_type)
    
    # Growth Rankings
    with tabs[4]:
        st.subheader("Growth Rankings")
        st.caption(f"Sorted by Growth Score — {len(clean_df)} NBOs")
        sorted_df = clean_df.sort_values("Growth_Rank")
        _render_ranking_table_safe(sorted_df, "Growth_Rank", report_type)
    
    # Target Rankings (only if available)
    with tabs[5]:
        st.subheader("% to Target Rankings")
        if report_type == "YTD" and "Target_Rank" in clean_df.columns:
            st.caption(f"Sorted by % to Target — {len(clean_df)} NBOs")
            sorted_df = clean_df.sort_values("Target_Rank")
            _render_ranking_table_safe(sorted_df, "Target_Rank", report_type)
        else:
            st.info("📊 Target rankings are only available in YTD reports. Upload a YTD file to see target rankings.")

def _render_ranking_table_safe(sorted_df, rank_column, report_type):
    """SAFE version: Render a ranking table with clean values - NO metadata"""
    
    # Rank column label
    rank_label = {
        "Competitive_Rank": "Overall",
        "AC_Rank": "AC",
        "NSC_Rank": "NSC",
        "Lives_Rank": "Lives",
        "Growth_Rank": "Growth",
        "Target_Rank": "Target"
    }.get(rank_column, "Rank")
    
    # Build HTML table
    html = '<div class="leaderboard-container"><table class="ranking-table">'
    
    # Header
    html += '<thead><tr>'
    html += f'<th>{rank_label}</th>'
    html += '<th>NBO</th>'
    html += '<th>AC</th>'
    html += '<th>NSC</th>'
    html += '<th>Lives</th>'
    html += '<th>Growth Rank</th>'
    if report_type == "YTD":
        html += '<th>% to Target</th>'
        html += '<th>Target Rank</th>'
    html += '</tr></thead>'
    
    # Body
    html += '<tbody>'
    
    for idx, row in sorted_df.iterrows():
        is_centurion = row["is_centurion"]
        row_class = 'centurion-row' if is_centurion else ''
        html += f'<tr class="{row_class}">'
        
        # Rank column
        rank_val = int(row[rank_column])
        if is_centurion:
            html += f'<td class="rank-number centurion-rank">#{rank_val}</td>'
        else:
            html += f'<td class="rank-number">#{rank_val}</td>'
        
        # NBO
        html += f'<td>{row["NBO_Display"]}</td>'
        
        # AC
        html += f'<td>{format_peso(row["AC"])}</td>'
        
        # NSC
        html += f'<td>{format_peso(row["NSC"])}</td>'
        
        # Lives
        html += f'<td>{int(row["Lives"]):,}</td>'
        
        # Growth Rank
        html += f'<td>#{int(row["Growth_Rank"])}</td>'
        
        # Target columns for YTD
        if report_type == "YTD":
            if row["Pct_Target"] > 0:
                html += f'<td>{row["Pct_Target"]:.1f}%</td>'
            else:
                html += '<td>—</td>'
            
            if row["Target_Rank"] > 0:
                html += f'<td>#{int(row["Target_Rank"])}</td>'
            else:
                html += '<td>—</td>'
        
        html += '</tr>'
    
    html += '</tbody></table></div>'
    
    st.markdown(html, unsafe_allow_html=True)
    
    # Show CENTURION position
    centurion_rows = sorted_df[sorted_df["is_centurion"]]
    if not centurion_rows.empty:
        centurion_row = centurion_rows.iloc[0]
        rank_val = int(centurion_row[rank_column])
        st.caption(f"⭐ CENTURION TREE is highlighted in gold — Rank #{rank_val}")

def render_management_actions(row, threats, forecast, health_score, data_source):
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
            "details": f"Competitor is only {format_peso(threats['gap_to_prev'])} behind overall. Increase productivity and accelerate growth to maintain your lead."
        })
    
    if threats.get("opportunity_value", 0) > 0:
        actions.append({
            "priority": "HIGH",
            "action": f"🎯 Overtake {threats['next_nbo']}",
            "details": f"Need +{threats['opportunity_percent']:.1f}% growth to pass {threats['next_nbo']} overall. Focus on competitive advantages and key opportunities."
        })
    
    if has_target_data(row) and forecast.get("gap_to_target", 0) > 0:
        actions.append({
            "priority": "MEDIUM",
            "action": "📊 Accelerate Target Attainment",
            "details": f"Gap to annual target: {format_peso(forecast['gap_to_target'])}. Increase sales activity on high-value opportunities."
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
        st.markdown("*Upload one or both files — MTD works on its own*")
        ytd_file = st.file_uploader("Upload YTD File", type=["xlsx"], key="ytd")
        mtd_file = st.file_uploader("Upload MTD File", type=["xlsx"], key="mtd")
        
        st.markdown("---")
        
        with st.expander("How Metrics Work"):
            st.markdown("""
            **Health Score** (0-100) — overall performance at a glance (unchanged)
            
            **Competitive Ranking** — weighted position across all NBOs
            - **YTD:** AC (25%), NSC (20%), Lives (15%), Growth (20%), Target (20%)
            - **MTD:** AC (35%), NSC (25%), Lives (20%), Growth (20%)
            
            **Terms:**
            - **Life AC** — total life insurance commission
            - **Life NSC** — commission from new policies
            - **Lives** — number of clients
            - **Overall Rank** — weighted competitive position (#1 is best)
            - **Growth Rank** — based on average of AC, NSC, and Lives growth
            - **Target Rank** — based on % to Target (YTD only)
            """)
        
        st.caption("Powered by Sun Life Data Analytics")

    ytd_df = None
    mtd_df = None
    centurion_ytd = None
    centurion_mtd = None
    load_errors = []

    if ytd_file:
        ytd_df = load_ytd_report(ytd_file)
        if ytd_df.empty:
            load_errors.append("YTD file loaded but no NBO data was found. Check that the **PER NBO** sheet is present.")
        else:
            centurion_ytd = find_centurion(ytd_df)
            if centurion_ytd.empty:
                load_errors.append(
                    f"YTD file loaded ({len(ytd_df)} NBOs) but **CENTURION TREE** was not found. "
                    f"Names found include: {format_nbo_sample(ytd_df)}"
                )

    if mtd_file:
        mtd_df = load_mtd_report(mtd_file)
        if mtd_df.empty:
            load_errors.append("MTD file loaded but no NBO data was found. Check that the **PER NBO** sheet is present.")
        else:
            centurion_mtd = find_centurion(mtd_df)
            if centurion_mtd.empty:
                load_errors.append(
                    f"MTD file loaded ({len(mtd_df)} NBOs) but **CENTURION TREE** was not found. "
                    f"Names found include: {format_nbo_sample(mtd_df)}"
                )

    ytd_ready = ytd_df is not None and not ytd_df.empty and centurion_ytd is not None and not centurion_ytd.empty
    mtd_ready = mtd_df is not None and not mtd_df.empty and centurion_mtd is not None and not centurion_mtd.empty

    if not ytd_ready and not mtd_ready:
        if load_errors:
            for msg in load_errors:
                st.error(msg)
        else:
            st.info("👈 Upload a **YTD** or **MTD** Excel file to begin. MTD-only is fully supported.")
        st.markdown("""
        ### Getting Started
        1. Upload an **MTD file** for this month's performance (works without YTD)
        2. Upload a **YTD file** for year-to-date analysis and annual targets
        3. Upload **both** to compare this month vs your monthly average
        
        ### What You'll See
        - **Health Score** — one number summarizing performance (unchanged)
        - **Competitive Rankings** — overall, AC, NSC, Lives, Growth, Target
        - **Executive Briefing** — plain-English insights for leadership
        - **Threat Monitor** — who is ahead or behind you overall
        - **Action Center** — prioritized next steps
        - **Leaderboard** — complete rankings of all NBOs
        """)
        return

    if ytd_ready and mtd_ready:
        view_mode = st.sidebar.radio(
            "Dashboard view",
            ["YTD (year to date)", "MTD (this month)"],
            help="Switch between annual and monthly views when both files are uploaded."
        )
        use_mtd = view_mode.startswith("MTD")
    elif mtd_ready:
        use_mtd = True
    else:
        use_mtd = False

    if use_mtd:
        row = centurion_mtd.iloc[0]
        df = mtd_df
        data_source = "MTD"
    else:
        row = centurion_ytd.iloc[0]
        df = ytd_df
        data_source = "YTD"

    include_target = has_target_data(row)

    # Health Score - UNCHANGED
    health_score = calculate_health_score(row, df, include_target=include_target)
    health_data = calculate_health_score_components(row, df, include_target=include_target)
    verdict = determine_verdict(health_score)
    
    # Threat metrics - UPDATED to use Competitive_Rank
    threats = calculate_threat_metrics(row, df)
    forecast = calculate_forecast(row)
    leakage, recovery = calculate_revenue_leakage(row)

    render_executive_overview(row, df, health_score, verdict, data_source)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    render_component_breakdown(health_data, data_source)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    tabs = st.tabs([
        "📋 Briefing",
        "📈 Forecast", 
        "🛡️ Threats",
        "📊 Case Size",
        "💰 Revenue",
        "🏆 Position",
        "🎯 Actions",
        "🏆 Rankings"
    ])
    
    with tabs[0]:
        render_executive_briefing(row, health_score, verdict, threats, forecast, df, data_source)
    
    with tabs[1]:
        render_forecast_center(forecast, row, data_source)
    
    with tabs[2]:
        render_threat_monitor(threats, row)
    
    with tabs[3]:
        render_productivity_benchmark(row, df)
    
    with tabs[4]:
        render_revenue_leakage(leakage, recovery, row)
    
    with tabs[5]:
        render_competitive_position(row, df)
    
    with tabs[6]:
        render_management_actions(row, threats, forecast, health_score, data_source)
    
    with tabs[7]:
        render_rankings_page(df, data_source, row)
    
    if ytd_ready and mtd_ready and centurion_ytd is not None and centurion_mtd is not None:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_mtd_comparison(centurion_ytd.iloc[0], centurion_mtd.iloc[0], ytd_df)

if __name__ == "__main__":
    main()