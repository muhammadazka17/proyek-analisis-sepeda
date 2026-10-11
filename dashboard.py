import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='darkgrid')
st.set_page_config(page_title='Bike Sharing Dashboard', page_icon='🚲', layout='wide')

@st.cache_data
def load_data():
    day_df = pd.read_csv('main_data.csv')
    hour_df = pd.read_csv('hour_data.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    season_map = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Clear', 2: 'Cloudy/Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Ice'}
    day_df['season_label'] = day_df['season'].map(season_map)
    day_df['weather_label'] = day_df['weathersit'].map(weather_map)
    hour_df['workingday_label'] = hour_df['workingday'].map({1: 'Hari Kerja', 0: 'Hari Libur'})
    return day_df, hour_df

day_df, hour_df = load_data()

st.sidebar.title('🚲 Filter Interaktif')
st.sidebar.markdown('Silakan filter data untuk melihat perubahan visualisasi.')
selected_year = st.sidebar.selectbox('Pilih Tahun:', [2011, 2012], index=1)
yr_val = 0 if selected_year == 2011 else 1

filtered_day = day_df[day_df['yr'] == yr_val]
filtered_hour = hour_df[hour_df['yr'] == yr_val]

st.title('🌟 Bike Sharing Analytics Dashboard')
st.markdown('Visualisasi data operasional Bike Sharing berdasarkan parameter interaktif.')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Penyewaan', f"{filtered_day['cnt'].sum():,}")
with col2:
    st.metric('Rata-rata Penyewaan Harian', f"{int(filtered_day['cnt'].mean()):,}")
with col3:
    st.metric('Pengguna Kasual', f"{filtered_day['casual'].sum():,}")

st.markdown('---')

st.subheader(f'1. Dampak Musim & Cuaca terhadap Penyewaan Harian ({selected_year})')
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x='season_label', y='cnt', hue='weather_label', data=filtered_day, palette='viridis', ax=ax1)
ax1.set_xlabel('Musim')
ax1.set_ylabel('Rata-rata Penyewaan')
ax1.legend(title='Kondisi Cuaca')
st.pyplot(fig1)

st.subheader(f'2. Pola Jam Sibuk: Hari Kerja vs Libur ({selected_year})')
hourly_trend = filtered_hour.groupby(['hr', 'workingday_label'])['cnt'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(x='hr', y='cnt', hue='workingday_label', data=hourly_trend, marker='o', linewidth=2, ax=ax2)
ax2.set_xlabel('Jam (0-23)')
ax2.set_ylabel('Rata-rata Penyewaan')
ax2.set_xticks(range(0, 24))
st.pyplot(fig2)

st.caption('Proyek Analisis Data Dicoding © 2026 - Muhammad Aditya Azka Azkia')