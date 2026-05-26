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
    .metric-card-env {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 4px solid #27ae60;
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
    .issue-card-env {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
        border-top: 3px solid #27ae60;
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
    .section-header-env {
        background: linear-gradient(135deg, #1e3d2f 0%, #27ae60 100%);
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
                "#8e44ad", "#16a085", "#d35400", "#1abc9c", "#e74c3c"]
COLORS_ENV = ["#27ae60", "#2ecc71", "#1abc9c", "#3498db", "#9b59b6", "#e67e22"]

def bar_chart(df, x, y, title, color_col=None, orientation="v", colors_seq=COLORS_MAIN):
    if orientation == "h":
        fig = px.bar(df, x=y, y=x, orientation="h", title=title,
                     color=color_col if color_col else y,
                     color_discrete_sequence=colors_seq)
        fig.update_traces(texttemplate="%{x}", textposition="outside")
    else:
        fig = px.bar(df, x=x, y=y, title=title,
                     color=color_col if color_col else x,
                     color_discrete_sequence=colors_seq)
        fig.update_traces(texttemplate="%{y}", textposition="outside")
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Plus Jakarta Sans", size=12),
        title_font=dict(family="Sora", size=15, color="#1a1a2e"),
        showlegend=False, margin=dict(t=50, b=20, l=20, r=20),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    return fig

def pie_chart(df, names, values, title, colors_seq=COLORS_MAIN):
    fig = px.pie(df, names=names, values=values, title=title,
                 color_discrete_sequence=colors_seq, hole=0.4)
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    fig.update_layout(
        paper_bgcolor="white", font=dict(family="Plus Jakarta Sans"),
        title_font=dict(family="Sora", size=15, color="#1a1a2e"),
        margin=dict(t=50, b=10, l=10, r=10),
    )
    return fig


# ─────────────────────────────────────────────
# LOAD DATA & NAVIGATION SIDEBAR
# ─────────────────────────────────────────────
df_k, df_kii = load_data()

with st.sidebar:
    st.markdown("## 🗺️ NAVIGATION")
    # Menu Navigasi Utama Halaman
    page_selection = st.radio(
        "Pilih Halaman Analisis:",
        ["🏠 Main Dashboard", "🌊 Analisis Bencana Alam"]
    )
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
    st.caption("Data: Program GECAR | Dashboard v1.1")

# Global Filter Application
mask_k = (df_k["Wilayah"].isin(sel_wilayah_k) & df_k["Kelompok_Usia"].isin(sel_usia) & df_k["Jenis_Kelamin"].isin(sel_gender))
dfk = df_k[mask_k].copy()

mask_kii = (df_kii["Wilayah"].isin(sel_wilayah_kii) & df_kii["Narsum"].isin(sel_narsum))
dfkii = df_kii[mask_kii].copy()


# ══════════════════════════════════════════════
# HALAMAN 1: MAIN DASHBOARD (SOSIAL & EKONOMI)
# ══════════════════════════════════════════════
if page_selection == "🏠 Main Dashboard":
    
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
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Responden Kelompok</div><div class="metric-value">{len(dfk)}</div><div class="metric-delta">3 Wilayah</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Responden KII</div><div class="metric-value">{len(dfkii)}</div><div class="metric-delta">7 Narasumber</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Wilayah Kajian</div><div class="metric-value">3</div><div class="metric-delta">Jayawijaya · Asmat · Sentani</div></div>', unsafe_allow_html=True)
    with col4:
        n_isu = dfk["Tanggapan"].str.lower().str.contains("mabuk|miras|aibon|ganja|narkoba", na=False).sum()
        st.markdown(f'<div class="metric-card"><div class="metric-label">Menyebut Narkoba/Miras</div><div class="metric-value" style="color:#c0392b;">{n_isu}</div><div class="metric-delta">Tanggapan Kelompok</div></div>', unsafe_allow_html=True)
    with col5:
        n_kdrt = dfk["Tanggapan"].str.lower().str.contains("kekerasan|dipukul|begal|pencurian|kriminal", na=False).sum()
        st.markdown(f'<div class="metric-card"><div class="metric-label">Menyebut Kekerasan/Kriminal</div><div class="metric-value" style="color:#c0392b;">{n_kdrt}</div><div class="metric-delta">Tanggapan Kelompok</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📋 Dataset 1 – Kelompok Masyarakat",
        "🏛️ Dataset 2 – KII Pemerintah/Lembaga",
        "📊 Perbandingan & Laporan Eksekutif",
    ])

    with tab1:
        st.markdown('<div class="section-header">📋 Analisis Tanggapan Kelompok Masyarakat</div>', unsafe_allow_html=True)
        st.markdown("### 🔴 Isu 1 · Peta Ketegangan & Konflik Sosial")
        
        tension_keywords = {
            "Miras / Mabuk": ["mabok", "mabuk", "miras", "alkohol", "minuman keras"],
            "Narkoba / Aibon": ["narkoba", "aibon", "ganja", "obat terlarang"],
            "Judol / Perjudian": ["judol", "judi", "perjudian"],
            "Pencurian / Begal": ["pencurian", "begal", "curi", "kriminal", "rampok"],
            "Perang Suku": ["perang suku", "konflik suku", "denda adat", "sajam"],
            "Korupsi / Dana Desa": ["dana desa", "kepala kampung", "korupsi", "dipotong", "simpatisan", "musrenbang"],
            "Kekerasan Fisik / KDRT": ["kekerasan", "dipukul", "parang", "pukul", "pukuli"],
            "Sengketa Tanah": ["sengketa tanah", "batas wilayah", "hak tanah", "hak ulayat", "lahan"],
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
                fig2 = px.bar(df_w, x="Wilayah", y="Jumlah", color="Isu", title="Ketegangan per Wilayah", barmode="stack", color_discrete_sequence=COLORS_MAIN)
                st.plotly_chart(fig2, width="stretch")

        st.markdown("**Kutipan Langsung Tokoh/Masyarakat:**")
        st.markdown('<div class="quote-box"><span class="tag">Asmat</span> "Bantuan yang sampai ke masyarakat dipotong di distrik dan di kampung sehingga yang sampai ke masyarakat tidak penuh."</div>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 🟠 Isu 2 · Kebutuhan Dasar yang Belum Terpenuhi")
        needs_keywords = {
            "Air Bersih / PAH": ["air bersih", "sumur bor", "blong", "pah", "air minum", "penampungan air"],
            "Pendidikan Anak": ["sekolah", "pendidikan", "belajar", "guru", "tk", "paud", "sd", "smp"],
            "Kesehatan": ["kesehatan", "imunisasi", "puskesmas", "rs", "hamil", "balita"],
            "Ekonomi / Pekerjaan": ["ekonomi", "pekerjaan", "kerja", "modal", "usaha", "keramba"],
            "Infrastruktur": ["jalan", "jembatan", "kamar mandi", "mck", "renovasi"],
        }
        col_n1, col_n2, col_n3 = st.columns(3)
        cols_need = [col_n1, col_n2, col_n3]
        for i, (wilayah) in enumerate(["Jayawijaya", "Asmat, Papua Selatan", "Sentani"]):
            sub = dfk[dfk["Wilayah"] == wilayah]["Tanggapan"]
            df_n = count_keyword_hits(sub, needs_keywords)
            df_n = df_n[df_n["Jumlah"] > 0]
            with cols_need[i]:
                if not df_n.empty:
                    fig = pie_chart(df_n, "Tema", "Jumlah", f"Kebutuhan Utama – {wilayah.split(',')[0]}")
                    st.plotly_chart(fig, width="stretch")

        st.divider()
        st.markdown("### 🟡 Isu 3 · Kekerasan terhadap Anak & Diskriminasi Gender")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            sentani_anak = dfk[(dfk["Wilayah"] == "Sentani") & (dfk["Kelompok_Usia"] == "Anak")]
            violence_kws = {
                "Kekerasan fisik dari orang tua": ["dipukul", "pukul", "kekerasan fisik"],
                "Ancaman dari orang mabuk": ["mabuk", "miras"],
                "Bullying / stigma sosial": ["bully", "fitnah"],
                "Diskriminasi gender / adat": ["perempuan tidak boleh", "dilarang"],
            }
            df_viol_p = count_keyword_hits(sentani_anak[sentani_anak["Jenis_Kelamin"] == "Perempuan"]["Tanggapan"], violence_kws).assign(Gender="Perempuan")
            df_viol_l = count_keyword_hits(sentani_anak[sentani_anak["Jenis_Kelamin"] == "Laki laki"]["Tanggapan"], violence_kws).assign(Gender="Laki-laki")
            df_viol = pd.concat([df_viol_p, df_viol_l])
            if not df_viol.empty:
                fig = px.bar(df_viol, x="Tema", y="Jumlah", color="Gender", barmode="group", title="Ketakutan Anak Sentani – per Gender", color_discrete_map={"Perempuan": "#e74c3c", "Laki-laki": "#2980b9"})
                st.plotly_chart(fig, width="stretch")
        with col_v2:
            st.markdown('<div class="alert-red">准 Kekerasan fisik orang tua disebut oleh <b>5 dari 9 anak perempuan</b> Sentani sebagai ketakutan utama mereka.</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-header">🏛️ Analisis Tanggapan KII – Pemerintah & Lembaga</div>', unsafe_allow_html=True)
        st.markdown("### 🔴 Isu 1 · Akar Ketegangan Struktural & Lokal")
        
        tension_kii_kws = {
            "Nepotisme / Korupsi Birokrasi": ["nepotisme", "birokrasi", "korupsi", "transparan"],
            "Kesenjangan OAP vs Pendatang": ["oap", "pendatang", "polarisasi"],
            "Hak Adat / Lahan": ["hak adat", "ulayat", "adat", "lahan", "deforestasi", "psn"],
            "Konflik Bersenjata / KKB": ["kkb", "bersenjata", "tni", "polri"],
            "Inflasi / Krisis Ekonomi": ["inflasi", "pangan", "logistik"],
        }
        
        df_tkii = extract_top_keywords(dfkii["Tanggapan"], tension_kii_kws)
        if not df_tkii.empty:
            fig = bar_chart(df_tkii, "Tema", "Jumlah", "Akar Ketegangan Utama Struktural – Perspektif Pembuat Kebijakan", orientation="h")
            st.plotly_chart(fig, width="stretch")

    with tab3:
        st.markdown('<div class="section-header">📊 Perbandingan Perspektif & Laporan Eksekutif</div>', unsafe_allow_html=True)
        
        shared_dimensions = ["Narkoba / Zat Berbahaya", "Korupsi / Dana Desa", "Kekerasan & Kriminalitas", "Kebutuhan Pendidikan", "Kebutuhan Kesehatan", "Konflik Lahan / Adat"]
        keywords_shared = {
            "Narkoba / Zat Berbahaya": ["narkoba", "aibon", "ganja", "mabuk", "miras"],
            "Korupsi / Dana Desa": ["dana desa", "kepala kampung", "korupsi", "nepotisme"],
            "Kekerasan & Kriminalitas": ["kekerasan", "pencurian", "begal", "dipukul"],
            "Kebutuhan Pendidikan": ["sekolah", "pendidikan", "belajar", "guru"],
            "Kebutuhan Kesehatan": ["kesehatan", "imunisasi", "puskesmas"],
            "Konflik Lahan / Adat": ["tanah", "lahan", "adat", "ulayat"],
        }
        
        scores_k, scores_kii = [], []
        for dim, kws in keywords_shared.items():
            pattern = "|".join(kws)
            scores_k.append(dfk["Tanggapan"].str.lower().str.contains(pattern, na=False).sum())
            scores_kii.append(dfkii["Tanggapan"].str.lower().str.contains(pattern, na=False).sum())
            
        max_k = max(scores_k) if max(scores_k) > 0 else 1
        max_kii = max(scores_kii) if max(scores_kii) > 0 else 1
        norm_k = [round(x / max_k * 10, 1) for x in scores_k]
        norm_kii = [round(x / max_kii * 10, 1) for x in scores_kii]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=norm_k + [norm_k[0]], theta=shared_dimensions + [shared_dimensions[0]], fill="toself", name="Masyarakat", line=dict(color="#e74c3c")))
        fig_radar.add_trace(go.Scatterpolar(r=norm_kii + [norm_kii[0]], theta=shared_dimensions + [shared_dimensions[0]], fill="toself", name="KII", line=dict(color="#2980b9")))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), title="Perbandingan Fokus Isu (Skor Relatif 0-10)")
        st.plotly_chart(fig_radar, width="stretch")


