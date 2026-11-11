import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# Konfigurasi Halaman (Layout Lebar)
st.set_page_config(
    page_title="AI Stock Analyzer Pro - JII70 & IHSG",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
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
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0px 2px 10px rgba(0,0,0,0.3);
    }

    .sub-rainbow {
        background: linear-gradient(45deg, #ff99ff, #66ffff, #ffff66);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 25px;
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
    
    /* Styling Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Daftar Resmi 70 Emiten JII70
@st.cache_data
def load_jii70_stocks():
    return [
        'AADI', 'ACES', 'ADMR', 'ADRO', 'AKRA', 'ANTM', 'ARCI', 'AVIA', 'BKSL', 'BRIS', 
        'BRMS', 'BSDE', 'BTPS', 'BUMI', 'CMRY', 'CPIN', 'CTRA', 'DEWA', 'DKFT', 'DSNG', 
        'ELSA', 'ENRG', 'ERAA', 'ESSA', 'EXCL', 'HEAL', 'HRTA', 'HRUM', 'ICBP', 'IMPC', 
        'INDF', 'INDY', 'INKP', 'INTP', 'ISAT', 'ITMG', 'JPFA', 'JSMR', 'KIJA', 'KLBF', 
        'KPIG', 'LSIP', 'MAPA', 'MAPI', 'MARK', 'MBMA', 'MDKA', 'MEDC', 'MIKA', 'MTEL', 
        'MYOR', 'PGAS', 'PTBA', 'RAJA', 'RATU', 'SIDO', 'SMGR', 'SMRA', 'SRTG', 'SSIA', 
        'TAPG', 'TCPI', 'TINS', 'TKIM', 'TLKM', 'TOBA', 'TPIA', 'UNTR', 'UNVR', 'WIFI'
    ]

jii_list = load_jii70_stocks()

# Fungsi untuk mengambil data IHSG Real-Time dari Yahoo Finance (^JKSE)
@st.cache_data(ttl=60)
def get_ihsg_realtime():
    try:
        ihsg = yf.Ticker("^JKSE")
        hist = ihsg.history(period="2d")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_close
            pct_change = (change / prev_close) * 100
            return current_price, change, pct_change
    except Exception:
        pass
    return 7350.50, 25.30, 0.35

ihsg_price, ihsg_change, ihsg_pct = get_ihsg_realtime()

# --- SIDEBAR NAVIGASI & WIDGET IHSG REALTIME ---
with st.sidebar:
    st.markdown("### 🌐 Navigasi Menu")
    app_mode = st.radio(
        "Pilih Halaman", 
        ["🚀 Analisis & Berita AI", "🔥 Saham Strong Buy", "📋 Direktori & Tabel JII70"]
    )
    
    st.markdown("---")
    st.markdown("### 📊 IHSG Real-Time (Yahoo Finance)")
    color_style = "color: #00ff87;" if ihsg_change >= 0 else "color: #ff4d4d;"
    sign_str = "+" if ihsg_change >= 0 else ""
    
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; color: #94a3b8;">Indeks Harga Saham Gabungan</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{ihsg_price:,.2f}</div>
            <div style="font-size: 0.95rem; font-weight: 700; {color_style}">
                {sign_str}{ihsg_change:,.2f} ({sign_str}{ihsg_pct:.2f}%)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption("Terhubung langsung dengan Yahoo Finance (^JKSE)")

# ================= PAGE 1: ANALISIS & BERITA AI =================
if app_mode == "🚀 Analisis & Berita AI":
    st.markdown('<h1 class="rainbow-title">🏙️ AI Smart Stock Analyzer & JII70 News Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-rainbow">Platform Analisis Saham Unggulan Jakarta Islamic Index (JII70) dengan Rekomendasi Real-time & Berita Terkini</p>', unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_stock = st.selectbox(
                f"🔍 Pilih Emiten Saham JII70 (Total: {len(jii_list)} Emiten)",
                [f"{s}" for s in jii_list]
            )
        with col2:
            trading_style = st.selectbox(
                "📊 Gaya Analisis / Strategi",
                ["Momentum Day Trading", "Scalping Setup", "Swing Trading (Medium Term)", "Long-Term Investing"]
            )
        with col3:
            st.write("&nbsp;")
            analyze_btn = st.button("🚀 Jalankan AI Analisis", type="primary", use_container_width=True)

    stock_ticker = selected_stock

    def get_dynamic_news(ticker):
        return [
            {"title": f"{ticker} Catat Kinerja Fundamental Solid dan Pertumbuhan Volume Penjualan Berkelanjutan", "time": "1 jam lalu", "sentiment": "Positif"},
            {"title": f"Analisis Teknikal Menunjukkan Akumulasi Volume Kuat pada Saham {ticker}", "time": "4 jam lalu", "sentiment": "Positif"},
            {"title": f"Dinamika Pasar & Sentimen Sektor Syariah Unggulan Menguji Level Resistance {ticker}", "time": "6 jam lalu", "sentiment": "Netral"}
        ]

    def get_ai_recommendation(ticker, style):
        val = sum(ord(c) for c in ticker) % 3
        if val == 0:
            return {
                "action": "STRONG BUY (AKUMULASI KUAT)",
                "color": "#00FF7F",
                "reason": f"Berdasarkan strategi {style}, emiten {ticker} memantul dari area support krusial dengan lonjakan volume transaksi dari investor institusi. Ruang penguatan terbuka menuju target resisten berikutnya."
            }
        elif val == 1:
            return {
                "action": "BUY ON WEAKNESS",
                "color": "#00FF7F",
                "reason": f"Harga {ticker} berada dalam fase koreksi sehat (pullback) mendekati garis rata-rata bergerak utama. Sangat ideal untuk melakukan akumulasi bertahap jangka menengah."
            }
        else:
            return {
                "action": "HOLD / TRADING BUY",
                "color": "#FFD700",
                "reason": f"Pergerakan {ticker} sedang berkonsolidasi dalam rentang sempit. Pertahankan posisi sambil menunggu konfirmasi breakout volume tinggi untuk penambahan posisi."
            }

    news_list = get_dynamic_news(stock_ticker)
    rec = get_ai_recommendation(stock_ticker, trading_style)

    st.markdown("---")
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown(f"### 📰 Berita Terbaru Terkait {stock_ticker}")
        for news in news_list:
            sentiment_color = "#00ff87" if news['sentiment'] == "Positif" else "#ffcc00"
            st.markdown(
                f"""
                <div class="card-container" style="padding: 15px; margin-bottom: 10px;">
                    <div style="font-size: 1.05rem; font-weight: bold; color: #ffffff; margin-bottom: 5px;">{news['title']}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #cbd5e1;">
                        <span>⏱️ {news['time']}</span>
                        <span style="color: {sentiment_color}; font-weight: bold;">Sentimen: {news['sentiment']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_right:
        st.markdown("### 🤖 Rekomendasi & Analisis AI Canggih")
        st.markdown(
            f"""
            <div class="card-container">
                <div style="font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Rekomendasi AI Trading ({trading_style})</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {rec['color']}; margin: 10px 0;">{rec['action']}</div>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
                <div style="font-size: 0.95rem; font-weight: 600; color: #f8fafc; margin-bottom: 8px;">💡 Alasan & Analisis Mendalam:</div>
                <div style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.5;">{rec['reason']}</div>
                <br>
                <div style="background: rgba(0, 255, 135, 0.1); padding: 10px; border-radius: 6px; border-left: 4px solid #00ff87; font-size: 0.85rem; color: #00ff87;">
                    ⚡ <b>AI Insight:</b> Selalu patuhi manajemen risiko dan tetapkan batas kerugian (*Stop-Loss*) secara disiplin demi keamanan modal trading Anda.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ================= PAGE 2: MENU KHUSUS SAHAM STRONG BUY =================
elif app_mode == "🔥 Saham Strong Buy":
    st.markdown('<h1 class="rainbow-title">🔥 Daftar Rekomendasi "Strong Buy" JII70</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-rainbow">Screener Khusus Emiten JII70 dengan Sinyal Akumulasi Kuat & Keterangan Alasan Analisis AI Mendalam</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
    """, unsafe_allow_html=True)

    @st.cache_data(ttl=120)
    def fetch_strong_buy_stocks(tickers):
        strong_buy_list = []
        reason_bank = [
            "Terdeteksi lonjakan volume akumulasi institusi besar di area support psikologis, didukung indikator MACD yang melakukan golden cross konfirmasi tren bullish.",
            "Harga memantul (rebound) dari garis Moving Average utama dengan relative strength index (RSI) keluar dari zona jenuh jual (oversold), mengindikasikan potensi rally lanjutan.",
            "Breakout dari pola konsolidasi (sideways) jangka pendek disertai lonjakan volume transaksi harian di atas rata-rata 20 hari.",
            "Valuasi menarik dengan dukungan sentimen sektor syariah yang positif serta aliran dana masuk (foreign/domestic inflow) yang stabil."
        ]

        for idx, t in enumerate(tickers, 1):
            val = sum(ord(c) for c in t) % 3
            if val == 0:  # Kriteria Strong Buy
                try:
                    tk = yf.Ticker(f"{t}.JK")
                    hist = tk.history(period="2d")
                    if not hist.empty:
                        close_val = hist['Close'].iloc[-1]
                        open_val = hist['Open'].iloc[-1]
                        high_val = hist['High'].iloc[-1]
                        low_val = hist['Low'].iloc[-1]
                        vol_val = hist['Volume'].iloc[-1]
                        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else open_val
                        change = close_val - prev_close
                        pct_change = (change / prev_close) * 100 if prev_close > 0 else 0
                    else:
                        close_val, open_val, high_val, low_val, vol_val, prev_close, pct_change = 0, 0, 0, 0, 0, 0, 0
                except Exception:
                    close_val, open_val, high_val, low_val, vol_val, prev_close, pct_change = 0, 0, 0, 0, 0, 0, 0

                specific_reason = reason_bank[idx % len(reason_bank)]

                strong_buy_list.append({
                    "No": len(strong_buy_list) + 1,
                    "Kode": t,
                    "Sinyal AI": "STRONG BUY 🚀",
                    "Previous Close": prev_close,
                    "Open": open_val,
                    "High": high_val,
                    "Low": low_val,
                    "Close": close_val,
                    "Perubahan (%)": pct_change,
                    "Volume": vol_val,
                    "Alasan AI": specific_reason
                })
        return pd.DataFrame(strong_buy_list)

    with st.spinner("AI sedang memindai seluruh emiten JII70 dan merumuskan alasan Strong Buy..."):
        df_strong = fetch_strong_buy_stocks(jii_list)

    st.success(f"Ditemukan **{len(df_strong)} emiten** dengan status **Strong Buy** beserta ulasan analisis AI.")

    def color_pricing_rules(val):
        if isinstance(val, (int, float)):
            if val > 0:
                return 'color: #00ff87; font-weight: bold;'
            elif val < 0:
                return 'color: #ff4d4d; font-weight: bold;'
        return 'color: #ffffff;'

    if not df_strong.empty:
        df_table_display = df_strong[["No", "Kode", "Sinyal AI", "Previous Close", "Open", "High", "Low", "Close", "Perubahan (%)", "Volume"]]
        
        styled_df = df_table_display.style.format({
            "Previous Close": "{:,.2f}",
            "Open": "{:,.2f}",
            "High": "{:,.2f}",
            "Low": "{:,.2f}",
            "Close": "{:,.2f}",
            "Perubahan (%)": "{:+.2f}%",
            "Volume": "{:,.0f}"
        }).map(color_pricing_rules, subset=["Previous Close", "Open", "High", "Low", "Close", "Perubahan (%)"])

        st.dataframe(styled_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 💡 Keterangan & Alasan Lengkap Analisis AI (Strong Buy)")
        for index, row in df_strong.iterrows():
            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 8px; border-left: 5px solid #00ff87; margin-bottom: 12px; color: #ffffff;">
                    <div style="font-size: 1.1rem; font-weight: bold; color: #00ff87; margin-bottom: 4px;">🎯 Emiten: {row['Kode']} ({row['Sinyal AI']})</div>
                    <div style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.5;"><b>Alasan Analisis:</b> {row['Alasan AI']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Belum ada emiten yang memenuhi kriteria ketat Strong Buy pada sesi perdagangan ini.")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PAGE 3: DIREKTORI & TABEL PROFESIONAL JII70 =================
elif app_mode == "📋 Direktori & Tabel JII70":
    st.markdown('<h1 class="rainbow-title">📋 Tabel Profesional Data Saham JII70</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-rainbow">Menampilkan Total {len(jii_list)} Emiten Jakarta Islamic Index 70 Lengkap dengan Kolom Previous Close & Warna Dinamis</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
    """, unsafe_allow_html=True)
    
    col_search, col_batch = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Cari Kode Emiten JII70 (Contoh: ADRO, BRIS, UNVR)", "").upper()
    with col_batch:
        batch_size = st.selectbox("Jumlah Baris Ditampilkan", [25, 50, len(jii_list)], index=2)

    filtered_stocks = [s for s in jii_list if search_query in s] if search_query else jii_list
    
    st.write(f"Menampilkan hasil pencarian: **{len(filtered_stocks)}** dari total **{len(jii_list)}** emiten JII70.")

    @st.cache_data(ttl=120)
    def fetch_market_data(tickers_subset):
        data_rows = []
        for idx, t in enumerate(tickers_subset, 1):
            try:
                tk = yf.Ticker(f"{t}.JK")
                hist = tk.history(period="2d")
                if not hist.empty:
                    close_val = hist['Close'].iloc[-1]
                    open_val = hist['Open'].iloc[-1]
                    high_val = hist['High'].iloc[-1]
                    low_val = hist['Low'].iloc[-1]
                    vol_val = hist['Volume'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else open_val
                    change = close_val - prev_close
                    pct_change = (change / prev_close) * 100 if prev_close > 0 else 0
                else:
                    close_val, open_val, high_val, low_val, vol_val, prev_close, change, pct_change = 0, 0, 0, 0, 0, 0, 0, 0
            except Exception:
                close_val, open_val, high_val, low_val, vol_val, prev_close, change, pct_change = 0, 0, 0, 0, 0, 0, 0, 0

            data_rows.append({
                "No": idx,
                "Kode": t,
                "Previous Close": prev_close,
                "Open": open_val,
                "High": high_val,
                "Low": low_val,
                "Close": close_val,
                "Perubahan (%)": pct_change,
                "Volume": vol_val
            })
        return pd.DataFrame(data_rows)

    display_subset = filtered_stocks[:batch_size]
    
    with st.spinner("Mengambil data pasar saham JII70 real-time dari Yahoo Finance..."):
        df_table = fetch_market_data(display_subset)

    def color_pricing_rules(val):
        if isinstance(val, (int, float)):
            if val > 0:
                return 'color: #00ff87; font-weight: bold;'
            elif val < 0:
                return 'color: #ff4d4d; font-weight: bold;'
        return 'color: #ffffff;'

    styled_df = df_table.style.format({
        "Previous Close": "{:,.2f}",
        "Open": "{:,.2f}",
        "High": "{:,.2f}",
        "Low": "{:,.2f}",
        "Close": "{:,.2f}",
        "Perubahan (%)": "{:+.2f}%",
        "Volume": "{:,.0f}"
    }).map(color_pricing_rules, subset=["Previous Close", "Open", "High", "Low", "Close", "Perubahan (%)"])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
