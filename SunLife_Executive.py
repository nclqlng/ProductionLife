
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sun Life Executive Command Center", page_icon="🌞", layout="wide")

SUN_GOLD="#FDB913"
SUN_DARK="#2D2D2D"
SUN_BG="#FAFAFA"

st.markdown(f"""
<style>
.stApp {{background:{SUN_BG};}}
[data-testid="metric-container"] {{
    border-left:5px solid {SUN_GOLD};
    border-radius:12px;
}}
</style>
""", unsafe_allow_html=True)

def clean_number(x):
    return pd.to_numeric(str(x).replace(",","").replace("%",""), errors="coerce")

@st.cache_data
def load_report(file, report_type):
    raw = pd.read_excel(file, sheet_name="PER NBO", header=None)
    rows=[]
    territory=None

    for r in raw.values.tolist():
        if len(r) < 17:
            continue

        name = r[1] if len(r) > 1 else None
        if pd.isna(name):
            continue

        name=str(name).strip()

        if "TERRITORY" in name.upper():
            territory=name
            continue

        lives=clean_number(r[3])
        if pd.isna(lives):
            continue

        rec={
            "Territory":territory,
            "NBO":name,
            "Lives":clean_number(r[3]),
            "AC":clean_number(r[4]),
            "NSC":clean_number(r[5]),
            "Lives_PY":clean_number(r[6]),
            "AC_PY":clean_number(r[7]),
            "NSC_PY":clean_number(r[8]),
            "SSP":clean_number(r[13]),
        }

        if report_type=="YTD":
            rec["Target"]=clean_number(r[15])
            rec["Pct_Target"]=clean_number(r[16])*100

        rows.append(rec)

    df=pd.DataFrame(rows)

    df["Lives Growth %"]=((df["Lives"]-df["Lives_PY"])/df["Lives_PY"]*100).replace([float("inf"),-float("inf")],0).fillna(0)
    df["AC Growth %"]=((df["AC"]-df["AC_PY"])/df["AC_PY"]*100).replace([float("inf"),-float("inf")],0).fillna(0)
    df["NSC Growth %"]=((df["NSC"]-df["NSC_PY"])/df["NSC_PY"]*100).replace([float("inf"),-float("inf")],0).fillna(0)

    df["AC Per Life"]=(df["AC"]/df["Lives"]).replace([float("inf"),-float("inf")],0).fillna(0)
    df["NSC Per Life"]=(df["NSC"]/df["Lives"]).replace([float("inf"),-float("inf")],0).fillna(0)

    df["AC Rank"]=df["AC"].rank(method="min", ascending=False)
    df["NSC Rank"]=df["NSC"].rank(method="min", ascending=False)
    df["Lives Rank"]=df["Lives"].rank(method="min", ascending=False)

    return df

st.title("🌞 Sun Life Executive Command Center")
report_type=st.sidebar.radio("Period",["YTD","MTD"])
uploaded=st.sidebar.file_uploader("Upload PER NBO", type=["xlsx"])

if uploaded:
    df=load_report(uploaded, report_type)

    centurion=df[df["NBO"].astype(str).str.upper().str.contains("CENTURION TREE", na=False)]

    if centurion.empty:
        st.error("CENTURION TREE not found")
        st.stop()

    c=centurion.iloc[0]
    ac_rank=int(c["AC Rank"])

    tabs=st.tabs([
        "📊 Executive Overview",
        "🎯 Target",
        "🏆 Competition",
        "📈 Analytics",
        "🚀 Insights"
    ])

    with tabs[0]:
        st.subheader("Executive Summary")

        summary=f"""
        CENTURION TREE generated ₱{c['AC']:,.0f} Life AC from {c['Lives']:,.0f} lives.
        AC growth is {c['AC Growth %']:.1f}% and NSC growth is {c['NSC Growth %']:.1f}%.
        Current AC rank is #{ac_rank}.
        """
        st.info(summary)

        cols=st.columns(6)
        cols[0].metric("Life AC",f"₱{c['AC']:,.0f}",f"{c['AC Growth %']:.1f}%")
        cols[1].metric("NSC",f"₱{c['NSC']:,.0f}",f"{c['NSC Growth %']:.1f}%")
        cols[2].metric("Lives",f"{c['Lives']:,.0f}",f"{c['Lives Growth %']:.1f}%")
        cols[3].metric("AC Rank",f"#{ac_rank}")
        cols[4].metric("AC/Life",f"₱{c['AC Per Life']:,.0f}")
        cols[5].metric("NSC/Life",f"₱{c['NSC Per Life']:,.0f}")

    with tabs[1]:
        if report_type=="YTD" and "Target" in c.index:
            remaining=max(c["Target"]-c["AC"],0)

            st.metric("Target Attainment",f"{c['Pct_Target']:.1f}%")
            st.metric("Remaining AC",f"₱{remaining:,.0f}")

            fig=go.Figure(go.Indicator(
                mode="gauge+number",
                value=float(c["Pct_Target"]),
                number={"suffix":"%"},
                title={"text":"Target Attainment"}
            ))
            st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.subheader("Top 20 AC Producers")
        st.dataframe(
            df.sort_values("AC",ascending=False)[["NBO","AC","NSC","Lives"]].head(20),
            use_container_width=True
        )

    with tabs[3]:
        fig=px.scatter(
            df,
            x="AC Growth %",
            y="AC",
            size="Lives",
            hover_name="NBO",
            title="Performance Quadrant"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[4]:
        insights=[]

        if c["Lives Growth %"] > 0 and c["AC Growth %"] < 0:
            insights.append("Lives increased but AC declined, indicating weaker conversion quality.")

        if c["AC Growth %"] > 0 and c["Lives Growth %"] > 0:
            insights.append("Healthy volume-to-value growth trend detected.")

        top3=df.nlargest(3,"AC")["AC"].mean()
        insights.append(f"Gap to Top 3 Average: ₱{max(top3-c['AC'],0):,.0f}")

        for i in insights:
            st.write("•", i)
