
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="CENTURION TREE Command Center",
    page_icon="🌳",
    layout="wide"
)

st.markdown("""
<style>
.block-container {padding-top: 1rem;}
[data-testid="metric-container"]{
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:12px;
}
</style>
""", unsafe_allow_html=True)

def clean_number(x):
    return pd.to_numeric(str(x).replace(",", "").replace("%", ""), errors="coerce")

@st.cache_data
def load_report(file, report_type):

    raw = pd.read_excel(file, sheet_name="PER NBO", header=None)

    data = []
    territory = None

    for r in raw.values.tolist():

        if len(r) < 17:
            continue

        name = r[1] if len(r) > 1 else None

        if pd.isna(name):
            continue

        name = str(name).strip()

        if not name:
            continue

        if "TERRITORY" in name.upper():
            territory = name
            continue

        if name.upper().startswith("METRO NORTH"):
            continue

        lives = clean_number(r[3])

        if pd.isna(lives):
            continue

        rec = {
            "Territory": territory,
            "NBO": name,
            "Lives": clean_number(r[3]),
            "AC": clean_number(r[4]),
            "NSC": clean_number(r[5]),
            "Lives_PY": clean_number(r[6]),
            "AC_PY": clean_number(r[7]),
            "NSC_PY": clean_number(r[8]),
            "SSP": clean_number(r[13])
        }

        if report_type == "YTD":
            rec["Target"] = clean_number(r[15])
            rec["Pct_Target"] = clean_number(r[16]) * 100

        data.append(rec)

    df = pd.DataFrame(data)

    df["Lives Growth %"] = (
        (df["Lives"] - df["Lives_PY"])
        / df["Lives_PY"] * 100
    ).replace([float("inf"), -float("inf")], 0).fillna(0)

    df["AC Growth %"] = (
        (df["AC"] - df["AC_PY"])
        / df["AC_PY"] * 100
    ).replace([float("inf"), -float("inf")], 0).fillna(0)

    df["NSC Growth %"] = (
        (df["NSC"] - df["NSC_PY"])
        / df["NSC_PY"] * 100
    ).replace([float("inf"), -float("inf")], 0).fillna(0)

    df = df.sort_values("AC", ascending=False).reset_index(drop=True)
    df["AC Rank"] = range(1, len(df) + 1)

    return df


st.title("🌳 CENTURION TREE Performance Command Center")

report_type = st.sidebar.selectbox(
    "Report Type",
    ["YTD", "MTD"]
)

uploaded = st.sidebar.file_uploader(
    "Upload Life Production Report",
    type=["xlsx"]
)

if uploaded:

    df = load_report(uploaded, report_type)

    centurion = df[
        df["NBO"].astype(str).str.upper().str.strip() == "CENTURION TREE"
    ]

    if centurion.empty:
        st.error("CENTURION TREE not found in report.")
        st.stop()

    selected = centurion.iloc[0]

    rank = int(selected["AC Rank"])

    percentile = (
        ((len(df) - rank) + 1)
        / len(df)
    ) * 100

    st.subheader("Executive Scorecard")

    c1,c2,c3,c4,c5,c6 = st.columns(6)

    c1.metric(
        "Life AC",
        f"₱{selected['AC']:,.0f}",
        f"{selected['AC Growth %']:.1f}%"
    )

    c2.metric(
        "Life NSC",
        f"₱{selected['NSC']:,.0f}",
        f"{selected['NSC Growth %']:.1f}%"
    )

    c3.metric(
        "Lives",
        f"{selected['Lives']:,.0f}",
        f"{selected['Lives Growth %']:.1f}%"
    )

    c4.metric(
        "SSP",
        f"₱{selected['SSP']:,.0f}"
    )

    c5.metric(
        "AC Rank",
        f"#{rank}"
    )

    c6.metric(
        "Top Percentile",
        f"{percentile:.0f}%"
    )

    score = 0

    if selected["AC Growth %"] >= 0:
        score += 30

    if selected["NSC Growth %"] >= 0:
        score += 20

    if report_type == "YTD" and selected.get("Pct_Target", 0) >= 50:
        score += 30

    score += 20

    st.metric("Performance Score", f"{score}/100")

    if rank > 1:
        above = df[df["AC Rank"] == rank - 1].iloc[0]
        gap = above["AC"] - selected["AC"]

        st.warning(
            f"Need ₱{gap:,.0f} additional Life AC to reach Rank #{rank-1}."
        )

    tabs = st.tabs([
        "📊 Overview",
        "🏆 Competitors",
        "🎯 Target",
        "🤖 Insights"
    ])

    with tabs[0]:

        growth_df = pd.DataFrame({
            "Metric": [
                "Lives",
                "Life AC",
                "Life NSC"
            ],
            "Growth %": [
                selected["Lives Growth %"],
                selected["AC Growth %"],
                selected["NSC Growth %"]
            ]
        })

        fig = px.bar(
            growth_df,
            x="Metric",
            y="Growth %",
            text="Growth %",
            title="Year-over-Year Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:

        competitors = df[
            (df["AC Rank"] >= max(1, rank-3))
            &
            (df["AC Rank"] <= rank+3)
        ][["AC Rank","NBO","AC"]]

        st.dataframe(
            competitors,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            competitors.sort_values("AC"),
            x="AC",
            y="NBO",
            orientation="h",
            title="Nearby Competitors by Life AC"
        )

        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:

        if report_type == "YTD" and "Target" in selected.index:

            remaining = max(
                selected["Target"] - selected["AC"],
                0
            )

            a,b,c = st.columns(3)

            a.metric(
                "Annual Target",
                f"₱{selected['Target']:,.0f}"
            )

            b.metric(
                "Current Life AC",
                f"₱{selected['AC']:,.0f}"
            )

            c.metric(
                "Remaining to Target",
                f"₱{remaining:,.0f}"
            )

            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=float(selected["Pct_Target"]),
                    number={"suffix":"%"},
                    title={"text":"Target Attainment"},
                    gauge={
                        "axis":{"range":[0,100]},
                        "steps":[
                            {"range":[0,50],"color":"#FEE2E2"},
                            {"range":[50,80],"color":"#FEF3C7"},
                            {"range":[80,100],"color":"#DCFCE7"}
                        ]
                    }
                )
            )

            st.plotly_chart(gauge, use_container_width=True)

    with tabs[3]:

        st.write(
            f"• CENTURION TREE ranks #{rank} out of {len(df)} NBOs."
        )

        st.write(
            f"• Submitted Lives: {selected['Lives']:,.0f} "
            f"({selected['Lives Growth %']:.1f}% vs PY)."
        )

        st.write(
            f"• Life AC: ₱{selected['AC']:,.0f} "
            f"({selected['AC Growth %']:.1f}% vs PY)."
        )

        st.write(
            f"• Life NSC: ₱{selected['NSC']:,.0f} "
            f"({selected['NSC Growth %']:.1f}% vs PY)."
        )

        st.write(
            f"• SSP: ₱{selected['SSP']:,.0f}."
        )

        if report_type == "YTD":

            remaining = max(
                selected["Target"] - selected["AC"],
                0
            )

            st.write(
                f"• Target Attainment: {selected['Pct_Target']:.1f}%."
            )

            st.write(
                f"• Remaining AC to Target: ₱{remaining:,.0f}."
            )

            if selected["AC Growth %"] < 0:
                st.warning("Life AC is below prior year performance.")

            if selected["NSC Growth %"] < 0:
                st.warning("Life NSC is below prior year performance.")
