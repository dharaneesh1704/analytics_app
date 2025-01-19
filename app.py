import streamlit as st
import pandas as pd
import sweetviz as sv
import tempfile
import os
import plotly.express as px

# Title and Description
st.title("Enhanced Data Analytics App")
st.write("Upload a CSV file, analyze it with Sweetviz, and explore key insights directly in the app!")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.dataframe(df)

        # Display basic info about the dataset
        st.write("### Dataset Information")
        st.write(f"**Number of Rows:** {df.shape[0]}")
        st.write(f"**Number of Columns:** {df.shape[1]}")
        st.write("**Columns and Data Types:")
        st.write(df.dtypes)

        # Column Selection for Analysis
        st.write("### Column Selection")
        selected_columns = st.multiselect(
            "Select columns for analysis (default: all columns):", df.columns, default=df.columns
        )
        df_filtered = df[selected_columns]

        # Generate Sweetviz Report
        st.write("### Generating Sweetviz Report...")
        with st.spinner("Analyzing data and generating the report..."):
            report = sv.analyze(df_filtered)

        # Use a temporary file to store the report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            report.show_html(filepath=temp_file.name, open_browser=False)
            sweetviz_report_path = temp_file.name

        st.success("Sweetviz Report generated successfully!")

        # Display interactive visualizations
        st.write("### Interactive Visualizations")

        # Plot numeric distributions
        numeric_columns = df_filtered.select_dtypes(include=["int64", "float64"]).columns
        if not numeric_columns.empty:
            st.write("#### Numeric Column Distributions")
            for col in numeric_columns:
                fig = px.histogram(df_filtered, x=col, title=f"Distribution of {col}")
                st.plotly_chart(fig, use_container_width=True)

        # Plot category counts
        categorical_columns = df_filtered.select_dtypes(include=["object", "category"]).columns
        if not categorical_columns.empty:
            st.write("#### Categorical Column Counts")
            for col in categorical_columns:
                # Count values for the categorical column
                value_counts = df_filtered[col].value_counts().reset_index()
                value_counts.columns = [col, "count"]  # Rename columns for clarity

                # Create a bar chart
                fig = px.bar(value_counts, x=col, y="count", title=f"Count of {col}")
                st.plotly_chart(fig, use_container_width=True)

        # Provide download buttons
        st.write("### Downloads")
        with open(sweetviz_report_path, "rb") as file:
            st.download_button(
                label="Download Sweetviz Report as HTML",
                data=file,
                file_name="sweetviz_report.html",
                mime="text/html",
            )

        # Option to download filtered data
        st.download_button(
            label="Download Filtered Data as CSV",
            data=df_filtered.to_csv(index=False).encode("utf-8"),
            file_name="filtered_data.csv",
            mime="text/csv",
        )

        # Clean up temporary files
        os.remove(sweetviz_report_path)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
