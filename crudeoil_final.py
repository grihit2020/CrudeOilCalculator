import yfinance as yf
import streamlit as st
from PIL import Image
import pandas as pd
from forex_python.converter import CurrencyRates

# Defining usernames and passwords which are valid/accepted
valid_credentials = {
    "modi": "akhandbharat",
    "putin": "myukraine",
    "salman": "habibi",
    "emmaneul": "parislove",
    "kishida": "oldsushi",
    "grihit": "password"
}

# For creating a Streamlit UI 
st.set_page_config(layout="centered")
page = st.sidebar.selectbox("Select a Page", ["Login", "Currency Converter", "Crude Oil Calculator"])

if page == "Login":
    st.title("Login")
    img=Image.open('rbi1.png')
    st.image(img)
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if username in valid_credentials and password == valid_credentials[username]:
            st.success("Logged in successfully!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials. Please try again.")

if page == "Currency Converter" and st.session_state.get("logged_in"):
    st.title("Currency Converter")

    # Taking the input for amount and currency
    amount = st.number_input("Enter Amount:", min_value=0.0)
    selected_currency = st.selectbox("Select a Currency:", ["USD", "EUR", "GBP", "JPY"])

    # For currency converter
    currency_converter = CurrencyRates()
    amount_usd = currency_converter.convert(selected_currency, "USD", amount)

    st.subheader(f"Conversion Result:")
    st.write(f"{amount:.2f} {selected_currency} is approximately ${amount_usd:.2f} USD")

if page == "Crude Oil Calculator" and st.session_state.get("logged_in"):
    st.title("Crude Oil Price Calculator") #If user logs in with valid username and password and selects/ wishes to got to crude oil calculator page

    # Taking the input for budget and selling limit
    budget_usd = st.number_input("Enter your budget (USD):", min_value=0.0)
    selling_limit = st.number_input("Enter your selling limit (barrels):", min_value=0.0)

    # Creating a dropdown menu for selecting the country between US and Mexico
    selected_country = st.selectbox("Select a Country:", ["United States", "Mexico"])

    # Here, we define the symbols for the selected countries
    country_symbols = {
        "United States": "CL=F",
        "Mexico": "MGC=F"
    }

    # For fetching historical price data for the selected country using yfinance
    symbol = country_symbols[selected_country]
    try:
        crude_oil_data = yf.Ticker(symbol)
        data = crude_oil_data.history(period="1825d")["Close"] #period allows us to change the number of previous days for which data will be shown
    except Exception as e:
        st.error(f"Error fetching crude oil price data for {selected_country}: {str(e)}")
        data = None

    # For calculating the amount of crude oil that can be purchased for the selected country
    st.subheader("Purchase and Selling Summary")
    if data is not None and not data.empty:
        current_price = data[-1]
        crude_oil_amount = budget_usd / current_price
        remaining_budget = budget_usd - (selling_limit * current_price) if selling_limit is not None else budget_usd
        st.write(f"For {selected_country}:")
        st.write(f"With ${budget_usd:.2f} USD, you can purchase approximately {crude_oil_amount:.2f} barrels of crude oil.")
        st.write(f"If you sell {selling_limit:.2f} barrels, you will have ${remaining_budget:.2f} USD remaining.")

    # For creating a graph for displaying the historical price data for the selected country
    st.subheader(f"Crude Oil Price History for {selected_country} (Last 5 Years)")
    if data is not None and not data.empty:
        st.line_chart(data)

    # For adding a slider to select the number of previous days to display
    num_days_to_display = st.slider("Number of Previous Days to Display:", min_value=1, max_value=30, value=7)
    st.subheader(f"Crude Oil Price History for {selected_country} (Last {num_days_to_display} Days)")
    if data is not None and not data.empty:
        st.line_chart(data.tail(num_days_to_display))
