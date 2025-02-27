import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image
import os

# Function to check if file exists
def file_exists(file_path):
    return os.path.exists(file_path)

# Function to calculate missing variable
def calculate_missing(rf, beta, rm, expected_return):
    try:
        if rf is None and beta is not None and rm is not None and expected_return is not None:
            if beta == 1:
                return None  # Avoid division by zero when beta is 1
            return (expected_return - beta * rm) / (1 - beta)  # Solve for Rf
        elif beta is None and rf is not None and rm is not None and expected_return is not None:
            return (expected_return - rf) / (rm - rf)  # Solve for Beta
        elif rm is None and rf is not None and beta is not None and expected_return is not None:
            return (expected_return - rf) / beta + rf  # Solve for Market Return
        elif expected_return is None and rf is not None and beta is not None and rm is not None:
            return rf + beta * (rm - rf)  # Solve for Expected Return
    except ZeroDivisionError:
        return None  # Handle any unexpected division errors
    return None  # Return None if inputs are invalid

# Function to format numbers dynamically
def format_number(value):
    return f"{value:.9f}".rstrip('0').rstrip('.') if '.' in f"{value:.9f}" else f"{value:.9f}"

# Function to show Mario GIF
def show_mario_gif():
    gif_path = "mario.gif"
    if file_exists(gif_path):
        st.image(gif_path, width=120)
    else:
        st.warning("Mario GIF not found!")

# Streamlit UI
st.title("CAPM Calculator")
st.markdown("## Capital Asset Pricing Model (CAPM)")

# Selection for known and unknown variable
variable_to_find = st.selectbox("Select the variable to calculate:", ["Expected Return", "Risk-Free Rate (Rf)", "Beta (β)", "Market Return (Rm)"])

rf = None
beta = None
rm = None
expected_return = None

if variable_to_find != "Risk-Free Rate (Rf)":
    rf = st.number_input("Risk-Free Rate (Rf) in %:", min_value=0.0, step=0.1, value=2.0) / 100
if variable_to_find != "Beta (β)":
    beta = st.number_input("Beta (β):", min_value=0.0, step=0.1, value=1.0)
if variable_to_find != "Market Return (Rm)":
    rm = st.number_input("Expected Market Return (Rm) in %:", min_value=0.0, step=0.1, value=8.0) / 100
if variable_to_find != "Expected Return":
    expected_return = st.number_input("Expected Return in %:", min_value=0.0, step=0.1, value=5.0) / 100

if st.button("Calculate"):
    with st.spinner("Calculating..."):
        time.sleep(2)  # Simulating Processing Time
        result = calculate_missing(rf, beta, rm, expected_return)
        
        if result is not None:
            result *= 100
            st.success(f"{variable_to_find}: {format_number(result)}%")
            # Show Mario GIF
            show_mario_gif()
        else:
            st.error("Invalid input combination. Please check your values.")

    # Plot Security Market Line (SML)
    if rf is not None and rm is not None:
        beta_range = np.linspace(0, 2, 100)
        sml = rf * 100 + beta_range * (rm * 100 - rf * 100)
        
        fig, ax = plt.subplots()
        ax.plot(beta_range, sml, label="Security Market Line (SML)", color="blue")
        if beta is not None and result is not None:
            ax.scatter(beta, result, color='red', label="Your Asset")
        ax.set_xlabel("Beta (β)")
        ax.set_ylabel("Expected Return (%)")
        ax.set_title("Security Market Line")
        ax.legend()
        st.pyplot(fig)

    # Bar Chart of Inputs
    st.subheader("Input Comparison")
    chart_data = {
        "Risk-Free Rate (%)": rf * 100 if rf is not None else 0,
        "Market Return (%)": rm * 100 if rm is not None else 0,
        "Expected Return (%)": result if result is not None else 0
    }
    st.bar_chart(chart_data)

# Syndicate 16 Signature
st.markdown("---")
st.markdown("### Prepared by - Syndicate 16")
