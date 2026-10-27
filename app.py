import json
import requests
import pandas as pd
import streamlit as st
import yfinance as yf
from groq import Groq

# 1. Konfigurasi Tampilan Halaman Streamlit
st.set_page_config(
    page_title="JII70 Groq AI Syariah Screener",
    page_icon="🕌",
    layout="wide",
)

st.title("🕌 JII70 Groq AI Syariah Screener + Telegram Alert")
st.subheader("Screener saham syariah gratis berbasis Groq Cloud AI")

# 2. Sidebar Konfigurasi API Groq & Telegram
st.sidebar.title("🔐 Konfigurasi Kredensial")
groq_api_key = st.sidebar.text_input("1. Groq API Key (gsk_...):", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("📢 Integrasi Telegram")
tele_token = st.sidebar.text_input("2. Telegram Bot Token:", type="password")
tele_chat_id = st.sidebar.text_input("3. Telegram Chat ID:")


# Fungsi mengirim alert ke Telegram
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
    except:
      pass


# 3. DAFTAR LENGKAP 70 KODE SAHAM SYARIAH JII70 YANG BENAR
JII70_TICKERS = [
    "AADI.JK", "ACES.JK", "ADMR.JK", "ADRO.JK", "AKRA.JK", "ANTM.JK", "ARCI.JK", "AVIA.JK", "BKSL.JK", "BRIS.JK",
    "BRMS.JK", "BSDE.JK", "BTPS.JK", "BUMI.JK", "CMRY.JK", "CPIN.JK", "CTRA.JK", "DEWA.JK", "DKFT.JK", "DSNG.JK",
    "ELSA.JK", "ENRG.JK", "ERAA.JK", "ESSA.JK", "EXCL.JK", "HEAL.JK", "HRTA.JK", "HRUM.JK", "ICBP.JK", "IMPC.JK",
    "INDF.JK", "INDY.JK", "INKP.JK", "INTP.JK", "ISAT.JK", "ITMG.JK", "JPFA.JK", "JSMR.JK", "KIJA.JK", "KLBF.JK",
    "KPIG.JK", "LSIP.JK", "MAPA.JK", "MAPI.JK", "MARK.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "MIKA.JK", "MTEL.JK",
    "MYOR.JK", "PGAS.JK", "PTBA.JK", "RAJA.JK", "RATU.JK", "SIDO.JK", "SMGR.JK", "SMRA.JK", "SRTG.JK", "SSIA.JK",
    "TAPG.JK", "TCPI.JK", "TINS.JK", "TKIM.JK", "TLKM.JK", "TOBA.JK", "TPIA.JK", "UNTR.JK", "UNVR.JK", "WIFI.JK"
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
      ihsg_pct = ((ihsg_close - ihsg_hist["Close"].iloc[-2]) / ihsg_hist["Close"].iloc[-2]) * 100
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
        v_change = ((today["Volume"] - yesterday["Volume"]) / yesterday["Volume"]) * 100

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


ihsg_val, ihsg_chg, df_jii70 = fetch_market_data()

st.metric(
    label="📊 Indeks Harga Saham Gabungan (IHSG)",
    value=f"{ihsg_val:,.2f}",
    delta=f"{ihsg_chg:.2f}%",
)

st.write(f"### 📋 Monitor Pasar Saham Syariah JII70 Terbaru ({len(df_jii70)} Emiten Aktif)")
st.dataframe(df_jii70, use_container_width=True, hide_index=True)
st.write("---")

st.write("### 🤖 Jalankan Perintah Screening AI Groq")
user_query = st.text_input(
    "Masukkan Kriteria:",
    value="Cari saham yang harganya diatas MA5 and RSI dibawah 60",
)

if st.button("Jalankan Screener & Kirim Alert"):
  if not groq_api_key:
    st.error("Silakan isi Groq API Key terlebih dahulu di sidebar.")
  else:
    client = Groq(api_key=groq_api_key)

    prompt_query = f"""
        Ubah instruksi ini menjadi parameter query pandas berdasarkan kolom: Ticker, Harga, Perubahan_%, Volume, Vol_Change_%, MA5, MA20, RSI.
        User request: "{user_query}"
        Keluarkan HANYA string query. Jangan berikan penutup markdown atau teks pembuka. Contoh output: RSI < 40 and Perubahan_% > 1
        """

    try:
      response_q = client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[{"role": "user", "content": prompt_query}],
          temperature=0.0,
      )
      q_string = response_q.choices.message.content.strip()

      if q_string.startswith("```"):
        q_string = q_string.replace("```python", "").replace("```", "").strip()

      df_filtered = df_jii70.query(q_string)

      if df_filtered.empty:
        st.warning("Tidak ada saham syariah yang cocok dengan kriteria tersebut.")
      else:
        st.success(f"Ditemukan {len(df_filtered)} saham potensial!")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

        prompt_analysis = f"""
            Anda adalah analis ekuitas senior bersertifikasi syariah (AASI).
            Berikut data saham JII70 hasil screening:
            {df_filtered.to_string()}
            
            Berikan rekomendasi dengan format terstruktur kaku JSON untuk mempermudah sistem.
            Keluarkan HANYA format JSON array valid seperti contoh di bawah, tanpa teks tambahan/markdown block.
            
            [
              {{"ticker": "BRIS", "rekomendasi": "BELI", "alasan": "Harga diatas MA5 dan RSI oversold 35", "risk": "Cutloss jika tembus support 2500"}},
              {{"ticker": "TLKM", "rekomendasi": "HOLD", "alasan": "Konsolidasi di MA20", "risk": "Pantau volume beli"}}
            ]
            """

        with st.spinner("Groq AI sedang menyusun keputusan trading..."):
          response_a = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              messages=[{"role": "user", "content": prompt_analysis}],
              temperature=0.1,
          )

          raw_json = response_a.choices.message.content.strip()
          if raw_json.startswith("```"):
            raw_json = raw_json.replace("```json", "").replace("```", "").strip()

          rekomendasi_list = json.loads(raw_json)

          st.write("### ⚡ Hasil Analisis & Eksekusi Alert:")

          for item in rekomendasi_list:
            color = "💚" if item["rekomendasi"] == "BELI" else ("❤️" if item["rekomendasi"] == "JUAL" else "💛")

            st.markdown(f"### {color} {item['ticker']} — **{item['rekomendasi']}**")
            st.markdown(f"- **Alasan**: {item['alasan']}")
            st.markdown(f"- **Manajemen Risiko**: {item['risk']}")
            st.write("---")

            if item["rekomendasi"] == "BELI":
              msg_telegram = (
                  f"🚨 *JII70 GROQ BUY ALERT* 🚨\n\n"
                  f"🔹 *Saham:* #{item['ticker']}\n"
                  f"🟢 *Rekomendasi:* BELI (BUY)\n"
                  f"📈 *Alasan:* {item['alasan']}\n"
                  f"🛡️ *Manajemen Risiko:* {item['risk']}\n\n"
                  f"⚡ _Sent from Groq AI Screener Dashboard_"
              )
              send_telegram_alert(msg_telegram)
              st.toast(f"🔔 Sinyal BELI {item['ticker']} terkirim ke Telegram!")

    except Exception as e:
      st.error(f"Terjadi kesalahan pemrosesan: {e}")
