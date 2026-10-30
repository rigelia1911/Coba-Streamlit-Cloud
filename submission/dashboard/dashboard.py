
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. KONFIGURASI DASHBOARD
# ==========================================

st.set_page_config(
    page_title="Analisis Kualitas Udara Dongsi",
    page_icon="🌫️",
    layout="wide"
)

st.title("🌫️ Dashboard Kualitas Udara")
st.subheader("Analisis PM2.5 di Stasiun Dongsi, Beijing")
st.caption("Periode pengamatan: Maret 2013 – Februari 2017")

# ==========================================
# 2. MEMUAT DATA
# ==========================================

DATA_PATH = Path(__file__).parent / "main_data.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    # Membuat kolom tanggal
    data["date"] = pd.to_datetime(
        data[["year", "month", "day"]]
    )

    # Memastikan kolom numerik
    kolom_numerik = ["PM2.5", "WSPM", "RAIN"]

    for kolom in kolom_numerik:
        data[kolom] = pd.to_numeric(
            data[kolom], errors="coerce"
        )

    return data

try:
    df = load_data()
except FileNotFoundError:
    st.error("File main_data.csv tidak ditemukan.")
    st.stop()
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca data: {e}")
    st.stop()

# ==========================================
# 3. FILTER DATA
# ==========================================

st.sidebar.header("Filter Dashboard")

daftar_tahun = sorted(df["year"].dropna().unique())

tahun_dipilih = st.sidebar.multiselect(
    "Pilih Tahun",
    options=daftar_tahun,
    default=daftar_tahun
)

if not tahun_dipilih:
    st.warning("Silakan pilih minimal satu tahun.")
    st.stop()

data_filter = df[df["year"].isin(tahun_dipilih)].copy()

if data_filter.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

# ==========================================
# 4. RINGKASAN DATA
# ==========================================

st.header("Ringkasan Kualitas Udara")

col1, col2, col3 = st.columns(3)

rata_pm25 = data_filter["PM2.5"].mean()
rata_wspm = data_filter["WSPM"].mean()
rata_rain = data_filter["RAIN"].mean()

col1.metric(
    "Rata-rata PM2.5",
    f"{rata_pm25:.2f} µg/m³"
)

col2.metric(
    "Rata-rata Kecepatan Angin",
    f"{rata_wspm:.2f}"
)

col3.metric(
    "Rata-rata Curah Hujan",
    f"{rata_rain:.2f}"
)

st.caption(
    f"Jumlah observasi: {len(data_filter):,} baris"
)

st.divider()

# ==========================================
# 5. PERTANYAAN BISNIS 1
# ==========================================

st.header("1. Tren Konsentrasi PM2.5")

st.write(
    "Bagaimana perubahan rata-rata PM2.5 selama periode "
    "pengamatan dan bulan mana yang perlu diprioritaskan?"
)

# Tren rata-rata PM2.5 per bulan secara kronologis
tren_bulanan = (
    data_filter
    .groupby(["year", "month"])["PM2.5"]
    .mean()
    .reset_index()
)

tren_bulanan["tanggal"] = pd.to_datetime(
    tren_bulanan[["year", "month"]].assign(day=1)
)

fig_tren = px.line(
    tren_bulanan,
    x="tanggal",
    y="PM2.5",
    markers=True,
    title="Tren Rata-rata PM2.5 per Bulan",
    labels={
        "tanggal": "Periode",
        "PM2.5": "Rata-rata PM2.5 (µg/m³)"
    }
)

st.plotly_chart(fig_tren, use_container_width=True)

# Rata-rata berdasarkan bulan kalender
rata_bulanan = (
    data_filter
    .groupby("month")["PM2.5"]
    .mean()
    .reset_index()
)

nama_bulan = {
    1: "Januari", 2: "Februari",
    3: "Maret", 4: "April",
    5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober",
    11: "November", 12: "Desember"
}

