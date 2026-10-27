import requests
import openai
import pandas as pd
import streamlit as st
import yfinance as yf

# 1. Konfigurasi Tampilan Halaman Streamlit
st.set_page_config(
    page_title="JII70 AI Screener + Telegram Alert",
    page_icon="🕌",
    layout="wide",
)

st.title("🕌 JII70 AI Syariah Screener + Telegram Alert")
st.subheader("Screener saham syariah otomatis dengan notifikasi real-time")

# 2. Sidebar Konfigurasi API & Telegram
st.sidebar.title("🔐 Konfigurasi Kredensial")
api_key = st.sidebar.text_input("1. OpenAI API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("📢 Integrasi Telegram")
tele_token = st.sidebar.text_input("2. Telegram Bot Token:", type="password")
tele_chat_id = st.sidebar.text_input("3. Telegram Chat ID:"


# Fungsi untuk mengirim pesan ke Telegram
def send_telegram_alert(message):
  if tele_token and tele_chat_id:
    url = f"https://telegram.org{tele_token}/sendMessage"
    payload = {
        "chat_id": tele_chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
      requests.post(url, json=payload)
    except Exception as e:
      st.sidebar.error(f"Gagal mengirim Telegram: {e}")


# 3. Data Konstituen JII70 & Fungsi Indikator
JII70_TICKERS = [
    "ADRO.JK",
    "AKRA.JK",
    "ANTM.JK",
    "ASII.JK",
    "BRIS.JK",
    "BRPT.JK",
    "CPIN.JK",
    "EXCL.JK",
    "INDF.JK",
    "ITMG.JK",
    "KLBF.JK",
    "MEDC.JK",
    "PGAS.JK",
    "PTBA.JK",
    "SMGR.JK",
    "TLKM.JK",
    "UNVR.JK",
]


def calculate_rsi(series, period=14):
  delta = series.diff()
  gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
  loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
  rs = gain / loss
  return 100 - (100 / (1 + rs))


@st.cache_data(ttl=60)
def fetch_market_data():
  ihsg_close, ihsg_pct = 0.0, 0.0
  try:
    ihsg = yf.Ticker("^JKSE")
    ihsg_hist = ihsg.history(period="2d")
    if len(ihsg_hist) >= 2:
      ihsg_close = ihsg_hist["Close"].iloc[-1]
      ihsg_pct = (
          (ihsg_close - ihsg_hist["Close"].iloc[-2])
          / ihsg_hist["Close"].iloc[-2]
      ) * 100
  except:
    pass

  rows = []
  for t in JII70_TICKERS:
    try:
      stock = yf.Ticker(t)
      hist = stock.history(period="3mo")
      if len(hist) >= 20:
        hist["MA5"] = hist["Close"].rolling(window=5).mean()
        hist["MA20"] = hist["Close"].rolling(window=20).mean()
        hist["RSI"] = calculate_rsi(hist["Close"], period=14)

        today = hist.iloc[-1]
        yesterday = hist.iloc[-2]

        change = ((today["Close"] - yesterday["Close"]) / yesterday["Close"]) * 100
        v_change = (
            (today["Volume"] - yesterday["Volume"]) / yesterday["Volume"]
        ) * 100

        rows.append({
            "Ticker": t.replace(".JK", ""),
            "Harga": round(today["Close"], 0),
            "Perubahan_%": round(change, 2),
            "Volume": int(today["Volume"]),
            "Vol_Change_%": round(v_change, 2),
            "MA5": round(today["MA5"], 0),
            "MA20": round(today["MA20"], 0),
            "RSI": round(today["RSI"], 2) if not pd.isna(today["RSI"]) else 50.0,
        })
    except:
      continue
  return ihsg_close, ihsg_pct, pd.DataFrame(rows)


# Load Data Pasar
ihsg_val, ihsg_chg, df_jii70 = fetch_market_data()

# Tampilan Ringkasan IHSG Realtime
st.metric(
    label="📊 Indeks Harga Saham Gabungan (IHSG)",
    value=f"{ihsg_val:,.2f}",
    delta=f"{ihsg_chg:.2f}%",
)

st.write("### 📋 Monitor Pasar Saham Syariah JII70 Terbaru")
st.dataframe(df_jii70, use_container_width=True, hide_index=True)
st.write("---")

# 4. Input Kriteria AI Screener
st.write("### 🤖 Jalankan Perintah Screening AI")
user_query = st.text_input(
    "Masukkan Kriteria:",
    value="Cari saham yang harganya diatas MA5 dan RSI dibawah 60",
)

if st.button("Jalankan Screener & Kirim Alert"):
  if not api_key:
    st.error("Silakan isi OpenAI API Key terlebih dahulu.")
  else:
    client = openai.OpenAI(api_key=api_key)

    # Tahap 1: Mengubah teks menjadi kode query dataframe
    prompt_query = f"""
        Ubah instruksi ini menjadi parameter query pandas berdasarkan kolom: Ticker, Harga, Perubahan_%, Volume, Vol_Change_%, MA5, MA20, RSI.
        User request: "{user_query}"
        Keluarkan HANYA string query. Contoh output: RSI < 40 and Perubahan_% > 1
        """

    try:
      response_q = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[{"role": "user", "content": prompt_query}],
          temperature=0.0,
      )
      q_string = response_q.choices.message.content.strip()

      df_filtered = df_jii70.query(q_string)

      if df_filtered.empty:
        st.warning("Tidak ada saham syariah yang cocok dengan kriteria tersebut.")
      else:
        st.success(f"Ditemukan {len(df_filtered)} saham potensial!")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

        # Tahap 2: Minta AI memberikan Rekomendasi & Analisis Beli/Jual
        prompt_analysis = f"""
            Anda adalah analis ekuitas senior bersertifikasi syariah (AASI).
            Berikut data saham JII70 hasil screening:
            {df_filtered.to_string()}
            
            Berikan rekomendasi dengan format terstruktur kaku JSON untuk mempermudah sistem.
            Keluarkan HANYA format JSON valid seperti contoh di bawah, tanpa teks tambahan/markdown block.
            
            Contoh Format Output:
            [
              {{"ticker": "BRIS", "rekomendasi": "BELI", "alasan": "Harga diatas MA5 dan RSI oversold 35", "risk": "Cutloss jika tembus support 2500"}},
              {{"ticker": "TLKM", "rekomendasi": "HOLD", "alasan": "Konsolidasi di MA20", "risk": "Pantau volume beli"}}
            ]
            """

        with st.spinner("AI sedang menyusun keputusan trading..."):
          response_a = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=[{"role": "user", "content": prompt_analysis}],
              temperature=0.1,
          )

          import json

          raw_json = response_a.choices.message.content.strip()
          # Membersihkan jika AI membungkus dengan ```json ... ```
          if raw_json.startswith("```"):
            raw_json = (
                raw_json.replace("```json", "").replace("```", "").strip()
            )

          rekomendasi_list = json.loads(raw_json)

          st.write("### ⚡ Hasil Analisis & Eksekusi Alert:")

          # Menampilkan di Dashboard Web & Kirim ke Telegram jika Dapat Sinyal "BELI"
          for item in rekomendasi_list:
            # Mengatur warna berdasarkan jenis rekomendasi
            color = (
                "💚"
                if item["rekomendasi"] == "BELI"
                else ("❤️" if item["rekomendasi"] == "JUAL" else "💛")
            )

            st.markdown(f"### {color} {item['ticker']} — **{item['rekomendasi']}**")
            st.markdown(f"- **Alasan**: {item['alasan']}")
            st.markdown(f"- **Manajemen Risiko**: {item['risk']}")
            st.write("---")

            # Kirim Notifikasi Otomatis ke Telegram khusus sinyal BELI (BUY Alert)
            if item["rekomendasi"] == "BELI":
              msg_telegram = (
                  f"🚨 *JII70 AI BUY SIGNAL ALERT* 🚨\n\n"
                  f"🔹 *Saham:* #{item['ticker']}\n"
                  f"🟢 *Rekomendasi:* BELI (BUY)\n"
                  f"📈 *Alasan:* {item['alasan']}\n"
                  f"🛡️ *Manajemen Risiko:* {item['risk']}\n\n"
                  f"⚡ _Dikirim otomatis oleh AI Screener Dashboard_"
              )
              send_telegram_alert(msg_telegram)
              st.toast(
                  f"🔔 Alert sinyal BELI untuk {item['ticker']} telah dikirim ke"
                  " Telegram!"
              )

    except Exception as e:
      st.error(f"Terjadi kesalahan pemrosesan: {e}")
