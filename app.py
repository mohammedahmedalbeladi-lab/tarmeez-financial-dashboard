import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="ترميز المالية | Demand & Supply Planning",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CSS (Executive Dark + Arabic RTL + Better Spacing)
# =========================================================
st.markdown(
    """
<style>
:root{
  --bg0:#071A14;
  --card:#06110E;
  --border: rgba(52,211,153,0.22);
  --text:#F9FAFB;
  --muted:#CBD5E1;
  --accent:#34D399;

  --inputBg: rgba(5,10,22,0.78);
  --inputBd: rgba(255,255,255,0.16);
  --popBg:  #071A14;
  --popBd:  rgba(52,211,153,0.22);
}

/* =========================================================
   Base background
   ========================================================= */
html, body, [data-testid="stAppViewContainer"]{
  background: var(--bg0) !important;
}

/* Main background gradient */
[data-testid="stAppViewContainer"] > .main{
  background:
    radial-gradient(1200px 700px at 80% 30%, rgba(30,107,75,0.65), transparent 55%),
    radial-gradient(900px 650px at 30% 70%, rgba(8,30,24,0.85), transparent 60%),
    linear-gradient(120deg, #050A16 0%, var(--bg0) 35%, rgba(30,107,75,0.70) 100%) !important;
}

/* Container spacing */
.block-container{
  padding-top: 1.1rem !important;
  padding-bottom: 1.5rem !important;
  max-width: 1500px;
}

/* Header transparent */
[data-testid="stHeader"]{ background: transparent !important; }

/* =========================================================
   ✅ RTL Scope (لا تطبق RTL على كل شيء!)
   نخلي RTL على محتوى الصفحة + السايدبار، ونستثني الهيدر/التولبار/السهم
   ========================================================= */

/* =========================================================
   ✅ RTL صح: على الـ containers مو على كل عنصر *
   ========================================================= */

/* =========================
   RTL للمحتوى فقط (بدون قلب الواجهة كاملة)
   ========================= */
[data-testid="stAppViewContainer"] .main{
  direction: rtl !important;
}
[data-testid="stAppViewContainer"] .block-container{
  direction: rtl !important;
  text-align: right !important;
}
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] label{
  text-align: right !important;
}

/* استثناءات لازم تكون LTR */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="collapsedControl"]{
  direction: ltr !important;
}
[data-testid="collapsedControl"] *{
  direction: ltr !important;
}

/* Plotly LTR */
.js-plotly-plot,
.js-plotly-plot *{
  direction: ltr !important;
  text-align: left !important;
}


/* =========================
   السهم: يمين دائمًا
   ========================= */
[data-testid="collapsedControl"]{
  position: fixed !important;
  right: 12px !important;
  left: auto !important;
  top: 10px !important;
  z-index: 9999 !important;
}
[data-testid="collapsedControl"] svg{
  transform: none !important;
}
/* =========================================================
   Sidebar styling
   ========================================================= */
/* =========================
   Sidebar (LEFT ثابت + حدود صحيحة)
   ========================= */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, #050A16 0%, #06110E 100%) !important;

  /* Sidebar position: LEFT */
  left: 0 !important;
  right: auto !important;

  /* Border مناسب لكونه يسار */
  border-right: 1px solid rgba(255,255,255,0.06) !important;
  border-left: 0 !important;
}
/* إصلاح السايدبار عند الإغلاق */
section[data-testid="stSidebar"][aria-expanded="false"]{
  width: 0 !important;
  min-width: 0 !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] > div{
  display:none !important;
}
[data-testid="stAppViewContainer"] .main{
  margin: 0 !important;
}

/* Make text brighter */
h1, h2, h3, h4, p, li, label, span, div{
  color: var(--text) !important;
}
.stCaption{ color: var(--muted) !important; }
hr{ border-color: rgba(255,255,255,0.10) !important; }

/* KPI Card */
.kpi-card{
  background:
    radial-gradient(900px 520px at 85% 20%, rgba(52,211,153,0.18), transparent 48%),
    radial-gradient(900px 520px at 15% 80%, rgba(34,197,94,0.10), transparent 55%),
    linear-gradient(145deg, rgba(5,10,22,0.90) 0%, rgba(6,17,14,0.92) 60%, rgba(10,40,30,0.95) 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px;
  box-shadow: 0 10px 26px rgba(0,0,0,0.45);
  position: relative;
  overflow: hidden;

  height: 110px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;

  transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease, filter 160ms ease;
  will-change: transform;
  cursor: default;
}
.kpi-card:hover{
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 18px 46px rgba(0,0,0,0.60);
  border-color: rgba(52,211,153,0.55);
  filter: brightness(1.05);
}
.kpi-card:before{
  content:"";
  position:absolute;
  inset:0;
  border-radius:16px;
  padding:1px;
  background: linear-gradient(135deg,
    rgba(52,211,153,0.60),
    rgba(34,197,94,0.20),
    rgba(255,255,255,0.10)
  );
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events:none;
}
.kpi-label{
  color: rgba(249,250,251,0.92) !important;
  font-size: 0.92rem;
  line-height: 1.2;
  margin: 0;
}
.kpi-value{
  color:#FFFFFF !important;
  font-size: clamp(1.20rem, 1.55vw, 1.65rem);
  font-weight: 900;
  line-height: 1.05;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  direction: ltr !important;
  text-align: left !important;
}
.kpi-sub{
  margin: 0;
  font-size: 0.82rem;
  color: rgba(203,213,225,0.95) !important;
}

/* spacing */
div[data-testid="stHorizontalBlock"]{ gap: 1.10rem !important; }
div[data-testid="column"]{ padding-top: 0.35rem !important; padding-bottom: 0.35rem !important; }

/* Buttons */
.stButton>button{
  background: rgba(52,211,153,0.14) !important;
  border: 1px solid rgba(52,211,153,0.30) !important;
  color: var(--text) !important;
  border-radius: 999px !important;
}
.stButton>button:hover{
  background: rgba(52,211,153,0.22) !important;
}

/* Plotly container */
[data-testid="stPlotlyChart"]{
  background: rgba(0,0,0,0) !important;
  border-radius: 14px;
}

/* Tabs */
button[data-baseweb="tab"]{
  color: rgba(249,250,251,0.80) !important;
  font-weight: 700 !important;
}
button[data-baseweb="tab"][aria-selected="true"]{
  color: #FFFFFF !important;
}

/* =========================================================
    ✅ Inputs / Select / Date (التصميم التنفيذي المطور)
    ========================================================= */

/* 1. الصندوق الرئيسي - لمسة زجاجية مع ظل خفيف */
div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(52, 211, 153, 0.15) !important;
    border-radius: 12px !important;
    padding: 2px 8px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.05) !important;
}

/* تأثير عند التركيز أو المرور بالماوس */
div[data-baseweb="select"] > div:hover {
    border-color: var(--accent) !important;
    background-color: rgba(52, 211, 153, 0.05) !important;
}

/* 2. القائمة المنسدلة (التي تظهر بعد الضغط) */
div[data-baseweb="popover"] > div {
    background-color: #0c1e19 !important; /* لون داكن عميق ومنسجم */
    border: 1px solid rgba(52, 211, 153, 0.2) !important;
    border-radius: 14px !important;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important;
    padding: 8px !important;
    margin-top: 4px !important;
}

/* تنظيف القائمة من أي خلفيات إضافية */
div[data-baseweb="menu"] {
    background-color: transparent !important;
    border: none !important;
}

/* 3. العناصر داخل القائمة (Options) */
li[role="option"] {
    border-radius: 8px !important;
    margin-bottom: 3px !important;
    padding: 12px 16px !important;
    color: var(--text) !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    border: none !important; /* حذف الحدود الداخلية المزعجة */
}

/* تأثير التمرير - ناعم جداً */
li[role="option"]:hover {
    background-color: rgba(52, 211, 153, 0.12) !important;
    color: var(--accent) !important;
    padding-right: 20px !important; /* حركة بسيطة تعطي طابع مودرن */
}

/* العنصر المختار حالياً - يبرز بذكاء */
li[aria-selected="true"] {
    background-color: var(--accent) !important;
    color: #071A14 !important; /* نص داكن للوضوح */
    font-weight: 700 !important;
}

/* 4. التقويم (Date Input) */
[data-testid="stDateInput"] input {
    background: transparent !important;
    color: var(--text) !important;
    border: none !important;
}

div[data-baseweb="calendar"] {
    background-color: #0c1e19 !important;
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    padding: 10px !important;
}

/* إخفاء حدود خلايا التقويم لجعلها أنظف */
div[data-baseweb="calendar"] [role="gridcell"] {
    border: none !important;
}

/* يوم اليوم المختار في التقويم */
div[data-baseweb="calendar"] [aria-selected="true"] {
    background-color: var(--accent) !important;
    color: #071A14 !important;
    border-radius: 50% !important;
}

/* تحسين السهم الصغير وأيقونة الحذف */
div[data-baseweb="select"] svg {
    fill: var(--muted) !important;
}

/* =========================================================
   ✅ BaseWeb portals (القوائم/الكالندر تظهر غالباً خارج stAppViewContainer)
   عشان كذا نخاطبها مباشرة
   ========================================================= */

/* Dropdown/Popover panel (القائمة نفسها) */
div[data-baseweb="popover"] > div{
  background: var(--popBg) !important;
  border: 1px solid var(--popBd) !important;
}

/* Menu list */
div[data-baseweb="menu"]{
  background: var(--popBg) !important;
  border: 1px solid var(--popBd) !important;
}
div[data-baseweb="menu"] *{
  color: var(--text) !important;
}

/* Options hover/active */
div[data-baseweb="menu"] [role="option"]{
  background: transparent !important;
}
div[data-baseweb="menu"] [role="option"][aria-selected="true"],
div[data-baseweb="menu"] [role="option"]:hover{
  background: rgba(52,211,153,0.14) !important;
}

/* Calendar popup */
div[data-baseweb="calendar"]{
  background: var(--popBg) !important;
  border: 1px solid var(--popBd) !important;
}
div[data-baseweb="calendar"] *{
  color: var(--text) !important;
}

/* =========================================================
   ✅ File Uploader
   ========================================================= */
[data-testid="stFileUploaderDropzone"]{
  background: rgba(5,10,22,0.70) !important;
  border: 1px dashed rgba(52,211,153,0.38) !important;
  border-radius: 14px !important;
}
[data-testid="stFileUploaderDropzone"] *{
  color: var(--text) !important;
}
[data-testid="stFileUploaderDropzone"] small{
  color: rgba(203,213,225,0.90) !important;
}

/* زر Browse files */
[data-testid="stFileUploaderDropzone"] button{
  background: rgba(52,211,153,0.14) !important;
  border: 1px solid rgba(52,211,153,0.30) !important;
  color: var(--text) !important;
  border-radius: 999px !important;
}
[data-testid="stFileUploaderDropzone"] button:hover{
  background: rgba(52,211,153,0.22) !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# Plotly Theme (Transparent + Unified Colors)
# =========================================================
COLORS = {
    "green_light": "#34D399",
    "green_dark":  "#14532D",
    "cyan":        "#22D3EE",
    "orange":      "#FB923C",
    "red":         "#F87171",
    "purple":      "#A78BFA",
    "grid":        "rgba(255,255,255,0.08)",
    "gray":        "#6CA4A6",
    "graay":        "#516162",
    
}

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",  # ✅ خلفية الشارت الخارجية شفافة
    plot_bgcolor="rgba(0,0,0,0)",   # ✅ خلفية داخل الرسم شفافة
    font=dict(color="#E5E7EB"),
    margin=dict(l=10, r=10, t=60, b=10),
)

def apply_plotly_theme(
    fig,
    height=360,
    title=None,
    showlegend=True,
    hovermode="closest",
    spikes=False,              # ✅ جديد: تفعيل/إلغاء الخط العمودي
    spike_axis="x",            # x أو y
):
    fig.update_layout(**PLOTLY_LAYOUT, height=height, showlegend=showlegend)

    if title:
        fig.update_layout(
            title=dict(
                text=title,
                x=1.0,
                xanchor="right",
                font=dict(size=22, color="#FFFFFF")
            )
        )

    # Grid subtle
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"], zeroline=False)

    # ✅ Hover موحّد
    fig.update_layout(
        hovermode=hovermode,
        hoverdistance=12,
        hoverlabel=dict(
            bgcolor="rgba(2, 6, 23, 0.95)",
            bordercolor="rgba(52,211,153,0.45)",
            font=dict(color="#FFFFFF", size=14),
            align="left",
            namelength=-1
        )
    )

    # ✅ أهم جزء: تحكم في الـ spike line
    if spikes:
        if spike_axis == "x":
            fig.update_xaxes(
                showspikes=True,
                spikemode="across",
                spikedash="dot",
                spikecolor="rgba(255,255,255,0.65)",
                spikethickness=1
            )
            fig.update_layout(spikedistance=-1)
        else:
            fig.update_yaxes(
                showspikes=True,
                spikemode="across",
                spikedash="dot",
                spikecolor="rgba(255,255,255,0.65)",
                spikethickness=1
            )
            fig.update_layout(spikedistance=-1)
    else:
        # ✅ اقفله تمامًا
        fig.update_xaxes(showspikes=False)
        fig.update_yaxes(showspikes=False)
        fig.update_layout(spikedistance=0)

    # ✅ Legend
    fig.update_layout(
        legend=dict(
            bgcolor="rgba(2, 6, 23, 0.55)",
            bordercolor="rgba(255,255,255,0.14)",
            borderwidth=1,
            font=dict(size=13, color="#FFFFFF"),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

# =========================================================
# Helpers
# =========================================================
DEFAULT_CSV_NAME = "Demand Supply Planning.csv"  # <-- عدّلها لو اسم ملفك مختلف

AR_MONTHS = {
    1:"يناير",2:"فبراير",3:"مارس",4:"أبريل",5:"مايو",6:"يونيو",
    7:"يوليو",8:"أغسطس",9:"سبتمبر",10:"أكتوبر",11:"نوفمبر",12:"ديسمبر"
}

def _smart_to_number(x):
    """Robust numeric parsing for mixed formats:
       - '1,505' could be thousand or decimal (we treat as thousand if many digits)
       - '0,1' -> 0.1
       - '$12,345.67' -> 12345.67
    """
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    s = str(x).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return np.nan

    # remove currency and spaces
    s = s.replace("$", "").replace("€", "").replace("£", "").replace("SAR", "").replace("USD", "").strip()
    s = s.replace(" ", "")

    # If both comma and dot exist -> likely comma thousands
    if "," in s and "." in s:
        s = s.replace(",", "")
        return pd.to_numeric(s, errors="coerce")

    # Only comma exists
    if "," in s and "." not in s:
        # If it's like '0,1' or '21,923' (could be decimal comma)
        # Heuristic: if comma appears once AND digits after comma <= 3 -> treat as decimal comma
        parts = s.split(",")
        if len(parts) == 2 and len(parts[1]) <= 3:
            s2 = parts[0] + "." + parts[1]
            return pd.to_numeric(s2, errors="coerce")
        # Otherwise treat as thousands separators (remove all commas)
        s = s.replace(",", "")
        return pd.to_numeric(s, errors="coerce")

    # Only dot or plain
    return pd.to_numeric(s, errors="coerce")


def fmt_money(x):
    if pd.isna(x):
        return "—"
    return f"${x:,.0f}" if abs(x) >= 100 else f"${x:,.2f}"

def fmt_pct(x, digits=2):
    if pd.isna(x):
        return "—"
    return f"{x:.{digits}f}%"

def fmt_num(x, digits=2):
    if pd.isna(x):
        return "—"
    return f"{x:,.{digits}f}"

def to_month_label(dt: pd.Timestamp) -> str:
    return f"{AR_MONTHS.get(dt.month, str(dt.month))} {dt.year}"

@st.cache_data(show_spinner=False)
def load_dsp_csv(path_or_buffer) -> pd.DataFrame:
    df = pd.read_csv(path_or_buffer)
    df.columns = [c.strip() for c in df.columns]

    # Required minimal columns (حسب الداتا اللي عرضتها)
    required = {
        "Month", "SKU_ID", "Product_Group",
        "Forecast_units", "Actual_Demand_units",
        "Unit_Cost_USD", "Inventory_Value_USD",
        "OnHand_Inventory_units",
        "Fill_Rate_pct", "Stockout_Flag",
        "Produced_InHouse"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"أعمدة ناقصة في الملف: {missing}")

    # Parse Month
    df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
    df = df.dropna(subset=["Month"]).copy()

    # Numeric columns
    num_cols = [
        "Forecast_units","Actual_Demand_units","Unit_Cost_USD","Inventory_Value_USD",
        "OnHand_Inventory_units","Fill_Rate_pct","Safety_Stock_units","Reorder_Point_units",
        "Planned_Receipts_units","Replenishment_Order_units","Production_Plan_units",
        "MOQ_units","Days_of_Inventory","Holding_Cost_USD_monthly",
        "Revenue_per_unit_USD","Monthly_Revenue_USD",
        "Supplier_LeadTime_days","Transit_days","Total_LeadTime_days",
        "Days_to_Expiry","Capacity_Utilization_pct","Expiry_Value_USD",
        "Absolute_Error_units","APE"
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = df[c].apply(_smart_to_number)

    # Normalize flags
    # Stockout_Flag might be 0/1 or TRUE/FALSE
    if df["Stockout_Flag"].dtype == object:
        df["Stockout_Flag"] = df["Stockout_Flag"].astype(str).str.upper().map(
            {"TRUE": 1, "FALSE": 0, "1": 1, "0": 0}
        ).fillna(0).astype(int)
    else:
        df["Stockout_Flag"] = df["Stockout_Flag"].fillna(0).astype(int)

    if df["Produced_InHouse"].dtype == object:
        df["Produced_InHouse"] = df["Produced_InHouse"].astype(str).str.upper().map(
            {"TRUE": "إنتاج داخلي", "FALSE": "مشتريات", "1": "إنتاج داخلي", "0": "مشتريات"}
        ).fillna("غير محدد")
    else:
        df["Produced_InHouse"] = df["Produced_InHouse"].fillna(0).map(
            {1: "إنتاج داخلي", 0: "مشتريات"}
        ).fillna("غير محدد")

    # Clean some text cols
    df["Product_Group"] = df["Product_Group"].astype(str).str.strip()
    df["SKU_ID"] = df["SKU_ID"].astype(str).str.strip()
    if "Forecast_Method" in df.columns:
        df["Forecast_Method"] = df["Forecast_Method"].astype(str).str.strip()
    else:
        df["Forecast_Method"] = "غير محدد"

    # Add Month label (Arabic)
    df["Month_Label"] = df["Month"].apply(to_month_label)

    # If Monthly_Revenue_USD missing -> estimate = Actual * Revenue_per_unit if exists
    if "Monthly_Revenue_USD" not in df.columns or df["Monthly_Revenue_USD"].isna().all():
        if "Revenue_per_unit_USD" in df.columns:
            df["Monthly_Revenue_USD"] = df["Actual_Demand_units"] * df["Revenue_per_unit_USD"]
        else:
            df["Monthly_Revenue_USD"] = np.nan

    # Estimated COGS = Actual * Unit_Cost
    df["Estimated_COGS_USD"] = df["Actual_Demand_units"] * df["Unit_Cost_USD"]

    # Forecast error (if not present)
    if "Absolute_Error_units" not in df.columns:
        df["Absolute_Error_units"] = (df["Forecast_units"] - df["Actual_Demand_units"]).abs()

    # APE (avoid div0)
    if "APE" not in df.columns:
        denom = df["Actual_Demand_units"].replace(0, np.nan)
        df["APE"] = (df["Absolute_Error_units"] / denom)

    # Bias (signed)
    df["Error_units"] = df["Forecast_units"] - df["Actual_Demand_units"]

    return df.sort_values("Month").reset_index(drop=True)


def weighted_mape(df: pd.DataFrame) -> float:
    # Weighted by Actual volume
    a = df["Actual_Demand_units"].replace(0, np.nan)
    ae = (df["Forecast_units"] - df["Actual_Demand_units"]).abs()
    w = df["Actual_Demand_units"].fillna(0)
    denom = w.sum()
    if denom == 0:
        return np.nan
    return ( (ae.fillna(0) * w).sum() / denom ) * 100

def bias_ratio(df: pd.DataFrame) -> float:
    # Bias as weighted mean error / weighted mean actual
    w = df["Actual_Demand_units"].fillna(0)
    denom = w.sum()
    if denom == 0:
        return np.nan
    return ( (df["Error_units"].fillna(0) * w).sum() / denom )

def weighted_fill_rate(df: pd.DataFrame) -> float:
    # If Fill_Rate_pct exists -> weight by actual
    if "Fill_Rate_pct" not in df.columns:
        return np.nan
    w = df["Actual_Demand_units"].fillna(0)
    denom = w.sum()
    if denom == 0:
        return np.nan
    return ( (df["Fill_Rate_pct"].fillna(0) * w).sum() / denom )

def stockout_rate(df: pd.DataFrame) -> float:
    if len(df) == 0:
        return np.nan
    return (df["Stockout_Flag"].fillna(0).astype(int).mean()) * 100

def value_weighted_doi(df: pd.DataFrame) -> float:
    # Weight by inventory value (working capital)
    if "Days_of_Inventory" not in df.columns:
        return np.nan
    w = df["Inventory_Value_USD"].fillna(0)
    denom = w.sum()
    if denom == 0:
        return np.nan
    return ( (df["Days_of_Inventory"].fillna(0) * w).sum() / denom )

def inventory_turnover(df: pd.DataFrame) -> float:
    # Turnover ~ COGS / Avg Inventory Value
    cogs = df["Estimated_COGS_USD"].sum(skipna=True)
    inv = df["Inventory_Value_USD"].mean(skipna=True)
    if pd.isna(inv) or inv == 0:
        return np.nan
    return cogs / inv

def revenue_at_risk(df: pd.DataFrame) -> float:
    # Approx: sum revenue of stockout rows
    if "Monthly_Revenue_USD" not in df.columns:
        return np.nan
    return df.loc[df["Stockout_Flag"] == 1, "Monthly_Revenue_USD"].sum(skipna=True)

def slobs(df: pd.DataFrame) -> tuple[float, float]:
    # SLOB_Flag if exists
    if "SLOB_Flag" not in df.columns:
        return (np.nan, np.nan)
    sflag = df["SLOB_Flag"]
    if sflag.dtype == object:
        sflag = sflag.astype(str).str.upper().map({"TRUE":1,"FALSE":0,"1":1,"0":0}).fillna(0).astype(int)
    else:
        sflag = sflag.fillna(0).astype(int)
    total_inv = df["Inventory_Value_USD"].sum(skipna=True)
    slob_val = df.loc[sflag==1, "Inventory_Value_USD"].sum(skipna=True)
    slob_pct = (slob_val / total_inv * 100) if total_inv and not pd.isna(total_inv) else np.nan
    return slob_val, slob_pct

def expiry_risk_value(df: pd.DataFrame, days_threshold=30) -> float:
    """
    Expiry risk value within a threshold (<= X days).
    - Prefer Expiry_Value_USD if it exists AND has meaningful values.
    - If Expiry_Value_USD is all zeros/NaN -> fallback to Inventory_Value_USD.
    """
    if "Days_to_Expiry" not in df.columns:
        return np.nan

    m = df["Days_to_Expiry"].apply(_smart_to_number)

    # Decide which value column to use
    use_expiry_col = False
    if "Expiry_Value_USD" in df.columns:
        s = df["Expiry_Value_USD"].replace([np.inf, -np.inf], np.nan)

        # Meaningful if:
        # 1) has at least one non-null
        # 2) and sum (or max) > 0
        if s.notna().any() and (s.fillna(0).sum() > 0 or s.fillna(0).max() > 0):
            use_expiry_col = True

    val_col = "Expiry_Value_USD" if use_expiry_col else "Inventory_Value_USD"
    if val_col not in df.columns:
        return np.nan

    return df.loc[m <= days_threshold, val_col].sum(skipna=True)

def forecast_variance_cost(df: pd.DataFrame) -> dict:
    """
    Financial impact of forecast error:
    - Total variance cost = sum(|Forecast-Actual| * Unit_Cost)
    - Over-forecast cost  = sum(max(Forecast-Actual,0) * Unit_Cost)
    - Under-forecast cost = sum(max(Actual-Forecast,0) * Unit_Cost)
    """
    if "Forecast_units" not in df.columns or "Actual_Demand_units" not in df.columns or "Unit_Cost_USD" not in df.columns:
        return {"total": np.nan, "over": np.nan, "under": np.nan}

    err = (df["Forecast_units"] - df["Actual_Demand_units"]).fillna(0)
    unit_cost = df["Unit_Cost_USD"].fillna(0)

    over_units = err.clip(lower=0)
    under_units = (-err).clip(lower=0)

    over_cost = (over_units * unit_cost).sum()
    under_cost = (under_units * unit_cost).sum()
    total_cost = (err.abs() * unit_cost).sum()

    return {"total": total_cost, "over": over_cost, "under": under_cost}


def lead_time_variability(df: pd.DataFrame) -> dict:
    """
    Supplier reliability proxy using Total_LeadTime_days:
    - avg, std, coefficient of variation (CoV = std/avg)
    """
    col = "Total_LeadTime_days"
    if col not in df.columns:
        return {"avg": np.nan, "std": np.nan, "cov": np.nan}

    s = df[col].replace([np.inf, -np.inf], np.nan).dropna()
    if len(s) < 2:
        return {"avg": np.nan if len(s) == 0 else float(s.mean()), "std": np.nan, "cov": np.nan}

    avg = float(s.mean())
    std = float(s.std(ddof=1))
    cov = (std / avg * 100) if avg != 0 else np.nan  # % CoV
    return {"avg": avg, "std": std, "cov": cov}


def parse_date_col(df: pd.DataFrame, col: str):
    if col not in df.columns:
        return None
    return pd.to_datetime(df[col], errors="coerce")


def late_receipt_cost(df: pd.DataFrame) -> dict:
    """
    Late receipt analysis (ONLY if you have these columns):
    - Planned_Receipt_Date
    - Actual_Receipt_Date
    Optionally uses Stockout_Flag + Monthly_Revenue_USD to estimate impact on late rows.
    """
    planned_col = "Planned_Receipt_Date"
    actual_col = "Actual_Receipt_Date"

    if planned_col not in df.columns or actual_col not in df.columns:
        return {"late_days_avg": np.nan, "late_rows_pct": np.nan, "late_stockout_rev": np.nan}

    planned = parse_date_col(df, planned_col)
    actual = parse_date_col(df, actual_col)
    if planned is None or actual is None:
        return {"late_days_avg": np.nan, "late_rows_pct": np.nan, "late_stockout_rev": np.nan}

    delay_days = (actual - planned).dt.days
    late_mask = delay_days > 0

    late_rows_pct = late_mask.mean() * 100 if len(df) else np.nan
    late_days_avg = delay_days[late_mask].mean() if late_mask.any() else 0

    # revenue-at-risk on late rows that ALSO have stockout
    late_stockout_rev = np.nan
    if "Stockout_Flag" in df.columns and "Monthly_Revenue_USD" in df.columns:
        late_stockout_rev = df.loc[late_mask & (df["Stockout_Flag"] == 1), "Monthly_Revenue_USD"].sum(skipna=True)

    return {"late_days_avg": late_days_avg, "late_rows_pct": late_rows_pct, "late_stockout_rev": late_stockout_rev}


# =========================================================
# Header
# =========================================================
app_dir = Path(__file__).resolve().parent
logo_path = app_dir / "logo.png"

h1, h2 = st.columns([1, 10], vertical_alignment="center")
with h1:
    if logo_path.exists():
        st.image(str(logo_path), width=62)
    else:
        st.write("")

with h2:
    st.markdown(
        """
        <div style="line-height:1.15; text-align:right;">
          <div style="font-size:34px; font-weight:900; color:#E5E7EB;">ترميز المالية</div>
          <div style="margin-top:6px; color:#94A3B8; font-size:14px;">
            لوحة تخطيط الطلب والإمداد — مؤشرات تنفيذية + دقة التنبؤ + صحة المخزون + مخاطر الإيراد
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# =========================================================
# Data Loading
# =========================================================
default_csv = app_dir / DEFAULT_CSV_NAME

with st.sidebar:
    st.success("✅ البيئة جاهزة")
    st.caption("تصميم تنفيذي (Executive)")

    st.markdown("---")
    use_upload = st.toggle("استخدم رفع ملف بدل الملف المحلي", value=False)

    uploaded_file = None
    data_source_label = ""
    if use_upload:
        uploaded_file = st.file_uploader("ارفع ملف البيانات (CSV)", type=["csv"])
        data_source_label = "ملف مرفوع"
    else:
        if default_csv.exists():
            data_source_label = f"ملف محلي: {DEFAULT_CSV_NAME}"
        else:
            st.warning(f"ما لقيت الملف المحلي: {DEFAULT_CSV_NAME} — فعّل الرفع.")
            data_source_label = "لا يوجد ملف محلي"

try:
    if use_upload:
        if uploaded_file is None:
            st.warning("ارفع الملف من الشريط الجانبي عشان نبدأ.")
            st.stop()
        df = load_dsp_csv(uploaded_file)
    else:
        if not default_csv.exists():
            st.error("الملف المحلي غير موجود داخل نفس مجلد app.py. حطه بالمجلد أو فعّل الرفع.")
            st.stop()
        df = load_dsp_csv(default_csv)
except Exception as e:
    st.error(f"خطأ في قراءة البيانات: {e}")
    st.stop()

# =========================================================
# Filters
# =========================================================
with st.sidebar:
    st.markdown("---")
    st.subheader("الفلاتر")

    # Date range
    min_m = df["Month"].min()
    max_m = df["Month"].max()
    date_range = st.date_input(
        "النطاق الزمني (شهري)",
        value=(min_m.date(), max_m.date()),
        min_value=min_m.date(),
        max_value=max_m.date()
    )

    product_groups = ["الكل"] + sorted(df["Product_Group"].dropna().unique().tolist())
    sku_list = ["الكل"] + sorted(df["SKU_ID"].dropna().unique().tolist())
    fm_list = ["الكل"] + sorted(df["Forecast_Method"].dropna().unique().tolist())
    prod_type_list = ["الكل"] + sorted(df["Produced_InHouse"].dropna().unique().tolist())

    pg = st.selectbox("مجموعة المنتجات", product_groups, index=0)
    sku = st.selectbox("SKU", sku_list, index=0)
    fm = st.selectbox("طريقة التنبؤ", fm_list, index=0)
    prod_type = st.selectbox("نوع التوريد/الإنتاج", prod_type_list, index=0)

    show_table = st.toggle("عرض جدول البيانات", value=False)

# Apply filters
filtered = df.copy()
start_d = pd.to_datetime(date_range[0])
end_d = pd.to_datetime(date_range[1])
filtered = filtered[(filtered["Month"] >= start_d) & (filtered["Month"] <= end_d)].copy()

if pg != "الكل":
    filtered = filtered[filtered["Product_Group"] == pg].copy()
if sku != "الكل":
    filtered = filtered[filtered["SKU_ID"] == sku].copy()
if fm != "الكل":
    filtered = filtered[filtered["Forecast_Method"] == fm].copy()
if prod_type != "الكل":
    filtered = filtered[filtered["Produced_InHouse"] == prod_type].copy()

filtered = filtered.reset_index(drop=True)

if len(filtered) == 0:
    st.warning("ما فيه بيانات بعد الفلاتر الحالية. وسّع النطاق أو غيّر الاختيارات.")
    st.stop()



# =========================================================
# KPI Card helper
# =========================================================
def kpi_card(label: str, value: str, sub: str = ""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Tabs (Arabic)
# =========================================================
tabs = st.tabs([
    "نظرة عامة",
    "التنبؤ",
    "الخدمة",
    "المخزون",
    "المشتريات",
    "الإنتاج",
    "الجودة",
    "الإيراد"
])

# =========================================================
# Common aggregations (Monthly)
# =========================================================
monthly = (
    filtered.groupby("Month", as_index=False)
    .agg(
        Forecast_units=("Forecast_units", "sum"),
        Actual_Demand_units=("Actual_Demand_units", "sum"),
        Inventory_Value_USD=("Inventory_Value_USD", "sum"),
        Stockouts=("Stockout_Flag", "sum"),
        Monthly_Revenue_USD=("Monthly_Revenue_USD", "sum"),
        Estimated_COGS_USD=("Estimated_COGS_USD", "sum"),
    )
    .sort_values("Month")
)
monthly["Month_Label"] = monthly["Month"].apply(to_month_label)


# =========================================================
# Extra Monthly: Forecast Variance Cost (Over vs Under)
# =========================================================
tmp_cost = filtered.copy()
tmp_cost["Error_units"] = (tmp_cost["Forecast_units"] - tmp_cost["Actual_Demand_units"]).fillna(0)

tmp_cost["Over_Cost_USD"]  = tmp_cost["Error_units"].clip(lower=0) * tmp_cost["Unit_Cost_USD"].fillna(0)
tmp_cost["Under_Cost_USD"] = (-tmp_cost["Error_units"]).clip(lower=0) * tmp_cost["Unit_Cost_USD"].fillna(0)
tmp_cost["Total_Variance_Cost_USD"] = tmp_cost["Over_Cost_USD"] + tmp_cost["Under_Cost_USD"]

monthly_cost = (
    tmp_cost.groupby("Month", as_index=False)
    .agg(
        Over_Cost_USD=("Over_Cost_USD", "sum"),
        Under_Cost_USD=("Under_Cost_USD", "sum"),
        Total_Variance_Cost_USD=("Total_Variance_Cost_USD", "sum"),
    )
    .sort_values("Month")
)
monthly_cost["Month_Label"] = monthly_cost["Month"].apply(to_month_label)


# =========================================================
# TAB 1: Overview
# =========================================================
with tabs[0]:
    st.markdown("##  مؤشرات تنفيذية (نظرة عامة)")
    st.caption(f"المصدر: **{data_source_label}** | عدد الصفوف بعد الفلاتر: **{len(filtered):,}**")

    total_inv = filtered["Inventory_Value_USD"].sum(skipna=True)
    total_rev = filtered["Monthly_Revenue_USD"].sum(skipna=True)
    so_rate = stockout_rate(filtered)
    wfill = weighted_fill_rate(filtered)
    wmape = weighted_mape(filtered)
    b = bias_ratio(filtered)
    doi_vw = value_weighted_doi(filtered)
    rev_risk = revenue_at_risk(filtered)
    slob_val, slob_pct = slobs(filtered)
    hold_cost = filtered["Holding_Cost_USD_monthly"].sum(skipna=True) if "Holding_Cost_USD_monthly" in filtered.columns else np.nan
    exp30 = expiry_risk_value(filtered, 30)

    # KPI grid (3 rows like executive)
    r1 = st.columns(4, gap="small")
    with r1[0]: kpi_card("إجمالي قيمة المخزون", fmt_money(total_inv))
    with r1[1]: kpi_card("إجمالي الإيراد (الفترة)", fmt_money(total_rev))
    with r1[2]: kpi_card("معدل نفاد المخزون", fmt_pct(so_rate))
    with r1[3]: kpi_card("معدل الخدمة (مرجّح)", fmt_pct(wfill), "مرجّح بحجم الطلب الفعلي")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    r2 = st.columns(4, gap="small")
    with r2[0]: kpi_card("دقة التنبؤ (W-MAPE)", fmt_pct(wmape), "هدف شائع: أقل من 15%")
    with r2[1]:
        bias_txt = "—" if pd.isna(b) else f"{b:.2f}"
        kpi_card("انحياز التنبؤ (Bias)", bias_txt, "موجب=نقص تقدير | سالب=مبالغة")
    with r2[2]: kpi_card("أيام تغطية المخزون (مرجّحة بالقيمة)", fmt_num(doi_vw, 1), "توازن بين خدمة وتكلفة")
    with r2[3]: kpi_card("الإيراد المعرّض للخطر", fmt_money(rev_risk), "إيراد داخل صفوف فيها Stockout")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    r3 = st.columns(4, gap="small")
    with r3[0]: kpi_card("قيمة SLOB", fmt_money(slob_val), "مخزون بطيء/منتهي")
    with r3[1]: kpi_card("نسبة SLOB من المخزون", fmt_pct(slob_pct), "هدف شائع: < 1%")
    with r3[2]: kpi_card("تكلفة التخزين (شهريًا)", fmt_money(hold_cost))
    with r3[3]: kpi_card("قيمة منتهية ≤ 30 يوم", fmt_money(exp30), "مخاطر صلاحية قريبة")

    st.markdown("---")
    st.markdown("### التنبؤ مقابل الفعلي (شهريًا)")
    

    c1, c2 = st.columns([7, 5])

    # 1) Forecast vs Actual (Area) — FIXED (no duplicate forecast)
    fig1 = go.Figure()

    # Forecast
    fig1.add_trace(go.Scatter(
        x=monthly["Month_Label"],
        y=monthly["Forecast_units"],
        mode="lines",
        name="التنبؤ",
        line=dict(color=COLORS["cyan"], width=3),
        fill="tozeroy",
        fillcolor="rgba(34,211,238,0.18)",
        hovertemplate="<b>%{x}</b><br>التنبؤ: %{y:,.0f} وحدة<extra></extra>",
    ))

    # Actual
    fig1.add_trace(go.Scatter(
        x=monthly["Month_Label"],
        y=monthly["Actual_Demand_units"],
        mode="lines",
        name="الفعلي",
        line=dict(color=COLORS["green_light"], width=3),
        fill="tozeroy",
        fillcolor="rgba(52,211,153,0.18)",
        hovertemplate="<b>%{x}</b><br>الفعلي: %{y:,.0f} وحدة<extra></extra>",
    ))

    apply_plotly_theme(
        fig1,
        height=360,
        showlegend=True,
        hovermode="x unified",
        spikes=True
    )

    fig1.update_xaxes(title="الشهر")
    fig1.update_yaxes(title="الوحدات")
    fig1.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig1, use_container_width=True, key="ov_forecast_vs_actual")


    # 2) Inventory Value (Bar)
    
    st.markdown("---")
    st.markdown("### قيمة المخزون (شهريًا)")
    with c2:
            fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=monthly["Month_Label"], y=monthly["Inventory_Value_USD"],
        name="قيمة المخزون",
        marker_color=COLORS["green_light"]
    ))

    apply_plotly_theme(fig2, height=360, showlegend=False)
    fig2.update_xaxes(title="الشهر")
    fig2.update_yaxes(title="USD")

    st.plotly_chart(fig2, use_container_width=True, key="ov_inventory_value")


    # 3) Stockouts (Bar)
        
    st.markdown("---")
    st.markdown("### حالات نفاد المخزون")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=monthly["Month_Label"], y=monthly["Stockouts"],
        name="حالات نفاد المخزون",
        marker_color=COLORS["green_light"]
    ))

    apply_plotly_theme(fig3, height=330,  showlegend=False)
    fig3.update_xaxes(title="الشهر")
    fig3.update_yaxes(title="عدد الحالات")

    st.plotly_chart(fig3, use_container_width=True, key="ov_stockouts")


    # 4) Revenue vs COGS (Subplots)
    st.markdown("###  الإيراد و COGS (شهريًا)")

    fig_rev = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.10,
        row_heights=[0.55, 0.45]
    )

    fig_rev.add_trace(
        go.Scatter(
            x=monthly["Month_Label"],
            y=monthly["Monthly_Revenue_USD"],
            mode="lines+markers",
            name="الإيراد",
            line=dict(color=COLORS["cyan"], width=3),
            marker=dict(size=7, color=COLORS["cyan"])
        ),
        row=1, col=1
    )

    fig_rev.add_trace(
        go.Bar(
            x=monthly["Month_Label"],
            y=monthly["Estimated_COGS_USD"],
            name="COGS (تقديري)",
            marker_color=COLORS["green_light"]
        ),
        row=2, col=1
    )

    apply_plotly_theme(fig_rev, height=520, showlegend=False)
    fig_rev.update_yaxes(title_text="USD", row=1, col=1, gridcolor=COLORS["grid"])
    fig_rev.update_yaxes(title_text="USD", row=2, col=1, gridcolor=COLORS["grid"])
    fig_rev.update_xaxes(title_text="الشهر", row=2, col=1, showgrid=False)

    st.plotly_chart(fig_rev, use_container_width=True, key="rev_cogs_overview")

    st.caption(" يساعدك تربط التخطيط بالأثر المالي: هل ارتفاع COGS/هبوط الإيراد مرتبط بنفاد أو سوء تنبؤ؟")


