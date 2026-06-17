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
    """Styled message box — avoids raw HTML tags showing in Streamlit widgets."""
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

# PER NBO sheet — same layout for YTD and MTD files
# Col A (0): Full NBO name | Col B (1): Broker code (numeric, NOT a name)
# Col C (2): Short NBO label | Col D-F (3-5): Current period Lives, AC, NSC
# Col G-I (6-8): Prior-year same period Lives, AC, NSC | Col M (12): SSP
# YTD only — Col N (13): 2026 Annual Life AC Target | Col O (14): % to target
# Sheet2 tab holds current-period values when PER NBO cols D-F are blank

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

def _looks_like_nbo_name(value):
    """True if the cell value looks like an NBO office name, not a metric or row index."""
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
    """Read NBO name from column A, fallback column C. Column B is always broker code."""
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

def _build_record(row, name, territory, report_type):
    """Build one NBO record from PER NBO column positions."""
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
    if report_type == "YTD" and len(row) > METRIC_COLUMNS["Pct_Target"]:
        record["Target"] = clean_number(row.iloc[METRIC_COLUMNS["Target"]])
        record["Pct_Target"] = _normalize_pct_target(row.iloc[METRIC_COLUMNS["Pct_Target"]])
    return record

def _load_sheet2_lookup(file):
    """Sheet2 has current-period metrics when PER NBO cols D-F are blank."""
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
    return lookup

def _supplement_current_metrics(record, sheet2_lookup, source_lookup):
    """Fill blank current-period cells from Sheet2 or SOURCE."""
    if record["AC"] > 0 or record["Lives"] > 0:
        return record

    key = _nbo_key(record["NBO"])
    if key in sheet2_lookup:
        src = sheet2_lookup[key]
    elif record["NBO"].upper() in source_lookup:
        src = source_lookup[record["NBO"].upper()]
    else:
        return record

    record["Lives"] = src.get("Lives", record["Lives"])
    record["AC"] = src.get("AC", record["AC"])
    record["NSC"] = src.get("NSC", record["NSC"])
    if record.get("SSP", 0) == 0 and src.get("SSP"):
        record["SSP"] = src["SSP"]
    return record

def _load_source_mtd_lookup(file):
    """SOURCE sheet has MTD metrics when PER NBO cols D-F are blank."""
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
    """Legacy wrapper — prefer _supplement_current_metrics per row."""
    for record in rows:
        _supplement_current_metrics(record, {}, lookup)
    return rows

def _normalize_pct_target(value):
    pct = clean_number(value)
    if pct <= 0:
        return 0
    return pct * 100 if pct <= 1.5 else pct

def enrich_dataframe(df, report_type):
    """Add growth, rank, and productivity columns required by the dashboard."""
    if df.empty:
        return df

    df = df.copy()
    df["AC_Growth"] = df.apply(lambda x: safe_divide(x["AC"] - x["AC_PY"], x["AC_PY"]) * 100, axis=1)
    df["NSC_Growth"] = df.apply(lambda x: safe_divide(x["NSC"] - x["NSC_PY"], x["NSC_PY"]) * 100, axis=1)
    df["Lives_Growth"] = df.apply(lambda x: safe_divide(x["Lives"] - x["Lives_PY"], x["Lives_PY"]) * 100, axis=1)
    df["AC_Per_Life"] = df.apply(lambda x: safe_divide(x["AC"], x["Lives"]), axis=1)
    df["NSC_Per_Life"] = df.apply(lambda x: safe_divide(x["NSC"], x["Lives"]), axis=1)
    df["AC_Rank"] = df["AC"].rank(method="min", ascending=False).astype(int)
    df["NSC_Rank"] = df["NSC"].rank(method="min", ascending=False).astype(int)
    df["Report_Type"] = report_type

    if "SSP" in df.columns:
        df["SSP_Growth"] = df.apply(
            lambda x: safe_divide(x["SSP"] - x.get("SSP_PY", 0), x.get("SSP_PY", 0)) * 100, axis=1
        )

    if "Target" not in df.columns:
        df["Target"] = None
    if "Pct_Target" not in df.columns:
        df["Pct_Target"] = None

    return df