# ══════════════════════════════════════════════
# HALAMAN 2: ANALISIS SPESIFIK BENCANA ALAM & IKLIM
# ══════════════════════════════════════════════
elif page_selection == "🌊 Analisis Bencana Alam":
    
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3d2f 0%,#27ae60 100%);
                padding:32px 36px; border-radius:14px; margin-bottom:28px;">
      <h1 style="color:white;margin:0;font-family:Sora,sans-serif;font-size:2rem;">
        🌊 Analisis Khusus: Kerentanan Bencana Alam & Dampak Lingkungan
      </h1>
      <p style="color:rgba(255,255,255,0.85);margin:8px 0 0;font-size:0.95rem;">
        Halaman khusus ekstraksi data kualitatif mengenai ancaman ekologis, cuaca ekstrem, iklim, dan bencana alam lokal dari perspektif masyarakat serta KII
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Kata kunci bencana alam
    disaster_keywords = {
        "Banjir / Luapan Air": ["banjir", "air pasang", "luapan danau", "rob", "tergenang"],
        "Kekeringan / Kemarau": ["kekeringan", "kering", "kemarau", "susah air"],
        "Embun Beku / Frost (Puncak)": ["embun beku", "frost", "hujan es", "dingin ekstrem", "tanaman ubi rusak"],
        "Longsor / Gempa Bumi": ["longsor", "gempa", "tanah runtuh", "pergeseran tanah"],
        "Cuaca Ekstrem / Angin Ribut": ["cuaca ekstrem", "angin kencang", "puting beliung", "badai", "pancaroba"]
    }

    # Hitung metrik spesifik bencana
    pattern_all = "banjir|air pasang|rob|kekeringan|kemarau|embun beku|frost|longsor|gempa|cuaca"
    total_disaster_k = dfk["Tanggapan"].str.lower().str.contains(pattern_all, na=False).sum()
    total_disaster_kii = dfkii["Tanggapan"].str.lower().str.contains(pattern_all, na=False).sum()

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""<div class="metric-card-env">
            <div class="metric-label">Sebutan Isu Bencana (Masyarakat)</div>
            <div class="metric-value" style="color:#27ae60;">{total_disaster_k}</div>
            <div class="metric-delta">Dari total data filter aktif</div>
        </div>""", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""<div class="metric-card-env">
            <div class="metric-label">Sebutan Isu Bencana (KII Pemerintah)</div>
            <div class="metric-value" style="color:#27ae60;">{total_disaster_kii}</div>
            <div class="metric-delta">Dari laporan pemangku kebijakan</div>
        </div>""", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""<div class="metric-card-env">
            <div class="metric-label">Status Urgensi Sektoral</div>
            <div class="metric-value" style="color:#e67e22;">Mendesak</div>
            <div class="metric-delta">Pengaruh langsung ke ketahanan pangan</div>
        </div>""", unsafe_allow_html=True)

    # Kartu Isu Konteks Geografis Papua
    st.markdown("""
    <div class="issue-card-env">
        <div class="issue-title">🌲 Karakteristik & Tipologi Risiko Ekologis Antar Wilayah</div>
        <div class="issue-desc">Analisis data kualitatif mengindikasikan korelasi geografis yang sangat spesifik:
        <li><b>Sentani:</b> Kerentanan didominasi oleh banjir luapan Danau Sentani dan riwayat banjir bandang akibat degradasi cagar alam Cycloop.</li>
        <li><b>Asmat:</b> Ancaman berupa siklus air pasang laut (Banjir Rob) yang mengikis jembatan panggung serta intrusi air asin yang merusak penampung air hujan (PAH).</li>
        <li><b>Jayawijaya:</b> Risiko tertinggi bersumber dari anomali iklim pegunungan tengah berupa bencana embun beku (frost/embun racun) yang mampu menghancurkan komoditas ubi jalar (hipere) secara masif dalam satu malam.</li>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Visualisasi Data Bencana
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        df_dis_k = extract_top_keywords(dfk["Tanggapan"], disaster_keywords)
        df_dis_k = df_dis_k[df_dis_k["Jumlah"] > 0]
        if not df_dis_k.empty:
            fig_dis_k = bar_chart(df_dis_k, "Tema", "Jumlah", "Jenis Bencana yang Paling Dikhawatirkan Masyarakat", orientation="h", colors_seq=COLORS_ENV)
            st.plotly_chart(fig_dis_k, width="stretch")
        else:
            st.info("Tidak ada sebutan isu bencana spesifik pada filter kelompok masyarakat saat ini.")

    with col_g2:
        # Distribusi Isu Bencana per Wilayah (Dataset Kelompok)
        df_dis_w = []
        for w in dfk["Wilayah"].unique():
            sub = dfk[dfk["Wilayah"] == w]["Tanggapan"]
            for label, kws in disaster_keywords.items():
                pattern = "|".join(kws)
                cnt = sub.str.lower().str.contains(pattern, na=False).sum()
                if cnt > 0:
                    df_dis_w.append({"Wilayah": w.split(",")[0], "Jenis Bencana": label, "Jumlah": cnt})
        df_dis_w = pd.DataFrame(df_dis_w)
        
        if not df_dis_w.empty:
            fig_dis_w = px.bar(df_dis_w, x="Wilayah", y="Jumlah", color="Jenis Bencana", barmode="stack",
                              title="Persebaran Keluhan Isu Lingkungan per Wilayah", color_discrete_sequence=COLORS_ENV)
            fig_dis_w.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(family="Plus Jakarta Sans"))
            st.plotly_chart(fig_dis_w, width="stretch")
        else:
            st.info("Data grafik sebaran wilayah kosong.")

    st.divider()

    # Perspektif Pemangku Kebijakan (KII) mengenai mitigasi krisis iklim
    st.markdown("### 🏛️ Sudut Pandang Kebijakan (KII Pemerintah & Lembaga Adat)")
    
    col_p1, col_p2 = st.columns([3, 2])
    with col_p1:
        df_dis_kii = extract_top_keywords(dfkii["Tanggapan"], disaster_keywords)
        df_dis_kii = df_dis_kii[df_dis_kii["Jumlah"] > 0]
        if not df_dis_kii.empty:
            fig_dis_kii = px.pie(df_dis_kii, names="Tema", values="Jumlah", title="Proporsi Pembahasan Mitigasi Bencana – Dataset KII",
                                 color_discrete_sequence=COLORS_ENV, hole=0.4)
            fig_dis_kii.update_layout(paper_bgcolor="white", font=dict(family="Plus Jakarta Sans"))
            st.plotly_chart(fig_dis_kii, width="stretch")
        else:
            st.info("Pemangku kebijakan belum menyentuh narasi mitigasi fisik lingkungan pada pilihan narasumber saat ini.")

    with col_p2:
        st.markdown("**Kutipan & Temuan Terkait Bencana Alam:**")
        st.markdown('<div class="quote-box"><span class="tag">Sentani | KII</span> "Mitigasi jangka panjang luapan danau memerlukan relasi tata ruang yang aman bagi area pemukiman pinggir air."</div>', unsafe_allow_html=True)
        st.markdown('<div class="quote-box"><span class="tag">Asmat | Kelompok</span> "Kalau musim air pasang naik (rob), jembatan papan rusak semua, anak-anak tidak bisa lewat ke sekolah dan air bersih jadi asin."</div>', unsafe_allow_html=True)
        st.markdown('<div class="quote-box"><span class="tag">Jayawijaya | KII</span> "Ancaman gagal panen ubi akibat fenomena cuaca kering dingin (frost) langsung berdampak pada naiknya ketegangan stok pangan antar kampung."</div>', unsafe_allow_html=True)