# =========================================================
# TAB 2: Forecasting
# =========================================================
with tabs[1]:
    st.markdown("##  التنبؤ (Forecasting)")

    # KPIs الأساسية
    wmape_val = weighted_mape(filtered)
    bias_val = bias_ratio(filtered)

    r = st.columns(4, gap="small")
    with r[0]: kpi_card("W-MAPE (مرجّح)", fmt_pct(wmape_val), "أقل = أفضل")
    with r[1]:
        bias_txt = "—" if pd.isna(bias_val) else f"{bias_val:.2f}"
        kpi_card("Bias (انحياز)", bias_txt, "قريب من 0 = ممتاز")
    with r[2]:
        mae = filtered["Absolute_Error_units"].mean(skipna=True) if "Absolute_Error_units" in filtered.columns else np.nan
        kpi_card("متوسط الخطأ المطلق (MAE)", fmt_num(mae, 1))
    with r[3]:
        mape = filtered["APE"].replace([np.inf, -np.inf], np.nan).mean(skipna=True) * 100
        kpi_card("MAPE (غير مرجّح)", fmt_pct(mape))

    # KPI الأثر المالي (Forecast Variance Cost)
    var_cost = forecast_variance_cost(filtered)

    st.markdown("---")
    st.markdown("###  الأثر المالي لخطأ التنبؤ (Forecast Variance Cost)")

    r_fin = st.columns(3, gap="small")
    with r_fin[0]:
        kpi_card("إجمالي تكلفة الانحراف (تقريبي)", fmt_money(var_cost["total"]), "Σ |Forecast-Actual| × Unit Cost")
    with r_fin[1]:
        kpi_card("تكلفة Over-Forecast", fmt_money(var_cost["over"]), "مخزون زائد/كاش مجمّد")
    with r_fin[2]:
        kpi_card("تكلفة Under-Forecast", fmt_money(var_cost["under"]), "نقص توريد/مبيعات ضائعة")

    # شارت شهري (Under vs Over) — استخدم monthly_cost الجاهز عندك فوق
    st.markdown("---")
    st.markdown("###  تكلفة انحراف التنبؤ شهريًا (Under vs Over)")

    fig_cost = go.Figure()
    fig_cost.add_trace(go.Bar(
        x=monthly_cost["Month_Label"],
        y=monthly_cost["Under_Cost_USD"],
        name="نقص التنبؤ",
        marker_color=COLORS["green_light"]
    ))
    fig_cost.add_trace(go.Bar(
        x=monthly_cost["Month_Label"],
        y=monthly_cost["Over_Cost_USD"],
        name=" زيادة التنبؤ",
        marker_color=COLORS["green_dark"]
    ))

    apply_plotly_theme(fig_cost, height=380,  showlegend=True, hovermode="closest")
    fig_cost.update_layout(barmode="stack")
    fig_cost.update_xaxes(title="الشهر")
    fig_cost.update_yaxes(title="USD")
    fig_cost.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig_cost.update_traces(
    hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:,.0f} USD<extra></extra>"
)
    st.plotly_chart(fig_cost, use_container_width=True, key="forecast_variance_cost_stack")

    st.markdown("---")
    st.markdown("###  توزيع الخطأ حسب مجموعة المنتجات")

    if filtered["Product_Group"].nunique() > 1:
        g = (
            filtered.groupby("Product_Group", as_index=False)
            .agg(AE=("Absolute_Error_units", "sum"))
            .sort_values("AE", ascending=False)
        )

        fig_pg = go.Figure()
        fig_pg.add_trace(go.Bar(
            x=g["Product_Group"],
            y=g["AE"],
            name="مجموع الخطأ المطلق",
            marker_color=COLORS["green_light"],
        ))

        apply_plotly_theme(fig_pg, height=380,  showlegend=False)
        fig_pg.update_xaxes(title="مجموعة المنتجات")
        fig_pg.update_yaxes(title="وحدات")

        st.plotly_chart(fig_pg, use_container_width=True, key="forecast_error_by_pg")
    else:
        st.info("الفلاتر الحالية فيها مجموعة منتجات واحدة فقط.")

    # أعلى 10 SKUs تسبب تكلفة انحراف التنبؤ
    st.markdown("---")
    st.markdown("###  أعلى 10 SKU تسبب تكلفة انحراف التنبؤ")

    tmp2 = filtered.copy()
    tmp2["Var_Cost_USD"] = (tmp2["Forecast_units"] - tmp2["Actual_Demand_units"]).abs() * tmp2["Unit_Cost_USD"].fillna(0)

    top = (
        tmp2.groupby("SKU_ID", as_index=False)
        .agg(Var_Cost_USD=("Var_Cost_USD", "sum"))
        .sort_values("Var_Cost_USD", ascending=False)
        .head(10)
    )
    fig_top = go.Figure()
    fig_top.add_trace(go.Bar(
        x=top["SKU_ID"],
        y=top["Var_Cost_USD"],
        name="Variance Cost",
        marker_color=COLORS["green_light"],
    ))

    apply_plotly_theme(fig_top, height=380, showlegend=False)
    fig_top.update_xaxes(title="SKU")
    fig_top.update_yaxes(title="USD")

    st.plotly_chart(fig_top, use_container_width=True, key="top10_sku_variance_cost")


