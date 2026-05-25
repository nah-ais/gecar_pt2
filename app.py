"""
GECAR Dashboard — Analisis Isu Komunitas Papua
Senior Data Scientist & Expert Streamlit Developer
Dataset: Gecar_-_Kelompok.csv & Gecar_-_KII.csv
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, re
from collections import Counter

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GECAR Dashboard | Analisis Isu Komunitas Papua",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp { background: #0f1117; }

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12151f 0%, #0d1117 100%);
    border-right: 1px solid #1e2a3a;
}
[data-testid="stSidebar"] .block-container { padding-top: 1rem; }

/* Headers */
h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #f0f4ff !important; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1a2744 0%, #0f2027 40%, #203a43 100%);
    border: 1px solid #2a3f5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #f0f9ff;
    letter-spacing: -0.5px;
    margin: 0 0 0.4rem 0;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #94a3b8;
    margin: 0;
    font-weight: 400;
}
.hero-tag {
    display: inline-block;
    background: rgba(56,189,248,0.12);
    color: #38bdf8;
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.8rem;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1a2130 0%, #141b2d 100%);
    border: 1px solid #1e2d40;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #38bdf8; }
.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #38bdf8;
    font-family: 'Space Mono', monospace;
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 0.3rem;
    font-weight: 600;
}
.metric-sub {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 0.2rem;
}

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #1e2d40;
}
.section-icon {
    font-size: 1.1rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0;
}

/* Isu card */
.isu-card {
    background: #111827;
    border: 1px solid #1e2d40;
    border-left: 3px solid;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s;
}
.isu-card:hover { background: #141e2e; }
.isu-title {
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.isu-desc {
    font-size: 0.82rem;
    color: #94a3b8;
    line-height: 1.5;
}

/* Quote block */
.quote-block {
    background: rgba(30,42,58,0.6);
    border-left: 3px solid #38bdf8;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.82rem;
    color: #cbd5e1;
    font-style: italic;
    line-height: 1.6;
}

/* Tab styling */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #0d1117;
    border-bottom: 1px solid #1e2a3a;
    gap: 0;
    padding: 0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-size: 0.87rem;
    font-weight: 600;
    color: #64748b;
    padding: 0.7rem 1.2rem;
    border-radius: 0;
    background: transparent;
    border-bottom: 2px solid transparent;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom-color: #38bdf8 !important;
    background: rgba(56,189,248,0.05) !important;
}

/* Divider */
.custom-divider {
    border: none;
    border-top: 1px solid #1e2d40;
    margin: 1.5rem 0;
}

/* Filter label */
.filter-label {
    font-size: 0.78rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    margin-bottom: 0.3rem;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
}
.badge-red { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.25); }
.badge-amber { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.25); }
.badge-green { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }
.badge-blue { background: rgba(56,189,248,0.15); color: #38bdf8; border: 1px solid rgba(56,189,248,0.25); }

/* Table */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Plotly chart bg */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

</style>
""", unsafe_allow_html=True)

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
COLORS = {
    'primary': '#38bdf8',
    'secondary': '#818cf8',
    'accent': '#f472b6',
    'success': '#4ade80',
    'warning': '#fbbf24',
    'danger': '#f87171',
    'chart': ['#38bdf8', '#818cf8', '#f472b6', '#4ade80', '#fbbf24', '#f87171', '#a78bfa', '#fb923c'],
    'bg': 'rgba(0,0,0,0)',
    'paper': 'rgba(0,0,0,0)',
    'grid': 'rgba(30,42,58,0.8)',
    'text': '#94a3b8',
    'text_main': '#e2e8f0',
}

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor=COLORS['bg'],
        plot_bgcolor=COLORS['bg'],
        font=dict(family='Plus Jakarta Sans', color=COLORS['text']),
        xaxis=dict(gridcolor=COLORS['grid'], zerolinecolor=COLORS['grid'], linecolor=COLORS['grid']),
        yaxis=dict(gridcolor=COLORS['grid'], zerolinecolor=COLORS['grid'], linecolor=COLORS['grid']),
        colorway=COLORS['chart'],
        margin=dict(l=40, r=20, t=40, b=40),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=COLORS['text'])),
    )
)


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    paths = {
        'kelompok': [
            'Gecar_-_Kelompok.csv',
            '/mnt/user-data/uploads/Gecar_-_Kelompok.csv',
        ],
        'kii': [
            'Gecar_-_KII.csv',
            '/mnt/user-data/uploads/Gecar_-_KII.csv',
        ]
    }
    dfs = {}
    for key, candidates in paths.items():
        for path in candidates:
            if os.path.exists(path):
                try:
                    dfs[key] = pd.read_csv(path)
                    break
                except Exception:
                    continue
        if key not in dfs:
            st.error(f"❌ File tidak ditemukan: {key}. Pastikan file CSV tersedia.")
            st.stop()
    return dfs['kelompok'], dfs['kii']


df_k, df_kii = load_data()

# ─── PREPROCESSING ────────────────────────────────────────────────────────────
@st.cache_data
def preprocess(df_k, df_kii):
    # Normalize column names
    df_k.columns = df_k.columns.str.strip()
    df_kii.columns = df_kii.columns.str.strip()

    # Kelompok: categorize questions
    def categorize_q(q):
        q_lower = str(q).lower()
        if any(kw in q_lower for kw in ['sehari-hari', 'kehidupan sehari']):
            return 'Kehidupan Sehari-hari'
        elif any(kw in q_lower for kw in ['berubah', 'perubahan']):
            return 'Perubahan Komunitas'
        elif 'ketakutan' in q_lower:
            return 'Ketakutan & Kekhawatiran'
        elif 'harapan' in q_lower:
            return 'Harapan Masa Depan'
        elif 'kebutuhan' in q_lower or 'kebutuhan utama' in q_lower:
            return 'Kebutuhan Utama'
        elif 'ketegangan' in q_lower:
            return 'Ketegangan Komunitas'
        elif 'tokoh' in q_lower or 'berpengaruh' in q_lower:
            return 'Tokoh Berpengaruh'
        elif '6 bulan' in q_lower or 'skenario' in q_lower:
            return 'Skenario 6 Bulan'
        elif 'pemuda' in q_lower or 'berkontribusi' in q_lower or 'kontribusi' in q_lower:
            return 'Kontribusi Pemuda'
        elif 'aman' in q_lower or 'merasa aman' in q_lower:
            return 'Rasa Aman'
        elif 'menyatukan' in q_lower or 'memecah' in q_lower:
            return 'Kohesi Sosial'
        elif 'tokoh' in q_lower or 'aktor' in q_lower:
            return 'Persepsi Aktor'
        elif 'perdamaian' in q_lower:
            return 'Upaya Perdamaian'
        elif 'masukan' in q_lower or 'wvi' in q_lower:
            return 'Masukan untuk WVI'
        else:
            return 'Lainnya'

    df_k['Kategori_Q'] = df_k['Pertanyaan'].apply(categorize_q)

    # KII: categorize questions
    def categorize_q_kii(q):
        q_lower = str(q).lower()
        if 'kebutuhan' in q_lower:
            return 'Kebutuhan Utama'
        elif 'ketegangan' in q_lower or 'tegangan' in q_lower:
            return 'Ketegangan & Konflik'
        elif 'kelompok rentan' in q_lower or 'rentan' in q_lower:
            return 'Kelompok Rentan'
        elif 'menyatukan' in q_lower or 'memecah' in q_lower:
            return 'Kohesi Sosial'
        elif 'perdamaian' in q_lower:
            return 'Upaya Perdamaian'
        elif 'berpengaruh' in q_lower or 'kelompok mana' in q_lower:
            return 'Aktor Kunci'
        elif '6 bulan' in q_lower or 'perkirakan' in q_lower or 'skenario' in q_lower:
            return 'Proyeksi 6 Bulan'
        elif 'konsekuensi' in q_lower or 'lsm' in q_lower or 'operasional' in q_lower:
            return 'Dampak bagi LSM'
        elif 'wvi' in q_lower or 'pesan' in q_lower or 'masukan' in q_lower:
            return 'Masukan & Harapan'
        elif 'hubungan' in q_lower or 'tujuan' in q_lower or 'kemampuan' in q_lower:
            return 'Peta Aktor'
        elif 'narkoba' in q_lower or 'aibon' in q_lower:
            return 'Isu Narkoba'
        else:
            return 'Lainnya'

    df_kii['Kategori_Q'] = df_kii['Pertanyaan'].apply(categorize_q_kii)

    return df_k, df_kii


