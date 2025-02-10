import streamlit as st
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Streamlit App Title
st.title("Analytics Dashboard with ydata-profiling")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load Dataset with Encoding Handling
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")

        # Check if DataFrame is empty
        if df.empty:
            st.warning("The uploaded CSV file is empty. Please upload a valid file.")
        else:
            # Display DataFrame Preview
            st.write("### Preview of Dataset", df.head())

            # Handle Large Datasets
            if len(df) > 100000:
                st.warning("Dataset is too large! Showing only the first 100,000 rows for analysis.")
                df = df.sample(n=100000, random_state=42)

            # Fix: Handling numpy VisibleDeprecationWarning issue
            if hasattr(np, "VisibleDeprecationWarning"):
                del np.VisibleDeprecationWarning

            # Generate ydata-profiling Report
            st.write("## Auto-Generated EDA Report with ydata-profiling")
            profile_report = ProfileReport(df, explorative=True)
            st_profile_report(profile_report)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to begin analysis.")
