"""
GECAR Dashboard — Analisis Tanggapan Masyarakat & Narasumber Pemerintah
Versi 2: Tema terang & kontras tinggi untuk keterbacaan maksimal
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# ──────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GECAR | Dashboard Analisis Isu Papua",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM — terang, kontras tinggi, mudah dibaca
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lora:wght@400;600&display=swap');

  /* ── Global ── */
  html, body, [data-testid="stAppViewContainer"] {
    background: #F5F7FA !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #1B2A4A !important;
    border-right: 3px solid #2E4070;
  }
  [data-testid="stSidebar"] * { color: #E8EDF5 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label {
    color: #A8B8D0 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  [data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #253559 !important;
    border-color: #3A5080 !important;
    color: #E8EDF5 !important;
  }

  /* ── Metric cards ── */
  [data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
    border: 1px solid #E2E8F0;
    border-top: 4px solid #E63946 !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }
  [data-testid="stMetricValue"] {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: #1B2A4A !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
  }
  [data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    color: #64748B !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  /* ── Section headers ── */
  .sec-hdr {
    background: #1B2A4A;
    color: #FFFFFF;
    padding: 13px 22px;
    border-radius: 10px;
    margin: 22px 0 14px 0;
    font-size: 0.97rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  /* ── Issue / insight cards ── */
  .icard {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 18px 22px;
    margin: 10px 0;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #E63946;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    color: #1E293B;
    font-size: 0.9rem;
    line-height: 1.7;
  }
  .icard b { color: #1B2A4A; font-size: 0.95rem; }
  .icard-blue  { border-left-color: #2563EB; }
  .icard-orange{ border-left-color: #EA6C00; }
  .icard-green { border-left-color: #16A34A; }
  .icard-purple{ border-left-color: #7C3AED; }

  /* ── Quote boxes ── */
  .qbox {
    background: #F0F5FF;
    border-left: 4px solid #2563EB;
    padding: 13px 18px;
    border-radius: 8px;
    font-style: italic;
    color: #1E3A5F;
    font-size: 0.87rem;
    line-height: 1.65;
    margin: 7px 0;
  }
  .qbox small { font-style: normal; color: #4A6FA5; font-weight: 600; font-size: 0.75rem; }

  .qbox-orange { background: #FFF5EB; border-left-color: #EA6C00; color: #4A2800; }
  .qbox-orange small { color: #9A4500; }
  .qbox-green  { background: #F0FAF4; border-left-color: #16A34A; color: #14532D; }
  .qbox-green  small { color: #166534; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #E8EEF8;
    border-radius: 12px;
    padding: 5px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    font-weight: 600;
    font-size: 0.88rem;
    color: #1B2A4A;
    padding: 9px 20px;
  }
  .stTabs [aria-selected="true"] {
    background: #1B2A4A !important;
    color: #FFFFFF !important;
  }

  /* ── Divider ── */
  hr { border: none; border-top: 2px solid #E2E8F0; margin: 22px 0; }

  /* ── Expander ── */
  .st-expander { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# PLOTLY BASE TEMPLATE — latar putih, kontras tinggi
# ──────────────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#F8FAFC",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#1E293B", size=12),
    title_font=dict(color="#1B2A4A", size=14, family="Plus Jakarta Sans, sans-serif"),
    xaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1", tickcolor="#64748B",
               tickfont=dict(color="#334155", size=11)),
    yaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1", tickcolor="#64748B",
               tickfont=dict(color="#334155", size=11)),
    legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#E2E8F0",
                borderwidth=1, font=dict(color="#334155", size=11)),
    margin=dict(l=10, r=20, t=50, b=10),
)

# Palet warna — tinggi kontras, terbaca di latar putih
C_MAIN   = ["#1B2A4A","#E63946","#2563EB","#EA6C00","#16A34A","#7C3AED","#0891B2","#CA8A04","#9F1239","#065F46"]
C_BLUE   = ["#DBEAFE","#93C5FD","#3B82F6","#1D4ED8","#1E3A8A"]
C_RED    = ["#FEE2E2","#FCA5A5","#EF4444","#DC2626","#991B1B"]
C_GREEN  = ["#DCFCE7","#86EFAC","#22C55E","#16A34A","#14532D"]
C_ORANGE = ["#FFF7ED","#FED7AA","#FB923C","#EA580C","#7C2D12"]
C_NAVY   = ["#EFF6FF","#BFDBFE","#60A5FA","#2563EB","#1E40AF"]
C_SEQ_RD = "Reds"
C_SEQ_BL = "Blues"
C_SEQ_GN = "Greens"
C_SEQ_OR = "Oranges"

def bar_h(df, x, y, title, color_scale=C_RED, text=True):
    """Horizontal bar chart helper."""
    fig = px.bar(
        df, x=x, y=y, orientation="h",
        color=x, color_continuous_scale=color_scale,
        title=title, text=x if text else None,
    )
    fig.update_traces(textposition="outside", textfont=dict(color="#1B2A4A", size=11))
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**PLOT_LAYOUT, height=370,
                      yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
    return fig

def bar_v(df, x, y, title, color=None, color_map=None):
    """Vertical bar chart helper."""
    kwargs = dict(x=x, y=y, title=title, text=y)
    if color:
        kwargs["color"] = color
    if color_map:
        kwargs["color_discrete_map"] = color_map
    elif color:
        kwargs["color_discrete_sequence"] = C_MAIN
    else:
        kwargs["color_discrete_sequence"] = [C_MAIN[0]]
    fig = px.bar(df, **kwargs)
    fig.update_traces(textposition="outside", textfont=dict(color="#1B2A4A", size=11))
    fig.update_layout(**PLOT_LAYOUT, height=360, xaxis_tickangle=-25)
    return fig

# ──────────────────────────────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Memuat data…")
def load_data():
    import os
    paths = [
        ("Gecar_-_Kelompok.csv", "Gecar_-_KII.csv"),
        ("/mnt/user-data/uploads/Gecar_-_Kelompok.csv", "/mnt/user-data/uploads/Gecar_-_KII.csv"),
    ]
    for p1, p2 in paths:
        if os.path.exists(p1) and os.path.exists(p2):
            return pd.read_csv(p1), pd.read_csv(p2)
    st.error("❌ File CSV tidak ditemukan. Pastikan kedua file CSV ada di folder yang sama.")
    st.stop()

df_k, df_i = load_data()

# ──────────────────────────────────────────────────────────────────────
# THEMATIC CLASSIFICATION
# ──────────────────────────────────────────────────────────────────────
THEMES_K = {
    "Kekerasan & Konflik":          ["perang suku","perang","konflik","kekerasan","miras","parang",
                                     "mabok","mabuk","ancaman","bentrok","begal","sajam","dipukul",
                                     "pukul","berkelahi","saling serang","pembunuhan"],
    "Narkoba & Zat Berbahaya":      ["aibon","narkoba","ganja","kecanduan","zat","hiv","aids","alkohol"],
    "Pendidikan":                   ["sekolah","belajar","guru","pendidikan","pelajar","paud",
                                     "rumah baca","kuliah","ijazah","les ","ekstrakurikuler","buku"],
    "Ekonomi & Kemiskinan":         ["ekonomi","miskin","pekerjaan","kerja","dana","bantuan","blt",
                                     "uang","harga","inflasi","pangan","sembako","logistik","usaha",
                                     "modal","ternak","kebun","karaka","ikan","bensin","keramba"],
    "Korupsi & Ketidakadilan":      ["dipotong","tidak adil","memihak","kepala kampung",
                                     "anti masyarakat","dicoret","oknum","tidak merata","tidak dapat",
                                     "nepotisme","timses","pinjam","hutang"],
    "Keamanan Lingkungan":          ["aman","keamanan","polisi","palang","linmas","pencurian","helm"],
    "Keluarga & Sosial":            ["orang tua","keluarga","mama","papa","bapa","adik","kakak",
                                     "nenek","broken home","suami","istri","perselingkuhan"],
    "Harapan & Kontribusi Pemuda":  ["harapan","berkontribusi","masa depan","cita","semangat",
                                     "kontribusi","motivasi","berubah jadi lebih baik","lomba"],
}

THEMES_I = {
    "Konflik Bersenjata & Separatisme": ["bersenjata","egianus","papua merdeka","separatis",
                                          "tni","polri","nduga","militer","penyanderaan","pilot susi"],
    "Krisis Pangan & Inflasi":          ["pangan","inflasi","logistik","sembako","harga",
                                          "krisis","bps","sandang","papan","udara","transportasi"],
    "Narkoba & HIV Anak":               ["narkoba","aibon","hiv","aids","rehabilitasi","bnn",
                                          "narkotika","mantan pengguna"],
    "Kualitas Pendidikan":              ["guru","paud","honor","mengajar","kurikulum",
                                          "panggilan","bangunan","gedung sekolah","apbd","bup"],
    "Konflik Lahan & PSN":              ["lahan","psn","food estate","penggusuran","deforestasi",
                                          "tanah adat","ulayat","gambut","rawa","tebu","korporasi"],
    "Diskriminasi OAP vs Pendatang":    ["oap","pendatang","orang asli papua","dikotomi",
                                          "diskriminasi","pns","kuota","polarisasi","identitas"],
    "Perlindungan Anak & Perempuan":    ["anak","remaja","perempuan","rentan","trauma",
                                          "kekerasan seksual","perlindungan","putus sekolah"],
    "Tata Kelola & Korupsi":            ["tidak transparan","nepotisme","oknum","keuangan",
                                          "distribusi tidak adil","korupsi","anggaran","pejabat"],
}

def classify(text, themes):
    t = str(text).lower()
    found = [theme for theme, kws in themes.items()
             if any(re.search(r'\b' + re.escape(kw) + r'\b', t) or kw in t for kw in kws)]
    return found if found else ["Kehidupan Sehari-hari & Lainnya"]

df_k["Tema_List"] = df_k["Tanggapan"].apply(lambda x: classify(x, THEMES_K))
df_i["Tema_List"] = df_i["Tanggapan"].apply(lambda x: classify(x, THEMES_I))
dfk_ = df_k.explode("Tema_List")
dfi_ = df_i.explode("Tema_List")

# ──────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗺️ GECAR Dashboard")
    st.markdown("**Analisis Isu Sosial Papua 2024–2025**")
    st.divider()
    st.markdown("### 📍 Filter — Masyarakat")
    wk_opts = ["Semua Wilayah"] + sorted(df_k["Wilayah"].dropna().unique().tolist())
    sel_wk  = st.selectbox("Wilayah", wk_opts, key="wk")
    uk_opts = ["Semua Usia"] + df_k["Kelompok_Usia"].dropna().unique().tolist()
    sel_uk  = st.selectbox("Kelompok Usia", uk_opts)
    gk_opts = ["Semua"] + df_k["Jenis_Kelamin"].dropna().unique().tolist()
    sel_gk  = st.selectbox("Jenis Kelamin", gk_opts)

    st.divider()
    st.markdown("### 🏛️ Filter — KII")
    wi_opts = ["Semua Wilayah"] + sorted(df_i["Wilayah"].dropna().unique().tolist())
    sel_wi  = st.selectbox("Wilayah", wi_opts, key="wi")
    ni_opts = ["Semua Narasumber"] + df_i["Narsum"].dropna().unique().tolist()
    sel_ni  = st.selectbox("Narasumber", ni_opts)

    st.divider()
    st.caption("GECAR | Data Papua 2024–2025")

# ──────────────────────────────────────────────────────────────────────
# FILTER HELPERS
# ──────────────────────────────────────────────────────────────────────
def fk(df):
    d = df.copy()
    if sel_wk != "Semua Wilayah": d = d[d["Wilayah"] == sel_wk]
    if sel_uk != "Semua Usia":    d = d[d["Kelompok_Usia"] == sel_uk]
    if sel_gk != "Semua":         d = d[d["Jenis_Kelamin"] == sel_gk]
    return d

def fi(df):
    d = df.copy()
    if sel_wi != "Semua Wilayah":    d = d[d["Wilayah"] == sel_wi]
    if sel_ni != "Semua Narasumber": d = d[d["Narsum"] == sel_ni]
    return d

FK  = fk(df_k);  FK_ = fk(dfk_)
FI  = fi(df_i);  FI_ = fi(dfi_)

# ──────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#1B2A4A;padding:28px 36px;border-radius:16px;
            color:#FFFFFF;margin-bottom:22px;border-bottom:4px solid #E63946;'>
  <h1 style='margin:0;font-size:1.85rem;font-weight:800;letter-spacing:-0.02em;
             font-family:"Plus Jakarta Sans",sans-serif;'>
    🗺️ GECAR — Dashboard Analisis Isu Sosial Papua
  </h1>
  <p style='margin:8px 0 0;color:#A8BDD8;font-size:0.92rem;font-family:"Plus Jakarta Sans",sans-serif;'>
    Tanggapan Masyarakat (FGD) &amp; Narasumber Pemerintah (KII) ·
    <strong style='color:#93C5FD;'>Jayawijaya · Asmat · Sentani</strong> · 2024–2025
  </p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "👥  Dataset 1 — Masyarakat (FGD)",
    "🏛️  Dataset 2 — KII (Narasumber Pemerintah)",
    "📄  Laporan Eksekutif & Rekomendasi",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — MASYARAKAT
# ══════════════════════════════════════════════════════════════════════
with tab1:

    # ── KPI ──────────────────────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>📌 Ringkasan Dataset 1 — Masyarakat (FGD)</div>",
                unsafe_allow_html=True)
    total = len(FK)
    n_anak   = (FK["Kelompok_Usia"]=="Anak").sum()
    n_dewasa = (FK["Kelompok_Usia"]=="Dewasa").sum()
    pct_konflik  = FK["Tanggapan"].str.contains(
        "perang|kekerasan|miras|mabuk|ancaman|begal|parang|pukul|dipukul",
        case=False,na=False).mean()*100
    pct_korupsi  = FK["Tanggapan"].str.contains(
        "dipotong|tidak adil|kepala kampung|oknum|dicoret|tidak merata",
        case=False,na=False).mean()*100

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Responden",        f"{total:,}")
    c2.metric("Responden Anak",          f"{n_anak:,}")
    c3.metric("Responden Dewasa",        f"{n_dewasa:,}")
    c4.metric("Menyebut Kekerasan/Konflik", f"{pct_konflik:.0f}%")
    c5.metric("Menyebut Korupsi Bantuan",   f"{pct_korupsi:.0f}%")

    st.divider()

    # ── ISU 1: DISTRIBUSI TEMA ────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>📊 Isu 1 — Distribusi Tema Tanggapan Masyarakat</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='icard icard-blue'>
    <b>Temuan:</b> Delapan tema dominan teridentifikasi dari tanggapan masyarakat.
    Isu ekonomi & kemiskinan mendominasi di Asmat, kekerasan & konflik paling menonjol di Jayawijaya,
    dan kebutuhan pendidikan konsisten muncul di ketiga wilayah.
    </div>""", unsafe_allow_html=True)

    tema_ct = FK_["Tema_List"].value_counts().reset_index()
    tema_ct.columns = ["Tema","Jumlah"]
    tema_ct = tema_ct[tema_ct["Tema"] != "Kehidupan Sehari-hari & Lainnya"].sort_values("Jumlah")

    fig_t = px.bar(
        tema_ct, x="Jumlah", y="Tema", orientation="h",
        color="Tema", color_discrete_sequence=C_MAIN,
        title="Frekuensi Kemunculan Tema Isu — Tanggapan Masyarakat",
        text="Jumlah",
    )
    fig_t.update_traces(textposition="outside",
                        textfont=dict(color="#1B2A4A", size=12, family="Plus Jakarta Sans"))
    fig_t.update_layout(**PLOT_LAYOUT, showlegend=False, height=400,
                        yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
    st.plotly_chart(fig_t, use_container_width=True)

    # ── ISU 2: KETAKUTAN ANAK ─────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>⚠️ Isu 2 — Kekerasan Domestik & Ketakutan Anak</div>",
                unsafe_allow_html=True)
    col_a, col_b = st.columns([3,2])

    with col_a:
        takut = {
            "Dipukul / Kekerasan Fisik dari Orang Tua":
                df_k["Tanggapan"].str.contains("dipukul|pukul|kekerasan fisik dari bap|dari orang tua",case=False,na=False).sum(),
            "Kekerasan Akibat Miras / Orang Mabuk":
                df_k["Tanggapan"].str.contains("miras|mabuk|mabok|parang saat marah|pegang parang",case=False,na=False).sum(),
            "Perang Suku & Konflik Antar Kampung":
                df_k["Tanggapan"].str.contains("perang suku|saling serang|antar kampung|konflik",case=False,na=False).sum(),
            "Aibon / Narkoba di Lingkungan":
                df_k["Tanggapan"].str.contains("aibon|narkoba|ganja",case=False,na=False).sum(),
            "Kehilangan Orang Tua / Keluarga":
                df_k["Tanggapan"].str.contains("kehilangan|meninggal|kehilangan papa|mama",case=False,na=False).sum(),
            "Ketidakpastian Masa Depan / Ekonomi":
                df_k["Tanggapan"].str.contains("masa depan|cita|pekerjaan|tidak pasti",case=False,na=False).sum(),
        }
        df_t = pd.DataFrame(list(takut.items()),columns=["Ketakutan","Jumlah"]).sort_values("Jumlah")
        fig_takut = px.bar(
            df_t, x="Jumlah", y="Ketakutan", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_RD,
            title="Jenis Ketakutan yang Dilaporkan Masyarakat",
            text="Jumlah",
        )
        fig_takut.update_traces(textposition="outside",
                                textfont=dict(color="#1B2A4A", size=12))
        fig_takut.update_layout(**PLOT_LAYOUT, showlegend=False, height=360,
                                coloraxis_showscale=False,
                                yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_takut, use_container_width=True)

    with col_b:
        st.markdown("""
        <div class='icard'>
        <b>🔴 Kekerasan dalam Rumah Tangga</b><br><br>
        Responden anak menyebut <b>kekerasan fisik dari orang tua</b> sebagai ketakutan utama —
        melebihi konflik sosial maupun bencana. Anak-anak melaporkan melarikan diri ke rumah nenek
        atau ke gereja sebagai strategi perlindungan diri.
        </div>""", unsafe_allow_html=True)

        kdrta = df_k[(df_k["Kelompok_Usia"]=="Anak") &
                     df_k["Tanggapan"].str.contains("dipukul|pukul.*bap|kekerasan fisik",case=False,na=False)]
        for _, row in kdrta.head(3).iterrows():
            txt = str(row["Tanggapan"])[:170] + ("…" if len(str(row["Tanggapan"]))>170 else "")
            st.markdown(f"""<div class='qbox'>&ldquo;{txt}&rdquo;
            <br><small>— {row.get('Wilayah','')}</small></div>""", unsafe_allow_html=True)

    # ── ISU 3: MIRAS ─────────────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>🍺 Isu 3 — Miras sebagai Pemicu Kekerasan Komunitas</div>",
                unsafe_allow_html=True)
    col_c, col_d = st.columns(2)

    with col_c:
        miras_w = {}
        for w in df_k["Wilayah"].dropna().unique():
            miras_w[w] = df_k[df_k["Wilayah"]==w]["Tanggapan"].str.contains(
                "miras|mabuk|mabok|alkohol",case=False,na=False).sum()
        df_mw = pd.DataFrame(list(miras_w.items()),columns=["Wilayah","Jumlah"])
        fig_mw = px.bar(
            df_mw, x="Wilayah", y="Jumlah", color="Wilayah",
            color_discrete_sequence=["#E63946","#2563EB","#EA6C00"],
            title="Frekuensi Tanggapan Terkait Miras per Wilayah",
            text="Jumlah",
        )
        fig_mw.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_mw.update_layout(**PLOT_LAYOUT, showlegend=False, height=320)
        st.plotly_chart(fig_mw, use_container_width=True)

    with col_d:
        dampak = {
            "Kekerasan Fisik / Pemukul":     df_k["Tanggapan"].str.contains("pukul|parang|marah|kekerasan",case=False,na=False).sum(),
            "Pencurian / Begal":             df_k["Tanggapan"].str.contains("pencurian|begal|curi|helm",case=False,na=False).sum(),
            "Konflik Antar Kampung":         df_k["Tanggapan"].str.contains("saling serang|antar kampung|perang",case=False,na=False).sum(),
            "Perselingkuhan / Perceraian":   df_k["Tanggapan"].str.contains("perselingkuhan|perceraian|pembunuhan",case=False,na=False).sum(),
        }
        df_dm = pd.DataFrame(list(dampak.items()),columns=["Dampak","Jumlah"])
        fig_dm = px.pie(
            df_dm, names="Dampak", values="Jumlah",
            color_discrete_sequence=["#E63946","#1B2A4A","#EA6C00","#64748B"],
            title="Dampak Turunan Miras yang Dilaporkan",
            hole=0.42,
        )
        fig_dm.update_traces(textposition="inside", textinfo="label+percent",
                             textfont=dict(color="#FFFFFF", size=11))
        fig_dm.update_layout(**PLOT_LAYOUT, showlegend=False, height=320)
        st.plotly_chart(fig_dm, use_container_width=True)

    # ── ISU 4: KORUPSI BLT ───────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>💸 Isu 4 — Korupsi & Pemotongan Dana Bantuan (BLT)</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='icard icard-orange'>
    <b>Temuan Kritis:</b> Masyarakat Asmat secara konsisten melaporkan pemotongan BLT oleh oknum kepala kampung,
    penunjukan kepala kampung oleh bupati tanpa suara rakyat, dan diskriminasi distribusi bantuan
    berbasis afiliasi politik. Ini adalah <b>korupsi berjamaah terstruktur</b> yang merusak kepercayaan
    masyarakat terhadap seluruh sistem pemerintahan kampung.
    </div>""", unsafe_allow_html=True)

    col_e, col_f = st.columns([2,3])
    with col_e:
        kor = {
            "BLT Dipotong Oknum":                   df_k["Tanggapan"].str.contains("dipotong|potong.*blt",case=False,na=False).sum(),
            "Kepala Kampung Memihak Simpatisan":     df_k["Tanggapan"].str.contains("memihak|simpatisan|timses",case=False,na=False).sum(),
            "Bantuan Tidak Merata":                  df_k["Tanggapan"].str.contains("tidak merata|tidak adil|tidak penuh|tidak dapat",case=False,na=False).sum(),
            "Kepala Kampung Tidak Dipercaya":        df_k["Tanggapan"].str.contains("tidak peduli|anti masyarakat|kepala kampung.*tidak",case=False,na=False).sum(),
            "Dana Desa Diselewengkan":               df_k["Tanggapan"].str.contains("pinjam.*add|membayar hutang|kebutuhan kepala",case=False,na=False).sum(),
        }
        df_kor = pd.DataFrame(list(kor.items()),columns=["Bentuk","Jumlah"])
        df_kor = df_kor[df_kor["Jumlah"]>0].sort_values("Jumlah")
        fig_kor = px.bar(
            df_kor, x="Jumlah", y="Bentuk", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_OR,
            title="Bentuk Penyimpangan Dana yang Dilaporkan",
            text="Jumlah",
        )
        fig_kor.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_kor.update_layout(**PLOT_LAYOUT, showlegend=False, height=320,
                              coloraxis_showscale=False,
                              yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_kor, use_container_width=True)

    with col_f:
        st.markdown("#### 📣 Suara Langsung Masyarakat")
        kor_rows = df_k[df_k["Tanggapan"].str.contains(
            "dipotong|memihak|anti masyarakat|pinjam.*add|dicoret|timses",
            case=False,na=False)].head(5)
        for _, row in kor_rows.iterrows():
            txt = str(row["Tanggapan"])[:230]+"…" if len(str(row["Tanggapan"]))>230 else str(row["Tanggapan"])
            st.markdown(f"""<div class='qbox qbox-orange'>&ldquo;{txt}&rdquo;
            <br><small>— {row.get('Wilayah','')}</small></div>""", unsafe_allow_html=True)

    # ── ISU 5: KEBUTUHAN vs HARAPAN ──────────────────────────────────
    st.markdown("<div class='sec-hdr'>🌱 Isu 5 — Kebutuhan Utama vs Harapan Masa Depan</div>",
                unsafe_allow_html=True)
    col_g, col_h = st.columns(2)

    with col_g:
        keb = {
            "Air Bersih / Sanitasi":    df_k["Tanggapan"].str.contains("air bersih|sumur|pah|sanitasi",case=False,na=False).sum(),
            "Lapangan Kerja":           df_k["Tanggapan"].str.contains("pekerjaan|kerja|lapangan kerja|lowongan",case=False,na=False).sum(),
            "Pendidikan / Sekolah":     df_k["Tanggapan"].str.contains("sekolah|pendidikan|belajar|guru",case=False,na=False).sum(),
            "Akses Kesehatan":          df_k["Tanggapan"].str.contains("kesehatan|rumah sakit|puskesmas|imunisasi",case=False,na=False).sum(),
            "Bantuan Pangan / BLT":     df_k["Tanggapan"].str.contains("pangan|sembako|blt|beras|raskin|bantuan",case=False,na=False).sum(),
            "Infrastruktur Jalan":      df_k["Tanggapan"].str.contains("jalan|jembatan|infrastruktur|akses",case=False,na=False).sum(),
            "Modal Usaha / Ekonomi":    df_k["Tanggapan"].str.contains("modal|usaha|ternak|kebun|keramba|bibit",case=False,na=False).sum(),
        }
        df_kb = pd.DataFrame(list(keb.items()),columns=["Kebutuhan","Jumlah"]).sort_values("Jumlah")
        fig_kb = px.bar(
            df_kb, x="Jumlah", y="Kebutuhan", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_BL,
            title="Kebutuhan Utama yang Disampaikan Masyarakat",
            text="Jumlah",
        )
        fig_kb.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_kb.update_layout(**PLOT_LAYOUT, showlegend=False, height=360,
                             coloraxis_showscale=False,
                             yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_kb, use_container_width=True)

    with col_h:
        har = {
            "Pendidikan Lebih Baik":         df_k["Tanggapan"].str.contains("sekolah.*baik|kuliah|ijazah|lulus",case=False,na=False).sum(),
            "Kegiatan Positif Pemuda":        df_k["Tanggapan"].str.contains("kegiatan.*positif|olahraga|bazaar|lomba|rumah baca",case=False,na=False).sum(),
            "Komunitas / Gereja Maju":        df_k["Tanggapan"].str.contains("gereja.*maju|komunitas.*baik|ibadah",case=False,na=False).sum(),
            "Pemerintah Lebih Adil":          df_k["Tanggapan"].str.contains("pemerintah.*adil|adil|pemimpin.*baik",case=False,na=False).sum(),
            "Lapangan Kerja":                 df_k["Tanggapan"].str.contains("lowongan|pekerjaan.*wvi|cari kerja",case=False,na=False).sum(),
            "Infrastruktur Kampung":          df_k["Tanggapan"].str.contains("jalan|jembatan|air bersih|renovasi|pembangunan",case=False,na=False).sum(),
        }
        df_hr = pd.DataFrame(list(har.items()),columns=["Harapan","Jumlah"]).sort_values("Jumlah")
        fig_hr = px.bar(
            df_hr, x="Jumlah", y="Harapan", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_GN,
            title="Harapan Masyarakat untuk Masa Depan Komunitas",
            text="Jumlah",
        )
        fig_hr.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_hr.update_layout(**PLOT_LAYOUT, showlegend=False, height=360,
                             coloraxis_showscale=False,
                             yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_hr, use_container_width=True)

    # ── ISU 6: HEATMAP ───────────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>🗺️ Isu 6 — Peta Isu: Tema per Wilayah (Heatmap)</div>",
                unsafe_allow_html=True)
    tw = FK_.groupby(["Wilayah","Tema_List"]).size().reset_index(name="Jumlah")
    tw = tw[tw["Tema_List"]!="Kehidupan Sehari-hari & Lainnya"]
    pivot = tw.pivot(index="Tema_List",columns="Wilayah",values="Jumlah").fillna(0)
    fig_hm = px.imshow(
        pivot, color_continuous_scale="YlOrRd",
        title="Intensitas Isu per Wilayah (Semakin Gelap = Semakin Dominan)",
        aspect="auto", text_auto=True,
    )
    fig_hm.update_traces(textfont=dict(color="#1B2A4A", size=12))
    fig_hm.update_layout(**PLOT_LAYOUT, height=390)
    st.plotly_chart(fig_hm, use_container_width=True)

    # ── ISU 7: ANAK vs DEWASA ─────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>👦👩 Perbandingan Isu: Anak vs Dewasa</div>",
                unsafe_allow_html=True)
    ck = {
        "Kekerasan / Pukul":       "dipukul|pukul|kekerasan",
        "Ekonomi / Pekerjaan":     "ekonomi|pekerjaan|kerja|dana|bantuan",
        "Pendidikan / Sekolah":    "sekolah|belajar|guru|pendidikan",
        "Miras / Narkoba":         "miras|mabuk|aibon|narkoba|ganja",
        "Harapan Masa Depan":      "harapan|cita|masa depan|berubah",
        "Peran Komunitas":         "gereja|ibadah|komunitas|berkontribusi",
    }
    rows_c = []
    for kel in ["Anak","Dewasa"]:
        sub = df_k[df_k["Kelompok_Usia"]==kel]
        for label, pat in ck.items():
            rows_c.append({"Kelompok":kel,"Isu":label,
                           "Frekuensi":sub["Tanggapan"].str.contains(pat,case=False,na=False).sum()})
    df_c = pd.DataFrame(rows_c)
    fig_c = px.bar(
        df_c, x="Isu", y="Frekuensi", color="Kelompok", barmode="group",
        color_discrete_map={"Anak":"#2563EB","Dewasa":"#E63946"},
        title="Perbandingan Prioritas Isu: Anak vs Dewasa",
        text="Frekuensi",
    )
    fig_c.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=11))
    fig_c.update_layout(**PLOT_LAYOUT, height=360, xaxis_tickangle=-20,
                        legend=dict(**PLOT_LAYOUT["legend"], orientation="h", y=1.08))
    st.plotly_chart(fig_c, use_container_width=True)

    with st.expander("📋 Lihat Data Mentah — Dataset Masyarakat"):
        st.dataframe(FK[["Wilayah","Kelompok_Usia","Jenis_Kelamin","Pertanyaan","Tanggapan"]],
                     use_container_width=True, height=340)

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — KII
# ══════════════════════════════════════════════════════════════════════
with tab2:

    # ── KPI ──────────────────────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>📌 Ringkasan Dataset 2 — KII (Narasumber Pemerintah)</div>",
                unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Pernyataan KII",          f"{len(FI):,}")
    c2.metric("Jayawijaya",                    f"{(FI['Wilayah']=='Jayawijaya').sum():,}")
    c3.metric("Sentani",                       f"{(FI['Wilayah']=='Sentani').sum():,}")
    c4.metric("Menyebut Anak/Remaja Rentan",   f"{FI['Tanggapan'].str.contains('anak|remaja|rentan',case=False,na=False).mean()*100:.0f}%")
    c5.metric("Menyebut Konflik/Keamanan",     f"{FI['Tanggapan'].str.contains('konflik|bersenjata|keamanan|kkb',case=False,na=False).mean()*100:.0f}%")

    st.divider()

    # ── ISU 1: DISTRIBUSI TEMA KII ────────────────────────────────────
    st.markdown("<div class='sec-hdr'>📊 Isu 1 — Peta Isu Strategis dari Narasumber Pemerintah</div>",
                unsafe_allow_html=True)
    col_a, col_b = st.columns([3,2])
    with col_a:
        tkii = FI_["Tema_List"].value_counts().reset_index()
        tkii.columns = ["Tema","Jumlah"]
        tkii = tkii[tkii["Tema"]!="Kehidupan Sehari-hari & Lainnya"].sort_values("Jumlah")
        fig_tk = px.bar(
            tkii, x="Jumlah", y="Tema", orientation="h",
            color="Tema", color_discrete_sequence=C_MAIN,
            title="Distribusi Tema dalam Pernyataan KII",
            text="Jumlah",
        )
        fig_tk.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_tk.update_layout(**PLOT_LAYOUT, showlegend=False, height=390,
                             yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_tk, use_container_width=True)

    with col_b:
        narsum_label = {
            "GTY":"GTY (Jayawijaya)","JPY":"JPY (Jayawijaya)","ACL":"ACL (Jayawijaya)",
            "Dinas Sosial":"Dinas Sosial (Sentani)","Dinas Pendidikan":"Dinas Pendidikan (Sentani)",
            "RJF":"RJF (Asmat)","WBW":"WBW (Asmat)",
        }
        nct = FI["Narsum"].value_counts().reset_index()
        nct.columns = ["Narsum","Jumlah"]
        nct["Narsum"] = nct["Narsum"].map(narsum_label).fillna(nct["Narsum"])
        fig_nc = px.pie(
            nct, names="Narsum", values="Jumlah",
            color_discrete_sequence=C_MAIN,
            title="Distribusi Pernyataan per Narasumber",
            hole=0.42,
        )
        fig_nc.update_traces(textposition="inside", textinfo="label+percent",
                             textfont=dict(color="#FFFFFF", size=11))
        fig_nc.update_layout(**PLOT_LAYOUT, showlegend=False, height=390)
        st.plotly_chart(fig_nc, use_container_width=True)

    # ── ISU 2: KONFLIK BERSENJATA ─────────────────────────────────────
    st.markdown("<div class='sec-hdr'>🔫 Isu 2 — Konflik Bersenjata & Kelompok Separatis (Jayawijaya)</div>",
                unsafe_allow_html=True)
    col_c, col_d = st.columns([2,3])
    with col_c:
        aktor = {
            "Kelompok Sipil Bersenjata (OPM)": df_i["Tanggapan"].str.contains("bersenjata|egianus|papua merdeka|kelompok sipil",case=False,na=False).sum(),
            "TNI / Polri":                     df_i["Tanggapan"].str.contains("tni|polri|aparat|militer",case=False,na=False).sum(),
            "Tokoh Adat":                      df_i["Tanggapan"].str.contains("tokoh adat|kepala suku|adat",case=False,na=False).sum(),
            "Gereja / Tokoh Agama":            df_i["Tanggapan"].str.contains("gereja|pendeta|tokoh agama",case=False,na=False).sum(),
            "Pemerintah Daerah":               df_i["Tanggapan"].str.contains("pemda|pemerintah daerah|bupati",case=False,na=False).sum(),
        }
        df_ak = pd.DataFrame(list(aktor.items()),columns=["Aktor","Jumlah"]).sort_values("Jumlah")
        fig_ak = px.bar(
            df_ak, x="Jumlah", y="Aktor", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_RD,
            title="Aktor Disebut dalam Konteks Konflik",
            text="Jumlah",
        )
        fig_ak.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_ak.update_layout(**PLOT_LAYOUT, showlegend=False, height=320,
                             coloraxis_showscale=False,
                             yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_ak, use_container_width=True)

    with col_d:
        st.markdown("#### 🔍 Pernyataan Kunci — Konflik Bersenjata")
        krf_rows = df_i[df_i["Tanggapan"].str.contains(
            "egianus|bersenjata|papua merdeka|nduga|separatis|penyanderaan",
            case=False,na=False)].head(4)
        for _, row in krf_rows.iterrows():
            txt = str(row["Tanggapan"])[:290]+"…" if len(str(row["Tanggapan"]))>290 else str(row["Tanggapan"])
            st.markdown(f"""<div class='qbox'>&ldquo;{txt}&rdquo;
            <br><small>— {row.get('Narsum','')} | {row.get('Wilayah','')}</small></div>""",
                        unsafe_allow_html=True)

    # ── ISU 3: NARKOBA & HIV ANAK ─────────────────────────────────────
    st.markdown("<div class='sec-hdr'>💊 Isu 3 — Narkoba, Aibon & HIV pada Anak (Sentani)</div>",
                unsafe_allow_html=True)
    col_e, col_f = st.columns(2)
    with col_e:
        nar_d = {
            "Narkoba di Sekolah (BNN)":     df_i["Tanggapan"].str.contains("narkoba.*sekolah|pemeriksaan.*bnn",case=False,na=False).sum(),
            "Aibon di Jalanan":             df_i["Tanggapan"].str.contains("aibon",case=False,na=False).sum(),
            "Kasus HIV pada Anak SD":       df_i["Tanggapan"].str.contains("hiv|aids",case=False,na=False).sum(),
            "Program Rehabilitasi":         df_i["Tanggapan"].str.contains("rehabilitasi|mantan pengguna|rehab",case=False,na=False).sum(),
            "Pencurian akibat Narkoba":     df_i["Tanggapan"].str.contains("pencurian.*helm|membeli.*narkoba|membeli.*aibon",case=False,na=False).sum(),
            "Broken Home → Narkoba":        df_i["Tanggapan"].str.contains("broken home|keluarga.*narkoba",case=False,na=False).sum(),
        }
        df_nd = pd.DataFrame(list(nar_d.items()),columns=["Isu","Jumlah"])
        df_nd = df_nd[df_nd["Jumlah"]>0].sort_values("Jumlah")
        fig_nd = px.bar(
            df_nd, x="Jumlah", y="Isu", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_OR,
            title="Isu Narkoba & Zat Berbahaya pada Anak-Remaja",
            text="Jumlah",
        )
        fig_nd.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_nd.update_layout(**PLOT_LAYOUT, showlegend=False, height=340,
                             coloraxis_showscale=False,
                             yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_nd, use_container_width=True)

    with col_f:
        st.markdown("#### 🔴 Pernyataan Narasumber — Dinas Sosial & Dinas Pendidikan")
        nar_rows = df_i[df_i["Tanggapan"].str.contains(
            "narkoba|aibon|hiv|rehabilitasi|bnn|pencandu",
            case=False,na=False)].head(4)
        for _, row in nar_rows.iterrows():
            txt = str(row["Tanggapan"])[:280]+"…" if len(str(row["Tanggapan"]))>280 else str(row["Tanggapan"])
            st.markdown(f"""<div class='qbox qbox-orange'>&ldquo;{txt}&rdquo;
            <br><small>— {row.get('Narsum','')} | {row.get('Wilayah','')}</small></div>""",
                        unsafe_allow_html=True)

    # ── ISU 4: KONFLIK LAHAN & PSN ────────────────────────────────────
    st.markdown("<div class='sec-hdr'>🌿 Isu 4 — Konflik Lahan & Proyek Strategis Nasional (Asmat)</div>",
                unsafe_allow_html=True)
    col_g, col_h = st.columns([3,2])
    with col_g:
        psn = {
            "Deforestasi & Lahan Gambut":        df_i["Tanggapan"].str.contains("deforestasi|gambut|rawa|lahan.*terbuka",case=False,na=False).sum(),
            "Penggusuran / Penolakan Lahan Adat": df_i["Tanggapan"].str.contains("penggusuran|penolakan|ulayat|hak adat",case=False,na=False).sum(),
            "Food Estate / Tebu (PSN)":           df_i["Tanggapan"].str.contains("food estate|tebu|psn|proyek strategis",case=False,na=False).sum(),
            "Aparat Dianggap Intimidatif":        df_i["Tanggapan"].str.contains("intimidatif|intimidasi|pengamanan.*ketat",case=False,na=False).sum(),
            "Masyarakat Adat vs Korporasi":       df_i["Tanggapan"].str.contains("korporasi|masyarakat adat.*konflik",case=False,na=False).sum(),
            "Kerusakan Ekosistem":                df_i["Tanggapan"].str.contains("ekosida|ekologi|lingkungan.*rusak",case=False,na=False).sum(),
        }
        df_psn = pd.DataFrame(list(psn.items()),columns=["Aspek","Jumlah"])
        df_psn = df_psn[df_psn["Jumlah"]>0].sort_values("Jumlah")
        fig_psn = px.bar(
            df_psn, x="Jumlah", y="Aspek", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_GN,
            title="Dimensi Konflik Lahan & PSN yang Dilaporkan KII",
            text="Jumlah",
        )
        fig_psn.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_psn.update_layout(**PLOT_LAYOUT, showlegend=False, height=360,
                              coloraxis_showscale=False,
                              yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_psn, use_container_width=True)

    with col_h:
        st.markdown("#### 📣 Suara Narasumber tentang PSN & Lahan")
        psn_rows = df_i[df_i["Tanggapan"].str.contains(
            "food estate|penggusuran|deforestasi|ulayat|psn|korporasi|ekosida",
            case=False,na=False)].head(4)
        for _, row in psn_rows.iterrows():
            txt = str(row["Tanggapan"])[:260]+"…" if len(str(row["Tanggapan"]))>260 else str(row["Tanggapan"])
            st.markdown(f"""<div class='qbox qbox-green'>&ldquo;{txt}&rdquo;
            <br><small>— {row.get('Narsum','')} | {row.get('Wilayah','')}</small></div>""",
                        unsafe_allow_html=True)

    # ── ISU 5: KUALITAS PENDIDIKAN ────────────────────────────────────
    st.markdown("<div class='sec-hdr'>📚 Isu 5 — Krisis Kualitas Pendidikan & Tata Kelola Guru</div>",
                unsafe_allow_html=True)
    col_i, col_j = st.columns(2)
    with col_i:
        pend = {
            "Guru Mengajar Demi Gaji Saja":   df_i["Tanggapan"].str.contains("panggilan.*guru|guru.*panggilan|hanya.*rutinitas|hanya.*gaji",case=False,na=False).sum(),
            "Honor Guru Terlambat":           df_i["Tanggapan"].str.contains("honor.*terlambat|terlambat.*honor|apbd.*tidak cukup",case=False,na=False).sum(),
            "PAUD Tidak Fungsional":          df_i["Tanggapan"].str.contains("paud.*tidak berjalan|tidak ada tenaga|bup.*bantuan",case=False,na=False).sum(),
            "Bangunan PAUD Bermasalah":       df_i["Tanggapan"].str.contains("rumah pribadi|sertifikat.*gedung|bangunan.*paud",case=False,na=False).sum(),
            "Putus Sekolah akibat Konflik":   df_i["Tanggapan"].str.contains("putus sekolah|sekolah.*ditutup|guru.*absen",case=False,na=False).sum(),
            "Siswa SD Terinfeksi HIV":        df_i["Tanggapan"].str.contains("kelas 5.*hiv|sd.*hiv|hiv.*anak",case=False,na=False).sum(),
        }
        df_pd = pd.DataFrame(list(pend.items()),columns=["Isu","Jumlah"])
        df_pd = df_pd[df_pd["Jumlah"]>0].sort_values("Jumlah")
        fig_pd = px.bar(
            df_pd, x="Jumlah", y="Isu", orientation="h",
            color="Jumlah", color_continuous_scale=C_SEQ_BL,
            title="Isu Pendidikan yang Diidentifikasi Narasumber",
            text="Jumlah",
        )
        fig_pd.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=12))
        fig_pd.update_layout(**PLOT_LAYOUT, showlegend=False, height=340,
                             coloraxis_showscale=False,
                             yaxis=dict(autorange="reversed", **PLOT_LAYOUT["yaxis"]))
        st.plotly_chart(fig_pd, use_container_width=True)

    with col_j:
        ske = {
            "Keamanan Fluktuatif":      df_i["Tanggapan"].str.contains("keamanan.*fluktuatif|rawan.*konflik|keamanan.*terkendali",case=False,na=False).sum(),
            "Krisis Pangan / Inflasi":  df_i["Tanggapan"].str.contains("pangan|inflasi|harga.*naik|logistik.*terganggu",case=False,na=False).sum(),
            "Trauma Psikososial":       df_i["Tanggapan"].str.contains("trauma|psikososial|ketakutan|kecemasan",case=False,na=False).sum(),
            "Putus Sekolah Sementara":  df_i["Tanggapan"].str.contains("putus sekolah|absensi.*sekolah|sekolah.*ditutup",case=False,na=False).sum(),
            "Konflik Lahan Meningkat":  df_i["Tanggapan"].str.contains("lahan.*meningkat|sengketa.*lahan|konflik.*lahan",case=False,na=False).sum(),
        }
        df_sk = pd.DataFrame(list(ske.items()),columns=["Skenario","Jumlah"])
        df_sk = df_sk[df_sk["Jumlah"]>0].sort_values("Jumlah",ascending=False)
        fig_sk = px.bar(
            df_sk, x="Skenario", y="Jumlah",
            color="Jumlah", color_continuous_scale=C_SEQ_OR,
            title="Proyeksi Risiko 6 Bulan ke Depan (menurut KII)",
            text="Jumlah",
        )
        fig_sk.update_traces(textposition="outside", textfont=dict(color="#1B2A4A",size=11))
        fig_sk.update_layout(**PLOT_LAYOUT, showlegend=False, height=340,
                             coloraxis_showscale=False, xaxis_tickangle=-20)
        st.plotly_chart(fig_sk, use_container_width=True)

    # ── HEATMAP KII ───────────────────────────────────────────────────
    st.markdown("<div class='sec-hdr'>🗺️ Intensitas Isu KII per Wilayah (Heatmap)</div>",
                unsafe_allow_html=True)
    twi = FI_.groupby(["Wilayah","Tema_List"]).size().reset_index(name="Jumlah")
    twi = twi[twi["Tema_List"]!="Kehidupan Sehari-hari & Lainnya"]
    pivot_i = twi.pivot(index="Tema_List",columns="Wilayah",values="Jumlah").fillna(0)
    fig_hmi = px.imshow(
        pivot_i, color_continuous_scale="Blues",
        title="Intensitas Isu per Wilayah — KII (Narasumber Pemerintah)",
        aspect="auto", text_auto=True,
    )
    fig_hmi.update_traces(textfont=dict(color="#1B2A4A", size=12))
    fig_hmi.update_layout(**PLOT_LAYOUT, height=380)
    st.plotly_chart(fig_hmi, use_container_width=True)

    with st.expander("📋 Lihat Data Mentah — Dataset KII"):
        st.dataframe(FI[["Wilayah","Narsum","Pertanyaan","Tanggapan"]],
                     use_container_width=True, height=340)

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — LAPORAN EKSEKUTIF
# ══════════════════════════════════════════════════════════════════════
with tab3:

    st.markdown("## 📄 Laporan Eksekutif — Analisis Isu Papua (GECAR 2024–2025)")
    st.markdown("---")

    st.markdown("""<div class='sec-hdr'>🧩 BAGIAN A — ISU UTAMA: MASYARAKAT (FGD Kelompok)</div>""",
                unsafe_allow_html=True)

    issues_k = [
        ("icard",        "🔴 ISU 1 — Kekerasan Domestik sebagai Ketakutan Utama Anak",
         "Responden anak dari ketiga wilayah menyebut <b>kekerasan fisik dari orang tua</b> sebagai ketakutan nomor satu, "
         "melebihi konflik sosial maupun bencana alam. Anak-anak melaporkan melarikan diri ke rumah nenek atau ke gereja "
         "untuk menghindari kekerasan. Ini merupakan sinyal kuat bahwa <b>program parenting positif dan perlindungan anak "
         "di tingkat komunitas sangat mendesak</b>."),
        ("icard icard-orange","🍺 ISU 2 — Miras sebagai Pemicu Utama Kekerasan Komunitas",
         "Miras disebut sebagai penyebab langsung kekerasan fisik, pencurian, perselingkuhan, dan perang suku di seluruh "
         "wilayah. Di Asmat, miras terkait kekerasan saat dana bantuan cair. Di Sentani, dikaitkan dengan kenakalan remaja "
         "dan pelecehan perempuan. Di Jayawijaya, miras memicu perang suku yang berujung pembunuhan. Pola lintas wilayah ini "
         "menunjukkan miras sebagai <b>amplifier kerentanan</b> yang membutuhkan regulasi dan program alternatif sosial."),
        ("icard icard-orange","💸 ISU 3 — Korupsi Sistemik Dana Bantuan (BLT) oleh Oknum Kepala Kampung",
         "Masyarakat Asmat melaporkan: BLT dipotong Rp200.000–300.000/KK untuk kepentingan pribadi; kepala kampung "
         "dipilih langsung oleh bupati karena merupakan tim sukses; penerima manfaat dicoret jika tidak memihak kepala "
         "kampung. Ini adalah <b>korupsi berjamaah terstruktur</b> yang merusak kepercayaan masyarakat terhadap "
         "seluruh sistem pemerintahan kampung."),
        ("icard icard-blue","📚 ISU 4 — Pendidikan Terganggu oleh Konflik, Kemiskinan & Kurangnya Pendampingan",
         "Anak-anak putus sekolah akibat pemalangan jalan, konflik, kemiskinan yang memaksa bekerja, serta kurangnya "
         "dukungan orang tua. Bagi responden anak, <b>sekolah adalah ruang aman satu-satunya</b> dari kekerasan di "
         "rumah dan komunitas. Akses pendidikan yang terputus berarti hilangnya perlindungan sosial utama mereka."),
        ("icard icard-green","🌱 ISU 5 — Potensi Pemuda yang Belum Difasilitasi",
         "Responden muda menunjukkan kesadaran tinggi: berkontribusi di rumah baca, mengajar adik, berperan di gereja, "
         "memotivasi teman yang putus sekolah. Namun potensi ini <b>belum difasilitasi secara terstruktur</b>. "
         "Harapan mereka konkret: lapangan olahraga, alat musik, kegiatan bazaar, dan forum kepemudaan aktif."),
    ]
    for cls, title, body in issues_k:
        st.markdown(f"""<div class='{cls}'><b>{title}</b><br><br>{body}</div>""",
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div class='sec-hdr'>🏛️ BAGIAN B — ISU UTAMA: NARASUMBER PEMERINTAH (KII)</div>""",
                unsafe_allow_html=True)

    issues_i = [
        ("icard",             "🔫 ISU 1 — Konflik Bersenjata Kelompok Separatis di Jayawijaya",
         "Narasumber GTY, JPY, ACL mengidentifikasi kelompok sipil bersenjata pimpinan Egianus Kogoya sebagai ancaman "
         "utama di Nduga dan Jayawijaya — berstruktur militer-politik, memiliki jaringan internasional di Pasifik Selatan. "
         "Anak-anak menjadi korban tidak langsung melalui <b>keterbatasan akses pendidikan dan trauma berkepanjangan</b>. "
         "Pembebasan pilot Susi Air (2024) membuktikan komunikasi berbasis kemanusiaan lebih efektif dari pendekatan militer."),
        ("icard icard-orange","💊 ISU 2 — Krisis Narkoba & HIV pada Anak di Sentani",
         "Dinas Sosial dan Dinas Pendidikan Sentani melaporkan: anak SD menggunakan narkoba (ditemukan BNN); anak-anak "
         "menghirup aibon di jalanan; <b>siswa kelas 5 SD terinfeksi HIV/AIDS</b> (diduga korban kekerasan seksual "
         "berbasis alkohol/narkoba); fasilitas rehabilitasi sangat terbatas. Akar masalah: keluarga broken home, "
         "tidak ada ruang bermain gratis, dan lemahnya pengawasan. Butuh <b>intervensi lintas sektor yang mendesak</b>."),
        ("icard icard-green", "🌿 ISU 3 — Konflik Lahan & Ekosida: PSN vs Masyarakat Adat (Asmat/Merauke)",
         "PSN food estate dan perkebunan tebu di Papua Selatan menyebabkan: deforestasi lahan gambut/rawa, penggusuran "
         "masyarakat adat tanpa konsultasi, konflik identitas Malind vs Mappi/Asmat dalam perebutan birokrasi, serta "
         "kehadiran militer yang dianggap intimidatif. Masyarakat adat memandang tanah sebagai <b>sakral secara budaya</b>. "
         "Berpotensi eskalasi jika tidak ada audit sosial yang transparan dan partisipatif."),
        ("icard icard-blue",  "📚 ISU 4 — Kualitas Pendidikan Rendah: Guru Demi Gaji, PAUD Fiktif",
         "Dinas Pendidikan Sentani: guru OAP mengajar <i>'hanya sebagai rutinitas dan mengincar gaji, bukan panggilan.'</i> "
         "PAUD dibuka hanya untuk dana BUP tanpa tenaga bersertifikat; bangunannya rumah pribadi yang tidak lolos syarat "
         "pencairan. Honor guru sering terlambat karena APBD tidak mencukupi. Kondisi ini menghasilkan "
         "<b>generasi yang kehilangan fondasi pendidikan sejak usia dini</b>."),
        ("icard icard-purple","📈 ISU 5 — Inflasi Tertinggi Nasional & Ketergantungan Jalur Udara",
         "BPS 2024: Papua Pegunungan mencatat <b>inflasi tertinggi nasional 5,65%</b>. Wamena sebagai pintu udara utama "
         "sangat rentan: setiap gangguan cuaca, keamanan, atau logistik langsung memicu kenaikan harga dan keresahan sosial. "
         "Narasumber menekankan perlunya <b>stok logistik buffer dan alternatif jalur distribusi</b> sebagai prioritas."),
    ]
    for cls, title, body in issues_i:
        st.markdown(f"""<div class='{cls}'><b>{title}</b><br><br>{body}</div>""",
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div class='sec-hdr'>✅ REKOMENDASI STRATEGIS UNTUK WVI & MITRA PROGRAM</div>""",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🏠 Perlindungan Anak & Pengasuhan Positif**
        - Program parenting positif untuk mengurangi kekerasan domestik
        - Posko ramah anak dan konseling berbasis komunitas
        - Pusat kegiatan pemuda yang terjangkau dan aman

        **💊 Intervensi Narkoba & Kesehatan Remaja**
        - Kerjasama WVI–BNN untuk penyuluhan aktif di sekolah
        - Dukungan fasilitasi ruang rehabilitasi komunitas
        - Edukasi kesehatan reproduksi & HIV untuk remaja

        **📚 Penguatan Pendidikan & Kapasitas Guru**
        - Program penyegaran guru: "Mengajar sebagai Panggilan"
        - Advokasi perbaikan status bangunan PAUD (syarat administrasi)
        - Beasiswa dan program mentoring anak putus sekolah
        """)
    with col2:
        st.markdown("""
        **💸 Akuntabilitas Dana Bantuan**
        - Mekanisme pelaporan warga atas penyalahgunaan BLT
        - Advokasi transparansi distribusi dana desa ke pemerintah
        - Pemberdayaan BAMUSKAM sebagai checks & balances

        **🌿 Advokasi Lahan & Pembangunan Damai**
        - Pendampingan hukum berbasis HAM untuk masyarakat adat Asmat
        - Dialog "Para-Para Adat" untuk mediasi konflik lokal
        - Dorong audit sosial PSN sebelum ekspansi proyek

        **🔐 Ketahanan Pangan & Logistik**
        - Program tabungan komunitas (ASKA) untuk antisipasi krisis pangan
        - Pengembangan kebun komunal & kelompok tani sebagai buffer lokal
        - Koordinasi stok pangan buffer dengan pemerintah daerah
        """)

    st.markdown("---")
    st.caption(
        "📊 Dashboard ini dibuat berdasarkan analisis data kualitatif GECAR 2024–2025. "
        "Frekuensi mencerminkan kemunculan tema dalam tanggapan, bukan persentase absolut. "
        "Data dikumpulkan dari Jayawijaya, Sentani, dan Asmat, Papua."
    )
