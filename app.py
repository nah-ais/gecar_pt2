"""
GECAR Dashboard — Analisis Tanggapan Masyarakat & Narasumber Pemerintah
Siap deploy ke Streamlit Community Cloud
Dibuat oleh: Senior Data Scientist | Streamlit + Plotly
"""

import re
from collections import Counter
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================================================================
# 1. CONFIG & APP STYLING
# ==============================================================================

st.set_page_config(
    page_title="GECAR | Dashboard Analisis Isu",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS dimasukkan ke dalam fungsi agar tidak mengotori global scope
def apply_custom_styles():
    st.markdown("""
    <style>
      /* Global */
      [data-testid="stAppViewContainer"] { background: #f7f9fc; }
      [data-testid="stSidebar"] { background: #1a2238; }
      [data-testid="stSidebar"] * { color: #e0e6ef !important; }
      [data-testid="stSidebar"] .stSelectbox label,
      [data-testid="stSidebar"] .stMultiSelect label { color: #b0bec5 !important; font-size: 0.82rem; }

      /* Metric cards */
      [data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 22px;
        border-left: 5px solid #e74c3c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
      }
      [data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 700; color: #1a2238; }
      [data-testid="stMetricLabel"] { font-size: 0.8rem !important; color: #7f8c8d; font-weight: 600; }

      /* Section headers */
      .section-header {
        background: linear-gradient(135deg, #1a2238 0%, #2c3e50 100%);
        color: white;
        padding: 14px 22px;
        border-radius: 10px;
        margin: 18px 0 12px 0;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.4px;
      }

      /* Issue card */
      .issue-card {
        background: #fff;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 10px 0;
        border-left: 5px solid #e74c3c;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
      }
      .issue-card-blue { border-left-color: #2980b9; }
      .issue-card-orange { border-left-color: #e67e22; }
      .issue-card-green { border-left-color: #27ae60; }
      .issue-card-purple { border-left-color: #8e44ad; }

      /* Quote */
      .quote-box {
        background: #eef2f7;
        border-left: 4px solid #3498db;
        padding: 12px 16px;
        border-radius: 6px;
        font-style: italic;
        color: #34495e;
        font-size: 0.88rem;
        margin: 6px 0;
      }

      /* Tab styling */
      [data-testid="stTab"] { font-weight: 600; }
      hr { border: none; border-top: 2px solid #ecf0f1; margin: 20px 0; }

      .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #f0f4f8;
        border-radius: 10px;
        padding: 6px;
      }
      .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
      }
      .stTabs [aria-selected="true"] {
        background: #1a2238 !important;
        color: white !important;
      }
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()


# ==============================================================================
# 2. DATA LOADING & MOCK DATA
# ==============================================================================

@st.cache_data(show_spinner="Memuat data...")
def load_data():
    """Load and preprocess both datasets. Falls back to mock data if files not found."""
    KELOMPOK_PATH = "Gecar_-_Kelompok.csv"
    KII_PATH      = "Gecar_-_KII.csv"

    try:
        df_k = pd.read_csv(KELOMPOK_PATH)
    except FileNotFoundError:
        df_k = pd.DataFrame({
            "Wilayah": (["Jayawijaya"]*40 + ["Asmat, Papua Selatan"]*40 + ["Sentani"]*55),
            "Kelompok_Usia": (["Anak"]*20 + ["Dewasa"]*20)*3 + ["Anak"]*15,
            "Jenis_Kelamin": (["Laki laki"]*12 + ["Perempuan"]*28)*3 + ["Laki laki"]*15,
            "Kategori_Responden": ["Masyarakat"]*135,
            "Pertanyaan": (["Apa ketakutanmu?"]*15 + ["Apa kebutuhan utama?"]*20 +
                           ["Apa yang berubah?"]*15 + ["Harapan masa depan?"]*20 +
                           ["Ketegangan komunitas?"]*25 + ["Bagaimana kamu berkontribusi?"]*15 +
                           ["Situasi ekonomi?"]*25),
            "Tanggapan": (["Takut dipukul orang tua"]*4 + ["Takut perang suku"]*3 +
                          ["Miras dan kekerasan"]*4 + ["Aibon dan narkoba"]*4 +
                          ["BLT dipotong kepala kampung"]*4 + ["Tidak ada lapangan kerja"]*5 +
                          ["Anak butuh sekolah"]*5 + ["Kebutuhan air bersih"]*3 +
                          ["Harapan dapat pekerjaan"]*5 + ["Berkontribusi di gereja"]*5 +
                          ["Ekonomi susah"]*4 + ["Pemerintah tidak peduli"]*3 +
                          ["Konflik lahan"]*3 + ["Bantuan tidak merata"]*4 +
                          ["Perang suku menakutkan"]*3 + ["Anak-anak putus sekolah"]*3 +
                          ["Gotong royong komunitas"]*4 + ["Ingin ada lapangan olahraga"]*4 +
                          ["Dana desa tidak cair"]*3 + ["Keluarga susah ekonomi"]*4 +
                          ["Kepala kampung tidak adil"]*4 + ["Perlu pembangunan jalan"]*3 +
                          ["Masa depan tidak pasti"]*4 + ["Ingin sekolah tinggi"]*3 +
                          ["Takut kehilangan orang tua"]*4 + ["Kecanduan miras"]*4 +
                          ["Ketersediaan pangan kurang"]*4 + ["Kurang fasilitas kesehatan"]*4),
        })

    try:
        df_i = pd.read_csv(KII_PATH)
    except FileNotFoundError:
        df_i = pd.DataFrame({
            "Wilayah": (["Jayawijaya"]*37 + ["Sentani"]*54 + ["Asmat"]*44),
            "Narsum": (["GTY"]*17 + ["JPY"]*20 + ["Dinas Sosial"]*29 +
                       ["Dinas Pendidikan"]*25 + ["RJF"]*44),
            "Kategori_Responden": ["KII"]*135,
            "Pertanyaan": ["Kebutuhan utama?"]*135,
            "Tanggapan": (
                ["Konflik kelompok bersenjata nduga egianus"]*10 +
                ["Inflasi pangan krisis logistik"]*8 +
                ["Narkoba aibon HIV anak sekolah"]*9 +
                ["Guru kualitas pendidikan paud honor"]*10 +
                ["Lahan PSN food estate penggusuran"]*9 +
                ["OAP pendatang diskriminasi PNS"]*8 +
                ["Anak remaja perempuan rentan trauma"]*12 +
                ["Perang suku separatisme kelompok bersenjata"]*9 +
                ["Bantuan tidak merata korupsi oknum"]*6 +
                ["Perlindungan anak kekerasan seksual"]*9 +
                ["Krisis pangan inflasi logistik"]*7 +
                ["Konflik lahan adat masyarakat"]*8 +
                ["Pendidikan guru PAUD sekolah"]*9 +
                ["Rehabilitasi narkoba aibon BNN"]*7 +
                ["Peran WVI LSM program damai"]*4
            )
        })

    return df_k, df_i


# ==============================================================================
# 3. THEMATIC DEFINITIONS & CLASSIFICATION
# ==============================================================================

THEMES_KELOMPOK = {
    "Kekerasan & Konflik": ["perang suku","perang","konflik","kekerasan","miras","parang","mabok","mabuk","ancaman","bentrok","begal","sajam","denda adat","dipukul","pukul","berkelahi","saling serang"],
    "Narkoba & Zat Berbahaya": ["aibon","narkoba","ganja","kecanduan","zat","hiv","aids","rokok","mabuk","alkohol"],
    "Pendidikan": ["sekolah","belajar","guru","pendidikan","sd ","smp","sma","kuliah","pelajar","siswa","paud","rumah baca","kurikulum","ijazah","les ","ekstrakurikuler","tes ","buku","pensil"],
    "Ekonomi & Kemiskinan": ["ekonomi","miskin","pekerjaan","kerja","dana","bantuan","blt","uang","harga","inflasi","pangan","sembako","logistik","usaha","modal","ternak","kebun","hasil","jual","beli","karaka","sagu","ikan","bensin","keramba"],
    "Korupsi & Ketidakadilan": ["dipotong","tidak adil","memihak","kepala kampung","anti masyarakat","dicoret","oknum","tidak merata","tidak peduli","nepotisme","kolektif","timses","manipulasi","bupati sendiri","pinjam","hutang"],
    "Keamanan Lingkungan": ["aman","keamanan","polisi","palang","blokir","linmas","pos kamling","penjagaan","kamtibmas","pencurian","helm"],
    "Keluarga & Sosial": ["orang tua","keluarga","mama","papa","bapa","adik","kakak","nenek","saudara","broken home","suami","istri","ibu","perselingkuhan","perceraian","duka"],
    "Harapan & Kontribusi Pemuda": ["harapan","berkontribusi","perubahan","masa depan","cita-cita","semangat","positif","kontribusi","mengajar","motivasi","berubah jadi lebih baik","bazaar","lomba"],
}

THEMES_KII = {
    "Konflik Bersenjata & Separatisme": ["bersenjata","egianus","papua merdeka","separatis","tni","polri","nduga","militer","kelompok sipil","gerilya","penyanderaan","pilot susi"],
    "Krisis Pangan & Inflasi": ["pangan","inflasi","logistik","sembako","harga","krisis","bps","sandang","papan","udara","transportasi","jalur","wamena"],
    "Narkoba & HIV Anak": ["narkoba","aibon","hiv","aids","rehabilitasi","bnn","narkotika","pencandu","mantan pengguna","rehab","penyalahgunaan"],
    "Kualitas Pendidikan": ["guru","paud","honor","mengajar","kurikulum","panggilan","bangunan","gedung sekolah","apbd","gelar","sertifikat","bup","tenaga pengajar"],
    "Konflik Lahan & PSN": ["lahan","psn","food estate","penggusuran","deforestasi","tanah adat","ulayat","gambut","rawa","tebu","merauke","waanan","ilwayab","korporasi"],
    "Diskriminasi OAP vs Pendatang": ["oap","pendatang","orang asli papua","dikotomi","diskriminasi","pns","lowongan","kuota","polarisasi","identitas","malind","mappi"],
    "Perlindungan Anak & Perempuan": ["anak","remaja","perempuan","rentan","trauma","kekerasan seksual","perlindungan","kelompok rentan","ibu tunggal","gangguan emosional","putus sekolah"],
    "Tata Kelola & Korupsi": ["tidak transparan","nepotisme","oknum","keuangan","distribusi tidak adil","korupsi","pengelolaan","anggaran","pejabat","pj "],
}

def classify(text: str, themes: dict) -> list[str]:
    text = str(text).lower()
    found = []
    for theme, kws in themes.items():
        for kw in kws:
            if re.search(r'\b' + re.escape(kw) + r'\b', text) or kw in text:
                found.append(theme)
                break
    return found if found else ["Kehidupan Sehari-hari & Lainnya"]


# Data Processing
df_k, df_i = load_data()
df_k["Tema_List"] = df_k["Tanggapan"].apply(lambda x: classify(x, THEMES_KELOMPOK))
df_k_exploded  = df_k.explode("Tema_List")

df_i["Tema_List"] = df_i["Tanggapan"].apply(lambda x: classify(x, THEMES_KII))
df_i_exploded  = df_i.explode("Tema_List")


# ==============================================================================
# 4. PLOTLY CHART HELPERS (Mengurangi Redundansi di Template Utama)
# ==============================================================================

def configure_chart_layout(fig, height=360, is_bar=True, reverse_y=True):
    """Fungsi pembantu untuk standarisasi style grafik Plotly."""
    layout_args = dict(
        height=height,
        plot_bgcolor="#f7f9fc",
        paper_bgcolor="#f7f9fc",
        font=dict(family="Inter, sans-serif"),
        title_font_size=13 if height < 350 else 14
    )
    if is_bar:
        layout_args['showlegend'] = False
        if reverse_y:
            layout_args['yaxis'] = dict(autorange="reversed")
            
    fig.update_layout(**layout_args)
    return fig


# ==============================================================================
# 5. SIDEBAR NAVIGATION & FILTERS
# ==============================================================================

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Lambang_Negara_Indonesia.svg/200px-Lambang_Negara_Indonesia.svg.png", width=60)
    st.markdown("## 🗺️ GECAR Dashboard")
    st.markdown("**Analisis Isu Masyarakat & Pemerintah**")
    st.divider()

    # Filter Dataset 1
    st.markdown("### 📍 Filter Dataset 1 – Masyarakat")
    wilayah_k_opts = ["Semua Wilayah"] + sorted(df_k["Wilayah"].dropna().unique().tolist())
    sel_wilayah_k  = st.selectbox("Wilayah", wilayah_k_opts, key="wk")

    usia_opts = ["Semua Usia"] + df_k["Kelompok_Usia"].dropna().unique().tolist()
    sel_usia  = st.selectbox("Kelompok Usia", usia_opts, key="uk")

    gender_opts = ["Semua"] + df_k["Jenis_Kelamin"].dropna().unique().tolist()
    sel_gender  = st.selectbox("Jenis Kelamin", gender_opts, key="gk")
    st.divider()

    # Filter Dataset 2
    st.markdown("### 🏛️ Filter Dataset 2 – KII")
    wilayah_i_opts = ["Semua Wilayah"] + sorted(df_i["Wilayah"].dropna().unique().tolist())
    sel_wilayah_i  = st.selectbox("Wilayah", wilayah_i_opts, key="wi")

    narsum_opts = ["Semua Narasumber"] + df_i["Narsum"].dropna().unique().tolist()
    sel_narsum  = st.selectbox("Narasumber", narsum_opts, key="ni")
    
    st.divider()
    st.caption("GECAR | Data Papua 2024–2025")

# Fungsi filter data
def get_filtered_kelompok():
    d = df_k.copy()
    d_exp = df_k_exploded.copy()
    if sel_wilayah_k != "Semua Wilayah":
        d = d[d["Wilayah"] == sel_wilayah_k]
        d_exp = d_exp[d_exp["Wilayah"] == sel_wilayah_k]
    if sel_usia != "Semua Usia":
        d = d[d["Kelompok_Usia"] == sel_usia]
        d_exp = d_exp[d_exp["Kelompok_Usia"] == sel_usia]
    if sel_gender != "Semua":
        d = d[d["Jenis_Kelamin"] == sel_gender]
        d_exp = d_exp[d_exp["Jenis_Kelamin"] == sel_gender]
    return d, d_exp

def get_filtered_kii():
    d = df_i.copy()
    d_exp = df_i_exploded.copy()
    if sel_wilayah_i != "Semua Wilayah":
        d = d[d["Wilayah"] == sel_wilayah_i]
        d_exp = d_exp[d_exp["Wilayah"] == sel_wilayah_i]
    if sel_narsum != "Semua Narasumber":
        d = d[d["Narsum"] == sel_narsum]
        d_exp = d_exp[d_exp["Narsum"] == sel_narsum]
    return d, d_exp

fk, fk_ = get_filtered_kelompok()
fi, fi_ = get_filtered_kii()

PALETTE_K = px.colors.qualitative.Bold
PALETTE_I = px.colors.qualitative.Vivid


# ==============================================================================
# 6. MAIN HEADER & TABS LAYOUT
# ==============================================================================

st.markdown("""
<div style='background:linear-gradient(135deg,#1a2238,#2c3e50);padding:28px 36px; border-radius:14px;color:white;margin-bottom:20px;'>
  <h1 style='margin:0;font-size:2rem;'>🗺️ GECAR — Dashboard Analisis Isu Papua</h1>
  <p style='margin:8px 0 0 0;color:#aab8c2;font-size:1rem;'>
    Analisis mendalam tanggapan masyarakat (Kelompok FGD) & narasumber pemerintah (KII) dari Jayawijaya, Sentani, dan Asmat • Data 2024–2025
  </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "👥 Dataset 1 — Masyarakat (FGD)",
    "🏛️ Dataset 2 — KII (Pemerintah & Narasumber)",
    "📊 Laporan Eksekutif & Rekomendasi",
])


