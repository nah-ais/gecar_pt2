"""
GECAR Dashboard - Analisis Isu Komunitas Papua
Streamlit App v1.0
Run: streamlit run app.py
Requires: streamlit, pandas, plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GECAR Dashboard – Analisis Isu Komunitas Papua",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Sora:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Sora', sans-serif; }
    
    .main { background-color: #f8f7f4; }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 4px solid #c0392b;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }
    .metric-label { font-size: 0.78rem; color: #888; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1a1a2e; line-height: 1.2; }
    .metric-delta { font-size: 0.8rem; color: #27ae60; font-weight: 600; }
    
    .issue-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
        border-top: 3px solid #e74c3c;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .issue-title { font-weight: 700; font-size: 0.95rem; color: #2c3e50; margin-bottom: 6px; }
    .issue-desc { font-size: 0.85rem; color: #555; line-height: 1.6; }
    
    .section-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-family: 'Sora', sans-serif;
        font-weight: 700;
    }
    
    .quote-box {
        background: #fef9f0;
        border-left: 3px solid #f39c12;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        font-style: italic;
        font-size: 0.85rem;
        color: #444;
        margin: 8px 0;
        line-height: 1.6;
    }
    
    .tag {
        display: inline-block;
        background: #e8f4fd;
        color: #2980b9;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 2px;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: #1a1a2e !important;
        color: white !important;
    }
    
    div[data-testid="stSidebar"] { background: #1a1a2e; }
    div[data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSidebar"] .stSelectbox label,
    div[data-testid="stSidebar"] .stMultiSelect label { color: #aaa !important; }
    
    .alert-red {
        background: #fdf0ef;
        border: 1px solid #e74c3c;
        border-radius: 8px;
        padding: 12px 16px;
        color: #c0392b;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .alert-yellow {
        background: #fefdf0;
        border: 1px solid #f39c12;
        border-radius: 8px;
        padding: 12px 16px;
        color: #d68910;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load both datasets. Adjust paths as needed."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    kelompok_path = os.path.join(base_dir, "Gecar_-_Kelompok.csv")
    kii_path      = os.path.join(base_dir, "Gecar_-_KII.csv")
    
    try:
        df_k = pd.read_csv(kelompok_path)
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {kelompok_path}")
        st.stop()

    try:
        df_kii = pd.read_csv(kii_path)
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {kii_path}")
        st.stop()

    # Basic cleaning
    df_k = df_k.dropna(subset=["Tanggapan"])
    df_kii = df_kii.dropna(subset=["Tanggapan"])
    df_k["Tanggapan"] = df_k["Tanggapan"].str.strip()
    df_kii["Tanggapan"] = df_kii["Tanggapan"].str.strip()

    return df_k, df_kii


# ─────────────────────────────────────────────
# KEYWORD EXTRACTION HELPERS
# ─────────────────────────────────────────────
def count_keyword_hits(series, keyword_groups: dict) -> pd.DataFrame:
    """
    Count how many rows mention each keyword group.
    keyword_groups = {'Label': ['kw1','kw2'], ...}
    Returns DataFrame with columns: Tema, Jumlah
    """
    results = []
    for label, keywords in keyword_groups.items():
        pattern = "|".join(keywords)
        count = series.str.lower().str.contains(pattern, na=False).sum()
        results.append({"Tema": label, "Jumlah": count})
    return pd.DataFrame(results).sort_values("Jumlah", ascending=False)


def extract_top_keywords(series, keyword_groups: dict, wilayah_series=None, wilayah_filter=None):
    """Filter by wilayah then count keyword hits."""
    if wilayah_filter and wilayah_series is not None:
        mask = wilayah_series.isin(wilayah_filter)
        series = series[mask]
    return count_keyword_hits(series, keyword_groups)


# ─────────────────────────────────────────────
# PLOT HELPERS
# ─────────────────────────────────────────────
COLORS_MAIN = ["#c0392b", "#e67e22", "#f1c40f", "#2ecc71", "#2980b9",
                "#8e44ad", "#16a085", "#d35400", "#1abc9c", "#e74c3c", "#34495e"]

def bar_chart(df, x, y, title, color_col=None, orientation="v"):
    if orientation == "h":
        fig = px.bar(df, x=y, y=x, orientation="h", title=title,
                     color=color_col if color_col else y,
                     color_discrete_sequence=COLORS_MAIN)
        fig.update_traces(texttemplate="%{x}", textposition="outside")
    else:
        fig = px.bar(df, x=x, y=y, title=title,
                     color=color_col if color_col else x,
                     color_discrete_sequence=COLORS_MAIN)
        fig.update_traces(texttemplate="%{y}", textposition="outside")
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Plus Jakarta Sans", size=12),
        title_font=dict(family="Sora", size=15, color="#1a1a2e"),
        showlegend=False, margin=dict(t=50, b=20, l=20, r=20),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    return fig

def pie_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values, title=title,
                 color_discrete_sequence=COLORS_MAIN, hole=0.4)
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    fig.update_layout(
        paper_bgcolor="white", font=dict(family="Plus Jakarta Sans"),
        title_font=dict(family="Sora", size=15, color="#1a1a2e"),
        margin=dict(t=50, b=10, l=10, r=10),
    )
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
df_k, df_kii = load_data()

with st.sidebar:
    st.markdown("## 🗺️ GECAR Dashboard")
    st.markdown("*Analisis Isu Komunitas Papua*")
    st.markdown("---")

    st.markdown("### Filter Kelompok Masyarakat")
    wilayah_options_k = sorted(df_k["Wilayah"].unique().tolist())
    sel_wilayah_k = st.multiselect("Wilayah", wilayah_options_k, default=wilayah_options_k, key="wk")
    sel_usia = st.multiselect("Kelompok Usia", sorted(df_k["Kelompok_Usia"].unique()), default=df_k["Kelompok_Usia"].unique().tolist())
    sel_gender = st.multiselect("Jenis Kelamin", sorted(df_k["Jenis_Kelamin"].unique()), default=df_k["Jenis_Kelamin"].unique().tolist())

    st.markdown("---")
    st.markdown("### Filter KII Pemerintah")
    wilayah_options_kii = sorted(df_kii["Wilayah"].unique().tolist())
    sel_wilayah_kii = st.multiselect("Wilayah KII", wilayah_options_kii, default=wilayah_options_kii, key="wkii")
    narsum_options = sorted(df_kii["Narsum"].unique().tolist())
    sel_narsum = st.multiselect("Narasumber", narsum_options, default=narsum_options)

    st.markdown("---")
    st.caption("Data: Program GECAR | Dashboard v1.0")

# Apply filters
mask_k = (
    df_k["Wilayah"].isin(sel_wilayah_k) &
    df_k["Kelompok_Usia"].isin(sel_usia) &
    df_k["Jenis_Kelamin"].isin(sel_gender)
)
dfk = df_k[mask_k].copy()

mask_kii = (
    df_kii["Wilayah"].isin(sel_wilayah_kii) &
    df_kii["Narsum"].isin(sel_narsum)
)
dfkii = df_kii[mask_kii].copy()


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1a1a2e 0%,#c0392b 100%);
            padding:32px 36px; border-radius:14px; margin-bottom:28px;">
  <h1 style="color:white;margin:0;font-family:Sora,sans-serif;font-size:2rem;">
    🗺️ GECAR – Dashboard Analisis Isu Komunitas Papua
  </h1>
  <p style="color:rgba(255,255,255,0.78);margin:8px 0 0;font-size:0.95rem;">
    Pemetaan isu, ketegangan, kebutuhan, dan harapan dari perspektif masyarakat (Kelompok) dan pemangku kebijakan (KII) di Jayawijaya, Asmat, dan Sentani
  </p>
</div>
""", unsafe_allow_html=True)

