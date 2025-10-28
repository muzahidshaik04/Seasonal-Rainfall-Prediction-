import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load your trained model
model = joblib.load("rainfalls_model.pkl")  # <-- change filename if needed

# App title
st.title("🌦️ Seasonal Rainfall Prediction App")
st.markdown("""
This app predicts **total or seasonal rainfall (in mm)** based on climatic and seasonal parameters.
Enter your values below and click **Predict Rainfall** 👇
""")

# Input fields
normal_winter = st.number_input("Normal Winter", value=17.8)
actual_winter = st.number_input("Actual Winter", value=17.9)
actual_southwest = st.number_input("Actual SW", value=558.7)
actual_northeast = st.number_input("Actual NE", value=31.5)

# Optional: if actual total rainfall known (for visual comparison)
actual_total = st.number_input("Total Actual (optional)", value=0.0)

# Predict button
if st.button("Predict Rainfall"):
    try:
        # Prepare features in same order as training
        features = np.array([[normal_winter, actual_winter,actual_southwest, actual_northeast]])

        # Prediction
        prediction = model.predict(features)[0]

        st.success(f"🌧️ **Predicted Total Rainfall:** {prediction:.2f} mm")

        # Create DataFrame for visualization
        data = {
            "Type": ["Predicted Rainfall"],
            "Rainfall (mm)": [prediction]
        }

        if actual_total > 0:
            data["Type"].append("Actual Rainfall")
            data["Rainfall (mm)"].append(actual_total)

        df = pd.DataFrame(data)

        # Plot chart
        st.subheader("📊 Predicted vs Actual Rainfall")
        fig, ax = plt.subplots()
        ax.bar(df["Type"], df["Rainfall (mm)"], color=["skyblue", "orange"])
        ax.set_ylabel("Rainfall (mm)")
        ax.set_title("Rainfall Comparison Chart")
        st.pyplot(fig)

        st.caption("This chart compares predicted rainfall with actual recorded rainfall (if provided).")

    except Exception as e:
        st.error(f"⚠️ Error during prediction: {e}")
        st.info("Please make sure your model file and input order are correct.")