# ==============================================================================
# TAB 1 — KELOMPOK (MASYARAKAT)
# ==============================================================================
with tab1:
    st.markdown("<div class='section-header'>📌 Ringkasan Data — Masyarakat (FGD)</div>", unsafe_allow_html=True)

    # Metrics Calculation
    total_resp = len(fk)
    n_anak = (fk["Kelompok_Usia"] == "Anak").sum()
    n_dewasa = (fk["Kelompok_Usia"] == "Dewasa").sum()
    pct_konflik = fk["Tanggapan"].str.contains("perang|kekerasan|miras|mabuk|ancaman|begal|parang|pukul|dipukul", case=False, na=False).mean() * 100
    pct_korupsi_blt = fk["Tanggapan"].str.contains("dipotong|tidak adil|kepala kampung|oknum|dicoret|tidak merata", case=False, na=False).mean() * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Responden", f"{total_resp:,}")
    c2.metric("Responden Anak", f"{n_anak:,}")
    c3.metric("Responden Dewasa", f"{n_dewasa:,}")
    c4.metric("Menyebut Kekerasan/Konflik", f"{pct_konflik:.0f}%")
    c5.metric("Menyebut Isu Korupsi Bantuan", f"{pct_korupsi_blt:.0f}%")
    st.divider()

    # Section 1: Distribusi Isu
    st.markdown("<div class='section-header'>📊 Isu 1 — Distribusi Tema Tanggapan Masyarakat</div>", unsafe_allow_html=True)
    st.markdown("**Insight:** Tanggapan masyarakat mencerminkan 8 tema dominan. Isu ekonomi & kemiskinan mendominasi di Asmat, sementara kekerasan & konflik paling menonjol di Sentani.")

    tema_count = fk_["Tema_List"].value_counts().reset_index()
    tema_count.columns = ["Tema", "Jumlah"]
    tema_count = tema_count[tema_count["Tema"] != "Kehidupan Sehari-hari & Lainnya"]

    fig_tema = px.bar(tema_count, x="Jumlah", y="Tema", orientation="h", color="Tema", color_discrete_sequence=PALETTE_K, title="Frekuensi Kemunculan Tema Isu dalam Tanggapan Masyarakat", text="Jumlah")
    fig_tema.update_traces(textposition="outside", textfont_size=12)
    st.plotly_chart(configure_chart_layout(fig_tema, height=420), use_container_width=True)

    # Section 2: Kekerasan Domestik
    st.markdown("<div class='section-header'>⚠️ Isu 2 — Kekerasan Domestik & Ketakutan Anak</div>", unsafe_allow_html=True)
    col_a, col_b = st.columns([3, 2])
    
    with col_a:
        ketakutan_map = {
            "Dipukul / Kekerasan Fisik dari Orang Tua": fk["Tanggapan"].str.contains("dipukul|pukul|kekerasan fisik dari bap|kekerasan fisik dari orang", case=False, na=False).sum(),
            "Kekerasan Akibat Miras / Orang Mabuk": fk["Tanggapan"].str.contains("miras|mabuk|mabok|parang saat marah|pegang parang", case=False, na=False).sum(),
            "Perang Suku & Konflik Antar Kampung": fk["Tanggapan"].str.contains("perang suku|saling serang|antar kampung|konflik", case=False, na=False).sum(),
            "Aibon / Narkoba di Lingkungan": fk["Tanggapan"].str.contains("aibon|narkoba|ganja", case=False, na=False).sum(),
            "Kehilangan Orang Tua / Keluarga": fk["Tanggapan"].str.contains("kehilangan|meninggal|kehilangan papa|kehilangan mama", case=False, na=False).sum(),
            "Masa Depan & Ketidakpastian Ekonomi": fk["Tanggapan"].str.contains("masa depan|cita|pekerjaan|tes tni|tidak pasti", case=False, na=False).sum(),
        }
        df_takut = pd.DataFrame(list(ketakutan_map.items()), columns=["Ketakutan", "Frekuensi"]).sort_values("Frekuensi", ascending=True)
        fig_takut = px.bar(df_takut, x="Frekuensi", y="Ketakutan", orientation="h", color="Frekuensi", color_continuous_scale=["#ffeaa7", "#e17055", "#d63031"], title="Jenis Ketakutan yang Dilaporkan Masyarakat", text="Frekuensi")
        fig_takut.update_traces(textposition="outside")
        fig_takut.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_takut, height=380), use_container_width=True)

    with col_b:
        st.markdown("#### 🔴 Temuan Kritis: Kekerasan dalam Rumah Tangga")
        st.markdown("<div class='issue-card'><b>Kekerasan Fisik dari Orang Tua</b><br>Responden anak menyebut ketakutan dipukul oleh orang tua sebagai ketakutan utama.</div>", unsafe_allow_html=True)
        kdrta = df_k[(df_k["Kelompok_Usia"] == "Anak") & df_k["Tanggapan"].str.contains("dipukul|pukul.*bap|kekerasan fisik", case=False, na=False)]
        for _, row in kdrta.head(3).iterrows():
            txt = str(row["Tanggapan"])[:160] + ("…" if len(str(row["Tanggapan"])) > 160 else "")
            st.markdown(f"<div class='quote-box'>&ldquo;{txt}&rdquo; <br><small>&mdash; {row.get('Wilayah', '')}</small></div>", unsafe_allow_html=True)

    # Section 3: Miras & Konflik
    st.markdown("<div class='section-header'>🍺 Isu 3 — Minuman Keras (Miras) sebagai Pemicu Kekerasan</div>", unsafe_allow_html=True)
    col_c, col_d = st.columns(2)
    
    with col_c:
        miras_per_wil = {w: df_k[df_k["Wilayah"] == w]["Tanggapan"].str.contains("miras|mabuk|mabok|alkohol", case=False, na=False).sum() for w in df_k["Wilayah"].dropna().unique()}
        df_miras = pd.DataFrame(list(miras_per_wil.items()), columns=["Wilayah", "Jumlah"])
        fig_miras = px.bar(df_miras, x="Wilayah", y="Jumlah", color="Wilayah", color_discrete_sequence=["#e17055", "#fdcb6e", "#74b9ff"], title="Frekuensi Tanggapan Terkait Miras per Wilayah", text="Jumlah")
        fig_miras.update_traces(textposition="outside")
        st.plotly_chart(configure_chart_layout(fig_miras, height=340, reverse_y=False), use_container_width=True)

    with col_d:
        dampak_miras = {
            "Kekerasan Fisik / Pemukul": df_k["Tanggapan"].str.contains("pukul|parang|marah|kekerasan", case=False, na=False).sum(),
            "Pencurian / Begal": df_k["Tanggapan"].str.contains("pencurian|begal|curi|helm", case=False, na=False).sum(),
            "Konflik Antar Kampung": df_k["Tanggapan"].str.contains("saling serang|antar kampung|perang", case=False, na=False).sum(),
            "Perselingkuhan / Perceraian": df_k["Tanggapan"].str.contains("perselingkuhan|perceraian|pembunuhan", case=False, na=False).sum(),
        }
        df_dampak = pd.DataFrame(list(dampak_miras.items()), columns=["Dampak", "Jumlah"])
        fig_dampak = px.pie(df_dampak, names="Dampak", values="Jumlah", color_discrete_sequence=["#e17055", "#d63031", "#fdcb6e", "#636e72"], title="Dampak Turunan Miras yang Dilaporkan", hole=0.45)
        fig_dampak.update_traces(textposition="inside", textinfo="label+percent")
        st.plotly_chart(configure_chart_layout(fig_dampak, height=340, is_bar=False), use_container_width=True)

    # Section 4: Korupsi BLT
    st.markdown("<div class='section-header'>💸 Isu 4 — Korupsi & Pemotongan Dana Bantuan (BLT)</div>", unsafe_allow_html=True)
    st.markdown("**Temuan Kritis:** Masyarakat Asmat secara konsisten melaporkan pemotongan BLT oleh kepala kampung sebesar **Rp200.000–300.000 per KK**.")
    col_e, col_f = st.columns([2, 3])
    
    with col_e:
        kor_types = {
            "BLT Dipotong Oknum": df_k["Tanggapan"].str.contains("dipotong|potong.*blt|blt.*potong", case=False, na=False).sum(),
            "Kepala Kampung Memihak Simpatisan": df_k["Tanggapan"].str.contains("memihak|simpatisan|berpihak|timses", case=False, na=False).sum(),
            "Bantuan Tidak Merata": df_k["Tanggapan"].str.contains("tidak merata|tidak adil|tidak penuh|tidak dapat", case=False, na=False).sum(),
            "Kepala Kampung Tidak Dipercaya": df_k["Tanggapan"].str.contains("tidak peduli|kurang dipercaya|anti masyarakat", case=False, na=False).sum(),
            "Dana Desa Diselewengkan": df_k["Tanggapan"].str.contains("pinjam.*add|membayar hutang|kebutuhan kepala kampung|keuangan.*kepala", case=False, na=False).sum(),
        }
        df_kor = pd.DataFrame(list(kor_types.items()), columns=["Bentuk Korupsi", "Frekuensi"])
        df_kor = df_kor[df_kor["Frekuensi"] > 0].sort_values("Frekuensi", ascending=False)
        fig_kor = px.bar(df_kor, x="Frekuensi", y="Bentuk Korupsi", orientation="h", color="Frekuensi", color_continuous_scale=["#ffeaa7", "#e17055"], title="Bentuk Penyimpangan Dana yang Dilaporkan", text="Frekuensi")
        fig_kor.update_traces(textposition="outside")
        fig_kor.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_kor, height=320), use_container_width=True)

    with col_f:
        st.markdown("#### 📣 Suara Langsung Masyarakat")
        korupsi_rows = df_k[df_k["Tanggapan"].str.contains("dipotong|memihak|anti masyarakat|pinjam.*add|dicoret|timses", case=False, na=False)].head(5)
        for _, row in korupsi_rows.iterrows():
            txt = str(row["Tanggapan"])[:220] + ("…" if len(str(row["Tanggapan"])) > 220 else "")
            st.markdown(f"<div class='quote-box issue-card-orange'>&ldquo;{txt}&rdquo; <br><small>&mdash; {row.get('Wilayah', '')}</small></div>", unsafe_allow_html=True)

    # Section 5: Kebutuhan vs Harapan
    st.markdown("<div class='section-header'>🌱 Isu 5 — Kebutuhan Utama vs Harapan Masa Depan</div>", unsafe_allow_html=True)
    col_g, col_h = st.columns(2)
    
    with col_g:
        kebutuhan = {
            "Air Bersih / Sanitasi": df_k["Tanggapan"].str.contains("air bersih|sumur|pah|sanitasi", case=False, na=False).sum(),
            "Lapangan Kerja": df_k["Tanggapan"].str.contains("pekerjaan|kerja|lapangan kerja|lowongan", case=False, na=False).sum(),
            "Pendidikan / Sekolah": df_k["Tanggapan"].str.contains("sekolah|pendidikan|belajar|guru", case=False, na=False).sum(),
            "Akses Kesehatan": df_k["Tanggapan"].str.contains("kesehatan|rs|rumah sakit|puskesmas|imunisasi|hpv", case=False, na=False).sum(),
            "Bantuan Pangan / BLT": df_k["Tanggapan"].str.contains("pangan|sembako|blt|beras|raskin|bantuan", case=False, na=False).sum(),
            "Infrastruktur Jalan": df_k["Tanggapan"].str.contains("jalan|jembatan|infrastruktur|akses", case=False, na=False).sum(),
            "Modal Usaha / Ekonomi": df_k["Tanggapan"].str.contains("modal|usaha|ternak|kebun|keramba|bibit", case=False, na=False).sum(),
        }
        df_keb = pd.DataFrame(list(kebutuhan.items()), columns=["Kebutuhan", "Jumlah"]).sort_values("Jumlah", ascending=True)
        fig_keb = px.bar(df_keb, x="Jumlah", y="Kebutuhan", orientation="h", color="Jumlah", color_continuous_scale=["#81ecec", "#00b894", "#006d5b"], title="Kebutuhan Utama yang Disampaikan Masyarakat", text="Jumlah")
        fig_keb.update_traces(textposition="outside")
        fig_keb.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_keb, height=360), use_container_width=True)

    with col_h:
        harapan = {
            "Pendidikan Lebih Baik": df_k["Tanggapan"].str.contains("sekolah.*baik|pendidikan.*maju|kuliah|ijazah|lulus", case=False, na=False).sum(),
            "Kegiatan Positif Pemuda": df_k["Tanggapan"].str.contains("kegiatan.*positif|olahraga|bazaar|lomba|rumah baca", case=False, na=False).sum(),
            "Komunitas / Gereja Maju": df_k["Tanggapan"].str.contains("gereja.*maju|komunitas.*baik|ramai.*gereja|ibadah", case=False, na=False).sum(),
            "Pemerintah Lebih Adil": df_k["Tanggapan"].str.contains("pemerintah.*adil|adil|perubahan.*kepala|pemimpin.*baik", case=False, na=False).sum(),
            "Lapangan Kerja": df_k["Tanggapan"].str.contains("lowongan|pekerjaan.*wvi|kerja.*kampung|cari kerja", case=False, na=False).sum(),
            "Infrastruktur Kampung": df_k["Tanggapan"].str.contains("jalan|jembatan|air bersih|renovasi|pembangunan", case=False, na=False).sum(),
        }
        df_har = pd.DataFrame(list(harapan.items()), columns=["Harapan", "Jumlah"]).sort_values("Jumlah", ascending=True)
        fig_har = px.bar(df_har, x="Jumlah", y="Harapan", orientation="h", color="Jumlah", color_continuous_scale=["#a29bfe", "#6c5ce7", "#2d3436"], title="Harapan Masyarakat untuk Masa Depan Komunitas", text="Jumlah")
        fig_har.update_traces(textposition="outside")
        fig_har.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_har, height=360), use_container_width=True)

    # Section 6: Heatmap
    st.markdown("<div class='section-header'>🗺️ Isu 6 — Peta Isu: Tema per Wilayah (Heatmap)</div>", unsafe_allow_html=True)
    tema_wil = fk_.groupby(["Wilayah", "Tema_List"]).size().reset_index(name="Jumlah")
    tema_wil = tema_wil[tema_wil["Tema_List"] != "Kehidupan Sehari-hari & Lainnya"]
    pivot = tema_wil.pivot(index="Tema_List", columns="Wilayah", values="Jumlah").fillna(0)

    fig_heat = px.imshow(pivot, color_continuous_scale="YlOrRd", title="Intensitas Isu per Wilayah (Semakin Gelap = Semakin Dominan)", aspect="auto", text_auto=True)
    fig_heat.update_layout(coloraxis_showscale=True)
    st.plotly_chart(configure_chart_layout(fig_heat, height=400, is_bar=False), use_container_width=True)

    # Section 7: Perbandingan Anak vs Dewasa
    st.markdown("<div class='section-header'>👦👩 Perbandingan Isu: Anak vs Dewasa</div>", unsafe_allow_html=True)
    concern_keys = {
        "Kekerasan / Pukul": "dipukul|pukul|kekerasan",
        "Ekonomi / Pekerjaan": "ekonomi|pekerjaan|kerja|dana|bantuan",
        "Pendidikan / Sekolah": "sekolah|belajar|guru|pendidikan",
        "Miras / Narkoba": "miras|mabuk|aibon|narkoba|ganja",
        "Harapan Masa Depan": "harapan|cita|masa depan|berubah",
        "Peran Komunitas": "gereja|ibadah|komunitas|berkontribusi",
    }
    rows_comp = []
    for kel in ["Anak", "Dewasa"]:
        sub = df_k[df_k["Kelompok_Usia"] == kel]
        for label, pat in concern_keys.items():
            count = sub["Tanggapan"].str.contains(pat, case=False, na=False).sum()
            rows_comp.append({"Kelompok": kel, "Isu": label, "Frekuensi": count})

    df_comp = pd.DataFrame(rows_comp)
    fig_comp = px.bar(df_comp, x="Isu", y="Frekuensi", color="Kelompok", barmode="group", color_discrete_map={"Anak": "#74b9ff", "Dewasa": "#e17055"}, title="Perbandingan Prioritas Isu: Anak vs Dewasa", text="Frekuensi")
    fig_comp.update_traces(textposition="outside")
    fig_comp.update_layout(legend=dict(orientation="h", y=1.08), xaxis_tickangle=-25)
    st.plotly_chart(configure_chart_layout(fig_comp, height=380, reverse_y=False), use_container_width=True)

    with st.expander("📋 Lihat Data Mentah — Dataset Masyarakat"):
        st.dataframe(fk[["Wilayah", "Kelompok_Usia", "Jenis_Kelamin", "Pertanyaan", "Tanggapan"]], use_container_width=True, height=350)