# =========================================================
# TAB 3: Service
# =========================================================
with tabs[2]:
    st.markdown("##  الخدمة (Service)")
    wfill = weighted_fill_rate(filtered)
    so_rate = stockout_rate(filtered)

    r = st.columns(4, gap="small")
    with r[0]: kpi_card("Weighted Fill Rate", fmt_pct(wfill), "مقياس خدمة العملاء")
    with r[1]: kpi_card("Stockout Rate", fmt_pct(so_rate), "نسبة الصفوف اللي فيها نفاد")
    with r[2]:
        po_ontime = np.nan
        if "PO_OnTime_Flag" in filtered.columns:
            s = filtered["PO_OnTime_Flag"]
            if s.dtype == object:
                s = s.astype(str).str.upper().map({"TRUE":1,"FALSE":0,"1":1,"0":0})
            po_ontime = s.mean(skipna=True) * 100
        kpi_card("التوريد في الوقت (تقريبي)", fmt_pct(po_ontime))
    with r[3]:
        # Revenue at risk service lens
        kpi_card("إيراد مفقود محتمل", fmt_money(revenue_at_risk(filtered)))

    st.markdown("---")
    st.markdown("###  حالات نفاد المخزون حسب الشهر")
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=monthly["Month_Label"],
    y=monthly["Stockouts"],
    name="Stockouts",
    marker_color=COLORS["green_light"]
))
    apply_plotly_theme(fig, height=360,  showlegend=False)
    fig.update_xaxes(title="الشهر")
    fig.update_yaxes(title="عدد الحالات")
    st.plotly_chart(fig, use_container_width=True, key="svc_stockouts_by_month")

