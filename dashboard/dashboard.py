import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

day_df = pd.read_csv("dashboard/day.csv")

def convert_to_datetime(day_df):
    # Konversi kolom 'dteday' ke format datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    # Menambahkan kolom tahun dan bulan untuk analisis agregat
    day_df['yr'] = day_df['dteday'].dt.year
    day_df['mnth'] = day_df['dteday'].dt.month

    # Mapping angka musim ke nama musim
    season_mapping = {
        1: 'Winter',
        2: 'Spring',
        3: 'Summer',
        4: 'Fall'
    }
    day_df['season_name'] = day_df['season'].map(season_mapping)

    # Menambahkan kolom hari dalam minggu
    day_df['weekday_name'] = day_df['weekday'].dt.day_name()

    # Konversi kolom cuaca menjadi kategori untuk efisiensi
    weather_mapping = {
        1: 'Clear or Partly Cloudy',
        2: 'Mist or Cloudy',
        3: 'Light Snow or Rain',
        4: 'Heavy Rain or Snow'
    }
    day_df['weather_name'] = day_df['weathersit'].map(weather_mapping)

    # Menambahkan kolom untuk indikasi musim panas atau libur
    day_df['is_summer'] = day_df['season'] == 3
    day_df['is_holiday'] = day_df['holiday'] == 1

    # Menambahkan kolom gabungan untuk analisis per musim
    day_df['season_month'] = day_df['season_name'] + " (" + day_df['mnth'].astype(str) + ")"

    return day_df

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

# Pivot table
pivot_table = day_df.groupby(by="mnth").agg({
    "instant": "nunique",
    "cnt": ["max", "min", "mean", "std"]
})

# Ambil rata-rata (mean) dari cnt untuk setiap bulan
mean_cnt = pivot_table[('cnt', 'mean')]

# Plot bar chart rata-rata cnt per bulan
plt.figure(figsize=(10, 6))
sns.barplot(x=mean_cnt.index, y=mean_cnt.values, palette="viridis")
plt.title("Mean CNT per Month", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Mean CNT", fontsize=14)
plt.xticks(ticks=range(len(mean_cnt.index)), labels=mean_cnt.index)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
st.pyplot(plt)

# Data untuk rata-rata cnt per tahun
data = {
    "yr": [0, 1],
    "cnt_mean": [3405.76, 5599.93]
}
day_df_summary = pd.DataFrame(data).set_index("yr")

# Plot bar chart untuk rata-rata cnt per tahun
plt.figure(figsize=(8, 5))
plt.bar(day_df_summary.index, day_df_summary["cnt_mean"], color="skyblue", width=0.5, label="Mean CNT")
plt.title("Mean CNT per Year", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Mean CNT", fontsize=14)
plt.xticks(ticks=day_df_summary.index, labels=["Year 0", "Year 1"])
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Data untuk rata-rata cnt per musim
data = {
    "season": ["Winter", "Spring", "Summer", "Fall"],
    "cnt_mean": [250, 300, 350, 280]
}
df = pd.DataFrame(data)

# Plot bar chart rata-rata cnt per musim
plt.figure(figsize=(10, 6))
sns.barplot(x="season", y="cnt_mean", data=df, palette="coolwarm")
plt.title("Rata-rata Jumlah (cnt) per Musim", fontsize=16)
plt.ylabel("Rata-rata (cnt)", fontsize=12)
plt.xlabel("Musim", fontsize=12)
plt.tight_layout()
st.pyplot(plt)