# ==============================================================================
# TAB 2 — KII (PEMERINTAH & NARASUMBER)
# ==============================================================================
with tab2:
    st.markdown("<div class='section-header'>📌 Ringkasan Data — KII (Narasumber Pemerintah)</div>", unsafe_allow_html=True)
    
    total_kii = len(fi)
    n_jaya = (fi["Wilayah"] == "Jayawijaya").sum()
    n_sent = (fi["Wilayah"] == "Sentani").sum()
    n_asmat = (fi["Wilayah"] == "Asmat").sum()
    pct_anak_kii = fi["Tanggapan"].str.contains("anak|remaja|perempuan|rentan", case=False, na=False).mean() * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Pernyataan KII", f"{total_kii:,}")
    c2.metric("Jayawijaya", f"{n_jaya:,}")
    c3.metric("Sentani", f"{n_sent:,}")
    c4.metric("Asmat", f"{n_asmat:,}")
    c5.metric("Menyebut Anak/Remaja Rentan", f"{pct_anak_kii:.0f}%")
    st.divider()

    st.markdown("<div class='section-header'>📊 Isu 1 — Peta Isu Strategis dari Narasumber Pemerintah</div>", unsafe_allow_html=True)
    col_a, col_b = st.columns([3, 2])
    
    with col_a:
        tema_kii = fi_["Tema_List"].value_counts().reset_index()
        tema_kii.columns = ["Tema", "Jumlah"]
        tema_kii = tema_kii[tema_kii["Tema"] != "Kehidupan Sehari-hari & Lainnya"]
        fig_kii_tema = px.bar(tema_kii, x="Jumlah", y="Tema", orientation="h", color="Tema", color_discrete_sequence=PALETTE_I, title="Distribusi Tema dalam Pernyataan KII", text="Jumlah")
        fig_kii_tema.update_traces(textposition="outside", textfont_size=12)
        st.plotly_chart(configure_chart_layout(fig_kii_tema, height=400), use_container_width=True)

    with col_b:
        narsum_ct = fi["Narsum"].value_counts().reset_index()
        narsum_ct.columns = ["Narsum", "Jumlah"]
        narsum_label = {"GTY": "GTY (Jayawijaya)", "JPY": "JPY (Jayawijaya)", "ACL": "ACL (Jayawijaya)", "Dinas Sosial": "Dinas Sosial (Sentani)", "Dinas Pendidikan": "Dinas Pendidikan (Sentani)", "RJF": "RJF (Asmat)", "WBW": "WBW (Asmat)"}
        narsum_ct["Narsum"] = narsum_ct["Narsum"].map(narsum_label).fillna(narsum_ct["Narsum"])
        fig_narsum = px.pie(narsum_ct, names="Narsum", values="Jumlah", color_discrete_sequence=PALETTE_I, title="Distribusi Pernyataan per Narasumber", hole=0.4)
        fig_narsum.update_traces(textposition="inside", textinfo="label+percent")
        st.plotly_chart(configure_chart_layout(fig_narsum, height=400, is_bar=False), use_container_width=True)

    # Section 2: Konflik Bersenjata
    st.markdown("<div class='section-header'>🔫 Isu 2 — Konflik Bersenjata & Kelompok Separatis (Jayawijaya)</div>", unsafe_allow_html=True)
    col_c, col_d = st.columns([2, 3])
    
    with col_c:
        aktor_konflik = {
            "Kelompok Sipil Bersenjata (OPM)": df_i["Tanggapan"].str.contains("bersenjata|egianus|papua merdeka|kelompok sipil", case=False, na=False).sum(),
            "TNI / Polri": df_i["Tanggapan"].str.contains("tni|polri|aparat|militer|batalion", case=False, na=False).sum(),
            "Tokoh Adat": df_i["Tanggapan"].str.contains("tokoh adat|kepala suku|adat", case=False, na=False).sum(),
            "Gereja / Tokoh Agama": df_i["Tanggapan"].str.contains("gereja|pendeta|tokoh agama|keuskupan", case=False, na=False).sum(),
            "Pemerintah Daerah": df_i["Tanggapan"].str.contains("pemda|pemerintah daerah|bupati|dprd|kepala kampung", case=False, na=False).sum(),
        }
        df_aktor = pd.DataFrame(list(aktor_konflik.items()), columns=["Aktor", "Frekuensi"]).sort_values("Frekuensi", ascending=True)
        fig_aktor = px.bar(df_aktor, x="Frekuensi", y="Aktor", orientation="h", color="Frekuensi", color_continuous_scale=["#dfe6e9", "#d63031"], title="Aktor yang Disebut dalam Konteks Konflik", text="Frekuensi")
        fig_aktor.update_traces(textposition="outside")
        fig_aktor.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_aktor, height=340), use_container_width=True)

    with col_d:
        st.markdown("#### 🔍 Pernyataan Kunci Narasumber tentang Konflik")
        konflik_rows = df_i[df_i["Tanggapan"].str.contains("egianus|bersenjata|papua merdeka|nduga|separatis|gerilya|penyanderaan", case=False, na=False).head(4)]
        for _, row in konflik_rows.iterrows():
            txt = str(row["Tanggapan"])[:280] + ("…" if len(str(row["Tanggapan"])) > 280 else "")
            st.markdown(f"<div class='quote-box'>&ldquo;{txt}&rdquo; <br><small>&mdash; {row.get('Narsum', '')} | {row.get('Wilayah', '')}</small></div>", unsafe_allow_html=True)

    # Section 3: Narkoba
    st.markdown("<div class='section-header'>💊 Isu 3 — Narkoba, Aibon & HIV pada Anak (Sentani)</div>", unsafe_allow_html=True)
    col_e, col_f = st.columns(2)
    
    with col_e:
        narkoba_detail = {
            "Narkoba di Sekolah (temuan BNN)": df_i["Tanggapan"].str.contains("narkoba.*sekolah|sekolah.*narkoba|pemeriksaan.*bnn", case=False, na=False).sum(),
            "Aibon di Jalanan": df_i["Tanggapan"].str.contains("aibon", case=False, na=False).sum(),
            "Kasus HIV pada Anak SD": df_i["Tanggapan"].str.contains("hiv|aids", case=False, na=False).sum(),
            "Pecandu / Rehabilitasi": df_i["Tanggapan"].str.contains("rehabilitasi|mantan pengguna|pencandu|rehab", case=False, na=False).sum(),
            "Pencurian akibat Narkoba": df_i["Tanggapan"].str.contains("pencurian.*helm|membeli.*narkoba|membeli.*aibon", case=False, na=False).sum(),
            "Broken Home → Narkoba": df_i["Tanggapan"].str.contains("broken home|keluarga.*narkoba|orang tua.*narkoba", case=False, na=False).sum(),
        }
        df_nar = pd.DataFrame(list(narkoba_detail.items()), columns=["Isu", "Frekuensi"]).sort_values("Frekuensi", ascending=True)
        fig_nar = px.bar(df_nar, x="Frekuensi", y="Isu", orientation="h", color="Frekuensi", color_continuous_scale=["#ffeaa7", "#e17055"], title="Isu Narkoba & Zat Berbahaya pada Anak-Remaja", text="Frekuensi")
        fig_nar.update_traces(textposition="outside")
        fig_nar.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_nar, height=340), use_container_width=True)

    with col_f:
        st.markdown("#### 🔴 Pernyataan Narasumber — Dinas Sosial & Dinas Pendidikan Sentani")
        nar_rows = df_i[df_i["Tanggapan"].str.contains("narkoba|aibon|hiv|rehabilitasi|bnn|pencandu", case=False, na=False)].head(4)
        for _, row in nar_rows.iterrows():
            txt = str(row["Tanggapan"])[:270] + ("…" if len(str(row["Tanggapan"])) > 270 else "")
            st.markdown(f"<div class='quote-box issue-card-orange'>&ldquo;{txt}&rdquo; <br><small>&mdash; {row.get('Narsum', '')} | {row.get('Wilayah', '')}</small></div>", unsafe_allow_html=True)

    # Section 4: PSN & Lahan
    st.markdown("<div class='section-header'>🌿 Isu 4 — Konflik Lahan & Proyek Strategis Nasional (Asmat)</div>", unsafe_allow_html=True)
    col_g, col_h = st.columns([3, 2])
    
    with col_g:
        psn_aspek = {
            "Deforestasi & Pembukaan Lahan Gambut": df_i["Tanggapan"].str.contains("deforestasi|gambut|rawa|lahan.*terbuka", case=False, na=False).sum(),
            "Penggusuran / Penolakan Lahan Adat": df_i["Tanggapan"].str.contains("penggusuran|penolakan|ulayat|hak adat", case=False, na=False).sum(),
            "Food Estate / Tebu (PSN)": df_i["Tanggapan"].str.contains("food estate|tebu|psn|proyek strategis", case=False, na=False).sum(),
            "Aparat Militer dianggap Intimidatif": df_i["Tanggapan"].str.contains("intimidatif|militer.*dianggap|aparat.*dianggap|intimidasi|pengamanan.*ketat", case=False, na=False).sum(),
            "Konflik Masyarakat Adat vs Korporasi": df_i["Tanggapan"].str.contains("korporasi|masyarakat adat.*konflik|bentrokan fisik", case=False, na=False).sum(),
            "Ekosida / Kerusakan Ekologi": df_i["Tanggapan"].str.contains("ekosida|ekologi|lingkungan.*rusak|kerusakan lingkungan", case=False, na=False).sum(),
        }
        df_psn = pd.DataFrame(list(psn_aspek.items()), columns=["Aspek", "Frekuensi"]).sort_values("Frekuensi", ascending=True)
        fig_psn = px.bar(df_psn, x="Frekuensi", y="Aspek", orientation="h", color="Frekuensi", color_continuous_scale=["#a8edea", "#096c18"], title="Dimensi Konflik Lahan & PSN yang Dilaporkan KII", text="Frekuensi")
        fig_psn.update_traces(textposition="outside")
        fig_psn.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_psn, height=360), use_container_width=True)

    with col_h:
        st.markdown("#### 📣 Suara Narasumber tentang PSN & Lahan")
        psn_rows = df_i[df_i["Tanggapan"].str.contains("food estate|penggusuran|deforestasi|ulayat|psn|korporasi|ekosida", case=False, na=False)].head(4)
        for _, row in psn_rows.iterrows():
            txt = str(row["Tanggapan"])[:250] + ("…" if len(str(row["Tanggapan"])) > 250 else "")
            st.markdown(f"<div class='quote-box issue-card-green'>&ldquo;{txt}&rdquo; <br><small>&mdash; {row.get('Narsum', '')} | {row.get('Wilayah', '')}</small></div>", unsafe_allow_html=True)

    # Section 5: Kualitas Pendidikan & Risiko Proyeksi
    st.markdown("<div class='section-header'>📚 Isu 5 — Krisis Kualitas Pendidikan & Tata Kelola Guru</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        pendidikan_isu = {
            "Guru Mengajar Bukan Panggilan": df_i["Tanggapan"].str.contains("panggilan.*guru|guru.*panggilan|hanya.*rutinitas|hanya.*gaji|sekadar rutin", case=False, na=False).sum(),
            "Honor Guru Terlambat": df_i["Tanggapan"].str.contains("honor.*terlambat|terlambat.*honor|apbd.*tidak cukup|tidak.*mencukupi", case=False, na=False).sum(),
            "PAUD Tidak Fungsional": df_i["Tanggapan"].str.contains("paud.*tidak berjalan|tidak.*paud|bup.*bantuan.*paud|tidak ada tenaga", case=False, na=False).sum(),
            "Bangunan PAUD Bermasalah": df_i["Tanggapan"].str.contains("rumah pribadi|sertifikat.*gedung|bangunan.*paud|gedung sekolah", case=False, na=False).sum(),
            "Putus Sekolah akibat Konflik": df_i["Tanggapan"].str.contains("putus sekolah|sekolah.*ditutup|guru.*absen|anak.*terpaksa.*kerja", case=False, na=False).sum(),
            "Kelas SD Terinfeksi HIV": df_i["Tanggapan"].str.contains("kelas 5.*hiv|sd.*hiv|hiv.*anak", case=False, na=False).sum(),
        }
        df_pend = pd.DataFrame(list(pendidikan_isu.items()), columns=["Isu", "Frekuensi"]).sort_values("Frekuensi", ascending=True)
        fig_pend = px.bar(df_pend, x="Frekuensi", y="Isu", orientation="h", color="Frekuensi", color_continuous_scale=["#d6eaf8", "#2980b9"], title="Isu Pendidikan yang Diidentifikasi Narasumber", text="Frekuensi")
        fig_pend.update_traces(textposition="outside")
        fig_pend.update_layout(coloraxis_showscale=False)
        st.plotly_chart(configure_chart_layout(fig_pend, height=340), use_container_width=True)

    with col2:
        skenario = {
            "Keamanan Fluktuatif": df_i["Tanggapan"].str.contains("keamanan.*fluktuatif|fluktuatif|rawan.*konflik|keamanan.*terkendali", case=False, na=False).sum(),
            "Krisis Pangan / Inflasi": df_i["Tanggapan"].str.contains("pangan|inflasi|harga.*naik|kenaikan harga|logistik.*terganggu", case=False, na=False).sum(),
            "Trauma Psikososial": df_i["Tanggapan"].str.contains("trauma|psikososial|ketakutan|gangguan tidur|kecemasan", case=False, na=False).sum(),
            "Putus Sekolah Sementara": df_i["Tanggapan"].str.contains("putus sekolah|absensi.*sekolah|sekolah.*ditutup", case=False, na=False).sum(),
            "Konflik Lahan Meningkat": df_i["Tanggapan"].str.contains("lahan.*meningkat|sengketa.*lahan|konflik.*lahan", case=False, na=False).sum(),
        }
        df_ske = pd.DataFrame(list(skenario.items()), columns=["Skenario Risiko", "Frekuensi"]).sort_values("Frekuensi", ascending=False)
        fig_ske = px.bar(df_ske, x="Skenario Risiko", y="Frekuensi", color="Frekuensi", color_continuous_scale=["#ffeaa7", "#e17055", "#d63031"], title="Proyeksi Risiko 6 Bulan ke Depan (menurut KII)", text="Frekuensi")
        fig_ske.update_traces(textposition="outside")
        fig_ske.update_layout(coloraxis_showscale=False, xaxis_tickangle=-25)
        st.plotly_chart(configure_chart_layout(fig_ske, height=340, reverse_y=False), use_container_width=True)

    # Heatmap KII
    st.markdown("<div class='section-header'>🗺️ Intensitas Isu KII per Wilayah (Heatmap)</div>", unsafe_allow_html=True)
    tema_wil_i = fi_.groupby(["Wilayah", "Tema_List"]).size().reset_index(name="Jumlah")
    tema_wil_i = tema_wil_i[tema_wil_i["Tema_List"] != "Kehidupan Sehari-hari & Lainnya"]
    pivot_i = tema_wil_i.pivot(index="Tema_List", columns="Wilayah", values="Jumlah").fillna(0)

    fig_heat_i = px.imshow(pivot_i, color_continuous_scale="Blues", title="Intensitas Isu per Wilayah — KII (Narasumber Pemerintah)", aspect="auto", text_auto=True)
    fig_heat_i.update_layout(coloraxis_showscale=True)
    st.plotly_chart(configure_chart_layout(fig_heat_i, height=380, is_bar=False), use_container_width=True)

    with st.expander("📋 Lihat Data Mentah — Dataset KII"):
        st.dataframe(fi[["Wilayah", "Narsum", "Pertanyaan", "Tanggapan"]], use_container_width=True, height=350)


