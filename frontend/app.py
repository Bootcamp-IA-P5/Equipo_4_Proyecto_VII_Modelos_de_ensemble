"""
Streamlit frontend for Fetal Health Classification
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# Page configuration
st.set_page_config(
    page_title="Fetal Health Classification",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .normal {
        background-color: #d4edda;
        border: 2px solid #28a745;
    }
    .suspect {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
    }
    .pathological {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)


def check_backend_health():
    """Check if backend is healthy"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200 and response.json().get("model_loaded", False)
    except Exception as e:
        st.error(f"Backend connection error: {str(e)}")
        return False


def get_dataset_info():
    """Get dataset information from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/dataset/info", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching dataset info: {str(e)}")
        return None


def make_prediction(features):
    """Make prediction using backend API"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/predict",
            json=features,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Prediction error: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Fetal Health Classification System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This application uses ensemble machine learning models to classify fetal health 
        based on cardiotocographic (CTG) data.
        
        **Classes:**
        - 🟢 **Normal**: Healthy fetal state
        - 🟡 **Suspect**: Requires monitoring
        - 🔴 **Pathological**: Requires immediate attention
        """)
        
        st.divider()
        
        # Backend status
        st.header("🔌 System Status")
        if check_backend_health():
            st.success("✅ Backend connected")
            st.success("✅ Model loaded")
        else:
            st.error("❌ Backend not available or model not loaded")
            st.info("Please ensure the model is trained first using: `docker compose --profile training up train-model`")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Make Prediction", "📈 Dataset Info", "ℹ️ Feature Descriptions"])
    
    with tab1:
        st.header("Enter Fetal Health Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Baseline Features")
            baseline_value = st.number_input("Baseline Value (FHR)", min_value=100.0, max_value=200.0, value=120.0, step=1.0)
            accelerations = st.number_input("Accelerations", min_value=0.0, max_value=0.1, value=0.0, step=0.001, format="%.4f")
            fetal_movement = st.number_input("Fetal Movement", min_value=0.0, max_value=0.5, value=0.0, step=0.001, format="%.4f")
            uterine_contractions = st.number_input("Uterine Contractions", min_value=0.0, max_value=0.02, value=0.0, step=0.001, format="%.4f")
            
        with col2:
            st.subheader("Decelerations")
            light_decelerations = st.number_input("Light Decelerations", min_value=0.0, max_value=0.02, value=0.0, step=0.001, format="%.4f")
            severe_decelerations = st.number_input("Severe Decelerations", min_value=0.0, max_value=0.01, value=0.0, step=0.001, format="%.4f")
            prolongued_decelerations = st.number_input("Prolongued Decelerations", min_value=0.0, max_value=0.01, value=0.0, step=0.001, format="%.4f")
            
            st.subheader("Variability")
            abnormal_short_term_variability = st.number_input("Abnormal Short Term Variability", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
            mean_value_of_short_term_variability = st.number_input("Mean Short Term Variability", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        
        with col3:
            st.subheader("Long Term Variability")
            percentage_of_time_with_abnormal_long_term_variability = st.number_input(
                "% Time Abnormal LTV", 
                min_value=0.0, max_value=100.0, value=0.0, step=1.0
            )
            mean_value_of_long_term_variability = st.number_input("Mean LTV", min_value=0.0, max_value=50.0, value=8.0, step=0.1)
            
        st.divider()
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.subheader("Histogram Features")
            histogram_width = st.number_input("Histogram Width", min_value=0.0, max_value=200.0, value=70.0, step=1.0)
            histogram_min = st.number_input("Histogram Min", min_value=0.0, max_value=200.0, value=60.0, step=1.0)
            histogram_max = st.number_input("Histogram Max", min_value=0.0, max_value=250.0, value=150.0, step=1.0)
            histogram_number_of_peaks = st.number_input("Number of Peaks", min_value=0.0, max_value=20.0, value=2.0, step=1.0)
        
        with col5:
            histogram_number_of_zeroes = st.number_input("Number of Zeroes", min_value=0.0, max_value=20.0, value=0.0, step=1.0)
            histogram_mode = st.number_input("Histogram Mode", min_value=0.0, max_value=200.0, value=120.0, step=1.0)
            histogram_mean = st.number_input("Histogram Mean", min_value=0.0, max_value=200.0, value=120.0, step=1.0)
        
        with col6:
            histogram_median = st.number_input("Histogram Median", min_value=0.0, max_value=200.0, value=120.0, step=1.0)
            histogram_variance = st.number_input("Histogram Variance", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
            histogram_tendency = st.number_input("Histogram Tendency", min_value=-1.0, max_value=1.0, value=0.0, step=0.1)
        
        st.divider()
        
        # Predict button
        if st.button("🔮 Make Prediction", type="primary", use_container_width=True):
            with st.spinner("Making prediction..."):
                features = {
                    "baseline_value": baseline_value,
                    "accelerations": accelerations,
                    "fetal_movement": fetal_movement,
                    "uterine_contractions": uterine_contractions,
                    "light_decelerations": light_decelerations,
                    "severe_decelerations": severe_decelerations,
                    "prolongued_decelerations": prolongued_decelerations,
                    "abnormal_short_term_variability": abnormal_short_term_variability,
                    "mean_value_of_short_term_variability": mean_value_of_short_term_variability,
                    "percentage_of_time_with_abnormal_long_term_variability": percentage_of_time_with_abnormal_long_term_variability,
                    "mean_value_of_long_term_variability": mean_value_of_long_term_variability,
                    "histogram_width": histogram_width,
                    "histogram_min": histogram_min,
                    "histogram_max": histogram_max,
                    "histogram_number_of_peaks": histogram_number_of_peaks,
                    "histogram_number_of_zeroes": histogram_number_of_zeroes,
                    "histogram_mode": histogram_mode,
                    "histogram_mean": histogram_mean,
                    "histogram_median": histogram_median,
                    "histogram_variance": histogram_variance,
                    "histogram_tendency": histogram_tendency
                }
                
                result = make_prediction(features)
                
                if result:
                    # Display prediction
                    prediction_class = result["prediction_label"].lower()
                    
                    st.markdown(f"""
                    <div class="prediction-box {prediction_class}">
                        <h2>Prediction: {result["prediction_label"]}</h2>
                        <p><strong>Class:</strong> {result["prediction"]}</p>
                        {f'<p><strong>Confidence:</strong> {result["confidence"]:.2%}</p>' if result.get("confidence") else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display confidence gauge if available
                    if result.get("confidence"):
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=result["confidence"] * 100,
                            title={'text': "Confidence Score"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 50], 'color': "lightgray"},
                                    {'range': [50, 75], 'color': "gray"},
                                    {'range': [75, 100], 'color': "lightgreen"}
                                ],
                            }
                        ))
                        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Dataset Information")
        
        dataset_info = get_dataset_info()
        
        if dataset_info:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Samples", dataset_info["total_samples"])
            with col2:
                st.metric("Number of Features", dataset_info["features"])
            with col3:
                st.metric("Number of Columns", len(dataset_info["columns"]))
            
            st.divider()
            
            # Target distribution
            if dataset_info.get("target_distribution"):
                st.subheader("Fetal Health Distribution")
                
                labels_map = {1: "Normal", 2: "Suspect", 3: "Pathological"}
                # Handle both string and float keys by converting to int
                target_dist = {}
                for k, v in dataset_info["target_distribution"].items():
                    try:
                        key = int(float(k))  # Convert to float first, then to int
                        target_dist[labels_map.get(key, str(key))] = v
                    except (ValueError, TypeError):
                        target_dist[str(k)] = v
                
                fig = px.pie(
                    values=list(target_dist.values()),
                    names=list(target_dist.keys()),
                    title="Distribution of Fetal Health Classes",
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Features list
            st.subheader("Available Features")
            st.dataframe(
                pd.DataFrame({"Feature": dataset_info["columns"]}),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("Dataset information not available")
    
    with tab3:
        st.header("Feature Descriptions")
        
        st.markdown("""
        ### Cardiotocographic (CTG) Features
        
        **Baseline Features:**
        - **Baseline Value**: Baseline Fetal Heart Rate (FHR) in beats per minute
        - **Accelerations**: Number of accelerations per second
        - **Fetal Movement**: Number of fetal movements per second
        - **Uterine Contractions**: Number of uterine contractions per second
        
        **Decelerations:**
        - **Light Decelerations**: Number of light decelerations per second
        - **Severe Decelerations**: Number of severe decelerations per second
        - **Prolongued Decelerations**: Number of prolonged decelerations per second
        
        **Variability:**
        - **Abnormal Short Term Variability**: Percentage of time with abnormal short-term variability
        - **Mean Short Term Variability**: Mean value of short-term variability
        - **Percentage Time Abnormal LTV**: Percentage of time with abnormal long-term variability
        - **Mean LTV**: Mean value of long-term variability
        
        **Histogram Features:**
        - **Width**: Width of the FHR histogram
        - **Min/Max**: Minimum and maximum values in the histogram
        - **Number of Peaks**: Number of peaks in the histogram
        - **Number of Zeroes**: Number of zeros in the histogram
        - **Mode**: Most frequent FHR value
        - **Mean**: Average FHR value
        - **Median**: Median FHR value
        - **Variance**: Variance of FHR values
        - **Tendency**: Tendency of the histogram (-1: left, 0: symmetric, 1: right)
        """)


if __name__ == "__main__":
    main()