df_k, df_kii = preprocess(df_k, df_kii)

# ─── THEME FREQUENCY ANALYSIS ────────────────────────────────────────────────
ISU_THEMES = {
    'Miras & Alkohol': ['miras', 'mabok', 'mabuk', 'alkohol', 'minuman keras', 'minuman'],
    'Narkoba & Aibon': ['narkoba', 'aibon', 'ganja', 'obat-obatan terlarang', 'bnn', 'narkotika'],
    'Pendidikan': ['sekolah', 'pendidikan', 'guru', 'belajar', 'paud', 'kuliah', 'ilmu'],
    'Kekerasan & Kriminalitas': ['pencurian', 'begal', 'kekerasan', 'pembunuhan', 'perang suku', 'kriminal', 'ancaman'],
    'Ekonomi & Kemiskinan': ['ekonomi', 'kemiskinan', 'pekerjaan', 'penghasilan', 'bantuan', 'modal', 'susah', 'miskin'],
    'Kesehatan': ['kesehatan', 'sakit', 'rumah sakit', 'dokter', 'hiv', 'imunisasi', 'hamil', 'medis'],
    'Infrastruktur': ['jalan', 'air bersih', 'listrik', 'infrastruktur', 'pembangunan', 'fasilitas', 'kamar mandi'],
    'Perang Suku & Konflik': ['perang suku', 'konflik', 'ketegangan', 'sengketa lahan', 'denda adat', 'suku'],
    'Pemerintahan': ['pemerintah', 'bupati', 'dinas', 'apbd', 'musrenbang', 'kepala kampung', 'korupsi'],
    'Perlindungan Anak': ['anak-anak', 'remaja', 'perlindungan anak', 'rentan', 'trauma', 'broken home'],
}


@st.cache_data
def compute_theme_freq(df, col='Tanggapan'):
    all_text = ' '.join(df[col].dropna().str.lower().tolist())
    result = {}
    for theme, kws in ISU_THEMES.items():
        cnt = sum(all_text.count(kw) for kw in kws)
        result[theme] = cnt
    return pd.DataFrame(list(result.items()), columns=['Tema', 'Frekuensi']).sort_values('Frekuensi', ascending=False)


