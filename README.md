# Dashboard Analisis Kualitas Udara Dongsi

## Deskripsi
Dashboard interaktif untuk menganalisis konsentrasi PM2.5 di Stasiun Dongsi, Beijing, selama periode Maret 2013 hingga Februari 2017.

Dashboard dibuat menggunakan Streamlit dan Plotly untuk membantu menjawab dua pertanyaan bisnis:
1. Bagaimana tren rata-rata konsentrasi PM2.5 bulanan dan bulan mana yang perlu diprioritaskan?
2. Bagaimana hubungan kecepatan angin (WSPM) dan curah hujan (RAIN) dengan PM2.5?

## Struktur Folder
```text
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── data_1.csv
│   └── data_2.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Persyaratan
- Python
- Streamlit
- Pandas
- Plotly

## Instalasi
1. Clone atau download repository.
2. Buka terminal pada folder proyek.
3. Instal library:

   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Dashboard
Jalankan perintah:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard dapat diakses melalui:

```text
http://localhost:8501
```

## Fitur Dashboard
- Filter data berdasarkan tahun.
- Ringkasan rata-rata PM2.5, WSPM, dan RAIN.
- Visualisasi tren PM2.5 bulanan.
- Perbandingan rata-rata PM2.5 berdasarkan bulan.
- Scatter plot hubungan WSPM dan RAIN terhadap PM2.5.
- Heatmap korelasi Spearman.
- Kesimpulan dan rekomendasi analisis.