# =========================================================
# TAB 4: Inventory
# =========================================================
with tabs[3]:
    st.markdown("##  المخزون (Inventory)")
    total_inv = filtered["Inventory_Value_USD"].sum(skipna=True)
    doi_vw = value_weighted_doi(filtered)
    turn = inventory_turnover(filtered)
    slob_val, slob_pct = slobs(filtered)

    r = st.columns(4, gap="small")
    with r[0]: kpi_card("إجمالي قيمة المخزون", fmt_money(total_inv))
    with r[1]: kpi_card("أيام تغطية المخزون (مرجّحة بالقيمة)", fmt_num(doi_vw,1))
    with r[2]:
        turn_txt = "—" if pd.isna(turn) else f"{turn:,.2f}"
        kpi_card("Inventory Turnover", turn_txt, "COGS / Avg Inv Value")
    with r[3]: kpi_card("SLOB %", fmt_pct(slob_pct))

    st.markdown("---")
    st.markdown("###  توزيع قيمة المخزون حسب مجموعة المنتجات")

    g = (
        filtered.groupby("Product_Group", as_index=False)
        .agg(Inventory_Value_USD=("Inventory_Value_USD", "sum"))
        .sort_values("Inventory_Value_USD", ascending=False)
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=g["Product_Group"],
        y=g["Inventory_Value_USD"],
        name="قيمة المخزون",
        marker_color=COLORS["green_light"],   # أو غيّره لـ green_dark لو تبي أغمق
    ))

    apply_plotly_theme(fig, height=380,  showlegend=False)
    fig.update_xaxes(title="مجموعة المنتجات")
    fig.update_yaxes(title="USD")

    st.plotly_chart(fig, use_container_width=True, key="inv_value_by_product_group")