@st.cache_data
def load_production_report(file, report_type, _parser_version=8):
    """Load YTD or MTD from PER NBO (same layout). YTD adds target cols N-O."""
    try:
        raw = pd.read_excel(file, sheet_name="PER NBO", header=None)
    except Exception as e:
        st.error(f"Error loading {report_type} file: {e}")
        return pd.DataFrame()

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

        record = _build_record(row, name, territory, report_type)
        record = _supplement_current_metrics(record, sheet2_lookup, source_lookup)
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
            "nsc_label": "Monthly Life NSC",
            "lives_label": "Lives (This Month)",
            "py_label": "same month last year",
            "growth_context": "vs same month last year",
            "rank_context": "among all NBOs this month",
        }
    return {
        "period": "year to date",
        "period_short": "YTD",
        "ac_label": "Year-to-Date Life AC",
        "nsc_label": "Year-to-Date Life NSC",
        "lives_label": "Lives (YTD)",
        "py_label": "prior year to date",
        "growth_context": "vs prior year to date",
        "rank_context": "among all NBOs year to date",
    }

@st.cache_data
def load_ytd_report(file):
    return load_production_report(file, "YTD")

@st.cache_data
def load_mtd_report(file):
    return load_production_report(file, "MTD")

# ============================================================================
# CALCULATION ENGINE
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

def _health_score_weights(include_target):
    if include_target:
        return {"ac": 0.25, "nsc": 0.15, "target": 0.25, "productivity": 0.15, "rank": 0.10, "momentum": 0.10}
    return {"ac": 0.30, "nsc": 0.20, "target": 0.0, "productivity": 0.20, "rank": 0.15, "momentum": 0.15}

def calculate_health_score(row, df, include_target=None):
    if include_target is None:
        include_target = has_target_data(row)

    ac_growth = row["AC_Growth"]
    ac_score = max(0, min(100, 50 + (ac_growth / 2)))
    
    nsc_growth = row["NSC_Growth"]
    nsc_score = max(0, min(100, 50 + (nsc_growth / 2)))
    
    target_pct = clean_number(row.get("Pct_Target", 0))
    target_score = min(target_pct, 100) if include_target else 50
    
    company_avg = df["AC_Per_Life"].mean() if df["AC_Per_Life"].mean() > 0 else 1
    productivity_score = min((row["AC_Per_Life"] / company_avg) * 100, 150) if company_avg > 0 else 50
    
    total_nbos = df.shape[0]
    rank_score = ((total_nbos - row["AC_Rank"]) / total_nbos * 100) if total_nbos > 0 else 50
    
    momentum_score = 80 if (ac_growth > 0 and nsc_growth > 0) else 60 if (ac_growth > 0 or nsc_growth > 0) else 40
    
    weights = _health_score_weights(include_target)
    health_score = (
        ac_score * weights["ac"] +
        nsc_score * weights["nsc"] +
        target_score * weights["target"] +
        productivity_score * weights["productivity"] +
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
    
    target_pct = clean_number(row.get("Pct_Target", 0))
    target_score = min(target_pct, 100) if include_target else 50
    
    company_avg = df["AC_Per_Life"].mean() if df["AC_Per_Life"].mean() > 0 else 1
    productivity_score = min((row["AC_Per_Life"] / company_avg) * 100, 150) if company_avg > 0 else 50
    
    total_nbos = df.shape[0]
    rank_score = ((total_nbos - row["AC_Rank"]) / total_nbos * 100) if total_nbos > 0 else 50
    
    momentum_score = 80 if (ac_growth > 0 and nsc_growth > 0) else 60 if (ac_growth > 0 or nsc_growth > 0) else 40
    
    weights = _health_score_weights(include_target)
    health_score = (
        ac_score * weights["ac"] +
        nsc_score * weights["nsc"] +
        target_score * weights["target"] +
        productivity_score * weights["productivity"] +
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
            "Target Attainment": {"score": target_score, "weight": weights["target"], "value": target_pct, "display": target_display, "note": target_note},
            "Productivity": {"score": productivity_score, "weight": weights["productivity"], "value": row["AC_Per_Life"], "display": format_peso(row["AC_Per_Life"])},
            "Competitive Position": {"score": rank_score, "weight": weights["rank"], "value": row["AC_Rank"], "display": f"#{row['AC_Rank']}"},
            "Momentum": {"score": momentum_score, "weight": weights["momentum"], "value": "Positive" if ac_growth > 0 else "Negative", "display": "Positive" if ac_growth > 0 else "Negative"}
        }
    }

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

