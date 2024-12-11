import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
season_mean.plot(kind="bar", ax=ax)
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 3: Rozkład wieku klientów
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots()
filtered_data["Age"].hist(bins=20, ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
st.pyplot(fig)

# Dodatkowe wykresy:
# Wykres 4: Procentowy udział metod płatności
st.write("### Procentowy udział metod płatności")
payment_counts = filtered_data["Payment Method"].value_counts(normalize=True) * 100
fig, ax = plt.subplots()
payment_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax, startangle=90)
ax.set_ylabel("")
st.pyplot(fig)

# Wykres 5: Rozkład ocen recenzji
st.write("### Rozkład ocen recenzji")
fig, ax = plt.subplots()
filtered_data["Review Rating"].hist(bins=10, ax=ax, color="orange")
ax.set_xlabel("Ocena recenzji")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 6: Top lokalizacje wg średnich wydatków
st.write("### Top 5 lokalizacji wg średnich wydatków")
location_mean = filtered_data.groupby("Location")["Purchase Amount (USD)"].mean().nlargest(5)
fig, ax = plt.subplots()
location_mean.plot(kind="bar", ax=ax, color="green")
ax.set_xlabel("Lokalizacja")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 7: Liczba zakupów w różnych sezonach
st.write("### Liczba zakupów w sezonach")
season_counts = filtered_data["Season"].value_counts()
fig, ax = plt.subplots()
season_counts.plot(kind="bar", ax=ax, color="purple")
ax.set_xlabel("Sezon")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)
