import streamlit as st
import pandas as pd
import numpy as np

# Define dataset path
DATA_PATH = "/Users/shubhamsaraswat/Desktop/PROJECTS/100_days_of_ml/Indian_Cars_Data.csv"

# Load car dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_PATH)

        # Convert 'Price' to numeric (removing non-numeric characters if needed)
        df['Price'] = df['Price'].astype(str).str.extract(r'([\d]+\.\d+|\d+)')

        # Convert to float and scale to INR (Lakh to full amount)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce') * 100000

        # Drop rows where Price couldn't be extracted properly
        df = df.dropna(subset=['Price'])

        # Convert 'Mileage' to numeric (removing 'km/l' or 'km/kg')
        df['Mileage'] = df['Mileage'].astype(str).str.extract(r'([\d]+\.\d+|\d+)')
        df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
        df = df.dropna(subset=['Mileage'])

        # Normalize text-based categories
        df['Fuel Type'] = df['Fuel Type'].astype(str).str.strip().str.capitalize()
        df['Transmission'] = df['Transmission'].astype(str).str.strip().str.capitalize()

        # Handle missing values
        df = df.dropna(subset=['Price', 'Fuel Type', 'Transmission'])

        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

df = load_data()

# Streamlit UI
st.title("🚗 Car Recommendation System")
st.sidebar.header("User Details")

# User Inputs
annual_income = st.sidebar.number_input("Annual Package (₹ in Lakhs)", min_value=2.0, max_value=100.0, value=10.0, step=0.5)
age = st.sidebar.slider("Age", 18, 70, 30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
city = st.sidebar.selectbox("City", df['City'].unique() if 'City' in df.columns else ["Metro", "Tier-1", "Tier-2"])

# ✅ Fix for Fuel Type Selection
if 'Fuel Type' in df.columns and not df['Fuel Type'].isna().all():
    fuel_options = sorted(df['Fuel Type'].dropna().unique())
else:
    fuel_options = ["Petrol", "Diesel", "Electric", "Hybrid"]  # Fallback values

fuel_preference = st.sidebar.selectbox("Preferred Fuel Type", fuel_options)

family_size = st.sidebar.slider("Family Size", 1, 7, 3)
transmission_preference = st.sidebar.selectbox("Transmission", ["Manual", "Automatic"])

# Determine Budget Range
if annual_income < 5:
    budget_min, budget_max = 500000, 1000000
    segment = "Entry-level"
elif 5 <= annual_income < 15:
    budget_min, budget_max = 1000000, 2000000
    segment = "Mid-range"
elif 15 <= annual_income < 30:
    budget_min, budget_max = 2000000, 4000000
    segment = "Premium"
else:
    budget_min, budget_max = 4000000, 10000000
    segment = "Luxury"

# Submit Button
if st.sidebar.button("Find My Car"):
    # Filter Cars based on Budget and Preferences
    filtered_cars = df[
        (df['Price'] >= budget_min) & (df['Price'] <= budget_max) &
        (df['Fuel Type'] == fuel_preference) &
        (df['Transmission'].str.contains(transmission_preference, case=False, na=False))
    ]

    # Display Recommendations
    st.subheader(f"🔍 Recommended Cars in {segment} Segment")
    
    if not filtered_cars.empty:
        # Select top 2-3 cars randomly (or based on best mileage)
        top_cars = filtered_cars.nlargest(3, 'Mileage')

        # Format columns for better readability
        top_cars['Price'] = top_cars['Price'].apply(lambda x: f"₹{int(x):,}")
        top_cars['Mileage'] = top_cars['Mileage'].apply(lambda x: f"{x} km/l")
        
        # Display the data as a styled dataframe
        st.dataframe(top_cars[['Brand', 'Car', 'Variant', 'Price', 'Fuel Type', 'Mileage', 'Transmission']], 
                     use_container_width=True)
    else:
        st.write("❌ No matching cars found. Try adjusting your preferences.")
