import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Halaman (Layout Lebar)
st.set_page_config(
    page_title="AI Stock Analyzer Pro - IHSG",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk Background Gedung Kota, Teks Warna-warni, dan Styling Modern
st.markdown("""
    <style>
    /* Background siluet gedung kota malam hari dengan overlay gelap agar kontras */
    .stApp {
        background: linear-gradient(rgba(10, 25, 47, 0.85), rgba(5, 15, 30, 0.95)), 
                    url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Efek Tulisan Warna-Warni Bergradasi */
    .rainbow-title {
        background: linear-gradient(45deg, #00ff87, #60efff, #ff007f, #fffc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0px 2px 10px rgba(0,0,0,0.3);
    }

    .sub-rainbow {
        background: linear-gradient(45deg, #ff99ff, #66ffff, #ffff66);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        margin-top: -15px;
        margin-bottom: 30px;
    }

    /* Styling Kotak Konten / Kartu Transparan */
    .card-container {
        background: rgba(15, 23, 42, 0.75);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
        color: #ffffff;
    }

    /* Sembunyikan elemen bawaan sidebar jika masih tersisa */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Judul Utama dengan Teks Warna-Warni
st.markdown('<h1 class="rainbow-title">🏙️ AI Smart Stock Analyzer & News Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-rainbow">Platform Analisis Saham IHSG Canggih dengan Rekomendasi Real-time & Berita Terkini</p>', unsafe_allow_html=True)

# --- PANEL KONTROL UTAMA ---
with st.container():
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        selected_stock = st.selectbox(
            "🔍 Pilih Emiten Saham (IHSG)",
            ["BBCA (Bank Central Asia Tbk)", "BBRI (Bank Rakyat Indonesia Tbk)", "ASII (Astra International Tbk)", 
             "TLKM (Telkom Indonesia Tbk)", "ADRO (Adaro Energy Indonesia Tbk)", "BMRI (Bank Mandiri Tbk)"]
        )
    with col2:
        trading_style = st.selectbox(
            "📊 Gaya Analisis / Strategi",
            ["Momentum Day Trading", "Scalping Setup", "Swing Trading (Medium Term)", "Long-Term Investing"]
        )
    with col3:
        st.write("&nbsp;")
        analyze_btn = st.button("🚀 Jalankan AI Analisis", type="primary", use_container_width=True)

# Simulasi Data Berita & Analisis Berdasarkan Pilihan Saham
stock_ticker = selected_stock.split(" ")[0]

news_database = {
    "BBCA": [
        {"title": "BBCA Catat Pertumbuhan Volume Transaksi Digital Sebesar 18% YoY", "time": "2 jam lalu", "sentiment": "Positif"},
        {"title": "Analis Asing Kembali Akumulasi Saham Big Banks Menjelang Akhir Bulan", "time": "5 jam lalu", "sentiment": "Positif"}
    ],
    "BBRI": [
        {"title": "Fokus Pembiayaan Mikro, Segmen Kridit Usaha Rakyat (KUR) Tunjukkan Tren Sehat", "time": "1 jam lalu", "sentiment": "Positif"},
        {"title": "Diterpa Isu Likuiditas Global, Sektor Perbankan Tetap Menarik Perhatian Investor", "time": "4 jam lalu", "sentiment": "Netral"}
    ],
    "ASII": [
        {"title": "Penjualan Kendaraan Bermotor Roda Empat Mengalami Penyesuaian Tipis", "time": "3 jam lalu", "sentiment": "Netral"},
        {"title": "Divisi Alat Berat dan Pertambangan Sumbang Pendapatan Solid", "time": "6 jam lalu", "sentiment": "Positif"}
    ],
    "TLKM": [
        {"title": "Telkom Perkuat Infrastruktur Konektivitas Data Center di Batam dan Jakarta", "time": "1 jam lalu", "sentiment": "Positif"},
        {"title": "Konsolidasi Harga Telkom, Peluang Akumulasi Jangka Panjang?", "time": "7 jam lalu", "sentiment": "Netral"}
    ],
    "ADRO": [
        {"title": "Harga Komoditas Batubara Global Bergerak Fluktuatif di Tengah Permintaan Asia", "time": "2 jam lalu", "sentiment": "Netral"},
        {"title": "Adaro Terus Genjot Diversifikasi ke Sektor Energi Hijau & Smelter", "time": "4 jam lalu", "sentiment": "Positif"}
    ],
    "BMRI": [
        {"title": "Bank Mandiri Optimis Proyeksi Kinerja Kuartal Ini Melampaui Target Konsensus", "time": "30 menit lalu", "sentiment": "Positif"},
        {"title": "Foreign Outflow Mereda, Saham Blue Chip Perbankan Jadi Incaran", "time": "5 jam lalu", "sentiment": "Positif"}
    ]
}

recommendation_database = {
    "BBCA": {
        "action": "STRONG BUY (AKUMULASI KUAT)",
        "color": "#00FF7F",
        "reason": "Secara teknikal berada di area support kuat dengan dukungan broker flow akumulasi asing. Valuasi masih atraktif untuk swing trade dan momentum penguatan lanjutan."
    },
    "BBRI": {
        "action": "BUY ON WEAKNESS",
        "color": "#00FF7F",
        "reason": "Pola pergerakan harga membentuk rounding bottom jangka pendek. Indikator MACD menunjukkan potensi golden cross, sangat baik untuk strategi akumulasi bertahap."
    },
    "ASII": {
        "action": "HOLD / TRADING BUY",
        "color": "#FFD700",
        "reason": "Pergerakan cenderung konsolidasi (sideways). Tunggu konfirmasi breakout resistance terdekat sebelum melakukan penambahan posisi dalam jumlah besar."
    },
    "TLKM": {
        "action": "ACCUMULATE BUY",
        "color": "#00FF7F",
        "reason": "Valuasi Price to Earnings (P/E) rasio berada di bawah rata-rata historis 3 tahun. Dividen yield yang stabil memberikan proteksi margin bawah yang kuat."
    },
    "ADRO": {
        "action": "SPECULATIVE BUY",
        "color": "#00FF7F",
        "reason": "Sangat sensitif terhadap pergerakan harga komoditas harian. Cocok untuk trader cepat (scalper) memanfaatkan pantulan (bounce) dari support minor."
    },
    "BMRI": {
        "action": "STRONG BUY",
        "color": "#00FF7F",
        "reason": "Pertumbuhan laba bersih konsisten dengan efisiensi operasional yang terjaga dengan baik. Volume transaksi harian melonjak signifikan di sesi kedua."
    }
}

# --- TAMPILAN HASIL ANALISIS & BERITA ---
st.markdown("---")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 📰 Berita Terbaru Terkait " + stock_ticker)
    news_list = news_database.get(stock_ticker, [])
    
    for news in news_list:
        sentiment_color = "#00ff87" if news['sentiment'] == "Positif" else "#ffcc00"
        st.markdown(f"""
        <div class="card-container" style="padding: 15px; margin-bottom: 10px;">
            <div style="font-size: 1.05rem; font-weight: bold; color: #ffffff; margin-bottom: 5px;">{news['title']}</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                <span>⏱️ {news['time']}</span>
                <span style="color: {sentiment_color}; font-weight: bold;">Sentimen: {news['sentiment']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 🤖 Rekomendasi & Analisis AI Canggih")
    rec = recommendation_database.get(stock_ticker, {"action": "HOLD", "color": "#FFD700", "reason": "Analisis netral berdasarkan kondisi pasar saat ini."})
    
    st.markdown(f"""
    <div class="card-container">
        <div style="font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Rekomendasi AI Trading ({trading_style})</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: {rec['color']}; margin: 10px 0;">{rec['action']}</div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
        <div style="font-size: 0.95rem; font-weight: 600; color: #f8fafc; margin-bottom: 8px;">💡 Alasan & Analisis Mendalam:</div>
        <div style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.5;">{rec['reason']}</div>
        <br>
        <div style="background: rgba(0, 255, 135, 0.1); padding: 10px; border-radius: 6px; border-left: 4px solid #00ff87; font-size: 0.85rem; color: #00ff87;">
            ⚡ <b>AI Insight:</b> Risiko terkelola dengan baik. Selalu pasang batasan risiko (*Trailing Stop-Loss*) sesuai profil manajemen risiko Anda.
        </div>
    </div>
    """, unsafe_allow_html=True)
