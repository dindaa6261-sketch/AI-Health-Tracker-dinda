import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="AI Health Tracker", page_icon="🔥", layout="wide")

# 2. Custom CSS untuk Tampilan "Dhashbor HEALTH"
st.markdown("""
    <style>
    /* Background utama gelap pekat */
    .stApp {
        background: radial-gradient(circle, #1a1a2e 0%, #16213e 100%);
        color: #e94560;
    }

    /* Header Utama dengan Efek Glow */
    .main-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.5);
        margin-bottom: 10px;
    }

    /* Kartu Metrik Neon */
    .metric-box {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 242, 254, 0.3);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: 0.3s;
    }
    .metric-box:hover {
        border-color: #00f2fe;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
    }

    /* Tombol Sidebar Custom */
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 10px 20px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3);
    }

    /* Khusus tombol hapus (warna merah) */
    .stButton>button[kind="secondary"] {
        background: linear-gradient(90deg, #ff4e50 0%, #f9d423 100%);
        border: none;
    }

    /* Label Input Sidebar */
    .st-at { color: #00f2fe !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title"> Selamat datang di🔥 AI HEALTH TRACKER </h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #4facfe;">Sistem Monitoring Kesehatan Masa Depan v2.0</p>', unsafe_allow_html=True)
st.divider()

# --- SIDEBAR ---
st.sidebar.markdown("<h2 style='color: #00f2fe;'>⚙️ SETTINGS</h2>", unsafe_allow_html=True)

# Form Input Data
with st.sidebar.form("input_form"):
    nama = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
    usia = st.number_input("Usia (Tahun)", min_value=1, max_value=120, step=1)
    st.markdown("---")
    berat = st.number_input("Berat (kg)", min_value=1.0, step=0.1)
    tinggi_cm = st.number_input("Tinggi (cm)", min_value=1.0, step=0.1)
    submit = st.form_submit_button("🚀 UPDATE DATA")

# Fitur Hapus Riwayat (Di luar Form agar langsung bereaksi)
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='color: #ff4e50;'></p>", unsafe_allow_html=True)
if st.sidebar.button("🗑️ HAPUS SEMUA DATA", type="secondary"):
    if os.path.exists("riwayat_imt.csv"):
        os.remove("riwayat_imt.csv")
        st.sidebar.success("Riwayat dihapus!")
        st.rerun() # Refresh aplikasi
    else:
        st.sidebar.error("Data sudah kosong.")

# --- LOGIKA DATA ---
if submit:
    if nama == "":
        st.sidebar.error("Nama tidak boleh kosong!")
    else:
        tinggi_m = tinggi_cm / 100
        imt = berat / (tinggi_m ** 2)
        waktu = datetime.now().strftime("%H:%M | %d %b")
        if imt < 18.5: kat = "KURUS"
        elif 18.5 <= imt < 25: kat = "IDEAL"
        elif 25 <= imt < 30: kat = "OVERWEIGHT"
        else: kat = "OBESITAS"

        # Menyimpan data termasuk Nama dan Usia
        data_baru = pd.DataFrame([[waktu, nama, usia, berat, tinggi_cm, round(imt, 2), kat]],
        columns=["Waktu", "Nama", "Usia", "Berat", "Tinggi", "IMT", "Kategori"])
        try:
            df_old = pd.read_csv("riwayat_imt.csv")
            df_final = pd.concat([df_old, data_baru], ignore_index=True)
        except:
            df_final = data_baru
        df_final.to_csv("riwayat_imt.csv", index=False)
        st.rerun()

# --- DASHBOARD ---
if os.path.exists("riwayat_imt.csv"):
    df = pd.read_csv("riwayat_imt.csv")

    # Grid Kolom Metrik
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-box"><p style="color:#00f2fe; margin:0;">SKOR IMT</p><h1 style="color:white; margin:0;">{df["IMT"].iloc[-1]}</h1></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><p style="color:#00f2fe; margin:0;">BERAT BADAN</p><h1 style="color:white; margin:0;">{df["Berat"].iloc[-1]}<span style="font-size:15px;">kg</span></h1></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><p style="color:#00f2fe; margin:0;">KATEGORI</p><h2 style="color:#00ff87; margin:0;">{df["Kategori"].iloc[-1]}</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Grafik dan Tabel
    tab1, tab2 = st.tabs(["📊 GRAFIK TREN", "📜 LOG RIWAYAT"])

    with tab1:
        st.area_chart(df.set_index('Waktu')['IMT'])

    with tab2:
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
else:
    st.info("Silakan isi Nama, Usia, dan data fisik Anda di samping.")