# =========================================================
# TAB 5: Procurement
# =========================================================
with tabs[4]:
    st.markdown("##  المشتريات (Procurement)")
    lead = filtered["Supplier_LeadTime_days"].mean(skipna=True) if "Supplier_LeadTime_days" in filtered.columns else np.nan
    transit = filtered["Transit_days"].mean(skipna=True) if "Transit_days" in filtered.columns else np.nan
    total_lt = filtered["Total_LeadTime_days"].mean(skipna=True) if "Total_LeadTime_days" in filtered.columns else np.nan

    r = st.columns(4, gap="small")
    with r[0]: kpi_card("متوسط Lead Time (مورد)", fmt_num(lead,1), "بالأيام")
    with r[1]: kpi_card("متوسط Transit", fmt_num(transit,1), "بالأيام")
    with r[2]: kpi_card("متوسط Total Lead Time", fmt_num(total_lt,1), "بالأيام")
    st.markdown("---")
    with r[3]:
        # Breach ROP: OnHand < Reorder_Point
        breach = np.nan
        if "Reorder_Point_units" in filtered.columns and "OnHand_Inventory_units" in filtered.columns:
            breach = (filtered["OnHand_Inventory_units"] < filtered["Reorder_Point_units"]).mean() * 100
        kpi_card("نسبة كسر نقطة إعادة الطلب", fmt_pct(breach))
            # =========================================================
    # Supplier Reliability (Lead Time Variability)
    # =========================================================
    lt_var = lead_time_variability(filtered)

   
    st.markdown("###  موثوقية المورد (Lead Time Variability)")

    r_var = st.columns(3, gap="small")
    with r_var[0]:
        kpi_card("متوسط Total Lead Time", fmt_num(lt_var["avg"], 1), "بالأيام")
    with r_var[1]:
        kpi_card("تذبذب Lead Time (Std)", fmt_num(lt_var["std"], 1),
                 "كل ما زاد = عدم استقرار")
    with r_var[2]:
        kpi_card("CoV %", fmt_pct(lt_var["cov"]),
                 "Std/Avg (كل ما زاد = Safety Stock أعلى)")
            # =========================================================
    # Late Receipt Cost (ONLY if columns exist)
    # =========================================================
    
    #st.markdown("---")

    st.markdown("---")
    st.markdown("###  تأخير التوريد (Late Receipt)")

    if ("Planned_Receipt_Date" in filtered.columns) and ("Actual_Receipt_Date" in filtered.columns):
        late = late_receipt_cost(filtered)

        
        # شارت شهري: نسبة التأخير
        df_dates = filtered.copy()
        df_dates["Planned_Receipt_Date"] = pd.to_datetime(df_dates["Planned_Receipt_Date"], errors="coerce")
        df_dates["Actual_Receipt_Date"] = pd.to_datetime(df_dates["Actual_Receipt_Date"], errors="coerce")
        df_dates["Delay_Days"] = (df_dates["Actual_Receipt_Date"] - df_dates["Planned_Receipt_Date"]).dt.days
        df_dates["Late_Flag"] = (df_dates["Delay_Days"] > 0).astype(int)

        late_month = (
            df_dates.groupby("Month", as_index=False)
            .agg(Late_Rate=("Late_Flag", "mean"), Avg_Delay=("Delay_Days", "mean"))
            .sort_values("Month")
        )
        late_month["Late_Rate"] = late_month["Late_Rate"] * 100
        late_month["Month_Label"] = late_month["Month"].apply(to_month_label)
        fig_late = go.Figure()
        fig_late.add_trace(go.Bar(
            x=late_month["Month_Label"],
            y=late_month["Late_Rate"],
            name="Late Rate %",
            marker_color=COLORS["green_light"],
        ))

        apply_plotly_theme(fig_late, height=360, showlegend=False)
        fig_late.update_xaxes(title="الشهر")
        fig_late.update_yaxes(title="%")

        st.plotly_chart(fig_late, use_container_width=True, key="late_rate_monthly")
    else:
        st.info("لا توجد أعمدة Planned_Receipt_Date و Actual_Receipt_Date — KPI Late Receipt يتطلبها.")



    st.markdown("---")
    st.markdown("###  تذبذب Lead Time بصريًا")

    if "Total_LeadTime_days" in filtered.columns:
        # 1) Monthly average lead time
        lt_month = (
            filtered.groupby("Month", as_index=False)
            .agg(Avg_Total_LeadTime=("Total_LeadTime_days", "mean"))
            .sort_values("Month")
        )
        lt_month["Month_Label"] = lt_month["Month"].apply(to_month_label)

        fig_lt = go.Figure()
        fig_lt.add_trace(go.Scatter(
            x=lt_month["Month_Label"],
            y=lt_month["Avg_Total_LeadTime"],
            mode="lines+markers",
            name="Avg Total Lead Time",
            line=dict(color=COLORS["cyan"], width=3),
            marker=dict(size=7, color=COLORS["cyan"]),
        ))

        apply_plotly_theme(fig_lt, height=360,  showlegend=False)
        fig_lt.update_xaxes(title="الشهر")
        fig_lt.update_yaxes(title="Days")

        st.plotly_chart(fig_lt, use_container_width=True, key="lt_month_avg")