# ==============================================================================
# TAB 3 — LAPORAN EKSEKUTIF
# ==============================================================================
with tab3:
    st.markdown("## 📄 Laporan Eksekutif — Analisis Isu Papua (GECAR 2024–2025)")
    st.markdown("---")

    # BAGIAN A
    st.markdown("<div class='section-header'>🧩 BAGIAN A — ISU UTAMA: MASYARAKAT (FGD Kelompok)</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='issue-card'>
      <b>🔴 ISU 1 — Kekerasan Domestik Terhadap Anak sebagai Ketakutan Utama</b><br>
      Responden anak dari ketiga wilayah (Jayawijaya, Asmat, Sentani) menyebut <b>kekerasan fisik dari orang tua</b> sebagai ketakutan nomor satu mereka. Tanggapan seperti <i>"mendapatkan kekerasan fisik dari bapak saya"</i> muncul berulang kali. Ini merupakan sinyal bahwa <b>program perlindungan anak dan parenting positif</b> sangat mendesak.
    </div>
    <div class='issue-card issue-card-orange'>
      <b>🍺 ISU 2 — Minuman Keras (Miras) sebagai Pemicu Utama Kekerasan Komunitas</b><br>
      Miras/alkohol disebut sebagai <b>penyebab langsung kekerasan fisik, pencurian, perselingkuhan, hingga perang suku</b>. Pola ini konsisten lintas wilayah, menunjukkan miras sebagai <b>amplifier kerentanan</b>.
    </div>
    <div class='issue-card' style='border-left-color:#e67e22;'>
      <b>💸 ISU 3 — Korupsi Sistemik Dana Bantuan (BLT) oleh Kepala Kampung</b><br>
      Masyarakat Asmat secara konsisten melaporkan pemotongan BLT sebesar Rp200.000–300.000 per KK, pengangkatan sepihak, dan ancaman pencoretan nama. Ini adalah <b>korupsi berjamaah yang terstruktur</b>.
    </div>
    <div class='issue-card issue-card-blue'>
      <b>📚 ISU 4 — Pendidikan Terganggu oleh Konflik, Kemiskinan & Kurangnya Pendampingan</b><br>
      Responden dewasa menekankan anak putus sekolah akibat pemalangan jalan dan faktor ekonomi, padahal responden anak menjadikan <b>sekolah sebagai ruang aman</b> mereka.
    </div>
    <div class='issue-card issue-card-green'>
      <b>🌱 ISU 5 — Pemuda Memiliki Potensi Kontribusi yang Belum Dimaksimalkan</b><br>
      Responden muda menunjukkan kesadaran tinggi untuk berkontribusi positif, namun potensi ini <b>belum difasilitasi secara terstruktur</b> (butuh alat musik, lapangan olahraga, forum pemuda).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # BAGIAN B
    st.markdown("<div class='section-header'>🏛️ BAGIAN B — ISU UTAMA: NARASUMBER PEMERINTAH (KII)</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='issue-card'>
      <b>🔫 ISU 1 — Konflik Bersenjata Kelompok Separatis di Jayawijaya</b><br>
      Narasumber mengidentifikasi kelompok Egianus Kogoya sebagai ancaman utama. Dampaknya terasa langsung pada <b>keterbatasan akses pendidikan dan trauma berkepanjangan bagi anak-anak</b>.
    </div>
    <div class='issue-card issue-card-orange'>
      <b>💊 ISU 2 — Krisis Narkoba & HIV pada Anak di Sentani (Temuan Mengejutkan)</b><br>
      Dinas Sosial & Pendidikan melaporkan temuan anak SD pemakai narkoba, hirup aibon, hingga <b>siswa kelas 5 SD terinfeksi HIV/AIDS</b> akibat kerentanan kekerasan seksual. Ini butuh <b>intervensi mendesak</b>.
    </div>
    <div class='issue-card' style='border-left-color:#27ae60;'>
      <b>🌿 ISU 3 — Konflik Lahan & Ekosida: PSN vs Masyarakat Adat di Asmat/Merauke</b><br>
      Proyek Strategis Nasional (food estate & tebu) memicu deforestasi gambut, penggusuran lahan adat tanpa konsultasi, serta polarisasi suku. Hubungan adat dengan tanah bersifat <b>sakral secara budaya</b>.
    </div>
    <div class='issue-card issue-card-blue'>
      <b>📚 ISU 4 — Kualitas Pendidikan Rendah: Guru Hanya Mencari Gaji, PAUD Tidak Fungsional</b><br>
      Banyak guru mengajar sekadar rutinitas komersial. PAUD dijalankan asal-asalan demi dana BUP menggunakan rumah pribadi tanpa standarisasi baku.
    </div>
    <div class='issue-card' style='border-left-color:#8e44ad;'>
      <b>📈 ISU 5 — Krisis Pangan & Inflasi Tertinggi Nasional</b><br>
      Papua Pegunungan mencatat <b>inflasi 5,65% (tertinggi nasional)</b> karena ketergantungan penuh logistik udara via Wamena yang rentan cuaca dan gangguan keamanan.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # REKOMENDASI
    st.markdown("<div class='section-header'>✅ REKOMENDASI STRATEGIS UNTUK WVI & MITRA PROGRAM</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏠 Perlindungan Anak & Pengasuhan Positif**
        - Program parenting positif untuk orang tua mengurangi kekerasan domestik.
        - Posko ramah anak dan ruang aman kepemudaan.

        **💊 Intervensi Narkoba & Kesehatan Remaja**
        - Kerjasama WVI–BNN untuk skrining/penyuluhan sekolah.
        - Edukasi kesehatan reproduksi & HIV sejak dini.
        
        **📚 Penguatan Pendidikan & Kapasitas Guru**
        - Program penyegaran guru "Mengajar sebagai Panggilan".
        - Advokasi administrasi kelayakan PAUD dan beasiswa putus sekolah.
        """)

    with col2:
        st.markdown("""
        **💸 Akuntabilitas Dana Bantuan**
        - Mekanisme pelaporan warga atas pemotongan dana desa/BLT.
        - Pemberdayaan BAMUSKAM sebagai fungsi pengawasan (checks & balances).

        **🌿 Advokasi Lahan & Pembangunan Damai**
        - Pendampingan hukum hak ulayat berbasis HAM bagi masyarakat adat.
        - Mediasi lokal via dialog "Para-Para Adat".

        **🔐 Ketahanan Pangan & Logistik**
        - Inisiasi program tabungan komunitas (ASKA) dan kebun komunal buffer lokal.
        """)

    st.markdown("---")
    st.caption("📊 Dashboard ini dibuat berdasarkan analisis data kualitatif GECAR 2024–2025. Frekuensi mencerminkan kemunculan tema dalam tanggapan, bukan persentase absolut.")