freq_k = compute_theme_freq(df_k)
freq_kii = compute_theme_freq(df_kii)


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1.2rem 0;">
        <div style="font-size:2.5rem;">🏔️</div>
        <div style="font-size:1rem; font-weight:800; color:#f0f9ff; margin-top:0.3rem;">GECAR</div>
        <div style="font-size:0.72rem; color:#64748b; font-family:'Space Mono',monospace; letter-spacing:1px;">COMMUNITY INSIGHT DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="filter-label">📍 Filter Wilayah</div>', unsafe_allow_html=True)
    all_wilayah = sorted(df_k['Wilayah'].dropna().unique().tolist())
    sel_wilayah = st.multiselect(
        label="Wilayah",
        options=all_wilayah,
        default=all_wilayah,
        label_visibility="collapsed"
    )

    st.markdown('<div class="filter-label" style="margin-top:1rem;">👤 Filter Kelompok Usia</div>', unsafe_allow_html=True)
    all_usia = sorted(df_k['Kelompok_Usia'].dropna().unique().tolist())
    sel_usia = st.multiselect(
        label="Kelompok Usia",
        options=all_usia,
        default=all_usia,
        label_visibility="collapsed"
    )

    st.markdown('<div class="filter-label" style="margin-top:1rem;">⚥ Filter Jenis Kelamin</div>', unsafe_allow_html=True)
    all_jk = sorted(df_k['Jenis_Kelamin'].dropna().unique().tolist())
    sel_jk = st.multiselect(
        label="Jenis Kelamin",
        options=all_jk,
        default=all_jk,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="filter-label">🏛️ Filter Narasumber (KII)</div>', unsafe_allow_html=True)
    narsum_label = {
        'GTY': 'GTY — Gereja/Tokoh Agama',
        'JPY': 'JPY — Jaringan Perdamaian',
        'ACL': 'ACL — Tokoh Lokal',
        'Dinas Sosial': 'Dinas Sosial',
        'Dinas Pendidikan': 'Dinas Pendidikan',
    }
    all_narsum = sorted(df_kii['Narsum'].dropna().unique().tolist())
    sel_narsum = st.multiselect(
        label="Narasumber",
        options=all_narsum,
        default=all_narsum,
        format_func=lambda x: narsum_label.get(x, x),
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem; color:#475569; text-align:center; line-height:1.6;">
        <span style="color:#64748b">Data:</span> GECAR Field Survey 2025<br>
        <span style="color:#64748b">Wilayah:</span> Jayawijaya · Sentani · Asmat<br>
        <span style="color:#64748b">Built with</span> Streamlit + Plotly
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER DATA ─────────────────────────────────────────────────────────────
if not sel_wilayah:
    sel_wilayah = all_wilayah
if not sel_usia:
    sel_usia = all_usia
if not sel_jk:
    sel_jk = all_jk
if not sel_narsum:
    sel_narsum = all_narsum

df_k_f = df_k[
    (df_k['Wilayah'].isin(sel_wilayah)) &
    (df_k['Kelompok_Usia'].isin(sel_usia)) &
    (df_k['Jenis_Kelamin'].isin(sel_jk))
]
df_kii_f = df_kii[
    (df_kii['Narsum'].isin(sel_narsum))
]

# ─── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">GECAR · FIELD ASSESSMENT · PAPUA 2025</div>
    <div class="hero-title">Dashboard Analisis Isu Komunitas Papua</div>
    <div class="hero-subtitle">
        Visualisasi interaktif hasil survei lapangan dari kelompok masyarakat & narasumber kunci (KII) 
        di Jayawijaya, Sentani, dan Asmat — mengidentifikasi isu, ketegangan, dan harapan komunitas.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── OVERVIEW METRICS ─────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    (c1, len(df_k_f), "Total Responden\nKelompok", f"{len(df_k_f['Wilayah'].unique())} wilayah"),
    (c2, len(df_kii_f), "Total Responden\nKII", f"{len(df_kii_f['Narsum'].unique())} narasumber"),
    (c3, len(df_k_f['Pertanyaan'].unique()), "Topik\nPertanyaan (Kelompok)", "multi-tema"),
    (c4, len(df_kii_f['Pertanyaan'].unique()), "Topik\nPertanyaan (KII)", "mendalam"),
    (c5, 10, "Tema Isu\nDianalisis", "lintas dataset"),
]
for col, val, label, sub in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Peta Isu Utama",
    "👥 Dataset Kelompok",
    "🏛️ Dataset KII",
    "🔍 Analisis Lintas Dataset",
    "📋 Laporan Eksekutif",
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1 — PETA ISU UTAMA
# ═══════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🗺️</span>
        <span class="section-title">Peta Isu: Frekuensi Kemunculan Tema dalam Respons</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Frekuensi dihitung berdasarkan kemunculan kata-kata kunci tematik dalam semua teks tanggapan responden (setelah filter diterapkan).")

    freq_k_f = compute_theme_freq(df_k_f)
    freq_kii_f = compute_theme_freq(df_kii_f)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**📣 Kelompok Masyarakat** — Tema dominan dalam tanggapan warga")
        fig = px.bar(
            freq_k_f.sort_values('Frekuensi'),
            x='Frekuensi', y='Tema', orientation='h',
            color='Frekuensi',
            color_continuous_scale=['#1e3a5f', '#38bdf8'],
            text='Frekuensi',
        )
        fig.update_traces(textposition='outside', textfont_color=COLORS['text_main'])
        fig.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            coloraxis_showscale=False,
            height=400,
            yaxis_title="", xaxis_title="Frekuensi Kata Kunci",
            title_text="",
        )
        st.plotly_chart(fig, width="stretch")

    with col_b:
        st.markdown("**🏛️ KII (Pemerintah & Tokoh Kunci)** — Tema dominan dalam tanggapan narasumber")
        fig2 = px.bar(
            freq_kii_f.sort_values('Frekuensi'),
            x='Frekuensi', y='Tema', orientation='h',
            color='Frekuensi',
            color_continuous_scale=['#1e1f5e', '#818cf8'],
            text='Frekuensi',
        )
        fig2.update_traces(textposition='outside', textfont_color=COLORS['text_main'])
        fig2.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            coloraxis_showscale=False,
            height=400,
            yaxis_title="", xaxis_title="Frekuensi Kata Kunci",
        )
        st.plotly_chart(fig2, width="stretch")

    # Radar comparison
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🎯</span>
        <span class="section-title">Radar Komparasi: Prioritas Isu Kelompok vs KII</span>
    </div>
    """, unsafe_allow_html=True)

    themes_common = freq_k_f['Tema'].tolist()
    k_vals = freq_k_f.set_index('Tema')['Frekuensi'].reindex(themes_common).fillna(0).tolist()
    kii_vals = freq_kii_f.set_index('Tema')['Frekuensi'].reindex(themes_common).fillna(0).tolist()

    # Normalize to 0-100
    max_k = max(k_vals) if max(k_vals) > 0 else 1
    max_kii = max(kii_vals) if max(kii_vals) > 0 else 1
    k_norm = [round(v / max_k * 100, 1) for v in k_vals]
    kii_norm = [round(v / max_kii * 100, 1) for v in kii_vals]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=k_norm + [k_norm[0]],
        theta=themes_common + [themes_common[0]],
        fill='toself',
        name='Kelompok Masyarakat',
        line_color=COLORS['primary'],
        fillcolor='rgba(56,189,248,0.15)',
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=kii_norm + [kii_norm[0]],
        theta=themes_common + [themes_common[0]],
        fill='toself',
        name='KII (Pemerintah/Tokoh)',
        line_color=COLORS['secondary'],
        fillcolor='rgba(129,140,248,0.15)',
    ))
    fig_radar.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=COLORS['grid'], color=COLORS['text']),
            angularaxis=dict(gridcolor=COLORS['grid'], color=COLORS['text']),
        ),
        height=420,
        showlegend=True,
    )
    st.plotly_chart(fig_radar, width="stretch")

    st.markdown("""
    <div class="quote-block">
    💡 <strong>Interpretasi Radar:</strong> Area yang lebih besar menunjukkan isu lebih sering disebut. 
    Perbedaan bentuk antara Kelompok Masyarakat (biru) dan KII (ungu) mencerminkan <em>gap persepsi</em> — 
    isu yang diprioritaskan warga tidak selalu sama dengan yang diprioritaskan aktor kebijakan.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# TAB 2 — DATASET KELOMPOK