# 2) Distribution (Box) — shows variability clearly
# 2) Distribution (Box) — shows variability clearly
        st.markdown("---")
        st.markdown("### توزيع Total Lead Time (Box Plot)")
        
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=filtered["Total_LeadTime_days"],
            name="Total Lead Time Distribution",
            boxmean=True,
            marker_color=COLORS["green_light"],
            # إجبار التلميح على إظهار القيم فقط دون اسم السلسلة لتوفير مساحة
            hoverinfo="y" 
        ))

        # نطبق التنسيق العام أولاً
        apply_plotly_theme(fig_box, height=360, showlegend=False, spikes=False)
        
        # هنا "مربط الفرس": إجبار وضع التجميع الموحد وتعديل شكل المربع
        fig_box.update_layout(
            hovermode="x unified",  # هذا يدمج كل الملصقات في مربع واحد
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)", # خلفية سوداء شفافة قليلاً لتبدو احترافية
                font_size=13,
                font_color="white"
            )
        )
        
        # إخفاء الخطوط الإضافية التي قد تسبب تشتت التلميح
        fig_box.update_xaxes(showspikes=False)
        fig_box.update_yaxes(title="Days", showspikes=False)

        st.plotly_chart(fig_box, use_container_width=True, key="lt_box")
    else:
        st.info("عمود Total_LeadTime_days غير موجود، ما نقدر نطلع شارتات Lead Time.")

    

        