# Top-level metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Responden Kelompok</div>
        <div class="metric-value">{len(dfk)}</div>
        <div class="metric-delta">3 Wilayah</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Responden KII (Pemerintah)</div>
        <div class="metric-value">{len(dfkii)}</div>
        <div class="metric-delta">7 Narasumber</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Wilayah Kajian</div>
        <div class="metric-value">3</div>
        <div class="metric-delta">Jayawijaya · Asmat · Sentani</div>
    </div>""", unsafe_allow_html=True)
with col4:
    n_isu = dfk["Tanggapan"].str.lower().str.contains("mabuk|miras|aibon|ganja|narkoba", na=False).sum()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Menyebut Narkoba/Miras</div>
        <div class="metric-value" style="color:#c0392b;">{n_isu}</div>
        <div class="metric-delta">Tanggapan Kelompok</div>
    </div>""", unsafe_allow_html=True)
with col5:
    n_kdrt = dfk["Tanggapan"].str.lower().str.contains("kekerasan|dipukul|begal|pencurian|kriminal", na=False).sum()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Menyebut Kekerasan/Kriminal</div>
        <div class="metric-value" style="color:#c0392b;">{n_kdrt}</div>
        <div class="metric-delta">Tanggapan Kelompok</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📋 Dataset 1 – Kelompok Masyarakat",
    "🏛️ Dataset 2 – KII Pemerintah/Lembaga",
    "📊 Perbandingan & Laporan Eksekutif",
])