rata_bulanan["Nama Bulan"] = (
    rata_bulanan["month"].map(nama_bulan)
)

fig_bulan = px.bar(
    rata_bulanan,
    x="Nama Bulan",
    y="PM2.5",
    title="Rata-rata PM2.5 Berdasarkan Bulan",
    labels={
        "PM2.5": "Rata-rata PM2.5 (µg/m³)",
        "Nama Bulan": "Bulan"
    }
)

st.plotly_chart(fig_bulan, use_container_width=True)

# Bulan prioritas berdasarkan rata-rata tertinggi
if not rata_bulanan.empty:
    bulan_tertinggi = rata_bulanan.loc[
        rata_bulanan["PM2.5"].idxmax()
    ]

    st.info(
        f"Bulan dengan rata-rata PM2.5 tertinggi pada "
        f"filter yang dipilih adalah "
        f"{bulan_tertinggi['Nama Bulan']} "
        f"({bulan_tertinggi['PM2.5']:.2f} µg/m³)."
    )

st.divider()

# ==========================================
# 6. PERTANYAAN BISNIS 2
# ==========================================

st.header("2. Hubungan Faktor Cuaca dengan PM2.5")

st.write(
    "Bagaimana hubungan kecepatan angin dan curah hujan "
    "dengan konsentrasi PM2.5?"
)

# Scatter plot WSPM
fig_wspm = px.scatter(
    data_filter,
    x="WSPM",
    y="PM2.5",
    opacity=0.4,
    title="Hubungan Kecepatan Angin dengan PM2.5",
    labels={
        "WSPM": "Kecepatan Angin",
        "PM2.5": "PM2.5 (µg/m³)"
    }
)

st.plotly_chart(fig_wspm, use_container_width=True)

# Scatter plot RAIN
fig_rain = px.scatter(
    data_filter,
    x="RAIN",
    y="PM2.5",
    opacity=0.4,
    title="Hubungan Curah Hujan dengan PM2.5",
    labels={
        "RAIN": "Curah Hujan",
        "PM2.5": "PM2.5 (µg/m³)"
    }
)

st.plotly_chart(fig_rain, use_container_width=True)

# Korelasi Spearman berdasarkan filter
korelasi = data_filter[
    ["PM2.5", "WSPM", "RAIN"]
].corr(method="spearman")

st.subheader("Korelasi Spearman")

fig_korelasi = px.imshow(
    korelasi,
    text_auto=".3f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    title="Heatmap Korelasi Spearman"
)

st.plotly_chart(fig_korelasi, use_container_width=True)

st.write(
    "Nilai korelasi negatif menunjukkan kecenderungan "
    "hubungan berlawanan arah, sedangkan nilai yang "
    "mendekati nol menunjukkan hubungan monotonik yang lemah."
)

st.divider()

# ==========================================
# 7. KESIMPULAN DAN REKOMENDASI
# ==========================================

st.header("3. Kesimpulan dan Rekomendasi")

st.markdown("""
**Kesimpulan:**

- Konsentrasi PM2.5 menunjukkan variasi berdasarkan waktu
  pengamatan. Bulan dengan rata-rata tertinggi dapat
  dijadikan salah satu periode prioritas pemantauan.
- Kecepatan angin memiliki hubungan negatif yang lebih kuat
  dengan PM2.5 dibandingkan curah hujan pada hasil analisis
  keseluruhan dataset.

**Rekomendasi:**

- Memprioritaskan pemantauan pada bulan dengan rata-rata
  PM2.5 tinggi.
- Memperhatikan kondisi kecepatan angin ketika mengevaluasi
  potensi peningkatan PM2.5.
- Melakukan pengumpulan data secara konsisten agar pola
  kualitas udara dapat dievaluasi dari waktu ke waktu.
""")

# ==========================================
# 8. MENAMPILKAN DATA
# ==========================================

with st.expander("Lihat Data yang Digunakan"):
    st.dataframe(data_filter, use_container_width=True)
