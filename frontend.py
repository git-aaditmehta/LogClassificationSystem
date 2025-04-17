import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Set page config
st.set_page_config(
    page_title="Log Classification System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add title and description
st.title("Log Classification System")
st.markdown("Upload your log file to classify log messages automatically.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Create two columns for input and output display
    col1, col2 = st.columns(2)
    
    try:
        # Read and display input file
        input_df = pd.read_csv(uploaded_file)
        with col1:
            st.subheader("Input Data")
            st.dataframe(input_df, use_container_width=True)
        
        # Prepare file for API request
        csv_string = StringIO()
        input_df.to_csv(csv_string, index=False)
        
        # Make API request to FastAPI backend
        files = {
            'file': ('input.csv', csv_string.getvalue(), 'text/csv')
        }
        response = requests.post('http://localhost:8000/classify', files=files)
        
        if response.status_code == 200:
            # Process and display output
            output_df = pd.read_csv(StringIO(response.text))
            with col2:
                st.subheader("Classified Output")
                st.dataframe(output_df, use_container_width=True)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}") 