# ══════════════════════════════════════════════
# TAB 1: KELOMPOK MASYARAKAT
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">📋 Analisis Tanggapan Kelompok Masyarakat</div>', unsafe_allow_html=True)

    # ── ISU 1: Ketegangan & Konflik ──────────────
    st.markdown("### 🔴 Isu 1 · Peta Ketegangan & Konflik Sosial")
    st.markdown("""
    <div class="issue-card">
        <div class="issue-title">⚠️ Ketegangan Utama yang Mempengaruhi Keluarga</div>
        <div class="issue-desc">Dari tanggapan masyarakat, ketegangan bersumber dari klaster besar: 
        perilaku destruktif, ketidakadilan distribusi bantuan, konflik horizontal, serta kerentanan lingkungan akibat cuaca ekstrem atau bencana alam lokal yang mempengaruhi ketahanan pangan keluarga.</div>
    </div>
    """, unsafe_allow_html=True)

    # TAMBAHAN: Isu bencana alam dimasukkan ke dalam tension_keywords
    tension_keywords = {
        "Miras / Mabuk": ["mabok", "mabuk", "miras", "alkohol", "minuman keras"],
        "Narkoba / Aibon": ["narkoba", "aibon", "ganja", "obat terlarang"],
        "Judol / Perjudian": ["judol", "judi", "perjudian"],
        "Pencurian / Begal": ["pencurian", "begal", "curi", "kriminal", "rampok"],
        "Perang Suku": ["perang suku", "konflik suku", "denda adat", "sajam"],
        "Korupsi / Dana Desa": ["dana desa", "kepala kampung", "korupsi", "dipotong", "simpatisan", "musrenbang"],
        "Kekerasan Fisik / KDRT": ["kekerasan", "dipukul", "parang", "pukul", "pukuli"],
        "Sengketa Tanah": ["sengketa tanah", "batas wilayah", "hak tanah", "hak ulayat", "lahan"],
        "Bencana Alam / Lingkungan": ["bencana", "banjir", "gempa", "longsor", "kekeringan", "iklim", "cuaca", "air pasang"]
    }

    col_t1, col_t2 = st.columns([3, 2])
    with col_t1:
        df_tension = extract_top_keywords(dfk["Tanggapan"], tension_keywords, dfk["Wilayah"], sel_wilayah_k)
        df_tension = df_tension[df_tension["Jumlah"] > 0]
        if not df_tension.empty:
            fig = bar_chart(df_tension, "Tema", "Jumlah", "Frekuensi Sebutan Jenis Ketegangan", orientation="h")
            st.plotly_chart(fig, width="stretch")

    with col_t2:
        df_w = []
        for w in dfk["Wilayah"].unique():
            sub = dfk[dfk["Wilayah"] == w]["Tanggapan"]
            for label, kws in tension_keywords.items():
                pattern = "|".join(kws)
                cnt = sub.str.lower().str.contains(pattern, na=False).sum()
                if cnt > 0:
                    df_w.append({"Wilayah": w, "Isu": label, "Jumlah": cnt})
        df_w = pd.DataFrame(df_w)
        if not df_w.empty:
            fig2 = px.bar(df_w, x="Wilayah", y="Jumlah", color="Isu", title="Ketegangan per Wilayah",
                          barmode="stack", color_discrete_sequence=COLORS_MAIN)
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans", size=11),
                title_font=dict(family="Sora", size=14, color="#1a1a2e"),
                legend=dict(font=dict(size=10)),
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig2, width="stretch")

    # Quotes
    st.markdown("**Kutipan Langsung dari Tanggapan Masyarakat:**")
    quotes_tension = [
        ("Jayawijaya", "Mabok, Judol, Tanaman ganja, Aibon, Pencurian, Begal, Pembunuhan..."),
        ("Asmat", "Kebutuhan masyarakat yang sudah dimasukkan di Musrenbang tidak dijawab karena pengadaan dilakukan hanya untuk kepentingan orang penting/keluarga pemimpin."),
        ("Asmat", "Bantuan yang sampai ke masyarakat dipotong di distrik dan di kampung sehingga yang sampai ke masyarakat tidak penuh."),
        ("Sentani", "Sengketa Tanah: ada kasus di mana hak pakai berubah menjadi hak milik karena transaksi uang yang tidak sah."),
    ]
    for wilayah, q in quotes_tension:
        st.markdown(f"""<div class="quote-box"><span class="tag">{wilayah}</span> {q}</div>""", unsafe_allow_html=True)

    st.divider()

    # ── ISU 2: Kebutuhan Dasar ──────────────
    st.markdown("### 🟠 Isu 2 · Kebutuhan Dasar yang Belum Terpenuhi")
    st.markdown("""
    <div class="issue-card">
        <div class="issue-title">💧 Akses Air, Pendidikan, Kesehatan & Ekonomi</div>
        <div class="issue-desc">Kebutuhan dasar yang paling banyak disebut adalah air bersih (PAH/blong rusak berulang), 
        akses pendidikan yang terbatas, kesehatan anak, dan mitigasi lingkungan/ekonomi produktif menghadapi perubahan musim.</div>
    </div>
    """, unsafe_allow_html=True)

    needs_keywords = {
        "Air Bersih / PAH": ["air bersih", "sumur bor", "blong", "pah", "air minum", "penampungan air"],
        "Pendidikan Anak": ["sekolah", "pendidikan", "belajar", "guru", "tk", "paud", "sd", "smp", "kuliah", "ijazah"],
        "Kesehatan": ["kesehatan", "imunisasi", "rs", "rumah sakit", "puskesmas", "hamil", "balita", "hpv", "posyandu"],
        "Ekonomi / Pekerjaan": ["ekonomi", "pekerjaan", "kerja", "modal", "usaha", "keramba", "kebun", "ikan", "bantuan", "blt"],
        "Infrastruktur": ["jalan", "jembatan", "kamar mandi", "mck", "renovasi", "bangunan", "gedung", "fiber", "speed"],
        "Keamanan": ["aman", "keamanan", "linmas", "polisi", "tni", "penjagaan"],
    }

    col_n1, col_n2, col_n3 = st.columns(3)
    cols_need = [col_n1, col_n2, col_n3]
    for i, (wilayah) in enumerate(["Jayawijaya", "Asmat, Papua Selatan", "Sentani"]):
        sub = dfk[dfk["Wilayah"] == wilayah]["Tanggapan"]
        df_n = count_keyword_hits(sub, needs_keywords)
        df_n = df_n[df_n["Jumlah"] > 0]
        with cols_need[i]:
            wlabel = wilayah.split(",")[0]
            if not df_n.empty:
                fig = pie_chart(df_n, "Tema", "Jumlah", f"Kebutuhan Utama – {wlabel}")
                st.plotly_chart(fig, width="stretch")

    st.divider()

    # ── ISU 3: Kekerasan terhadap Anak & Perempuan ──
    st.markdown("### 🟡 Isu 3 · Kekerasan terhadap Anak & Diskriminasi Gender")
    st.markdown("""
    <div class="issue-card">
        <div class="issue-title">🚨 KDRT, Kekerasan Orang Tua, dan Pembatasan Peran Perempuan</div>
    </div>
    """, unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        sentani_anak = dfk[(dfk["Wilayah"] == "Sentani") & (dfk["Kelompok_Usia"] == "Anak")]
        violence_kws = {
            "Kekerasan fisik dari orang tua": ["dipukul", "pukul", "kekerasan fisik"],
            "Ancaman dari orang mabuk": ["mabuk", "miras"],
            "Bullying / stigma sosial": ["bully", "fitnah", "diceritakan", "tidak senang"],
            "Diskriminasi gender / adat": ["perempuan tidak boleh", "dilarang", "dianggap buruk", "ob"],
            "Ketakutan masa depan": ["masa depan", "cita-cita", "pekerjaan"],
            "Kehilangan orang tua": ["kehilangan", "orang tua", "mama", "bapa sakit"],
        }
        df_viol_p = count_keyword_hits(
            sentani_anak[sentani_anak["Jenis_Kelamin"] == "Perempuan"]["Tanggapan"], violence_kws)
        df_viol_l = count_keyword_hits(
            sentani_anak[sentani_anak["Jenis_Kelamin"] == "Laki laki"]["Tanggapan"], violence_kws)

        df_viol_p = df_viol_p[df_viol_p["Jumlah"] > 0].assign(Gender="Perempuan")
        df_viol_l = df_viol_l[df_viol_l["Jumlah"] > 0].assign(Gender="Laki-laki")
        df_viol = pd.concat([df_viol_p, df_viol_l])

        if not df_viol.empty:
            fig = px.bar(df_viol, x="Tema", y="Jumlah", color="Gender", barmode="group",
                         title="Ketakutan Anak Sentani – per Gender",
                         color_discrete_map={"Perempuan": "#e74c3c", "Laki-laki": "#2980b9"})
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans", size=11),
                title_font=dict(family="Sora", size=14),
                xaxis_tickangle=-30, margin=dict(t=50, b=80)
            )
            st.plotly_chart(fig, width="stretch")

    with col_v2:
        st.markdown("**Kutipan Anak Perempuan Sentani:**")
        child_quotes = [
            "mendapatkan kekerasan fisik dari bapak saya",
            "Takut orang mabuk, berpotensi melecehkan",
            "Tidak boleh naik ke gereja, karena kami dilarang (majelis tertentu) – diceritakan yang buruk",
            "Tidak boleh duduk di OB (rumah adat) karena dianggap perempuan tidak boleh berlebihan",
            "Bully di kampung (mama-mama tidak senang melihat kami bergaya)",
        ]
        for q in child_quotes:
            st.markdown(f'<div class="quote-box">"{q}"</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="alert-red">⚠️ Kekerasan fisik orang tua disebut oleh <b>5 dari 9 anak perempuan</b> Sentani sebagai ketakutan utama mereka.</div>', unsafe_allow_html=True)

    st.divider()

    # ── ISU 4: Harapan Pemuda & Kontribusi ──
    st.markdown("### 🟢 Isu 4 · Harapan & Potensi Pemuda")
    
    hope_keywords = {
        "Pendidikan & Belajar": ["belajar", "sekolah", "kuliah", "ijazah", "beasiswa", "rumah baca", "mengajar"],
        "Pekerjaan / Ekonomi": ["kerja", "pekerjaan", "lowongan", "usaha", "modal"],
        "Peran di Gereja / Iman": ["gereja", "ibadah", "firman tuhan", "pelayan", "pengasuh", "rohani"],
        "Olahraga & Seni Budaya": ["olahraga", "bola", "badminton", "lomba", "seni", "budaya", "lagu", "paduan suara"],
        "Komunitas & Gotong Royong": ["gotong royong", "swadaya", "bersama", "masyarakat", "berkontribusi"],
        "Keamanan & Perdamaian": ["aman", "damai", "perubahan", "lebih baik"],
    }

    hope_q_filter = dfk["Pertanyaan"].str.contains("harapan|kontribusi|berkontribusi", case=False, na=False)
    dfk_hope = dfk[hope_q_filter]

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        df_hope_all = count_keyword_hits(dfk_hope["Tanggapan"], hope_keywords)
        df_hope_all = df_hope_all[df_hope_all["Jumlah"] > 0]
        if not df_hope_all.empty:
            fig = bar_chart(df_hope_all, "Tema", "Jumlah", "Tema Harapan Masyarakat", orientation="h")
            st.plotly_chart(fig, width="stretch")

    with col_h2:
        df_hope_w = []
        for w in dfk["Wilayah"].unique():
            sub = dfk_hope[dfk_hope["Wilayah"] == w]["Tanggapan"]
            for label, kws in hope_keywords.items():
                pattern = "|".join(kws)
                cnt = sub.str.lower().str.contains(pattern, na=False).sum()
                if cnt > 0:
                    df_hope_w.append({"Wilayah": w.split(",")[0], "Harapan": label, "Jumlah": cnt})
        df_hope_w = pd.DataFrame(df_hope_w)
        if not df_hope_w.empty:
            fig2 = px.bar(df_hope_w, x="Wilayah", y="Jumlah", color="Harapan", barmode="stack",
                          title="Harapan per Wilayah", color_discrete_sequence=COLORS_MAIN)
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans", size=11),
                title_font=dict(family="Sora", size=14),
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig2, width="stretch")

    st.divider()

    # ── ISU 5: Respons Skenario 6 Bulan ke Depan ──
    st.markdown("### 🔵 Isu 5 · Proyeksi Situasi 6 Bulan ke Depan")
    col_s1, col_s2 = st.columns(2)

    scenario_cols = ["keamanan", "politik", "ekonomi", "sosial"]
    scenario_labels = {
        "keamanan": {"pos": ["aman", "damai", "terkendali", "penjagaan"], "neg": ["pencurian", "mabuk", "kericuhan", "konflik"]},
        "ekonomi":  {"pos": ["bantuan", "usaha", "modal", "tabungan", "meningkat"], "neg": ["habis", "susah", "kekurangan", "miskin"]},
        "sosial":   {"pos": ["gotong royong", "saling bantu", "bersama", "baik"], "neg": ["diri sendiri", "memecah", "tidak ada"]},
        "politik":  {"pos": ["perubahan", "adil", "renovasi"], "neg": ["tidak ada perubahan", "partisan", "tidak pernah"]},
    }

    scenario_q_filter = dfk["Pertanyaan"].str.contains("6 bulan|skenario", case=False, na=False)
    dfk_sc = dfk[scenario_q_filter]

    rows_sc = []
    for dim, kws in scenario_labels.items():
        pos = dfk_sc["Tanggapan"].str.lower().str.contains("|".join(kws["pos"]), na=False).sum()
        neg = dfk_sc["Tanggapan"].str.lower().str.contains("|".join(kws["neg"]), na=False).sum()
        rows_sc.append({"Dimensi": dim.capitalize(), "Optimistis": pos, "Pesimistis": neg})
    df_sc = pd.DataFrame(rows_sc)

    with col_s1:
        fig_sc = go.Figure()
        fig_sc.add_trace(go.Bar(name="Optimistis", x=df_sc["Dimensi"], y=df_sc["Optimistis"],
                                 marker_color="#27ae60", text=df_sc["Optimistis"], textposition="outside"))
        fig_sc.add_trace(go.Bar(name="Pesimistis", x=df_sc["Dimensi"], y=df_sc["Pesimistis"],
                                 marker_color="#e74c3c", text=df_sc["Pesimistis"], textposition="outside"))
        fig_sc.update_layout(
            title="Sentimen Skenario 6 Bulan – Kelompok Masyarakat",
            barmode="group", plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Plus Jakarta Sans", size=12),
            title_font=dict(family="Sora", size=14),
            legend=dict(orientation="h", y=1.1), margin=dict(t=60, b=20)
        )
        st.plotly_chart(fig_sc, width="stretch")

    with col_s2:
        st.markdown("**Kutipan Proyeksi Masyarakat:**")
        sc_quotes = [
            ("Asmat – Ekonomi", "Jika dapat dana bantuan akan segera habis sehingga perlu dimasukkan ASKA agar ada tabungan."),
            ("Asmat – Keamanan", "Adanya Polsek, Satgas, akan damai karena adanya penjagaan, Linmas tidak berjaga tiap malam. Pencurian semakin meningkat."),
            ("Asmat – Sosial", "Saling jaga dan gotong royong akan tetap dilakukan. Ada bapak yang bagi bibit sagu ke masyarakat yang belum punya."),
            ("Sentani – Politik", "Jika ada perubahan kepala kampung, bupati dan wakil bupati maka yakin akan ada perubahan dan pembagian yang lebih adil."),
        ]
        for wilayah, q in sc_quotes:
            st.markdown(f'<div class="quote-box"><span class="tag">{wilayah}</span> "{q}"</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2: KII PEMERINTAH / LEMBAGA
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">🏛️ Analisis Tanggapan KII – Pemerintah & Lembaga</div>', unsafe_allow_html=True)

    st.markdown("### 🔴 Isu 1 · Akar Ketegangan Struktural & Lokal")
    st.markdown("""
    <div class="issue-card">
        <div class="issue-title">🏗️ Nepotisme, Kesenjangan, Konflik Lahan, dan Kerentanan Krisis Ekologis</div>
        <div class="issue-desc">Para narasumber KII mengidentifikasi akar masalah struktural, termasuk bagaimana deforestasi massif atau bencana alam lokal memperparah kerentanan sosial OAP.</div>
    </div>
    """, unsafe_allow_html=True)

    # TAMBAHAN: Isu bencana alam dimasukkan ke dalam kii_keywords
    tension_kii_kws = {
        "Nepotisme / Korupsi Birokrasi": ["nepotisme", "birokrasi", "korupsi", "transparan", "distribusi tidak merata", "musrenbang"],
        "Kesenjangan OAP vs Pendatang": ["oap", "pendatang", "polarisasi", "identitas", "rasisme"],
        "Hak Adat / Lahan": ["hak adat", "ulayat", "adat", "lahan", "deforestasi", "psn", "tanah"],
        "Konflik Bersenjata / KKB": ["kkb", "bersenjata", "kelompok sipil bersenjata", "tni", "polri", "nduga", "penyanderaan"],
        "Inflasi / Krisis Ekonomi": ["inflasi", "pangan", "logistik", "krisis moneter", "harga"],
        "Masalah Rumah Tangga / Sosial": ["perselingkuhan", "rumah tangga", "mabuk", "kriminal"],
        "Isu Politik Lokal": ["pemilu", "pilkada", "rekrutmen", "pejabat", "kepala kampung"],
        "Trauma Sosial / Historis": ["trauma", "historis", "konflik masa lalu", "susi air"],
        "Bencana Alam / Dampak Iklim": ["bencana", "banjir", "gempa", "longsor", "kekeringan", "iklim", "cuaca", "ekologis"]
    }

    col_k1, col_k2 = st.columns([3, 2])
    with col_k1:
        df_tkii = extract_top_keywords(dfkii["Tanggapan"], tension_kii_kws)
        df_tkii = df_tkii[df_tkii["Jumlah"] > 0]
        if not df_tkii.empty:
            fig = bar_chart(df_tkii, "Tema", "Jumlah", "Frekuensi Sebutan Akar Ketegangan – KII", orientation="h")
            st.plotly_chart(fig, width="stretch")

    with col_k2:
        df_tkii_w = []
        base_kii = df_kii[df_kii["Narsum"].isin(sel_narsum)]
        for w in sorted(df_kii["Wilayah"].unique()):
            sub = base_kii[base_kii["Wilayah"] == w]["Tanggapan"]
            for label, kws in tension_kii_kws.items():
                pattern = "|".join(kws)
                cnt = sub.str.lower().str.contains(pattern, na=False).sum()
                if cnt > 0:
                    df_tkii_w.append({"Wilayah": w, "Isu": label, "Jumlah": cnt})
        df_tkii_w = pd.DataFrame(df_tkii_w)
        if not df_tkii_w.empty:
            wilayah_order = sorted(df_kii["Wilayah"].unique().tolist())
            df_tkii_w["Wilayah"] = pd.Categorical(df_tkii_w["Wilayah"], categories=wilayah_order, ordered=True)
            df_tkii_w = df_tkii_w.sort_values("Wilayah")
            fig2 = px.bar(df_tkii_w, x="Wilayah", y="Jumlah", color="Isu", barmode="stack",
                          title="Isu per Wilayah – Perspektif KII (Semua Wilayah)",
                          color_discrete_sequence=COLORS_MAIN,
                          category_orders={"Wilayah": wilayah_order})
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans", size=11),
                title_font=dict(family="Sora", size=14),
                margin=dict(t=50, b=20),
                legend=dict(font=dict(size=9), orientation="v"),
            )
            st.plotly_chart(fig2, width="stretch")

    st.divider()

    # ── ISU 2 KII: Kelompok Rentan ──
    st.markdown("### 🟠 Isu 2 · Kelompok Rentan yang Paling Terdampak")
    
    vuln_kws = {
        "Anak-anak / Remaja": ["anak", "remaja", "pelajar", "generasi muda"],
        "Perempuan": ["perempuan", "ibu", "mama", "wanita"],
        "Ibu Hamil / Balita": ["ibu hamil", "balita", "bayi"],
        "Lansia": ["lansia", "orang tua", "tua"],
        "Disabilitas": ["disabilitas", "difabel", "cacat"],
        "Komunitas Terpencil": ["terpencil", "tolikara", "nduga", "pedalaman", "isolasi"],
        "Keluarga Broken Home": ["broken home", "cerai", "perceraian", "tidak ada orang tua"],
    }

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        vuln_q_filter = dfkii["Pertanyaan"].str.contains("rentan|berisiko", case=False, na=False)
        df_vuln_kii = count_keyword_hits(dfkii[vuln_q_filter]["Tanggapan"], vuln_kws)
        df_vuln_kii = df_vuln_kii[df_vuln_kii["Jumlah"] > 0]
        if not df_vuln_kii.empty:
            fig = pie_chart(df_vuln_kii, "Tema", "Jumlah", "Komposisi Kelompok Rentan – Perspektif KII")
            st.plotly_chart(fig, width="stretch")

    with col_v2:
        st.markdown("**Gambaran Dampak per Kelompok Rentan:**")
        vuln_data = {
            "Kelompok": ["Anak-anak", "Ibu Hamil/Balita", "Perempuan", "Komunitas Terpencil", "Keluarga Broken Home"],
            "Risiko Utama": [
                "Dilibatkan perang suku, trauma konflik, putus sekolah, penyalahgunaan zat",
                "Tidak bisa menyuarakan kebutuhan, pasrah terhadap kondisi",
                "Kekerasan fisik (KDRT), diskriminasi adat, HIV akibat kekerasan seksual",
                "Blokade logistik, isolasi layanan kesehatan & pendidikan",
                "Rentan penyalahgunaan narkoba & aibon, putus sekolah",
            ]
        }
        st.dataframe(pd.DataFrame(vuln_data), width="stretch", hide_index=True)

    st.divider()

    # ── ISU 3 KII: Aktor Berpengaruh ──
    st.markdown("### 🟡 Isu 3 · Peta Aktor Berpengaruh & Dinamika Kekuasaan")
    
    actor_data = {
        "Aktor": ["Gereja / Tokoh Agama", "Kepala Suku / Adat", "TNI / Polri", "Pemerintah / Pemda",
                   "Pemuda", "LSM / NGO", "Kepala Kampung", "WVI"],
        "Pengaruh (1-10)": [9, 8, 7, 6, 8, 5, 4, 7],
        "Kepercayaan Publik (1-10)": [9, 8, 6, 4, 6, 7, 3, 8],
        "Kategori": ["Agama", "Adat", "Keamanan", "Politik", "Masyarakat", "Kemanusiaan", "Politik", "Kemanusiaan"],
    }
    df_actors = pd.DataFrame(actor_data)

    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        fig_actors = px.scatter(df_actors, x="Pengaruh (1-10)", y="Kepercayaan Publik (1-10)",
                                 size="Pengaruh (1-10)", color="Kategori", text="Aktor",
                                 title="Peta Aktor – Pengaruh vs. Kepercayaan Publik",
                                 color_discrete_sequence=COLORS_MAIN, size_max=40)
        fig_actors.update_traces(textposition="top center", textfont_size=10)
        fig_actors.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Plus Jakarta Sans", size=11),
            title_font=dict(family="Sora", size=14),
            margin=dict(t=60, b=20)
        )
        st.plotly_chart(fig_actors, width="stretch")

    with col_a2:
        st.markdown("**Pandangan Masyarakat terhadap Aktor:**")
        actor_quotes = [
            ("Dewan Gereja", "Masyarakat biasanya menghargai dan mendengar."),
            ("WVI", "Masyarakat sangat berterima kasih karena WVI turun langsung ke orang tua dan anak-anak."),
            ("Kepala Kampung", "Tidak peduli dengan masyarakat dan kurang dipercaya masyarakat."),
        ]
        for aktor, q in actor_quotes:
            st.markdown(f'<div class="quote-box"><span class="tag">{aktor}</span> "{q}"</div>', unsafe_allow_html=True)

    st.divider()

    # ── ISU 4 KII: Rekomendasi ──
    st.markdown("### 🟢 Isu 4 · Rekomendasi Kegiatan Pembinaan Perdamaian & Kesiapsiagaan")
    
    peace_kws = {
        "Psikososial / Trauma": ["trauma", "psikososial", "konseling", "pemulihan", "dukungan"],
        "Pendidikan Perdamaian": ["kurikulum damai", "edukasi perdamaian", "sekolah aman", "pelatihan guru"],
        "Pemberdayaan Ekonomi": ["ekonomi lokal", "pemberdayaan", "kapasitas", "beasiswa"],
        "Dialog & Mediasi Adat": ["dialog", "mediasi", "adat", "para-para", "musyawarah"],
        "Pelibatan Pemuda": ["pemuda", "olahraga", "seni", "penggerak damai", "remaja produktif"],
        "Advokasi Hak": ["advokasi", "hak ulayat", "hak adat", "pemetaan"],
        "Perlindungan Anak": ["perlindungan anak", "ramah anak", "unit perlindungan"],
    }

    peace_q = dfkii["Pertanyaan"].str.contains("perdamaian|pembinaan|kontribusi|bisa kami", case=False, na=False)
    df_peace = count_keyword_hits(dfkii[peace_q]["Tanggapan"], peace_kws)
    df_peace = df_peace[df_peace["Jumlah"] > 0]

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if not df_peace.empty:
            fig = bar_chart(df_peace, "Tema", "Jumlah", "Tema Rekomendasi Pembinaan Perdamaian – KII")
            st.plotly_chart(fig, width="stretch")

    with col_p2:
        df_peace_ns = []
        for ns in dfkii["Narsum"].unique():
            sub = dfkii[dfkii["Narsum"] == ns]
            sub_peace = sub[sub["Pertanyaan"].str.contains("perdamaian|pembinaan|kontribusi", case=False, na=False)]["Tanggapan"]
            for label, kws in peace_kws.items():
                pattern = "|".join(kws)
                cnt = sub_peace.str.lower().str.contains(pattern, na=False).sum()
                if cnt > 0:
                    df_peace_ns.append({"Narsum": ns, "Tema": label, "Jumlah": cnt})
        df_peace_ns = pd.DataFrame(df_peace_ns)
        if not df_peace_ns.empty:
            fig2 = px.bar(df_peace_ns, x="Narsum", y="Jumlah", color="Tema", barmode="stack",
                          title="Rekomendasi per Narasumber", color_discrete_sequence=COLORS_MAIN)
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans", size=11),
                title_font=dict(family="Sora", size=14),
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig2, width="stretch")

    st.divider()

    # ── ISU 5 KII: Skenario ──
    st.markdown("### 🔵 Isu 5 · Skenario Masa Depan & Implikasi bagi Operasional LSM")
    
    scenario_kii_kws = {
        "Stabilitas Terjaga": ["stabil", "terkendali", "aman", "sukses", "damai"],
        "Risiko Konflik Lahan": ["lahan", "ulayat", "deforestasi", "psn", "konflik baru"],
        "Risiko Ekonomi / Inflasi": ["inflasi", "pangan", "logistik", "harga", "krisis"],
        "Risiko Politik Lokal": ["pilkada", "pemilu", "kepala kampung", "kepercayaan rendah"],
        "Peluang Pembangunan": ["pembangunan", "infrastruktur", "investasi", "kapasitas"],
        "Hambatan Operasional LSM": ["palang", "akses", "hambatan", "keamanan operasi"],
    }

    sc_q_kii = dfkii["Pertanyaan"].str.contains("skenario|6 bulan|konsekuensi|operasional", case=False, na=False)
    df_sc_kii = count_keyword_hits(dfkii[sc_q_kii]["Tanggapan"], scenario_kii_kws)
    df_sc_kii = df_sc_kii[df_sc_kii["Jumlah"] > 0]

    col_sc1, col_sc2 = st.columns(2)
    with col_sc1:
        if not df_sc_kii.empty:
            colors_sc = ["#27ae60" if "Stab" in t or "Peluang" in t else "#e74c3c" for t in df_sc_kii["Tema"]]
            fig_sc2 = go.Figure(go.Bar(
                x=df_sc_kii["Jumlah"], y=df_sc_kii["Tema"],
                orientation="h", marker_color=colors_sc,
                text=df_sc_kii["Jumlah"], textposition="outside"
            ))
            fig_sc2.update_layout(
                title="Sebutan Faktor Risiko vs Peluang – Perspektif KII",
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Plus Jakarta Sans", size=11),
                title_font=dict(family="Sora", size=14),
                margin=dict(t=50, b=20, l=200, r=60)
            )
            st.plotly_chart(fig_sc2, width="stretch")

    with col_sc2:
        st.markdown("**Kutipan KII – Proyeksi & Rekomendasi:**")
        kii_sc_quotes = [
            ("Asmat | WBW", "Sidang MPL PGI Februari 2026 menolak PSN pangan dan militerisme. Deforestasi masif menghancurkan sumber pangan alami masyarakat adat."),
            ("Asmat | RJF", "Contingency Plan: alih metode ke daring/radio komunitas bila perlu."),
        ]
        for narsum, q in kii_sc_quotes:
            st.markdown(f'<div class="quote-box"><span class="tag">{narsum}</span> {q}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3: PERBANDINGAN & LAPORAN EKSEKUTIF
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">📊 Perbandingan Perspektif & Laporan Eksekutif</div>', unsafe_allow_html=True)

    st.markdown("### 🔍 Perbandingan Isu Utama: Perspektif Masyarakat vs. KII Pemerintah")

    # TAMBAHAN: Isu bencana alam & lingkungan dimasukkan ke radar chart perbandingan
    shared_dimensions = ["Narkoba / Zat Berbahaya", "Korupsi / Dana Desa", "Kekerasan & Kriminalitas",
                         "Kebutuhan Pendidikan", "Kebutuhan Kesehatan", "Konflik Lahan / Adat",
                         "Harapan pada Pemuda", "Kepercayaan pada Pemerintah", "Bencana Alam & Lingkungan"]

    keywords_shared = {
        "Narkoba / Zat Berbahaya": ["narkoba", "aibon", "ganja", "mabuk", "miras"],
        "Korupsi / Dana Desa": ["dana desa", "kepala kampung", "korupsi", "simpatisan", "musrenbang", "nepotisme"],
        "Kekerasan & Kriminalitas": ["kekerasan", "pencurian", "begal", "dipukul", "kriminal"],
        "Kebutuhan Pendidikan": ["sekolah", "pendidikan", "belajar", "guru"],
        "Kebutuhan Kesehatan": ["kesehatan", "imunisasi", "puskesmas", "rs", "hamil"],
        "Konflik Lahan / Adat": ["tanah", "lahan", "adat", "ulayat", "sengketa"],
        "Harapan pada Pemuda": ["pemuda", "generasi", "kontribusi", "berkontribusi"],
        "Kepercayaan pada Pemerintah": ["pemerintah", "bupati", "dinas", "aparat"],
        "Bencana Alam & Lingkungan": ["bencana", "banjir", "gempa", "longsor", "kekeringan", "cuaca", "iklim"]
    }

    scores_k, scores_kii = [], []
    for dim, kws in keywords_shared.items():
        pattern = "|".join(kws)
        sc_k = dfk["Tanggapan"].str.lower().str.contains(pattern, na=False).sum()
        sc_kii = dfkii["Tanggapan"].str.lower().str.contains(pattern, na=False).sum()
        scores_k.append(sc_k)
        scores_kii.append(sc_kii)

    max_k = max(scores_k) if max(scores_k) > 0 else 1
    max_kii = max(scores_kii) if max(scores_kii) > 0 else 1
    norm_k = [round(x / max_k * 10, 1) for x in scores_k]
    norm_kii = [round(x / max_kii * 10, 1) for x in scores_kii]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=norm_k + [norm_k[0]], theta=shared_dimensions + [shared_dimensions[0]],
        fill="toself", name="Kelompok Masyarakat",
        line=dict(color="#e74c3c", width=2), fillcolor="rgba(231,76,60,0.15)"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=norm_kii + [norm_kii[0]], theta=shared_dimensions + [shared_dimensions[0]],
        fill="toself", name="KII Pemerintah/Lembaga",
        line=dict(color="#2980b9", width=2), fillcolor="rgba(41,128,185,0.15)"
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], gridcolor="#eee"),
                   angularaxis=dict(gridcolor="#eee")),
        showlegend=True, title="Perbandingan Fokus Isu – Kelompok vs. KII (Skor Relatif 0-10)",
        paper_bgcolor="white", font=dict(family="Plus Jakarta Sans", size=11),
        title_font=dict(family="Sora", size=15),
        margin=dict(t=60, b=40)
    )
    st.plotly_chart(fig_radar, width="stretch")

    st.divider()

    # Table & Executive Summary
    st.markdown("### 📋 Ringkasan Perbandingan Isu per Wilayah")
    comparison_data = {
        "Wilayah": ["Jayawijaya", "Asmat (Papua Selatan)", "Sentani"],
        "Isu Utama Masyarakat": [
            "Miras, judol, aibon, perang suku, kurang pendidikan karakter anak",
            "Korupsi kepala kampung, distribusi bantuan tidak merata, kebutuhan air bersih & infrastruktur",
            "Sengketa tanah, kenakalan remaja, kekerasan dalam keluarga (KDRT pada anak perempuan)",
        ],
        "Isu Utama KII": [
            "Nepotisme birokrasi, kesenjangan OAP vs pendatang, potensi eskalasi politik",
            "Hak adat terancam PSN/deforestasi, krisis pangan lokal akibat cuaca/perubahan ekosistem",
            "Narkoba & aibon pada anak, HIV anak SD, keterbatasan fasilitas rehabilitasi",
        ],
        "Titik Konvergensi": [
            "Anak-anak rentan: putus sekolah & dilibatkan konflik",
            "Ketidakadilan distribusi bantuan & lemahnya tata kelola kampung",
            "Minimnya ruang aman bagi anak & remaja",
        ],
        "Tokoh Kunci": [
            "Kepala suku, tokoh agama, pemimpin gereja",
            "Dewan adat, gereja, kepala marga",
            "Kepala kampung, pendeta, Dinas Sosial",
        ]
    }
    df_compare = pd.DataFrame(comparison_data)
    st.dataframe(df_compare, width="stretch", hide_index=True)

    st.divider()

    # Raw Data Explorer
    with st.expander("🔎 Eksplorasi Data Mentah"):
        tab_raw1, tab_raw2 = st.tabs(["Dataset Kelompok", "Dataset KII"])
        with tab_raw1:
            q_filter = st.selectbox("Filter Pertanyaan:", ["(Semua)"] + sorted(dfk["Pertanyaan"].unique().tolist()), key="q1")
            df_show = dfk if q_filter == "(Semua)" else dfk[dfk["Pertanyaan"] == q_filter]
            st.dataframe(df_show[["Wilayah", "Kelompok_Usia", "Jenis_Kelamin", "Pertanyaan", "Tanggapan"]],
                         width="stretch", hide_index=True)
        with tab_raw2:
            q_filter2 = st.selectbox("Filter Pertanyaan:", ["(Semua)"] + sorted(dfkii["Pertanyaan"].unique().tolist()), key="q2")
            df_show2 = dfkii if q_filter2 == "(Semua)" else dfkii[dfkii["Pertanyaan"] == q_filter2]
            st.dataframe(df_show2[["Wilayah", "Narsum", "Pertanyaan", "Tanggapan"]],
                         width="stretch", hide_index=True)
