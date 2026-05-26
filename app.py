"""
GECAR Dashboard — Analisis Kondisi Sosial Papua
Streamlit Dashboard | Senior Data Scientist Edition
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GECAR — Dashboard Analisis Sosial Papua",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2130, #252836);
        border: 1px solid #2e3250;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    [data-testid="metric-container"] label { color: #9ca3af !important; font-size: 0.78rem !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.6rem !important; font-weight: 700; }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #1a1f35, #1e2540);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 10px 0;
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .insight-box strong { color: #a5b4fc; }

    .insight-box-red {
        background: linear-gradient(135deg, #1f1a1a, #2a1e1e);
        border-left: 4px solid #ef4444;
    }
    .insight-box-red strong { color: #fca5a5; }

    .insight-box-green {
        background: linear-gradient(135deg, #1a1f1a, #1e2a1e);
        border-left: 4px solid #22c55e;
    }
    .insight-box-green strong { color: #86efac; }

    .insight-box-yellow {
        background: linear-gradient(135deg, #1f1e1a, #2a261e);
        border-left: 4px solid #f59e0b;
    }
    .insight-box-yellow strong { color: #fcd34d; }

    /* Section header */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e2e8f0;
        padding: 6px 0 4px;
        border-bottom: 2px solid #6366f1;
        margin-bottom: 14px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: #1a1d27; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; color: #9ca3af; font-weight: 600; padding: 8px 20px; }
    .stTabs [aria-selected="true"] { background: #6366f1 !important; color: white !important; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #13161f; border-right: 1px solid #2e3250; }

    /* Quote card */
    .quote-card {
        background: #1a1d27;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 6px 0;
        border: 1px solid #2e3250;
        font-style: italic;
        color: #94a3b8;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    .quote-meta { font-style: normal; font-size: 0.75rem; color: #6366f1; margin-top: 6px; font-weight: 600; }

    /* Badge */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 700;
        margin: 2px;
    }
    .badge-red { background: #3b1515; color: #fca5a5; border: 1px solid #ef4444; }
    .badge-yellow { background: #2d2510; color: #fde68a; border: 1px solid #f59e0b; }
    .badge-blue { background: #151e3b; color: #93c5fd; border: 1px solid #3b82f6; }
    .badge-green { background: #15301e; color: #86efac; border: 1px solid #22c55e; }
    .badge-purple { background: #201535; color: #d8b4fe; border: 1px solid #a855f7; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    paths = [
        ("Gecar_-_Kelompok.csv", "Gecar_-_KII.csv"),
        ("/mnt/user-data/uploads/Gecar_-_Kelompok.csv", "/mnt/user-data/uploads/Gecar_-_KII.csv"),
    ]
    for p1, p2 in paths:
        if os.path.exists(p1) and os.path.exists(p2):
            df_k = pd.read_csv(p1)
            df_k2 = pd.read_csv(p2)
            return df_k, df_k2
    st.error("❌ File CSV tidak ditemukan. Pastikan 'Gecar_-_Kelompok.csv' dan 'Gecar_-_KII.csv' ada di direktori yang sama dengan app.py.")
    st.stop()

df_kelompok, df_kii = load_data()

# ─────────────────────────────────────────────
# KEYWORD EXTRACTION HELPER
# ─────────────────────────────────────────────

ISSUE_KEYWORDS = {
    "Narkoba/Aibon/Miras": [
        "narkoba", "aibon", "miras", "mabuk", "alkohol", "zat", "obat terlarang",
        "pecandu", "rehabilitasi", "bnn", "hiv", "narkotika"
    ],
    "Kekerasan & Konflik Suku": [
        "perang suku", "kekerasan", "konflik", "bentrok", "senjata", "sajam",
        "parang", "korban", "pembunuhan", "begal", "serang", "tembak"
    ],
    "Ketimpangan & Korupsi Dana": [
        "korupsi", "dana desa", "add", "kepala kampung", "tidak transparan",
        "dipotong", "tidak merata", "orang tertentu", "nepotisme", "musrenbang",
        "bantuan tidak sampai", "pemotongan", "blt"
    ],
    "Akses Pendidikan": [
        "sekolah", "pendidikan", "guru", "belajar", "pelajar", "kurikulum",
        "honor guru", "paud", "sd", "rusak", "palang sekolah", "putus sekolah",
        "tidak sekolah", "bangunan rusak", "tenaga pengajar"
    ],
    "Kebutuhan Dasar & Infrastruktur": [
        "air bersih", "sanitasi", "jalan", "rumah", "pangan", "blong",
        "penampungan air", "infrastruktur", "speed", "fiber", "kamar mandi",
        "kebun apung", "sumur", "pah", "banjir", "beras"
    ],
    "Trauma & Keamanan Anak": [
        "trauma", "anak", "remaja", "rentan", "korban", "ikut perang",
        "ketakutan", "kehilangan", "penyanderaan", "putus sekolah",
        "anak jalanan", "tidak aman", "berisiko"
    ],
    "Polarisasi Identitas (OAP vs Pendatang)": [
        "oap", "pendatang", "diskriminasi", "rasisme", "orang asli papua",
        "suku", "identitas", "ketidakpercayaan", "polarisasi", "kesenjangan"
    ],
    "Hoaks & Media Sosial": [
        "hoaks", "medsos", "media sosial", "whatsapp", "provokasi", "rumor",
        "informasi palsu", "digital", "internet", "literasi"
    ],
    "Peran Gereja & Tokoh Adat": [
        "gereja", "tokoh adat", "ibadah", "agama", "hamba tuhan", "pastor",
        "pendeta", "tokoh agama", "adat", "bakar batu", "kekerabatan"
    ],
    "Sengketa Tanah": [
        "tanah", "sengketa", "batas wilayah", "hak milik", "pemalangan",
        "kepemilikan", "pelepasan tanah", "lahan"
    ],
}

def tag_issues(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    text_lower = text.lower()
    found = []
    for label, keywords in ISSUE_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(label)
    return found if found else ["Aspirasi Umum / Lainnya"]


def build_issue_df(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        issues = tag_issues(str(row["Tanggapan"]))
        for isu in issues:
            entry = {col: row[col] for col in group_cols}
            entry["Isu"] = isu
            rows.append(entry)
    return pd.DataFrame(rows)


# Build issue dataframes
issue_k = build_issue_df(
    df_kelompok,
    ["Wilayah", "Kelompok_Usia", "Jenis_Kelamin", "Pertanyaan", "Tanggapan"]
)
issue_kii = build_issue_df(
    df_kii,
    ["Wilayah", "Narsum", "Pertanyaan", "Tanggapan"]
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏔️ GECAR Dashboard")
    st.markdown("<small style='color:#6b7280'>Analisis Kondisi Sosial Papua</small>", unsafe_allow_html=True)
    st.divider()

    st.markdown("### 🔍 Filter Global")

    all_wilayah = sorted(df_kelompok["Wilayah"].unique().tolist() + [w for w in df_kii["Wilayah"].unique() if w not in df_kelompok["Wilayah"].tolist()])
    sel_wilayah = st.multiselect("Wilayah", all_wilayah, default=all_wilayah)

    st.divider()
    st.markdown("### 📊 Filter Dataset 1 (Kelompok)")
    all_usia = sorted(df_kelompok["Kelompok_Usia"].unique().tolist())
    sel_usia = st.multiselect("Kelompok Usia", all_usia, default=all_usia)

    all_gender = sorted(df_kelompok["Jenis_Kelamin"].unique().tolist())
    sel_gender = st.multiselect("Jenis Kelamin", all_gender, default=all_gender)

    st.divider()
    st.markdown("### 📋 Filter Dataset 2 (KII)")
    all_narsum = sorted(df_kii["Narsum"].unique().tolist())
    sel_narsum = st.multiselect("Narasumber", all_narsum, default=all_narsum)

    st.divider()
    st.caption("© 2025 GECAR Analysis | WVI Program")

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
def flt_k(df, isu):
    mask = (
        df["Wilayah"].isin(sel_wilayah) &
        df["Kelompok_Usia"].isin(sel_usia) &
        df["Jenis_Kelamin"].isin(sel_gender)
    )
    return isu[mask] if isinstance(isu, pd.DataFrame) else df[mask]

def flt_kii(df, isu):
    mask = (
        df["Wilayah"].isin(sel_wilayah) &
        df["Narsum"].isin(sel_narsum)
    )
    return isu[mask] if isinstance(isu, pd.DataFrame) else df[mask]

dk = df_kelompok[
    df_kelompok["Wilayah"].isin(sel_wilayah) &
    df_kelompok["Kelompok_Usia"].isin(sel_usia) &
    df_kelompok["Jenis_Kelamin"].isin(sel_gender)
].copy()

dk2 = df_kii[
    df_kii["Wilayah"].isin(sel_wilayah) &
    df_kii["Narsum"].isin(sel_narsum)
].copy()

ik = issue_k[
    issue_k["Wilayah"].isin(sel_wilayah) &
    issue_k["Kelompok_Usia"].isin(sel_usia) &
    issue_k["Jenis_Kelamin"].isin(sel_gender)
].copy()

ik2 = issue_kii[
    issue_kii["Wilayah"].isin(sel_wilayah) &
    issue_kii["Narsum"].isin(sel_narsum)
].copy()

# ─────────────────────────────────────────────
# PLOTLY TEMPLATE
# ─────────────────────────────────────────────
TMPL = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(20,22,35,0.6)",
        font=dict(color="#cbd5e1", family="Inter, sans-serif", size=12),
        title=dict(font=dict(color="#e2e8f0", size=14)),
        xaxis=dict(gridcolor="#1e2540", zerolinecolor="#1e2540"),
        yaxis=dict(gridcolor="#1e2540", zerolinecolor="#1e2540"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)),
        colorway=["#6366f1","#22c55e","#f59e0b","#ef4444","#06b6d4","#a855f7","#f97316","#14b8a6","#e879f9","#84cc16"],
    )
)
COLORS = ["#6366f1","#22c55e","#f59e0b","#ef4444","#06b6d4","#a855f7","#f97316","#14b8a6","#e879f9","#84cc16"]


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(135deg, #1a1d27 0%, #1e2540 100%);
            border-radius: 16px; padding: 24px 32px; margin-bottom: 20px;
            border: 1px solid #2e3250;'>
    <h1 style='margin:0; color:#e2e8f0; font-size:1.9rem; font-weight:800;'>
        🏔️ GECAR — Dashboard Analisis Kondisi Sosial Papua
    </h1>
    <p style='margin:6px 0 0; color:#94a3b8; font-size:0.9rem;'>
        Visualisasi interaktif tanggapan masyarakat & pemangku kepentingan di wilayah Papua |
        <strong style='color:#6366f1;'>Jayawijaya · Asmat · Sentani</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP METRICS
# ─────────────────────────────────────────────
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("📝 Total Tanggapan Kelompok", f"{len(dk):,}")
m2.metric("🏛️ Total Tanggapan KII", f"{len(dk2):,}")
m3.metric("📍 Wilayah Aktif", f"{len(dk['Wilayah'].unique()) + len(dk2['Wilayah'].unique())} wilayah")
m4.metric("🎯 Isu Teridentifikasi", f"{ik['Isu'].nunique()} kategori")
m5.metric("👥 Resp. Anak (Kelompok)", f"{len(dk[dk['Kelompok_Usia']=='Anak']):,}")
m6.metric("🏢 Narsum Pemerintah", f"{dk2['Narsum'].nunique()} instansi")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab_overview, tab_kelompok, tab_kii, tab_laporan = st.tabs([
    "📊 Ringkasan Isu",
    "👥 Dataset 1 — Tanggapan Masyarakat",
    "🏛️ Dataset 2 — Narasumber Pemerintah",
    "📄 Laporan Eksekutif"
])

# ════════════════════════════════════════════════════════
# TAB 1 — RINGKASAN ISU
# ════════════════════════════════════════════════════════
with tab_overview:
    st.markdown("<div class='section-header'>🔎 Gambaran Lintas Dataset — Isu Dominan</div>", unsafe_allow_html=True)

    # Combined issue count
    ik_top = ik["Isu"].value_counts().reset_index()
    ik_top.columns = ["Isu", "Jumlah"]
    ik_top["Sumber"] = "Masyarakat (Kelompok)"

    ik2_top = ik2["Isu"].value_counts().reset_index()
    ik2_top.columns = ["Isu", "Jumlah"]
    ik2_top["Sumber"] = "Pemerintah (KII)"

    combined = pd.concat([ik_top, ik2_top])

    fig_compare = px.bar(
        combined, x="Jumlah", y="Isu", color="Sumber", barmode="group",
        orientation="h", title="Perbandingan Isu Dominan: Masyarakat vs. Pemangku Kepentingan",
        color_discrete_map={"Masyarakat (Kelompok)": "#6366f1", "Pemerintah (KII)": "#22c55e"},
        template=TMPL,
    )
    fig_compare.update_layout(height=480, yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig_compare, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-header'>🔴 Top 5 Isu — Masyarakat</div>", unsafe_allow_html=True)
        top5k = ik["Isu"].value_counts().head(5)
        fig_pk = px.pie(
            values=top5k.values, names=top5k.index,
            color_discrete_sequence=COLORS, template=TMPL,
            hole=0.45, title="Distribusi Isu Kelompok Masyarakat"
        )
        fig_pk.update_traces(textinfo="label+percent")
        st.plotly_chart(fig_pk, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>🏛️ Top 5 Isu — Narasumber Pemerintah</div>", unsafe_allow_html=True)
        top5k2 = ik2["Isu"].value_counts().head(5)
        fig_pk2 = px.pie(
            values=top5k2.values, names=top5k2.index,
            color_discrete_sequence=COLORS[::-1], template=TMPL,
            hole=0.45, title="Distribusi Isu Narasumber KII"
        )
        fig_pk2.update_traces(textinfo="label+percent")
        st.plotly_chart(fig_pk2, use_container_width=True)

    # Heatmap: Isu per Wilayah (Kelompok)
    st.markdown("<div class='section-header'>🗺️ Peta Panas Isu per Wilayah</div>", unsafe_allow_html=True)
    heatmap_k = ik.groupby(["Wilayah", "Isu"]).size().reset_index(name="n")
    heatmap_pivot = heatmap_k.pivot_table(index="Isu", columns="Wilayah", values="n", fill_value=0)
    fig_hm = px.imshow(
        heatmap_pivot,
        color_continuous_scale="Viridis",
        title="Intensitas Isu per Wilayah — Tanggapan Masyarakat",
        template=TMPL,
        aspect="auto",
        text_auto=True,
    )
    fig_hm.update_layout(height=500, coloraxis_colorbar=dict(title="Frekuensi"))
    st.plotly_chart(fig_hm, use_container_width=True)

    # Key findings
    st.markdown("<div class='section-header'>💡 Temuan Kunci Lintas Dataset</div>", unsafe_allow_html=True)
    insights = [
        ("🔴", "insight-box-red",
         "<strong>Krisis Penyalahgunaan Zat pada Anak & Remaja</strong>",
         "Isu narkoba, aibon, dan miras konsisten muncul di ketiga wilayah. Dinas Sosial Sentani "
         "mengkonfirmasi adanya anak SD yang terinfeksi HIV diduga terkait kekerasan seksual berbasis zat. "
         "Ini menunjukkan rantai krisis yang jauh lebih dalam dari sekadar kenakalan remaja."),
        ("🔴", "insight-box-red",
         "<strong>Korupsi & Ketimpangan Distribusi Bantuan</strong>",
         "Asmat melaporkan bantuan dari pemerintah (ADD, musrenbang) hanya mengalir ke keluarga kepala "
         "kampung dan kontraktor tertentu. Jayawijaya menyebut dana desa yang tidak transparan sebagai "
         "pemicu ketegangan sosial. Polarisasi antara yang 'mendapat' dan 'tidak mendapat' memperparah konflik."),
        ("🟡", "insight-box-yellow",
         "<strong>Perang Suku & Trauma Intergenerasi pada Anak</strong>",
         "Jayawijaya mencatat anak usia 10 tahun ke atas sudah dilibatkan dalam perang suku. Akibatnya, "
         "anak-anak memiliki mindset bahwa 'perang seperti bermain bola', kehilangan motivasi bersekolah, "
         "dan mewarisi siklus kekerasan dari generasi ke generasi."),
        ("🟡", "insight-box-yellow",
         "<strong>Krisis Pendidikan: Infrastruktur & Komitmen Guru</strong>",
         "Dinas Pendidikan Sentani mengidentifikasi gedung SD yang rusak, PAUD fiktif yang dibentuk hanya "
         "demi dana BUP, pemalangan sekolah akibat sengketa tanah, hingga honor guru yang terlambat. "
         "Kombinasi ini menciptakan lingkungan belajar yang rapuh dan tidak berkelanjutan."),
        ("🔵", "insight-box",
         "<strong>Hoaks & Media Sosial Sebagai Akselerator Konflik</strong>",
         "Narasumber ACL (Jayawijaya) menyatakan bahwa konflik di Wamena kini semakin mudah terpicu "
         "oleh pesan berantai di grup WhatsApp, bahkan sebelum kejadian nyata terjadi. "
         "Literasi digital yang rendah memperbesar potensi eskalasi."),
    ]
    for icon, cls, title, body in insights:
        st.markdown(f"""
        <div class='insight-box {cls}'>
            {icon} {title}<br><br>{body}
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 2 — KELOMPOK MASYARAKAT
# ════════════════════════════════════════════════════════
with tab_kelompok:
    st.markdown("<div class='section-header'>👥 Dataset 1 — Tanggapan Kelompok Masyarakat</div>", unsafe_allow_html=True)

    # Distribusi demografi
    st.markdown("#### 📊 Demografi Responden")
    c1, c2, c3 = st.columns(3)

    with c1:
        dist_w = dk.groupby("Wilayah").size().reset_index(name="n")
        fig_w = px.pie(dist_w, values="n", names="Wilayah",
                       title="Distribusi per Wilayah",
                       color_discrete_sequence=COLORS, hole=0.4, template=TMPL)
        fig_w.update_traces(textinfo="label+percent")
        st.plotly_chart(fig_w, use_container_width=True)

    with c2:
        dist_u = dk.groupby("Kelompok_Usia").size().reset_index(name="n")
        fig_u = px.pie(dist_u, values="n", names="Kelompok_Usia",
                       title="Kelompok Usia",
                       color_discrete_sequence=["#6366f1","#22c55e"], hole=0.4, template=TMPL)
        fig_u.update_traces(textinfo="label+percent")
        st.plotly_chart(fig_u, use_container_width=True)

    with c3:
        dist_g = dk.groupby("Jenis_Kelamin").size().reset_index(name="n")
        fig_g = px.pie(dist_g, values="n", names="Jenis_Kelamin",
                       title="Jenis Kelamin",
                       color_discrete_sequence=["#06b6d4","#f97316"], hole=0.4, template=TMPL)
        fig_g.update_traces(textinfo="label+percent")
        st.plotly_chart(fig_g, use_container_width=True)

    st.divider()

    # ── ISU 1: Narkoba/Aibon/Miras ──
    st.markdown("### 🔴 Isu 1 — Penyalahgunaan Zat: Narkoba, Aibon, dan Miras")
    st.markdown("""
    <div class='insight-box insight-box-red'>
    <strong>Temuan kritis:</strong> Penyalahgunaan zat adalah isu lintas wilayah dan lintas usia yang paling berdampak langsung pada keamanan komunitas dan masa depan anak-anak.
    Tanggapan menyebut narkoba, aibon, miras, hingga ganja secara eksplisit sebagai pemicu kekerasan, pencurian, dan perang antar kelompok.
    </div>""", unsafe_allow_html=True)

    drug_data = ik[ik["Isu"] == "Narkoba/Aibon/Miras"]
    c1, c2 = st.columns(2)
    with c1:
        dd_w = drug_data.groupby("Wilayah").size().reset_index(name="Frekuensi Penyebutan")
        fig_d1 = px.bar(dd_w, x="Wilayah", y="Frekuensi Penyebutan",
                        title="Frekuensi Isu Zat Berbahaya per Wilayah",
                        color="Wilayah", color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_d1, use_container_width=True)
    with c2:
        dd_ug = drug_data.groupby(["Kelompok_Usia","Jenis_Kelamin"]).size().reset_index(name="n")
        fig_d2 = px.bar(dd_ug, x="Kelompok_Usia", y="n", color="Jenis_Kelamin",
                        barmode="group",
                        title="Kelompok yang Melaporkan Isu Zat",
                        color_discrete_map={"Laki laki":"#06b6d4","Perempuan":"#f97316"},
                        template=TMPL)
        st.plotly_chart(fig_d2, use_container_width=True)

    st.markdown("**💬 Kutipan Tanggapan Representatif:**")
    drug_quotes = dk[dk["Tanggapan"].str.contains("aibon|narkoba|miras|mabuk|ganja|alkohol", case=False, na=False)].head(6)
    for i, (_, row) in enumerate(drug_quotes.iterrows()):
        st.markdown(f"""<div class='quote-card'>
        "{row['Tanggapan'][:250]}..."
        <div class='quote-meta'>📍 {row['Wilayah']} | {row['Kelompok_Usia']} · {row['Jenis_Kelamin']}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU 2: Korupsi & Ketimpangan Dana ──
    st.markdown("### 🟡 Isu 2 — Korupsi & Ketimpangan Distribusi Dana Pemerintah")
    st.markdown("""
    <div class='insight-box insight-box-yellow'>
    <strong>Temuan penting:</strong> Masyarakat di Asmat dan Jayawijaya secara eksplisit menyebut dana ADD dan bantuan program
    hanya mengalir ke kelompok tertentu (keluarga kepala kampung, kontraktor, pendukung politik).
    Ketidaktransparanan ini menciptakan "bom waktu" sosial karena kebutuhan nyata tidak pernah terpenuhi melalui jalur resmi.
    </div>""", unsafe_allow_html=True)

    dana_data = ik[ik["Isu"] == "Ketimpangan & Korupsi Dana"]
    c1, c2 = st.columns(2)
    with c1:
        dd2_w = dana_data.groupby("Wilayah").size().reset_index(name="Frekuensi")
        fig_dn1 = px.bar(dd2_w, x="Wilayah", y="Frekuensi",
                         title="Keluhan Ketimpangan Dana per Wilayah",
                         color="Wilayah", color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_dn1, use_container_width=True)
    with c2:
        dd2_wu = dana_data.groupby(["Wilayah","Kelompok_Usia"]).size().reset_index(name="n")
        fig_dn2 = px.bar(dd2_wu, x="Wilayah", y="n", color="Kelompok_Usia",
                         barmode="stack",
                         title="Usia Responden yang Melaporkan Ketimpangan Dana",
                         color_discrete_sequence=["#6366f1","#f59e0b"],
                         template=TMPL)
        st.plotly_chart(fig_dn2, use_container_width=True)

    st.markdown("**💬 Kutipan Tanggapan Representatif:**")
    dana_quotes = dk[dk["Tanggapan"].str.contains(
        "add|dana desa|kepala kampung|tidak merata|dipotong|musrenbang|tidak sampai|orang tertentu|kepala kampung|proyek|kontraktor",
        case=False, na=False)].head(5)
    for _, row in dana_quotes.iterrows():
        st.markdown(f"""<div class='quote-card'>
        "{row['Tanggapan'][:300]}..."
        <div class='quote-meta'>📍 {row['Wilayah']} | {row['Kelompok_Usia']} · {row['Jenis_Kelamin']}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU 3: Perang Suku & Trauma Anak ──
    st.markdown("### 🔴 Isu 3 — Perang Suku & Dampak Trauma pada Generasi Muda")
    st.markdown("""
    <div class='insight-box insight-box-red'>
    <strong>Temuan kritis:</strong> Anak-anak di Jayawijaya mulai ikut terlibat dalam konflik suku sejak usia 10 tahun.
    Ibu-ibu melaporkan bahwa anak-anak sudah menormalisasi perang ("seperti main bola") dan kehilangan motivasi bersekolah.
    Ini bukan sekadar masalah keamanan, melainkan krisis pembentukan karakter generasi penerus.
    </div>""", unsafe_allow_html=True)

    konflik_data = ik[ik["Isu"] == "Kekerasan & Konflik Suku"]
    c1, c2 = st.columns(2)
    with c1:
        kd_w = konflik_data.groupby("Wilayah").size().reset_index(name="Frekuensi")
        fig_k1 = px.bar(kd_w, x="Wilayah", y="Frekuensi",
                        title="Laporan Kekerasan & Konflik Suku per Wilayah",
                        color="Wilayah", color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_k1, use_container_width=True)
    with c2:
        kd_ug = konflik_data.groupby(["Kelompok_Usia","Jenis_Kelamin"]).size().reset_index(name="n")
        fig_k2 = px.bar(kd_ug, x="Kelompok_Usia", y="n", color="Jenis_Kelamin",
                        barmode="group",
                        title="Laporan Konflik Berdasarkan Usia & Gender",
                        color_discrete_map={"Laki laki":"#06b6d4","Perempuan":"#f97316"},
                        template=TMPL)
        st.plotly_chart(fig_k2, use_container_width=True)

    st.markdown("**💬 Kutipan Tanggapan Representatif:**")
    konflik_quotes = dk[dk["Tanggapan"].str.contains(
        "perang|pembunuhan|begal|kekerasan|sajam|parang|konflik|perang suku",
        case=False, na=False)].head(5)
    for _, row in konflik_quotes.iterrows():
        st.markdown(f"""<div class='quote-card'>
        "{row['Tanggapan'][:300]}..."
        <div class='quote-meta'>📍 {row['Wilayah']} | {row['Kelompok_Usia']} · {row['Jenis_Kelamin']}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU 4: Akses Pendidikan ──
    st.markdown("### 🔵 Isu 4 — Hambatan Akses & Kualitas Pendidikan")
    st.markdown("""
    <div class='insight-box'>
    <strong>Temuan penting:</strong> Masyarakat Sentani menyebut terbatasnya kuota TK/PAUD, sengketa tanah sekolah,
    dan bangunan rusak sebagai hambatan utama. Di Jayawijaya, perempuan dewasa menekankan pentingnya pendidikan karakter
    dan keterlibatan orang tua. Isu ini berkaitan erat dengan isu kekerasan dan narkoba — anak yang tidak bersekolah
    lebih rentan terjerumus ke pergaulan negatif.
    </div>""", unsafe_allow_html=True)

    pendidikan_data = ik[ik["Isu"] == "Akses Pendidikan"]
    c1, c2 = st.columns(2)
    with c1:
        pd_w = pendidikan_data.groupby("Wilayah").size().reset_index(name="Frekuensi")
        fig_p1 = px.bar(pd_w, x="Wilayah", y="Frekuensi",
                        title="Keluhan Akses Pendidikan per Wilayah",
                        color="Wilayah", color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_p1, use_container_width=True)
    with c2:
        pd_ug = pendidikan_data.groupby(["Kelompok_Usia","Jenis_Kelamin"]).size().reset_index(name="n")
        fig_p2 = px.bar(pd_ug, x="Kelompok_Usia", y="n", color="Jenis_Kelamin",
                        barmode="group",
                        title="Siapa yang Melaporkan Masalah Pendidikan",
                        color_discrete_map={"Laki laki":"#06b6d4","Perempuan":"#f97316"},
                        template=TMPL)
        st.plotly_chart(fig_p2, use_container_width=True)

    st.divider()

    # ── ISU 5: Kebutuhan Dasar & Infrastruktur ──
    st.markdown("### 🟢 Isu 5 — Kebutuhan Dasar & Infrastruktur yang Belum Terpenuhi")
    st.markdown("""
    <div class='insight-box insight-box-green'>
    <strong>Temuan:</strong> Asmat melaporkan kebutuhan mendesak berupa penampungan air hujan, perbaikan kamar mandi,
    renovasi kebun apung, dan jaring ikan. Sentani menyoroti tidak tersedianya hunian memadai seiring pertumbuhan
    penduduk dan luapan sungai. Kebutuhan dasar yang tidak terpenuhi memperdalam kesenjangan dan menjadi lahan subur
    bagi ketegangan sosial.
    </div>""", unsafe_allow_html=True)

    infra_data = ik[ik["Isu"] == "Kebutuhan Dasar & Infrastruktur"]
    c1, c2 = st.columns(2)
    with c1:
        id_w = infra_data.groupby("Wilayah").size().reset_index(name="Frekuensi")
        fig_i1 = px.bar(id_w, x="Wilayah", y="Frekuensi",
                        title="Keluhan Kebutuhan Dasar per Wilayah",
                        color="Wilayah", color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_i1, use_container_width=True)
    with c2:
        # Radar chart per wilayah across top issues
        top_issues = ik["Isu"].value_counts().head(5).index.tolist()
        radar_data = ik[ik["Isu"].isin(top_issues)].groupby(["Wilayah","Isu"]).size().reset_index(name="n")
        fig_radar = go.Figure()
        for i, wil in enumerate(sel_wilayah):
            sub = radar_data[radar_data["Wilayah"]==wil]
            vals = [sub[sub["Isu"]==isu]["n"].sum() for isu in top_issues]
            vals += [vals[0]]  # close
            fig_radar.add_trace(go.Scatterpolar(
                r=vals, theta=top_issues + [top_issues[0]],
                fill="toself", name=wil, line_color=COLORS[i],
            ))
        fig_radar.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(visible=True, gridcolor="#2e3250"),
                       angularaxis=dict(gridcolor="#2e3250")),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1"),
            title="Profil Isu per Wilayah (Radar)",
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            height=380,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.divider()

    # ── Harapan & Ketakutan ──
    st.markdown("### 💚 Harapan vs. Ketakutan Masyarakat")
    harapan_q = dk[dk["Pertanyaan"].str.contains("harapan", case=False, na=False)]
    takut_q = dk[dk["Pertanyaan"].str.contains("ketakutan|takut", case=False, na=False)]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**✨ Kata Kunci Harapan:**")
        # Simple keyword frequency from hopes
        hope_keywords = {"Pendidikan": 0, "Perdamaian": 0, "Ekonomi Lebih Baik": 0,
                         "Pemuda Berkarakter": 0, "Pemerintah Perhatian": 0, "Gereja Berkembang": 0}
        for _, row in harapan_q.iterrows():
            t = str(row["Tanggapan"]).lower()
            if any(k in t for k in ["sekolah","pendidikan","belajar"]): hope_keywords["Pendidikan"] += 1
            if any(k in t for k in ["damai","aman","tentram"]): hope_keywords["Perdamaian"] += 1
            if any(k in t for k in ["ekonomi","kerja","usaha","berkembang"]): hope_keywords["Ekonomi Lebih Baik"] += 1
            if any(k in t for k in ["pemuda","generasi","anak muda","karakter"]): hope_keywords["Pemuda Berkarakter"] += 1
            if any(k in t for k in ["pemerintah","perhatian","kebijakan"]): hope_keywords["Pemerintah Perhatian"] += 1
            if any(k in t for k in ["gereja","ibadah","iman","tuhan"]): hope_keywords["Gereja Berkembang"] += 1
        hdf = pd.DataFrame(list(hope_keywords.items()), columns=["Harapan","Frekuensi"]).sort_values("Frekuensi", ascending=True)
        fig_h = px.bar(hdf, x="Frekuensi", y="Harapan", orientation="h",
                       color_discrete_sequence=["#22c55e"], template=TMPL,
                       title="Tema Harapan Masyarakat")
        st.plotly_chart(fig_h, use_container_width=True)

    with c2:
        st.markdown("**😰 Kata Kunci Ketakutan:**")
        fear_keywords = {"Kehilangan Orang Tua": 0, "Perang/Kekerasan": 0, "Narkoba/Pergaulan Buruk": 0,
                         "Masa Depan Tidak Jelas": 0, "Generasi Tanpa Arah": 0, "Ancaman Alam": 0}
        for _, row in takut_q.iterrows():
            t = str(row["Tanggapan"]).lower()
            if any(k in t for k in ["orang tua","papa","mama","meninggal"]): fear_keywords["Kehilangan Orang Tua"] += 1
            if any(k in t for k in ["perang","kekerasan","parang","sajam","ancaman"]): fear_keywords["Perang/Kekerasan"] += 1
            if any(k in t for k in ["aibon","narkoba","miras","pergaulan","negatif"]): fear_keywords["Narkoba/Pergaulan Buruk"] += 1
            if any(k in t for k in ["tujuan hidup","ke depan","masa depan","tidak tahu"]): fear_keywords["Masa Depan Tidak Jelas"] += 1
            if any(k in t for k in ["generasi","penerus","muda"]): fear_keywords["Generasi Tanpa Arah"] += 1
            if any(k in t for k in ["hujan","angin","pohon","banjir","alam"]): fear_keywords["Ancaman Alam"] += 1
        fdf = pd.DataFrame(list(fear_keywords.items()), columns=["Ketakutan","Frekuensi"]).sort_values("Frekuensi", ascending=True)
        fig_f = px.bar(fdf, x="Frekuensi", y="Ketakutan", orientation="h",
                       color_discrete_sequence=["#ef4444"], template=TMPL,
                       title="Tema Ketakutan Masyarakat")
        st.plotly_chart(fig_f, use_container_width=True)


# ════════════════════════════════════════════════════════
# TAB 3 — KII (PEMERINTAH)
# ════════════════════════════════════════════════════════
with tab_kii:
    st.markdown("<div class='section-header'>🏛️ Dataset 2 — Tanggapan Narasumber KII (Key Informant Interview)</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        dist_n = dk2.groupby(["Wilayah","Narsum"]).size().reset_index(name="n")
        fig_n = px.bar(dist_n, x="Narsum", y="n", color="Wilayah",
                       title="Jumlah Tanggapan per Narasumber & Wilayah",
                       barmode="group", color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_n, use_container_width=True)
    with c2:
        isu_n = ik2.groupby(["Narsum","Isu"]).size().reset_index(name="n")
        top_isu_n = ik2["Isu"].value_counts().head(5).index.tolist()
        isu_n_top = isu_n[isu_n["Isu"].isin(top_isu_n)]
        fig_n2 = px.bar(isu_n_top, x="Narsum", y="n", color="Isu",
                        barmode="stack",
                        title="Distribusi Isu per Narasumber (Top 5 Isu)",
                        color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_n2, use_container_width=True)

    st.divider()

    # ── ISU KII 1: Krisis Narkoba & Anak (Dinas Sosial) ──
    st.markdown("### 🔴 Isu KII 1 — Krisis Anak: Narkoba, Aibon & HIV (Sentani)")
    st.markdown("""
    <div class='insight-box insight-box-red'>
    <strong>Dinas Sosial Sentani</strong> mengungkap adanya anak SD yang terinfeksi HIV (diduga akibat kekerasan seksual
    berbasis narkoba/alkohol), anak-anak yang menggunakan aibon di jalanan, serta pencurian helm sebagai cara
    membiayai kebiasaan tersebut. Penyebab strukturalnya: keluarga broken home, tidak adanya ruang bermain gratis,
    dan terbatasnya fasilitas rehabilitasi.
    </div>""", unsafe_allow_html=True)

    dinsosq = dk2[dk2["Narsum"]=="Dinas Sosial"]
    if not dinsosq.empty:
        dinsos_isu = ik2[ik2["Narsum"]=="Dinas Sosial"]["Isu"].value_counts().reset_index()
        dinsos_isu.columns = ["Isu","n"]
        fig_ds = px.bar(dinsos_isu.head(7), x="n", y="Isu", orientation="h",
                        title="Profil Isu — Dinas Sosial Sentani",
                        color_discrete_sequence=["#ef4444"], template=TMPL)
        fig_ds.update_layout(yaxis=dict(categoryorder="total ascending"))
        c1, c2 = st.columns([3,2])
        with c1:
            st.plotly_chart(fig_ds, use_container_width=True)
        with c2:
            st.markdown("**💬 Kutipan Kunci:**")
            for _, row in dinsosq[dinsosq["Tanggapan"].str.contains(
                    "narkoba|aibon|hiv|rehabilitasi|broken|anak|pencurian", case=False, na=False)].head(4).iterrows():
                st.markdown(f"""<div class='quote-card'>
                "{str(row['Tanggapan'])[:200]}..."
                <div class='quote-meta'>🏛️ Dinas Sosial | Sentani</div>
                </div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU KII 2: Krisis Pendidikan (Dinas Pendidikan) ──
    st.markdown("### 🔵 Isu KII 2 — Krisis Tata Kelola Pendidikan (Sentani)")
    st.markdown("""
    <div class='insight-box'>
    <strong>Dinas Pendidikan Sentani</strong> mengidentifikasi: PAUD fiktif hanya untuk dana BUP, gedung SD rusak
    yang tidak bisa diperbaiki karena sengketa tanah, honor guru yang terlambat akibat kekurangan APBD, serta
    mentalitas guru OAP yang mengajar hanya demi gaji bukan panggilan. Sekolah dipalang oleh pemilik tanah
    sehingga anak-anak tidak bisa bersekolah.
    </div>""", unsafe_allow_html=True)

    dinpendq = dk2[dk2["Narsum"]=="Dinas Pendidikan"]
    if not dinpendq.empty:
        dp_isu = ik2[ik2["Narsum"]=="Dinas Pendidikan"]["Isu"].value_counts().reset_index()
        dp_isu.columns = ["Isu","n"]
        fig_dp = px.bar(dp_isu.head(7), x="n", y="Isu", orientation="h",
                        title="Profil Isu — Dinas Pendidikan Sentani",
                        color_discrete_sequence=["#6366f1"], template=TMPL)
        fig_dp.update_layout(yaxis=dict(categoryorder="total ascending"))
        c1, c2 = st.columns([3,2])
        with c1:
            st.plotly_chart(fig_dp, use_container_width=True)
        with c2:
            st.markdown("**💬 Kutipan Kunci:**")
            for _, row in dinpendq[dinpendq["Tanggapan"].str.contains(
                    "tanah|paud|rusak|honor|guru|palang|bup|dana", case=False, na=False)].head(4).iterrows():
                st.markdown(f"""<div class='quote-card'>
                "{str(row['Tanggapan'])[:200]}..."
                <div class='quote-meta'>🏛️ Dinas Pendidikan | Sentani</div>
                </div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU KII 3: Konflik Bersenjata & KKB (Jayawijaya) ──
    st.markdown("### 🔴 Isu KII 3 — Kelompok Bersenjata & Polarisasi OAP vs. Pendatang (Jayawijaya)")
    st.markdown("""
    <div class='insight-box insight-box-red'>
    Narasumber GTY dan JPY dari Jayawijaya mengkonfirmasi bahwa kelompok sipil bersenjata (termasuk yang berafiliasi
    dengan ideologi Papua Merdeka) beroperasi di Nduga dan Jayawijaya, berdampak langsung pada akses pendidikan anak
    dan keamanan warga sipil. Selain itu, polarisasi antara OAP dan pendatang di lapangan kerja PNS dan ekonomi informal
    menjadi pemicu ketegangan yang terus membara.
    </div>""", unsafe_allow_html=True)

    jay_isu = ik2[ik2["Wilayah"]=="Jayawijaya"]["Isu"].value_counts().reset_index()
    jay_isu.columns = ["Isu","n"]
    c1, c2 = st.columns(2)
    with c1:
        fig_j1 = px.bar(jay_isu.head(8), x="n", y="Isu", orientation="h",
                        title="Profil Isu — Jayawijaya (Semua Narsum)",
                        color="n", color_continuous_scale="Reds", template=TMPL)
        fig_j1.update_layout(yaxis=dict(categoryorder="total ascending"), coloraxis_showscale=False)
        st.plotly_chart(fig_j1, use_container_width=True)
    with c2:
        narsum_comp = ik2[ik2["Wilayah"]=="Jayawijaya"].groupby(["Narsum","Isu"]).size().reset_index(name="n")
        fig_j2 = px.bar(narsum_comp[narsum_comp["Isu"].isin(jay_isu["Isu"].head(5))],
                        x="Narsum", y="n", color="Isu", barmode="stack",
                        title="Perbandingan Isu Antar Narsum — Jayawijaya",
                        color_discrete_sequence=COLORS, template=TMPL)
        st.plotly_chart(fig_j2, use_container_width=True)

    # GTY/JPY quotes about armed groups
    st.markdown("**💬 Kutipan Kunci — Konflik Bersenjata:**")
    arm_quotes = dk2[
        (dk2["Wilayah"]=="Jayawijaya") &
        dk2["Tanggapan"].str.contains("bersenjata|kkb|papua merdeka|nduga|konflik|egianus|tni|polri|keamanan", case=False, na=False)
    ].head(5)
    for _, row in arm_quotes.iterrows():
        st.markdown(f"""<div class='quote-card'>
        "{str(row['Tanggapan'])[:300]}..."
        <div class='quote-meta'>🏛️ {row['Narsum']} | {row['Wilayah']}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU KII 4: Hoaks & Media Sosial ──
    st.markdown("### 🟡 Isu KII 4 — Hoaks & Media Sosial Sebagai Pemantik Konflik")
    st.markdown("""
    <div class='insight-box insight-box-yellow'>
    <strong>Narasumber ACL (Jayawijaya)</strong> secara tegas menyatakan bahwa konflik di Wamena kini dipercepat
    oleh grup WhatsApp yang menyebarkan rumor dan hoaks sebelum kejadian nyata terjadi. Literasi digital yang rendah
    di komunitas akar rumput membuat masyarakat mudah terprovokasi. Ini adalah isu baru yang belum sepenuhnya
    diantisipasi oleh program pembangunan perdamaian konvensional.
    </div>""", unsafe_allow_html=True)

    hoaks_q = dk2[dk2["Tanggapan"].str.contains("hoaks|media sosial|whatsapp|rumor|provokasi|digital", case=False, na=False)]
    if not hoaks_q.empty:
        for _, row in hoaks_q.head(4).iterrows():
            st.markdown(f"""<div class='quote-card'>
            "{str(row['Tanggapan'])[:350]}..."
            <div class='quote-meta'>🏛️ {row['Narsum']} | {row['Wilayah']}</div>
            </div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU KII 5: Skenario 6 Bulan ke Depan ──
    st.markdown("### 🔮 Isu KII 5 — Proyeksi & Kekhawatiran 6 Bulan ke Depan")
    st.markdown("""
    <div class='insight-box'>
    Seluruh narasumber (GTY, JPY, ACL, Dinas Sosial, Dinas Pendidikan) memberikan proyeksi risiko untuk 6 bulan ke depan.
    Tema yang konsisten muncul: krisis pangan & inflasi, stabilitas pasca-Pemilu yang rentan, pencurian oleh anak-anak
    (Sentani), dan potensi konflik akibat dana yang belum cair (Dinas Pendidikan). Jayawijaya tetap menjadi wilayah
    dengan risiko keamanan paling kompleks.
    </div>""", unsafe_allow_html=True)

    skenario_q = dk2[dk2["Pertanyaan"].str.contains("6 bulan|skenario|ke depan", case=False, na=False)]
    if not skenario_q.empty:
        ske_isu = issue_kii[
            issue_kii["Tanggapan"].isin(skenario_q["Tanggapan"]) &
            issue_kii["Narsum"].isin(sel_narsum)
        ]
        ske_cnt = ske_isu.groupby(["Narsum","Isu"]).size().reset_index(name="n")
        fig_ske = px.sunburst(
            ske_cnt, path=["Narsum","Isu"], values="n",
            title="Distribusi Isu dalam Proyeksi 6 Bulan ke Depan",
            color_discrete_sequence=COLORS, template=TMPL,
        )
        fig_ske.update_layout(height=450, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_ske, use_container_width=True)

        st.markdown("**💬 Kutipan Proyeksi:**")
        for _, row in skenario_q.head(6).iterrows():
            st.markdown(f"""<div class='quote-card'>
            "{str(row['Tanggapan'])[:250]}..."
            <div class='quote-meta'>🏛️ {row['Narsum']} | {row['Wilayah']}</div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 4 — LAPORAN EKSEKUTIF
# ════════════════════════════════════════════════════════
with tab_laporan:
    st.markdown("""
<div style='background: linear-gradient(135deg, #1e2130, #252836); border-radius: 14px; padding: 28px 36px; margin-bottom: 20px; border: 1px solid #2e3250;'>
<h2 style='color:#e2e8f0; margin-top:0; font-size:1.5rem;'>📄 Laporan Eksekutif — Analisis Kondisi Sosial Papua (GECAR)</h2>
<p style='color:#94a3b8; font-size:0.85rem; margin-bottom:0;'>Ringkasan temuan dari FGD Kelompok Masyarakat & Key Informant Interview (KII) di Jayawijaya, Asmat, dan Sentani</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style='color:#cbd5e1; line-height:1.85; font-size:0.92rem;'>

## 🏔️ Latar Belakang

Pengumpulan data dilakukan di tiga wilayah Papua — **Jayawijaya** (Pegunungan Tengah), **Asmat** (Papua Selatan), 
dan **Sentani** (Jayapura) — melalui dua metode: Focus Group Discussion berbasis kelompok masyarakat (anak dan dewasa) 
serta Key Informant Interview (KII) dengan pemangku kepentingan dari instansi pemerintah dan komunitas strategis. 
Total tanggapan yang dianalisis: **356 tanggapan kelompok masyarakat** dan **167 tanggapan KII**.

---

## 🔴 ISU KRITIS 1 — Penyalahgunaan Zat: Narkoba, Aibon, dan Miras

<span style='background:#3b1515;color:#fca5a5;padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;'>TINGKAT DARURAT: TINGGI</span>

Isu ini muncul di **seluruh wilayah survei** dengan konsistensi yang mengkhawatirkan. Jayawijaya menyebut miras, 
aibon, ganja, dan narkoba secara berulang dalam konteks ketegangan komunitas. Di Sentani, Dinas Sosial mengkonfirmasi 
temuan lapangan yang jauh lebih serius: **anak-anak sekolah dasar ditemukan menggunakan narkoba**, seorang **anak SD 
terinfeksi HIV** (diduga melalui kekerasan seksual yang dipicu zat), dan anak-anak menggunakan aibon di jalanan untuk 
membiayai kebiasaan tersebut dengan cara mencuri.

**Akar masalah teridentifikasi:** keluarga broken home, tidak adanya ruang bermain terjangkau (stadion berbiaya), 
minimnya fasilitas rehabilitasi, dan lemahnya keterlibatan keluarga dalam pemulihan.

**Rekomendasi:** Penyediaan ruang bermain gratis dan aman; penguatan program pasca-rehabilitasi berbasis komunitas; 
penyuluhan di sekolah dengan melibatkan mantan pengguna; pendampingan keluarga secara intensif.

---

## 🔴 ISU KRITIS 2 — Perang Suku & Trauma Intergenerasi pada Anak

<span style='background:#3b1515;color:#fca5a5;padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;'>TINGKAT DARURAT: TINGGI</span>

Jayawijaya menjadi episentrum isu ini. Ibu-ibu dewasa melaporkan bahwa **anak usia 10 tahun ke atas sudah aktif 
diikutsertakan dalam konflik bersenjata suku**, dengan orang tua maupun komunitas yang secara tidak sadar mewariskan 
narasi kekerasan kepada generasi berikutnya ("pemikiran anak hanya soal perang"). Akibatnya, motivasi sekolah menurun 
drastis dan siklus kekerasan berlanjut.

Narasumber KII (GTY, JPY) mengkonfirmasi bahwa **kelompok bersenjata beroperasi aktif di Nduga dan Jayawijaya**, 
berdampak pada akses pendidikan, trauma psikologis anak, dan keterbatasan ruang gerak warga sipil. Penyanderaan pilot 
Susi Air pada 2024 menjadi bukti nyata risiko ini.

**Rekomendasi:** Program psikososial untuk anak korban konflik; keterlibatan tokoh adat dan gereja dalam pendidikan 
perdamaian berbasis budaya; program alternatif bagi pemuda agar tidak terseret ideologi kekerasan.

---

## 🟡 ISU PENTING 3 — Korupsi & Ketimpangan Distribusi Dana Pemerintah

<span style='background:#2d2510;color:#fde68a;padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;'>TINGKAT DARURAT: MENENGAH-TINGGI</span>

Asmat menjadi wilayah dengan laporan paling rinci. Masyarakat menyebut secara eksplisit bahwa **bantuan program 
(ADD, musrenbang, BLT) dipotong di level distrik dan kampung, hanya mengalir ke keluarga kepala kampung, kontraktor, 
dan pendukung politik**. Kepala kampung di beberapa desa bahkan meminjam dana desa untuk keperluan pribadi dan 
membayarnya dengan ADD, sehingga honor kader posyandu tidak dibayarkan selama berbulan-bulan.

Di Jayawijaya, ACL mengidentifikasi bahwa ketidaktransparanan dana desa adalah salah satu pemicu utama ketegangan sosial 
yang berulang. Model penyelesaian konflik berbasis **kompensasi uang** yang berlaku saat ini dinilai hanya meredam, 
bukan menyelesaikan akar masalah.

**Rekomendasi:** Mekanisme transparansi dana desa berbasis komunitas; pelibatan ibu-ibu dan kelompok rentan dalam 
pengawasan distribusi bantuan; audit partisipatif secara berkala.

---

## 🔵 ISU PENTING 4 — Krisis Tata Kelola Pendidikan

<span style='background:#151e3b;color:#93c5fd;padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;'>TINGKAT DARURAT: MENENGAH</span>

**Dinas Pendidikan Sentani** mengungkap dimensi yang jarang muncul dalam laporan standar: PAUD yang dibentuk hanya 
demi menerima dana BUP tanpa operasional nyata; gedung SD rusak yang tidak bisa diperbaiki karena sengketa tanah 
yang belum terselesaikan; pemalangan sekolah oleh pemilik lahan sehingga anak-anak tidak dapat bersekolah; 
serta honor guru yang terlambat akibat keterbatasan APBD.

Sentani juga melaporkan bahwa kuota 1 TK + 1 PAUD per kampung tidak memadai, sementara populasi anak terus bertambah.

Di Jayawijaya, masyarakat menyoroti kurangnya pendidikan karakter dan lemahnya peran orang tua dalam proses tumbuh kembang anak.

**Rekomendasi:** Penyelesaian sengketa tanah sekolah sebagai prioritas; audit PAUD dan penghentian dana untuk lembaga 
fiktif; pelatihan guru berbasis panggilan dan kompetensi; penambahan kuota satuan pendidikan di kampung terpencil.

---

## 🟡 ISU PENTING 5 — Hoaks, Media Sosial & Akselerasi Konflik

<span style='background:#2d2510;color:#fde68a;padding:2px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;'>TINGKAT DARURAT: MENENGAH — EMERGING RISK</span>

Narasumber ACL (Jayawijaya) memberikan analisis yang sangat relevan: **media sosial, khususnya grup WhatsApp, kini 
berperan sebagai akselerator konflik** — informasi palsu atau rumor dapat memicu ketegangan massa bahkan sebelum 
kejadian nyata terjadi. Literasi digital yang rendah menjadikan masyarakat rentan terhadap provokasi digital.

Ini merupakan isu yang relatif baru namun memiliki dampak yang cepat dan meluas. Dinas Pendidikan Sentani juga 
mencatat bahwa nama instansi mulai "dijelek-jelekan" di media sosial terkait dana yang belum cair.

**Rekomendasi:** Program literasi digital berbasis komunitas akar rumput; pelatihan verifikasi informasi untuk 
pemuda dan tokoh gereja; pembangunan narasi perdamaian di platform digital.

---

## ✅ Faktor Penyatu yang Perlu Diperkuat

Meski menghadapi banyak tekanan, masyarakat di ketiga wilayah secara konsisten mengidentifikasi faktor-faktor penyatu yang masih kuat:

- **Gereja** sebagai ruang spiritual, sosial, dan mediasi yang dipercaya lintas lapisan masyarakat
- **Tokoh Adat** (kepala suku, orang tua-tua) sebagai penjaga legitimasi budaya dan penengah konflik
- **Tradisi Kebersamaan** (bakar batu, gotong royong, duka bersama, mas kawin) yang menjaga kohesi sosial

Program perdamaian yang efektif harus **membangun di atas fondasi ini**, bukan mengabaikannya.

---

## 🎯 Rekomendasi Strategis untuk WVI

| Prioritas | Aksi | Wilayah Fokus |
|-----------|------|---------------|
| 🔴 Darurat | Program rehabilitasi & pendampingan anak (narkoba, aibon, HIV) | Sentani, Jayawijaya |
| 🔴 Darurat | Psikososial anak korban konflik suku & trauma | Jayawijaya |
| 🟡 Menengah | Edukasi perdamaian berbasis adat & gereja (akar rumput) | Jayawijaya |
| 🟡 Menengah | Advokasi transparansi dana desa & pengawasan komunitas | Asmat, Sentani |
| 🔵 Jangka Panjang | Literasi digital untuk mencegah hoaks pemicu konflik | Jayawijaya |
| 🔵 Jangka Panjang | Dukungan kualitas guru & penyelesaian sengketa tanah sekolah | Sentani |

</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.78rem; padding: 20px 0 10px;'>
    GECAR Dashboard | Data: Gecar_-_Kelompok.csv & Gecar_-_KII.csv |
    Built with Streamlit + Plotly | © 2025
</div>
""", unsafe_allow_html=True)