# =========================================================
# TAB 6: Production
# =========================================================
with tabs[5]:
    st.markdown("##  الإنتاج (Production)")
    prod_sum = filtered["Production_Plan_units"].sum(skipna=True) if "Production_Plan_units" in filtered.columns else np.nan
    cap = filtered["Capacity_Utilization_pct"].mean(skipna=True) if "Capacity_Utilization_pct" in filtered.columns else np.nan

    r = st.columns(4, gap="small")
    with r[0]: kpi_card("إجمالي خطة الإنتاج (وحدات)", fmt_num(prod_sum,0))
    with r[1]: kpi_card("متوسط استغلال الطاقة", fmt_pct(cap), "Capacity Utilization")
    with r[2]:
        inhouse_pct = (filtered["Produced_InHouse"] == "إنتاج داخلي").mean() * 100
        kpi_card("نسبة إنتاج داخلي", fmt_pct(inhouse_pct))
    st.markdown("---")
    with r[3]:
        changeover = filtered["Line_Changeover_time_hrs"].mean(skipna=True) if "Line_Changeover_time_hrs" in filtered.columns else np.nan
        kpi_card("متوسط زمن التبديل (ساعات)", fmt_num(changeover,1))

# =========================================================
# TAB 7: Quality
# =========================================================
# =========================================================
# TAB 7: Quality (Replacement - Useful even if no <=90)
# =========================================================
with tabs[6]:
    st.markdown("##  الجودة (Quality)")

    if "Days_to_Expiry" not in filtered.columns:
        st.info("عمود Days_to_Expiry غير موجود، ما نقدر نحسب مؤشرات الجودة المتعلقة بالصلاحية.")
        st.stop()

    d = filtered["Days_to_Expiry"].replace([np.inf, -np.inf], np.nan).dropna()

    # --- KPIs مفيدة ---
    min_days = float(d.min()) if len(d) else np.nan
    avg_days = float(d.mean()) if len(d) else np.nan
    med_days = float(d.median()) if len(d) else np.nan

    pct_180 = float((d <= 180).mean() * 100) if len(d) else np.nan
    pct_365 = float((d <= 365).mean() * 100) if len(d) else np.nan
    pct_730 = float((d <= 730).mean() * 100) if len(d) else np.nan  # سنتين

    r = st.columns(4, gap="small")
    with r[0]: kpi_card("أقل أيام حتى الانتهاء", fmt_num(min_days, 0))
    with r[1]: kpi_card("متوسط أيام حتى الانتهاء", fmt_num(avg_days, 1))
    with r[2]: kpi_card("الوسيط (Median)", fmt_num(med_days, 0), "يقلل تأثير القيم الشاذة")
    with r[3]: kpi_card("Coverage ≤ 180 يوم", fmt_pct(pct_180), "مؤشر مبكر (6 شهور)")
        # هذا KPI “إشاري” بدال الصفر
       

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    r2 = st.columns(3, gap="small")
    with r2[0]: kpi_card("Coverage ≤ 365 يوم", fmt_pct(pct_365), "نسبة الصفوف تحت سنة")
    with r2[1]: kpi_card("Coverage ≤ 730 يوم", fmt_pct(pct_730), "نسبة الصفوف تحت سنتين")
    with r2[2]:
        # قيمة المخزون للأقرب انتهاء (مثلاً أقل 10% أيام)
        if len(d):
            cutoff = d.quantile(0.10)
            near_mask = filtered["Days_to_Expiry"].apply(_smart_to_number) <= cutoff
            near_inv = filtered.loc[near_mask, "Inventory_Value_USD"].sum(skipna=True) if "Inventory_Value_USD" in filtered.columns else np.nan
        else:
            near_inv = np.nan
        kpi_card("قيمة مخزون الأقرب انتهاء (أقل 10%)", fmt_money(near_inv), "قيمة مخزون الأصناف الأقل أيام")

    st.markdown("---")

    # --- 1) Distribution Chart: Histogram Days_to_Expiry ---
    st.markdown("### توزيع Days_to_Expiry (Histogram)")

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=d,
        nbinsx=20,
        name="Days_to_Expiry",
        marker_color=COLORS["green_light"],
        hovertemplate="Days: %{x}<br>Count: %{y}<extra></extra>"
    ))
    apply_plotly_theme(fig_hist, height=380, showlegend=False)
    fig_hist.update_xaxes(title="Days_to_Expiry")
    fig_hist.update_yaxes(title="Count")
    st.plotly_chart(fig_hist, use_container_width=True, key="quality_expiry_hist")

    st.markdown("---")

    # --- 2) Top 10 closest to expiry (SKUs) ---
    st.markdown("### أقرب 10 SKUs للانتهاء (حتى لو كانت بعيدة)")

    tmp = filtered.copy()
    tmp["Days_to_Expiry_num"] = tmp["Days_to_Expiry"].apply(_smart_to_number)

    top10 = (
        tmp.dropna(subset=["Days_to_Expiry_num"])
        .sort_values("Days_to_Expiry_num", ascending=True)
        .head(10)
        .copy()
    )

    if len(top10) == 0:
        st.info("لا توجد قيم صالحة في Days_to_Expiry بعد الفلاتر.")
    else:
        # شارت بسيط: SKU vs Days_to_Expiry
        fig_top = go.Figure()
        fig_top.add_trace(go.Bar(
            x=top10["SKU_ID"],
            y=top10["Days_to_Expiry_num"],
            name="Days_to_Expiry",
            marker_color=COLORS["green_light"],
            hovertemplate="<b>SKU:</b> %{x}<br><b>Days:</b> %{y:,.0f}<extra></extra>"
        ))
        apply_plotly_theme(fig_top, height=380, showlegend=False)
        fig_top.update_xaxes(title="SKU")
        fig_top.update_yaxes(title="Days_to_Expiry")
        st.plotly_chart(fig_top, use_container_width=True, key="quality_top10_closest")

     

    # رسالة ذكية بدل “أصفار”
    if (d <= 90).sum() == 0:
        st.success("✅ لا توجد أصناف قريبة الانتهاء خلال 90 يوم — مؤشر ممتاز (لا مخاطر صلاحية قصيرة).")

