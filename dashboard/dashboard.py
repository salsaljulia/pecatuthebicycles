import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

day_df = pd.read_csv("dashboard/day.csv")

def convert_to_datetime(df):
    # Konversi kolom 'dteday' ke format datetime
    df['dteday'] = pd.to_datetime(df['dteday'])

    # Menambahkan kolom tahun dan bulan untuk analisis agregat
    df['yr'] = df['dteday'].dt.year
    df['mnth'] = df['dteday'].dt.month

    # Mapping angka musim ke nama musim
    season_mapping = {
        1: 'Winter',
        2: 'Spring',
        3: 'Summer',
        4: 'Fall'
    }
    df['season_name'] = df['season'].map(season_mapping)

    # Menambahkan kolom hari dalam minggu
    df['weekday_name'] = df['weekday'].dt.day_name()

    # Konversi kolom cuaca menjadi kategori untuk efisiensi
    weather_mapping = {
        1: 'Clear or Partly Cloudy',
        2: 'Mist or Cloudy',
        3: 'Light Snow or Rain',
        4: 'Heavy Rain or Snow'
    }
    df['weather_name'] = df['weathersit'].map(weather_mapping)

    # Menambahkan kolom untuk indikasi musim panas atau libur
    df['is_summer'] = df['season'] == 3
    df['is_holiday'] = df['holiday'] == 1

    # Menambahkan kolom gabungan untuk analisis per musim
    df['season_month'] = df['season_name'] + " (" + df['mnth'].astype(str) + ")"

    return df

# Konversi kolom datetime dan pengurutan data
datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Rentang tanggal
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

# Sidebar
with st.sidebar:
    st.image("https://assets-a1.kompasiana.com/items/album/2022/08/05/spongebob-jellyfishing-by-athenatt-da6y2g-62ec8cd408a8b514d7326582.jpg?t=o&v=780")  # Placeholder logo URL

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

# Header aplikasi
st.header('Pecatu Bicycle :sparkles:')

# Pivot table per Bulan
pivot_table_mnth = main_df.groupby(by="mnth").agg({
    "instant": "nunique",
    "cnt": ["mean"]
})

# Ambil rata-rata (mean) dari cnt untuk setiap bulan
mean_cnt = pivot_table_mnth[('cnt', 'mean')]

# Plot bar chart rata-rata cnt per bulan
plt.figure(figsize=(10, 6))
sns.barplot(x=mean_cnt.index, y=mean_cnt.values, palette="viridis")
plt.title("Rata-Rata Jumlah Terbanyak Penyewa per Bulan", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Rata-rata", fontsize=14)
plt.xticks(ticks=range(len(mean_cnt.index)), labels=mean_cnt.index)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
st.pyplot(plt)

# Pivot table per Tahun
pivot_table_yr = main_df.groupby(by="yr").agg({
    "cnt": ["mean"]
}).reset_index()

# Merapikan nama kolom
pivot_table_yr.columns = ["yr", "cnt_mean"]

# Plot bar chart untuk rata-rata cnt per tahun
plt.figure(figsize=(8, 5))
plt.bar(pivot_table_yr["yr"], pivot_table_yr["cnt_mean"], color="skyblue", width=0.5, label="Mean CNT")

# Buat label dinamis berdasarkan data
labels = [f"Year {int(year)}" for year in pivot_table_yr["yr"]]

plt.title("Rata-Rata Jumlah Penyewa per Tahun", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Rata-rata Penyewa", fontsize=14)
plt.xticks(ticks=pivot_table_yr["yr"], labels=labels)  # Gunakan label dinamis
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Pivot table per Musim
pivot_table_season = main_df.groupby(by="season").agg({
    "cnt": ["mean"]
}).reset_index()

# Merapikan nama kolom
pivot_table_season.columns = ["season", "cnt_mean"]

# Mengakses kolom 'cnt_mean' secara langsung
mean_cnt = pivot_table_season["cnt_mean"]

# Plot bar chart rata-rata cnt per musim
plt.figure(figsize=(10, 6))
sns.barplot(x="season", y="cnt_mean", data=pivot_table_season, palette="coolwarm")
plt.title("Rata-rata Jumlah Penyewa (cnt) per Musim", fontsize=16)
plt.ylabel("Rata-rata Penyewa", fontsize=12)
plt.xlabel("Musim", fontsize=12)
plt.tight_layout()
st.pyplot(plt)

st.caption('Copyright (c) Salsa Julia Jasmine - 2024')