def calculate_forecast(row):
    ac = clean_number(row.get("AC", 0))
    has_target = has_target_data(row)
    target = clean_number(row.get("Target")) if has_target else 0

    if has_target and target == 0 and clean_number(row.get("Pct_Target", 0)) > 0:
        target = safe_divide(ac, clean_number(row.get("Pct_Target", 0)) / 100)

    if has_target and target > 0:
        pct = clean_number(row.get("Pct_Target", 0))
        target_attainment = pct if pct > 0 else safe_divide(ac, target) * 100
        is_mtd = str(row.get("Report_Type", "")).upper() == "MTD"
        annual_projection = ac * 12 if is_mtd else ac * 2
        if pct > 0:
            gap_to_target = max(target * (1 - pct / 100), 0)
        elif is_mtd:
            gap_to_target = max(target - ac, 0)
        else:
            gap_to_target = max(target - annual_projection, 0)
    else:
        target_attainment = 0
        annual_projection = ac * 12 if ac > 0 else 0  # MTD: rough annualized from monthly pace
        target = 0
        gap_to_target = 0

    return {
        "target": target,
        "has_target": has_target,
        "target_attainment": target_attainment,
        "gap_to_target": gap_to_target,
        "annual_projection": annual_projection,
        "current_ac": ac,
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
        pct_rank = 100 - (row['AC_Rank']/df.shape[0]*100) if df.shape[0] > 0 else 0
        st.metric("AC Rank", f"#{row['AC_Rank']} of {df.shape[0]}", delta=f"Top {pct_rank:.0f}% {labels['rank_context']}")
    with col6:
        if has_target_data(row):
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
                "Productivity": "speed",
                "Competitive Position": "emoji_events",
                "Momentum": "rocket"
            }
            icon_name = icon_map.get(name, "assessment")
            
            # Plain English explanation
            period_word = labels["period"]
            explanations = {
                "AC Growth": f"How much Life AC grew {labels['growth_context']} ({period_word})",
                "NSC Growth": f"How much new business commission grew {labels['growth_context']}",
                "Target Attainment": "How much of your annual sales target you have reached (YTD reports only)",
                "Productivity": "Life AC earned per client — higher means more revenue per life",
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
        <strong>Rank</strong> = position vs other NBO offices (#1 is best)
    </div>
    """, unsafe_allow_html=True)
    
    rank_pct = 100 - (row['AC_Rank']/df.shape[0]*100) if df.shape[0] > 0 else 0
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
            • <strong>Rank:</strong> #{row['AC_Rank']} of {df.shape[0]} NBOs — top {rank_pct:.0f}% {labels['rank_context']}
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

    if threats.get("gap_to_next", 0) > 0:
        status, icon, title = "stable", "rocket", f"One rank away: #{row['AC_Rank'] - 1}"
        content = f"""
        <strong>You can move up one spot with focused effort.</strong><br><br>
        • NBO ahead of you: <strong>{threats['next_nbo']}</strong> ({format_peso(threats['next_ac'])})<br>
        • You need: <strong>{format_peso(threats['gap_to_next'])}</strong> more Life AC ({threats['opportunity_percent']:.1f}% increase)<br><br>
        <strong>What to do:</strong> Target high-value cases and advisors closest to closing.
        """
        explanation = "Closing this gap moves CENTURION TREE up one rank in the leaderboard."
    else:
        status, icon, title = "strong", "emoji_events", "You hold the #1 rank"
        content = f"""
        <strong>No other NBO has higher Life AC {labels['rank_context']}.</strong><br><br>
        Protect your lead by maintaining advisor activity and client retention.
        """
        explanation = "Rank #1 means you lead the field for this reporting period."
    
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
    ahead = sum(1 for d in results if d >= 0)
    if ahead == 3:
        render_callout(
            "Strong month across the board",
            "Life AC, Life NSC, and Lives are all running above your YTD monthly pace. "
            "Document what is working and replicate it next month.",
            "success",
        )
    elif ahead >= 2:
        render_callout(
            "Mostly on track",
            f"{ahead} of 3 metrics are above your YTD monthly average. "
            "Review the lagging metric with your team this week.",
            "info",
        )
    elif ahead == 1:
        render_callout(
            "Mixed month — action needed",
            "Only one metric is above your YTD monthly pace. "
            "Prioritize pipeline reviews and high-value case closing to recover.",
            "warning",
        )
    else:
        render_callout(
            "Below pace on all metrics",
            f"This month's production is below your YTD monthly average on Life AC, NSC, and Lives. "
            f"Schedule an immediate review of advisor activity, pipeline, and conversion.",
            "danger",
        )

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
            render_callout(
                "Opportunity to move up",
                f"<strong>{threats['next_nbo']}</strong> is ahead of you with {format_peso(threats['next_ac'])} Life AC. "
                f"You have {format_peso(row['AC'])}. You need {format_peso(threats['gap_to_next'])} more "
                f"({threats['opportunity_percent']:.1f}% increase) to overtake them.",
                "info",
            )
        else:
            render_callout(
                "You hold the top spot",
                "No other NBO has higher Life AC than you. Focus on maintaining and extending your lead.",
                "success",
            )
    
    with col2:
        if threats["gap_to_prev"] > 0:
            threat_pct = safe_divide(threats["gap_to_prev"], row["AC"]) * 100
            if threat_pct < 5:
                render_callout(
                    "High threat — competitor very close",
                    f"<strong>{threats['prev_nbo']}</strong> is only {format_peso(threats['gap_to_prev'])} "
                    f"({threat_pct:.1f}%) behind you. Accelerate growth to protect your rank.",
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
                "No NBO is close behind you in the rankings. Focus on closing the gap to the next rank up.",
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
        scenarios = {"Worst Case": current_ac * 1.8, "Expected": current_ac * 2.2, "Best Case": current_ac * 2.5}
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
            "details": f"Competitor is only {format_peso(threats['gap_to_prev'])} behind. Increase productivity and accelerate growth to maintain your lead."
        })
    
    if threats.get("opportunity_value", 0) > 0:
        actions.append({
            "priority": "HIGH",
            "action": f"🎯 Overtake {threats['next_nbo']}",
            "details": f"Need +{threats['opportunity_percent']:.1f}% growth to pass {threats['next_nbo']}. Focus on competitive advantages and key opportunities."
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
            **Health Score** (0-100) — overall performance at a glance
            
            **YTD and MTD use the same PER NBO sheet layout.**  
            YTD files include columns N (Annual Life AC Target) and O (% to target).
            
            **Terms:**
            - **Life AC** — total life insurance commission
            - **Life NSC** — commission from new policies
            - **Lives** — number of clients
            - **Rank** — position vs other NBOs (#1 is best)
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
        - **Health Score** — one number summarizing performance
        - **Executive Briefing** — plain-English insights for leadership
        - **Threat Monitor** — who is ahead or behind you
        - **Action Center** — prioritized next steps
        """)
        return

    # Choose active view: MTD-only uses MTD; when both exist, let user pick
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

    # Calculate all metrics
    health_score = calculate_health_score(row, df, include_target=include_target)
    health_data = calculate_health_score_components(row, df, include_target=include_target)
    verdict = determine_verdict(health_score)
    threats = calculate_threat_metrics(row, df)
    forecast = calculate_forecast(row)
    leakage, recovery = calculate_revenue_leakage(row)

    # Render everything
    render_executive_overview(row, df, health_score, verdict, data_source)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    render_component_breakdown(health_data, data_source)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Create tabs with icons
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
    
    # MTD vs YTD comparison — when both files are loaded
    if ytd_ready and mtd_ready and centurion_ytd is not None and centurion_mtd is not None:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_mtd_comparison(centurion_ytd.iloc[0], centurion_mtd.iloc[0], ytd_df)

if __name__ == "__main__":
    main()