# =========================================================
# TAB 8: Revenue
# =========================================================
with tabs[7]:
    st.markdown("##  الإيراد (Revenue)")
    total_rev = filtered["Monthly_Revenue_USD"].sum(skipna=True)
    cogs = filtered["Estimated_COGS_USD"].sum(skipna=True)
    gross = total_rev - cogs if (not pd.isna(total_rev) and not pd.isna(cogs)) else np.nan
    r_risk = revenue_at_risk(filtered)

    r = st.columns(4, gap="small")
    with r[0]: kpi_card("إجمالي الإيراد", fmt_money(total_rev))
    with r[1]: kpi_card("COGS (تقديري)", fmt_money(cogs), "Actual × Unit Cost")
    with r[2]: kpi_card("Gross Margin (تقريبي)", fmt_money(gross))
    with r[3]: kpi_card("Revenue at Risk", fmt_money(r_risk), "صفوف فيها Stockout")

    st.markdown("---")
    st.markdown("###  الإيراد حسب الشهر")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month_Label"],
        y=monthly["Monthly_Revenue_USD"],
        mode="lines+markers",
        name="الإيراد",
        line=dict(color=COLORS["cyan"], width=3),
        marker=dict(size=7, color=COLORS["cyan"]),
    ))

    apply_plotly_theme(fig, height=360, showlegend=False)
    fig.update_xaxes(title="الشهر")
    fig.update_yaxes(title="USD")

    st.plotly_chart(fig, use_container_width=True, key="revenue_monthly")

# =========================================================
# Optional table
# =========================================================
if show_table:
    st.markdown("---")
    st.markdown("###  معاينة البيانات بعد الفلاتر")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