# ═══════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">👥</span>
        <span class="section-title">Analisis Dataset Kelompok Masyarakat</span>
    </div>
    """, unsafe_allow_html=True)

    # Sub-metrics
    m1, m2, m3, m4 = st.columns(4)
    for col, val, label in [
        (m1, df_k_f['Wilayah'].nunique(), "Wilayah"),
        (m2, df_k_f[df_k_f['Kelompok_Usia']=='Anak'].shape[0], "Resp. Anak"),
        (m3, df_k_f[df_k_f['Kelompok_Usia']=='Dewasa'].shape[0], "Resp. Dewasa"),
        (m4, df_k_f['Pertanyaan'].nunique(), "Topik Pertanyaan"),
    ]:
        with col:
            st.metric(label, val)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # 1. Distribusi respons per wilayah
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### 📍 Distribusi Respons per Wilayah & Kategori Pertanyaan")
        cat_wilayah = df_k_f.groupby(['Wilayah', 'Kategori_Q']).size().reset_index(name='Jumlah')
        fig_bar = px.bar(
            cat_wilayah, x='Wilayah', y='Jumlah', color='Kategori_Q',
            barmode='stack',
            color_discrete_sequence=COLORS['chart'],
        )
        fig_bar.update_layout(**PLOTLY_TEMPLATE['layout'], height=380, xaxis_title="", yaxis_title="Jumlah Respons")
        st.plotly_chart(fig_bar, width="stretch")

    with col2:
        st.markdown("#### 🎯 Kategori Pertanyaan Terbanyak")
        cat_count = df_k_f['Kategori_Q'].value_counts().reset_index()
        cat_count.columns = ['Kategori', 'Jumlah']
        fig_pie = px.pie(
            cat_count, values='Jumlah', names='Kategori',
            hole=0.45,
            color_discrete_sequence=COLORS['chart'],
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
        fig_pie.update_layout(**PLOTLY_TEMPLATE['layout'], height=380, showlegend=False)
        st.plotly_chart(fig_pie, width="stretch")

    # 2. ISU UTAMA: Ketegangan & Kebutuhan
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### ⚠️ ISU 1 — Ketegangan Sosial: Apa yang Disebut Masyarakat?")
    col_a, col_b = st.columns([1, 1])

    # Ketegangan - extract specific issues
    df_ket = df_k_f[df_k_f['Kategori_Q'] == 'Ketegangan Komunitas'].copy()

    # Keyword tagging
    def tag_ketegangan(text):
        t = str(text).lower()
        tags = []
        if any(kw in t for kw in ['mabok', 'miras', 'mabuk', 'alkohol']): tags.append('Miras/Alkohol')
        if any(kw in t for kw in ['judol', 'judi']): tags.append('Judi Online')
        if any(kw in t for kw in ['ganja', 'narkoba', 'aibon']): tags.append('Narkoba/Aibon')
        if any(kw in t for kw in ['pencurian', 'begal', 'curi']): tags.append('Pencurian/Begal')
        if any(kw in t for kw in ['perang suku', 'konflik', 'perang']): tags.append('Perang Suku')
        if any(kw in t for kw in ['pembunuhan', 'bunuh']): tags.append('Kekerasan/Pembunuhan')
        if any(kw in t for kw in ['ekonomi', 'kerja', 'pekerjaan', 'kemiskinan']): tags.append('Ekonomi')
        if any(kw in t for kw in ['pemerintah', 'dinas', 'kepala']): tags.append('Tata Kelola')
        if any(kw in t for kw in ['lahan', 'tanah', 'warisan']): tags.append('Sengketa Lahan')
        if any(kw in t for kw in ['pendidikan', 'sekolah', 'guru']): tags.append('Pendidikan')
        return tags if tags else ['Lainnya']

    all_tags = []
    for text in df_ket['Tanggapan'].dropna():
        all_tags.extend(tag_ketegangan(text))
    tag_counts = Counter(all_tags)

    with col_a:
        if tag_counts:
            tag_df = pd.DataFrame(tag_counts.items(), columns=['Isu', 'Frekuensi']).sort_values('Frekuensi', ascending=True)
            fig_tag = px.bar(
                tag_df, x='Frekuensi', y='Isu', orientation='h',
                color='Frekuensi',
                color_continuous_scale=['#1e2d40', '#f87171'],
                text='Frekuensi',
            )
            fig_tag.update_traces(textposition='outside', textfont_color=COLORS['text_main'])
            fig_tag.update_layout(
                **PLOTLY_TEMPLATE['layout'],
                coloraxis_showscale=False,
                height=340, title_text="Jenis Ketegangan (Kelompok Masyarakat)",
                yaxis_title="", xaxis_title="Kemunculan dalam Respons",
            )
            st.plotly_chart(fig_tag, width="stretch")

    with col_b:
        st.markdown("**💬 Kutipan Langsung — Ketegangan di Komunitas**")
        sample_ket = df_ket['Tanggapan'].dropna().sample(min(6, len(df_ket)), random_state=42).tolist()
        for q in sample_ket:
            st.markdown(f'<div class="quote-block">"{q[:180]}{"..." if len(q)>180 else ""}"</div>', unsafe_allow_html=True)

    # 3. ISU 2: Kebutuhan Utama
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🏥 ISU 2 — Kebutuhan Utama Komunitas per Wilayah")

    df_keb = df_k_f[df_k_f['Kategori_Q'] == 'Kebutuhan Utama'].copy()

    def tag_kebutuhan(text):
        t = str(text).lower()
        tags = []
        if any(kw in t for kw in ['sekolah', 'pendidikan', 'guru', 'belajar', 'paud']): tags.append('Pendidikan')
        if any(kw in t for kw in ['kesehatan', 'sakit', 'rumah sakit', 'dokter', 'imunisasi', 'rs']): tags.append('Kesehatan')
        if any(kw in t for kw in ['air', 'sumur', 'blong', 'pah']): tags.append('Air Bersih')
        if any(kw in t for kw in ['jalan', 'infrastruktur', 'kamar mandi', 'jembatan']): tags.append('Infrastruktur')
        if any(kw in t for kw in ['ekonomi', 'kerja', 'modal', 'usaha', 'ternak', 'bibit', 'ikan']): tags.append('Ekonomi/Mata Pencaharian')
        if any(kw in t for kw in ['pemerintah', 'dinas', 'bantuan', 'bama', 'bansos']): tags.append('Dukungan Pemerintah')
        if any(kw in t for kw in ['anak', 'remaja', 'pemuda']): tags.append('Perlindungan Anak/Remaja')
        return tags if tags else ['Lainnya']

    all_keb_tags = []
    wilayah_keb = []
    for _, row in df_keb.iterrows():
        tags = tag_kebutuhan(str(row['Tanggapan']))
        for t in tags:
            all_keb_tags.append(t)
            wilayah_keb.append(row['Wilayah'])

    keb_df = pd.DataFrame({'Kebutuhan': all_keb_tags, 'Wilayah': wilayah_keb})
    keb_cross = keb_df.groupby(['Wilayah', 'Kebutuhan']).size().reset_index(name='Jumlah')

    fig_keb = px.bar(
        keb_cross, x='Kebutuhan', y='Jumlah', color='Wilayah',
        barmode='group',
        color_discrete_sequence=COLORS['chart'],
        text_auto=True,
    )
    fig_keb.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        height=380, xaxis_title="", yaxis_title="Kemunculan",
        xaxis_tickangle=-20,
    )
    st.plotly_chart(fig_keb, width="stretch")

    # 4. ISU 3: Rasa Aman & Ketakutan
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 😰 ISU 3 — Ketakutan & Rasa Aman: Perspektif Anak vs Dewasa")

    df_takut = df_k_f[df_k_f['Kategori_Q'] == 'Ketakutan & Kekhawatiran']
    df_aman = df_k_f[df_k_f['Kategori_Q'] == 'Rasa Aman']

    def categorize_fear(text):
        t = str(text).lower()
        if any(kw in t for kw in ['miras', 'mabok', 'mabuk', 'alkohol', 'parang', 'pukul']): return 'Kekerasan akibat Miras'
        elif any(kw in t for kw in ['perang suku', 'konflik', 'perang', 'suku']): return 'Perang Suku & Konflik'
        elif any(kw in t for kw in ['orang tua', 'bapa', 'mama', 'keluarga', 'papa']): return 'Kehilangan/Masalah Keluarga'
        elif any(kw in t for kw in ['sekolah', 'nilai', 'ujian', 'guru']): return 'Akademik & Sekolah'
        elif any(kw in t for kw in ['masa depan', 'tujuan hidup', 'generasi', 'canggih']): return 'Masa Depan & Arah Hidup'
        elif any(kw in t for kw in ['bencana', 'hujan', 'angin', 'pohon']): return 'Bencana Alam'
        elif any(kw in t for kw in ['kecelakaan', 'tebang', 'gergaji', 'kerja']): return 'Kecelakaan Kerja'
        else: return 'Lainnya'

    fear_tags = df_takut['Tanggapan'].dropna().apply(categorize_fear)
    fear_df = pd.DataFrame({'Ketakutan': fear_tags, 'Kelompok_Usia': df_takut.loc[fear_tags.index, 'Kelompok_Usia']})
    fear_cross = fear_df.groupby(['Ketakutan', 'Kelompok_Usia']).size().reset_index(name='Jumlah')

    col_f1, col_f2 = st.columns([3, 2])
    with col_f1:
        fig_fear = px.bar(
            fear_cross, x='Jumlah', y='Ketakutan', color='Kelompok_Usia',
            barmode='group', orientation='h',
            color_discrete_map={'Anak': COLORS['primary'], 'Dewasa': COLORS['secondary']},
            text_auto=True,
        )
        fig_fear.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            height=350, title_text="Jenis Ketakutan: Anak vs Dewasa",
            yaxis_title="", xaxis_title="Jumlah Responden",
        )
        st.plotly_chart(fig_fear, width="stretch")

    with col_f2:
        st.markdown("**🛡️ Kutipan — Apa yang Membuat Mereka Merasa Aman?**")
        sample_aman = df_aman['Tanggapan'].dropna().sample(min(5, len(df_aman)), random_state=7).tolist()
        for q in sample_aman:
            st.markdown(f'<div class="quote-block">"{q[:160]}{"..." if len(q)>160 else ""}"</div>', unsafe_allow_html=True)

    # 5. ISU 4: Harapan & Kontribusi Pemuda
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🌟 ISU 4 — Harapan Masa Depan & Peran Pemuda")

    df_harapan = df_k_f[df_k_f['Kategori_Q'] == 'Harapan Masa Depan']
    df_pemuda = df_k_f[df_k_f['Kategori_Q'] == 'Kontribusi Pemuda']

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.markdown("**💭 Harapan Masyarakat**")
        for t in df_harapan['Tanggapan'].dropna().head(6).tolist():
            st.markdown(f'<div class="quote-block">"{t[:200]}{"..." if len(t)>200 else ""}"</div>', unsafe_allow_html=True)
    with col_h2:
        st.markdown("**🚀 Kontribusi Pemuda**")
        for t in df_pemuda['Tanggapan'].dropna().head(6).tolist():
            st.markdown(f'<div class="quote-block">"{t[:200]}{"..." if len(t)>200 else ""}"</div>', unsafe_allow_html=True)

    # 6. ISU 5: Skenario 6 bulan ke depan
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🔮 ISU 5 — Proyeksi Komunitas: 6 Bulan ke Depan")

    df_ske = df_k_f[df_k_f['Kategori_Q'] == 'Skenario 6 Bulan']

    def tag_skenario(text):
        t = str(text).lower()
        if any(kw in t for kw in ['aman', 'keamanan', 'damai']): return 'Keamanan'
        elif any(kw in t for kw in ['politik', 'pilkada', 'bupati', 'kepala kampung']): return 'Politik'
        elif any(kw in t for kw in ['ekonomi', 'kerja', 'bantuan', 'uang', 'harga']): return 'Ekonomi'
        elif any(kw in t for kw in ['sosial', 'masyarakat', 'gotong', 'saling']): return 'Sosial'
        elif any(kw in t for kw in ['pendidikan', 'sekolah', 'guru']): return 'Pendidikan'
        else: return 'Lainnya'

    ske_tags = df_ske['Tanggapan'].dropna().apply(tag_skenario)
    ske_wilayah = df_ske.loc[ske_tags.index, 'Wilayah']
    ske_df = pd.DataFrame({'Aspek': ske_tags, 'Wilayah': ske_wilayah})
    ske_cross = ske_df.groupby(['Aspek', 'Wilayah']).size().reset_index(name='Jumlah')

    fig_ske = px.sunburst(
        ske_cross, path=['Aspek', 'Wilayah'], values='Jumlah',
        color='Aspek',
        color_discrete_sequence=COLORS['chart'],
    )
    fig_ske.update_layout(**PLOTLY_TEMPLATE['layout'], height=380)
    st.plotly_chart(fig_ske, width="stretch")


# ═══════════════════════════════════════════════════════════════════════
# TAB 3 — DATASET KII
# ═══════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🏛️</span>
        <span class="section-title">Analisis Dataset KII — Narasumber Kunci (Pemerintah & Tokoh)</span>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    with k1: st.metric("Total Respons", len(df_kii_f))
    with k2: st.metric("Narasumber Aktif", df_kii_f['Narsum'].nunique())
    with k3: st.metric("Topik Dibahas", df_kii_f['Kategori_Q'].nunique())

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ISU 1: Penyalahgunaan Narkoba & Aibon
    st.markdown("#### 💊 ISU 1 (KII) — Darurat Narkoba, Aibon, dan HIV pada Anak")

    col_n1, col_n2 = st.columns([2, 1])
    with col_n1:
        narko_kws = ['narkoba', 'aibon', 'bnn', 'hiv', 'rehabilitasi', 'broken home', 'pecandu', 'rehab', 'zat berbahaya']
        narko_counts = {}
        for ns in df_kii_f['Narsum'].unique():
            text = ' '.join(df_kii_f[df_kii_f['Narsum']==ns]['Tanggapan'].dropna().str.lower().tolist())
            narko_counts[ns] = sum(text.count(kw) for kw in narko_kws)

        ndf = pd.DataFrame(list(narko_counts.items()), columns=['Narasumber', 'Kemunculan Kata Kunci Narkoba'])
        fig_nark = px.bar(
            ndf.sort_values('Kemunculan Kata Kunci Narkoba', ascending=True),
            x='Kemunculan Kata Kunci Narkoba', y='Narasumber', orientation='h',
            color='Kemunculan Kata Kunci Narkoba',
            color_continuous_scale=['#1a0a0a', '#f87171'],
            text='Kemunculan Kata Kunci Narkoba',
        )
        fig_nark.update_traces(textposition='outside', textfont_color=COLORS['text_main'])
        fig_nark.update_layout(
            **PLOTLY_TEMPLATE['layout'],
            coloraxis_showscale=False, height=300,
            title_text="Kemunculan Isu Narkoba/Aibon per Narasumber",
        )
        st.plotly_chart(fig_nark, width="stretch")

    with col_n2:
        st.markdown("**⚠️ Fakta Kritis dari KII:**")
        st.markdown("""
        <div class="isu-card" style="border-left-color:#f87171;">
            <div class="isu-title" style="color:#f87171;">🚨 HIV pada Siswa SD</div>
            <div class="isu-desc">Ditemukan kasus anak kelas 5 SD terinfeksi HIV/AIDS, diduga akibat kekerasan seksual yang dipicu alkohol atau narkoba (Dinas Sosial, Sentani).</div>
        </div>
        <div class="isu-card" style="border-left-color:#fbbf24;">
            <div class="isu-title" style="color:#fbbf24;">⚡ Aibon di Jalanan</div>
            <div class="isu-desc">Anak-anak menggunakan aibon di jalanan. Fasilitas rehab sangat terbatas dan kurang mendukung pemulihan berkelanjutan.</div>
        </div>
        <div class="isu-card" style="border-left-color:#fb923c;">
            <div class="isu-title" style="color:#fb923c;">🏠 Broken Home & Kurang Pengawasan</div>
            <div class="isu-desc">Mayoritas anak yang terlibat narkoba berasal dari keluarga broken home. Ruang publik aman sangat minim.</div>
        </div>
        """, unsafe_allow_html=True)

    # ISU 2: Konflik & Ketegangan
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### ⚔️ ISU 2 (KII) — Konflik Bersenjata, Perang Suku & Ketegangan Identitas")

    df_konflik = df_kii_f[df_kii_f['Kategori_Q'].isin(['Ketegangan & Konflik', 'Aktor Kunci', 'Peta Aktor'])]

    col_k1, col_k2 = st.columns(2)
    with col_k1:
        # Aktor konflik mapping
        aktor_data = {
            'Kelompok Sipil Bersenjata\n(Egianus Kogoya)': 3,
            'Perang Suku\n(akar budaya)': 4,
            'Polarisasi Identitas\n(OAP vs Pendatang)': 3,
            'Media Sosial\n& Hoaks': 2,
            'Sengketa Lahan': 2,
            'Kontestasi Politik\n(Pilkada)': 2,
        }
        fig_aktor = px.treemap(
            names=list(aktor_data.keys()),
            parents=['Sumber Konflik'] * len(aktor_data),
            values=list(aktor_data.values()),
            color=list(aktor_data.values()),
            color_continuous_scale=['#1e1b4b', '#818cf8'],
        )
        fig_aktor.update_layout(**PLOTLY_TEMPLATE['layout'], height=320, title_text="Akar Sumber Konflik (Perspektif KII)")
        st.plotly_chart(fig_aktor, width="stretch")

    with col_k2:
        st.markdown("**💬 Perspektif Narasumber tentang Konflik:**")
        konflik_quotes = df_konflik['Tanggapan'].dropna().head(5).tolist()
        for q in konflik_quotes:
            st.markdown(f'<div class="quote-block">"{q[:220]}{"..." if len(q)>220 else ""}"</div>', unsafe_allow_html=True)

    # ISU 3: Kelompok Rentan
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 👦 ISU 3 (KII) — Kelompok Rentan: Anak, Remaja & Perempuan")

    df_rentan = df_kii_f[df_kii_f['Kategori_Q'] == 'Kelompok Rentan']
    rentan_kws = {
        'Anak-anak': ['anak', 'anak-anak'],
        'Remaja': ['remaja'],
        'Perempuan': ['perempuan'],
        'Masyarakat Sipil': ['sipil', 'masyarakat'],
        'Keluarga Broken Home': ['broken home', 'keluarga bermasalah'],
        'Petani/Ekonomi Lemah': ['petani', 'ekonomi lemah', 'miskin'],
    }
    rentan_counts = {}
    for cat, kws in rentan_kws.items():
        text = ' '.join(df_rentan['Tanggapan'].dropna().str.lower().tolist())
        rentan_counts[cat] = sum(text.count(kw) for kw in kws)

    rdf = pd.DataFrame(list(rentan_counts.items()), columns=['Kelompok', 'Kemunculan'])
    fig_rentan = px.pie(
        rdf[rdf['Kemunculan']>0], values='Kemunculan', names='Kelompok',
        hole=0.4, color_discrete_sequence=COLORS['chart'],
    )
    fig_rentan.update_traces(textinfo='percent+label', textfont_size=11)
    fig_rentan.update_layout(**PLOTLY_TEMPLATE['layout'], height=350, showlegend=True,
                             title_text="Kelompok Rentan yang Disebutkan Narasumber KII")
    st.plotly_chart(fig_rentan, width="stretch")

    # ISU 4: Pendidikan
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🎓 ISU 4 (KII) — Krisis Pendidikan: Guru, PAUD & Honor Tertunda")

    df_diknas = df_kii_f[df_kii_f['Narsum'] == 'Dinas Pendidikan']
    if not df_diknas.empty:
        for t in df_diknas['Tanggapan'].dropna().tolist():
            st.markdown(f'<div class="quote-block">📚 "{t[:280]}{"..." if len(t)>280 else ""}"</div>', unsafe_allow_html=True)
    else:
        st.info("Data Dinas Pendidikan tidak tersedia dalam filter saat ini.")

    # ISU 5: Proyeksi 6 Bulan
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🔭 ISU 5 (KII) — Proyeksi 6 Bulan Mendatang menurut Narasumber Kunci")

    df_proj = df_kii_f[df_kii_f['Kategori_Q'] == 'Proyeksi 6 Bulan']

    aspek_order = ['Keamanan', 'Politik', 'Ekonomi', 'Sosial']

    def tag_proj(text):
        t = str(text).lower()
        if any(kw in t for kw in ['keamanan', 'aman', 'konflik', 'bersenjata', 'stabil']): return 'Keamanan'
        elif any(kw in t for kw in ['politik', 'pemilu', 'pilkada', 'polarisasi']): return 'Politik'
        elif any(kw in t for kw in ['ekonomi', 'inflasi', 'pangan', 'krisis', 'harga']): return 'Ekonomi'
        elif any(kw in t for kw in ['sosial', 'stigma', 'masyarakat', 'komunitas']): return 'Sosial'
        else: return 'Lainnya'

    proj_tags = df_proj['Tanggapan'].dropna().apply(tag_proj)
    proj_narsum = df_proj.loc[proj_tags.index, 'Narsum']
    proj_df = pd.DataFrame({'Aspek': proj_tags, 'Narasumber': proj_narsum})
    proj_cross = proj_df.groupby(['Aspek', 'Narasumber']).size().reset_index(name='Jumlah')

    if not proj_cross.empty:
        fig_proj = px.bar(
            proj_cross, x='Aspek', y='Jumlah', color='Narasumber',
            barmode='stack', color_discrete_sequence=COLORS['chart'],
            text_auto=True,
        )
        fig_proj.update_layout(**PLOTLY_TEMPLATE['layout'], height=340, xaxis_title="Aspek Proyeksi", yaxis_title="Jumlah Respons")
        st.plotly_chart(fig_proj, width="stretch")
    else:
        st.info("Tidak ada data proyeksi dalam filter saat ini.")


# ═══════════════════════════════════════════════════════════════════════
# TAB 4 — ANALISIS LINTAS DATASET
# ═══════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🔍</span>
        <span class="section-title">Analisis Lintas Dataset: Gap Persepsi Masyarakat vs Pemangku Kebijakan</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="quote-block">
    🎯 <strong>Hipotesis Analisis:</strong> Isu yang diprioritaskan oleh masyarakat akar rumput (Kelompok) 
    tidak selalu selaras dengan perspektif narasumber kunci (KII). Identifikasi <em>gap ini</em> penting 
    untuk merancang program intervensi yang tepat sasaran.
    </div>
    """, unsafe_allow_html=True)

    # Comparison table
    st.markdown("#### 📊 Perbandingan Frekuensi Tema: Kelompok vs KII")

    freq_k_f2 = compute_theme_freq(df_k_f).set_index('Tema')['Frekuensi']
    freq_kii_f2 = compute_theme_freq(df_kii_f).set_index('Tema')['Frekuensi']
    themes_all = list(ISU_THEMES.keys())
    compare_df = pd.DataFrame({
        'Tema': themes_all,
        'Kelompok (Masyarakat)': [freq_k_f2.get(t, 0) for t in themes_all],
        'KII (Pemerintah/Tokoh)': [freq_kii_f2.get(t, 0) for t in themes_all],
    })
    compare_df['Gap (KII - Kelompok)'] = compare_df['KII (Pemerintah/Tokoh)'] - compare_df['Kelompok (Masyarakat)']
    compare_df['Status'] = compare_df['Gap (KII - Kelompok)'].apply(
        lambda x: '🔴 KII Lebih Prioritas' if x > 3 else ('🟢 Kelompok Lebih Prioritas' if x < -3 else '🟡 Seimbang')
    )

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name='Kelompok Masyarakat', x=compare_df['Tema'], y=compare_df['Kelompok (Masyarakat)'],
        marker_color=COLORS['primary'], opacity=0.85,
    ))
    fig_comp.add_trace(go.Bar(
        name='KII', x=compare_df['Tema'], y=compare_df['KII (Pemerintah/Tokoh)'],
        marker_color=COLORS['secondary'], opacity=0.85,
    ))
    fig_comp.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        barmode='group', height=400,
        xaxis_tickangle=-30,
        yaxis_title="Frekuensi Kata Kunci",
        xaxis_title="",
        title_text="Perbandingan Prioritas Isu: Kelompok vs KII",
    )
    st.plotly_chart(fig_comp, width="stretch")

    # Gap analysis
    st.markdown("#### 🚦 Analisis Gap: Isu Mana yang Under/Over-Prioritas?")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("**🔴 Isu yang Lebih Diprioritaskan KII (vs Masyarakat)**")
        over_kii = compare_df[compare_df['Gap (KII - Kelompok)'] > 0].sort_values('Gap (KII - Kelompok)', ascending=False)
        for _, row in over_kii.iterrows():
            st.markdown(f"""
            <div class="isu-card" style="border-left-color:#818cf8;">
                <div class="isu-title" style="color:#a5b4fc;">{row['Tema']}</div>
                <div class="isu-desc">KII: <strong>{row['KII (Pemerintah/Tokoh)']}</strong> | Kelompok: <strong>{row['Kelompok (Masyarakat)']}</strong> | Gap: +{row['Gap (KII - Kelompok)']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_g2:
        st.markdown("**🟢 Isu yang Lebih Diprioritaskan Masyarakat (vs KII)**")
        over_k = compare_df[compare_df['Gap (KII - Kelompok)'] < 0].sort_values('Gap (KII - Kelompok)')
        for _, row in over_k.iterrows():
            st.markdown(f"""
            <div class="isu-card" style="border-left-color:#38bdf8;">
                <div class="isu-title" style="color:#7dd3fc;">{row['Tema']}</div>
                <div class="isu-desc">Kelompok: <strong>{row['Kelompok (Masyarakat)']}</strong> | KII: <strong>{row['KII (Pemerintah/Tokoh)']}</strong> | Gap: {row['Gap (KII - Kelompok)']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Insight matrix
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🧩 Matriks Tindak Lanjut: Urgensi vs Kesenjangan Respons")

    matrix_data = {
        'Isu': ['Narkoba/Aibon', 'Miras/Alkohol', 'Pendidikan', 'Kesehatan', 'Infrastruktur', 'Ekonomi', 'Perang Suku', 'Perlindungan Anak'],
        'Urgensi (1-10)': [9, 7, 8, 8, 6, 7, 8, 9],
        'Respons Pemerintah (1-10)': [4, 3, 5, 5, 4, 4, 5, 4],
        'Ukuran': [9, 7, 8, 8, 6, 7, 8, 9],
    }
    mx_df = pd.DataFrame(matrix_data)
    mx_df['Gap'] = mx_df['Urgensi (1-10)'] - mx_df['Respons Pemerintah (1-10)']

    fig_mat = px.scatter(
        mx_df, x='Respons Pemerintah (1-10)', y='Urgensi (1-10)',
        size='Ukuran', color='Gap', text='Isu',
        color_continuous_scale=['#4ade80', '#fbbf24', '#f87171'],
        size_max=40,
    )
    fig_mat.update_traces(textposition='top center', textfont=dict(color=COLORS['text_main'], size=10))
    fig_mat.add_hline(y=7, line_dash="dash", line_color=COLORS['warning'], annotation_text="Urgensi Tinggi", annotation_font_color=COLORS['warning'])
    fig_mat.add_vline(x=5, line_dash="dash", line_color=COLORS['primary'], annotation_text="Respons Cukup", annotation_font_color=COLORS['primary'])
    fig_mat.update_layout(
        **PLOTLY_TEMPLATE['layout'],
        height=460,
        xaxis_title="Tingkat Respons Pemerintah (1=Rendah, 10=Tinggi)",
        yaxis_title="Tingkat Urgensi Isu (1=Rendah, 10=Tinggi)",
        title_text="📌 Kuadran Prioritas: Isu dengan Urgensi Tinggi & Respons Rendah = DARURAT",
    )
    st.plotly_chart(fig_mat, width="stretch")
    st.caption("⚠️ Isu di kuadran kanan atas: urgensi tinggi, respons memadai. Isu di kiri atas: DARURAT — urgensi tinggi namun respons rendah.")


# ═══════════════════════════════════════════════════════════════════════
# TAB 5 — LAPORAN EKSEKUTIF
# ═══════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📋</span>
        <span class="section-title">Laporan Eksekutif — Temuan Utama dari Survei Lapangan GECAR</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
---

## 📌 Ringkasan Eksekutif

Survei lapangan GECAR 2025 dilaksanakan di tiga wilayah — **Jayawijaya**, **Sentani**, dan **Asmat, Papua Selatan** — melibatkan **356 responden kelompok** (anak dan dewasa) dan **167 tanggapan dari narasumber KII** (Key Informant Interview) yang mencakup pejabat pemerintah, tokoh lokal, dan pemangku kebijakan. Berikut adalah temuan isu-isu kritis yang teridentifikasi dari kedua dataset.

---

## 🧩 Dataset 1: Kelompok Masyarakat

### ISU 1 — Ketegangan Sosial: Miras, Judol, dan Kriminalitas
Ketika masyarakat ditanya tentang ketegangan yang terjadi di komunitas mereka, **miras/alkohol, judi online (judol), dan ganja** menjadi jawaban yang paling sering muncul. Pola ini konsisten di ketiga wilayah. Konsumsi miras secara langsung dikaitkan dengan peningkatan kekerasan rumah tangga, aksi begal, dan pencurian. Masyarakat juga melaporkan perang suku yang dipicu oleh perselingkuhan atau sengketa lahan, yang kerap memakan korban dari kelompok tidak bersalah — termasuk anak-anak.

> *"Kecanduan miras sehingga melakukan aksi begal, pencurian. Pencurian karena ekonomi susah, tidak ada pekerjaan."*

> *"Ketakutan dipukul atau kekerasan karena ada yang miras atau ada yang pegang parang saat marah."*

**Implikasi:** Program penanganan miras dan pengurangan risiko kekerasan harus menjadi prioritas lintas sektoral, bukan sekadar penegakan hukum.

---

### ISU 2 — Kebutuhan Utama: Pendidikan, Kesehatan, dan Infrastruktur Dasar
Masyarakat secara konsisten mengidentifikasi **pendidikan anak**, **akses layanan kesehatan**, dan **infrastruktur dasar (air bersih, jalan, kamar mandi)** sebagai kebutuhan paling mendesak. Di Asmat, keterbatasan akses air bersih dan kerusakan fasilitas sanitasi merupakan isu kritis. Di Jayawijaya, akses ke layanan kesehatan terhambat oleh birokrasi dan jarak geografis. Masyarakat juga menyebutkan sulitnya mengakses administrasi rumah sakit karena ketidakmauan petugas membantu.

> *"Pas masuk RS susah untuk bagian admin karena tidak mau mengurusnya padahal itu penting."*

> *"Air bersih (sumur bor) — sudah 2 kali pasang tapi rusak karena hanya menggunakan selang."*

---

### ISU 3 — Rasa Aman dan Ketakutan: Berbeda antara Anak dan Dewasa
Anak-anak paling banyak menyatakan ketakutan terhadap **kekerasan akibat miras** dan **masalah keluarga** (kehilangan orang tua, orang tua yang memukul). Orang dewasa lebih khawatir tentang perang suku, sengketa lahan, dan keselamatan kerja. Menariknya, rasa aman bagi banyak responden terikat pada **institusi gereja dan kehadiran keluarga** — bukan pada aparat keamanan formal, yang mengindikasikan rendahnya kepercayaan publik terhadap penegak hukum.

> *"Di gereja saya merasa aman ketika belajar Firman Tuhan dan bersama dengan generasi saya."*

---

### ISU 4 — Harapan dan Kontribusi Pemuda
Masyarakat, khususnya kaum muda, masih memiliki harapan yang besar dan konstruktif. Pemuda mengidentifikasi peran mereka dalam **mengajar di rumah baca, terlibat di gereja, dan memberi teladan kepada adik-adik**. Namun, harapan ini terbentur dengan minimnya fasilitas, kurangnya lapangan kerja, dan migrasi pemuda ke kota. Kebutuhan akan **ruang publik yang positif** dan **lapangan pekerjaan berbasis kampung** sangat dirasakan.

---

### ISU 5 — Proyeksi 6 Bulan: Ketidakpastian Ekonomi dan Bergantung pada Bantuan
Masyarakat mengantisipasi **masuknya bantuan sosial (bansos, dana desa)** dalam waktu dekat, tetapi sadar bahwa uang tersebut akan cepat habis karena budaya berbagi yang kuat. Di Asmat, ketergantungan pada bantuan luar sangat tinggi, sementara basis ekonomi mandiri (seperti keramba ikan dan kelompok tani) masih sangat terbatas. Ini menciptakan siklus kerentanan ekonomi yang berulang.

---

## 🏛️ Dataset 2: KII (Narasumber Kunci — Pemerintah & Tokoh)

### ISU 1 — Darurat Narkoba, Aibon, dan Kasus HIV pada Anak di Sentani
Dinas Sosial melaporkan temuan yang sangat mengkhawatirkan: **anak-anak sudah menggunakan narkoba sejak dini**, ditemukan kasus aibon di jalanan, dan bahkan ditemukan **seorang siswa kelas 5 SD yang terinfeksi HIV/AIDS** — diduga akibat kekerasan seksual yang dipicu penggunaan alkohol atau narkoba oleh pelaku. Fasilitas rehabilitasi sangat terbatas, dan keluarga sering tidak kooperatif dalam proses pemulihan.

> *"Ditemukan anak-anak yang sudah menggunakan narkoba (hasil pemeriksaan bersama BNN di sekolah), ada anak yang menggunakan aibon di jalanan."*

**Ini adalah isu paling kritis dan mendesak yang memerlukan intervensi multi-lembaga segera.**

---

### ISU 2 — Konflik Bersenjata, Perang Suku, dan Polarisasi Identitas
Narasumber KII dari Jayawijaya mengidentifikasi **konflik bersenjata yang dipimpin kelompok sipil bersenjata (termasuk jaringan Egianus Kogoya di Nduga)** sebagai ancaman keamanan utama. Di tingkat lokal, perang suku masih berlangsung dan sering dipicu oleh sengketa kecil. Yang memperburuk situasi adalah **peran media sosial (WhatsApp)** yang menyebarkan rumor dan hoaks yang memicu ketegangan sebelum peristiwa nyata terjadi.

> *"Konflik di Wamena semakin mudah terjadi karena peran media sosial. Informasi atau rumor yang beredar melalui grup WhatsApp sering memicu ketegangan sebelum peristiwa benar-benar terjadi."*

---

### ISU 3 — Kelompok Rentan: Anak, Remaja, dan Perempuan sebagai Korban Ganda
Seluruh narasumber KII sepakat bahwa **anak-anak dan remaja adalah kelompok paling rentan**. Mereka berisiko menjadi korban langsung (trauma, kehilangan akses pendidikan) sekaligus pelaku (terseret dalam konflik atau penggunaan narkoba). Perempuan juga disebutkan rentan kehilangan mata pencaharian saat konflik memaksa penutupan pasar.

---

### ISU 4 — Krisis Pendidikan: Honor Guru Tertunggak dan Kualitas PAUD Rendah
Dinas Pendidikan mengungkapkan bahwa **banyak PAUD hanya dibuka untuk mendapatkan dana BUP** tanpa tenaga pengajar yang kompeten. Lebih parahnya, **pembayaran honor guru sering tertunda** karena keterbatasan APBD — yang berdampak langsung pada motivasi dan kehadiran guru di kelas.

---

### ISU 5 — Kebutuhan Keadilan Sosial: Diskriminasi OAP vs Pendatang
Narasumber KII menyoroti **ketegangan laten antara Orang Asli Papua (OAP) dan pendatang** dalam perebutan kursi PNS, akses ekonomi, dan kontestasi politik lokal. Isu ini bersifat struktural dan memerlukan kebijakan yang transparan dan berkeadilan. Tanpa penanganan sistemik, polarisasi identitas ini berpotensi menjadi pemicu konflik sosial yang lebih luas.

---

## 🚦 Rekomendasi Prioritas

| Prioritas | Isu | Tindakan Disarankan | Aktor Kunci |
|-----------|-----|---------------------|-------------|
| 🔴 DARURAT | Narkoba/Aibon & HIV pada Anak | Penambahan fasilitas rehab, penyuluhan sekolah, ruang bermain gratis | Dinas Sosial, BNN, WVI |
| 🔴 TINGGI | Kekerasan akibat Miras | Penertiban distribusi miras, program kesadaran komunitas | Kepala Kampung, Polsek, Tokoh Adat |
| 🟠 TINGGI | Pendidikan Berkualitas | Pembayaran honor guru tepat waktu, pelatihan kompetensi PAUD | Dinas Pendidikan, WVI |
| 🟠 TINGGI | Kesehatan & Sanitasi Dasar | Perbaikan air bersih, kemudahan akses RS, imunisasi anak | Dinas Kesehatan, NGO |
| 🟡 SEDANG | Ketegangan Identitas (OAP/Pendatang) | Kebijakan inklusif, dialog lintas komunitas | Pemerintah Daerah |
| 🟡 SEDANG | Peran Media Sosial dalam Konflik | Literasi digital, pesan perdamaian proaktif | Gereja, Tokoh Pemuda |

---

*Laporan ini disusun berdasarkan analisis kualitatif-kuantitatif dari data survei lapangan GECAR 2025. 
Disusun menggunakan Streamlit + Plotly. Data bersumber dari kedua dataset: Gecar_-_Kelompok.csv & Gecar_-_KII.csv.*
""")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.75rem; margin-top:3rem; padding: 1rem; border-top: 1px solid #1e2d40;">
    <span style="font-family:'Space Mono',monospace; color:#475569;">GECAR DASHBOARD</span> · 
    Papua Community Insight Analysis · 2025 · 
    Built with Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
