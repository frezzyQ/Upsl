# Dodano bibliotekę Seaborn do zaawansowanych i estetycznych wykresów.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ustawienia globalne Seaborn
sns.set_theme(style="whitegrid")

# Wczytaj dane
@st.cache
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
min_review_rating = st.sidebar.slider("Minimalna ocena recenzji", 0.0, 5.0, 3.0)
season_filter = st.sidebar.multiselect("Sezon", data["Season"].unique(), data["Season"].unique())
payment_method_filter = st.sidebar.multiselect("Metoda płatności", data["Payment Method"].unique(), data["Payment Method"].unique())
min_previous_purchases = st.sidebar.slider("Minimalna liczba wcześniejszych zakupów", 0, int(data["Previous Purchases"].max()), 5)
preferred_payment_methods = st.sidebar.multiselect("Ulubiona metoda płatności", data["Preferred Payment Method"].unique(), data["Preferred Payment Method"].unique())

# Filtruj dane
filtered_data = data[
    (data["Age"] >= age_filter[0]) & 
    (data["Age"] <= age_filter[1]) & 
    (data["Category"].isin(category_filter)) & 
    (data["Review Rating"] >= min_review_rating) & 
    (data["Season"].isin(season_filter)) & 
    (data["Payment Method"].isin(payment_method_filter)) & 
    (data["Previous Purchases"] > min_previous_purchases) & 
    (data["Preferred Payment Method"].isin(preferred_payment_methods)) & 
    (data["Subscription Status"] == "Yes") & 
    (data["Discount Applied"] == "Yes")
]

# Wyświetlanie danych
st.write("### Filtrowane dane", filtered_data)

# Wykresy
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=category_counts.index, y=category_counts.values, ax=ax, palette="viridis")
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
ax.set_title("Liczba zakupów wg kategorii")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_mean.index, y=season_mean.values, ax=ax, palette="coolwarm")
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
ax.set_title("Średnia kwota zakupów wg sezonu")
st.pyplot(fig)

# Wykres 3: Rozkład wieku klientów
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_data["Age"], kde=True, bins=20, ax=ax, color="purple", edgecolor="black")
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
ax.set_title("Rozkład wieku klientów")
st.pyplot(fig)

# Wykres 4: Procentowy udział metod płatności
st.write("### Procentowy udział metod płatności")
payment_counts = filtered_data["Payment Method"].value_counts(normalize=True) * 100
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=payment_counts.index, y=payment_counts.values, ax=ax, palette="pastel")
ax.set_xlabel("Metoda płatności")
ax.set_ylabel("Procentowy udział (%)")
ax.set_title("Procentowy udział metod płatności")
st.pyplot(fig)

# Wykres 5: Rozkład ocen recenzji
st.write("### Rozkład ocen recenzji")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="Review Rating", data=filtered_data, ax=ax, color="orange")
ax.set_xlabel("Ocena recenzji")
ax.set_title("Rozkład ocen recenzji")
st.pyplot(fig)

# Wykres 6: Top lokalizacje wg średnich wydatków
st.write("### Top 5 lokalizacji wg średnich wydatków")
location_mean = filtered_data.groupby("Location")["Purchase Amount (USD)"].mean().nlargest(5)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=location_mean.index, y=location_mean.values, ax=ax, palette="cool")
ax.set_xlabel("Lokalizacja")
ax.set_ylabel("Średnia kwota zakupów (USD)")
ax.set_title("Top 5 lokalizacji wg średnich wydatków")
st.pyplot(fig)

# Wykres 7: Liczba zakupów w różnych sezonach
st.write("### Liczba zakupów w sezonach")
season_counts = filtered_data["Season"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_counts.index, y=season_counts.values, ax=ax, palette="Set2")
ax.set_xlabel("Sezon")
ax.set_ylabel("Liczba zakupów")
ax.set_title("Liczba zakupów w sezonach")
st.pyplot(fig)
