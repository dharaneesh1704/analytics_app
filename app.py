import streamlit as st
import pandas as pd
import sweetviz as sv
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tempfile
import streamlit.components.v1 as components

# Streamlit App Title
st.title("Analytics Dashboard with Sweetviz")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load Dataset
        df = pd.read_csv(uploaded_file)

        # Display DataFrame Preview
        st.write("### Preview of Dataset", df.head())

        # Extract Numeric Columns
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

        if numeric_columns:
            st.write("### Numeric Columns Detected:", numeric_columns)
        else:
            st.warning("No numeric columns found in the uploaded file.")

        # Let User Select a Column for Analysis
        selected_column = st.selectbox("Select a numeric column for analysis:", numeric_columns)

        if selected_column:
            st.write(f"### Statistics for {selected_column}")
            st.write(df[selected_column].describe())

            # Histogram
            st.write(f"### Histogram of {selected_column}")
            fig, ax = plt.subplots()
            sns.histplot(df[selected_column], bins=30, kde=True, ax=ax)
            st.pyplot(fig)

            # Box Plot
            st.write(f"### Boxplot of {selected_column}")
            fig, ax = plt.subplots()
            sns.boxplot(y=df[selected_column], ax=ax)
            st.pyplot(fig)

            # Correlation Matrix (Optional)
            if len(numeric_columns) > 1:
                st.write("### Correlation Matrix")
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

        # Generate Sweetviz Report
        st.write("## Auto-Generated EDA Report with Sweetviz")

        # Use a Temporary Directory
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = os.path.join(temp_dir, "sweetviz_report.html")

            # Generate and save report
            report = sv.analyze(df)
            report.show_html(report_path, open_browser=False)

            # Read the HTML file and display it
            with open(report_path, "r", encoding="utf-8") as file:
                report_html = file.read()
                components.html(report_html, height=800, scrolling=True)

            # Provide a download button
            st.download_button(
                label="📥 Download Sweetviz Report",
                data=open(report_path, "rb").read(),
                file_name="Sweetviz_Report.html",
                mime="text/html"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to begin analysis.")
