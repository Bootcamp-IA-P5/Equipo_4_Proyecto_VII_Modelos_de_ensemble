"""
FastAPI backend for Fetal Health Classification
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import joblib
import os
from pathlib import Path

app = FastAPI(
    title="Fetal Health Classification API",
    description="API for predicting fetal health using ensemble models",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths
BASE_DIR = Path("/app")
MODELS_DIR = BASE_DIR / "models"
DATASETS_DIR = BASE_DIR / "data" / "raw"

# Global variables for model and scaler
model = None
scaler = None
feature_names = None


class FetalHealthFeatures(BaseModel):
    """Input features for fetal health prediction"""
    baseline_value: float
    accelerations: float
    fetal_movement: float
    uterine_contractions: float
    light_decelerations: float
    severe_decelerations: float
    prolongued_decelerations: float
    abnormal_short_term_variability: float
    mean_value_of_short_term_variability: float
    percentage_of_time_with_abnormal_long_term_variability: float
    mean_value_of_long_term_variability: float
    histogram_width: float
    histogram_min: float
    histogram_max: float
    histogram_number_of_peaks: float
    histogram_number_of_zeroes: float
    histogram_mode: float
    histogram_mean: float
    histogram_median: float
    histogram_variance: float
    histogram_tendency: float
    
    class Config:
        # Allow population by field name with spaces (from dataset)
        allow_population_by_field_name = True


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    prediction: int
    prediction_label: str
    confidence: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool


@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model, scaler, feature_names
    model_path = MODELS_DIR / "fetal_health_model.pkl"
    
    if model_path.exists():
        try:
            # Load the model dictionary
            model_dict = joblib.load(model_path)
            
            # Extract components from dictionary
            if isinstance(model_dict, dict):
                model = model_dict.get('model')
                scaler = model_dict.get('scaler')
                feature_names = model_dict.get('feature_names')
                print(f"✓ Model loaded successfully from {model_path}")
                print(f"  - Model type: {type(model).__name__}")
                print(f"  - Model name: {model_dict.get('model_name', 'Unknown')}")
                print(f"  - Features: {len(feature_names) if feature_names else 'Unknown'}")
            else:
                # If it's not a dict, assume it's the model directly (backward compatibility)
                model = model_dict
                print(f"✓ Model loaded successfully from {model_path} (legacy format)")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            model = None
            scaler = None
            feature_names = None
    else:
        print(f"✗ Model not found at {model_path}. Please train the model first.")
        model = None
        scaler = None
        feature_names = None


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Fetal Health Classification API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "dataset_info": "/dataset/info"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: FetalHealthFeatures):
    """
    Make a prediction for fetal health classification
    
    - **features**: Dictionary containing all required features
    - Returns prediction (1: Normal, 2: Suspect, 3: Pathological)
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )
    
    try:
        # Convert input to DataFrame
        features_dict = features.dict()
        
        # Create DataFrame - pandas will use the dict keys as column names
        input_data = pd.DataFrame([features_dict])
        
        # Rename 'baseline_value' to 'baseline value' (with space) to match training data
        input_data = input_data.rename(columns={'baseline_value': 'baseline value'})
        
        # Ensure column order matches training if feature_names available
        if feature_names is not None:
            # Reorder columns to match training data
            input_data = input_data[feature_names]
        
        # Apply scaling if scaler is available
        if scaler is not None:
            input_data_scaled = scaler.transform(input_data)
        else:
            input_data_scaled = input_data
        
        # Make prediction
        prediction = model.predict(input_data_scaled)[0]
        
        # Get prediction label
        labels = {1: "Normal", 2: "Suspect", 3: "Pathological"}
        prediction_label = labels.get(int(prediction), "Unknown")
        
        # Get confidence if model supports predict_proba
        confidence = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_data_scaled)[0]
            confidence = float(max(probabilities))
        
        return {
            "prediction": int(prediction),
            "prediction_label": prediction_label,
            "confidence": confidence
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error making prediction: {str(e)}"
        )


@app.get("/dataset/info")
async def dataset_info():
    """Get information about the dataset"""
    dataset_path = DATASETS_DIR / "fetal_health.csv"
    
    if not dataset_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )
    
    try:
        df = pd.read_csv(dataset_path)
        
        return {
            "total_samples": len(df),
            "features": len(df.columns) - 1,  # Excluding target column
            "columns": df.columns.tolist(),
            "target_distribution": df['fetal_health'].value_counts().to_dict() if 'fetal_health' in df.columns else None,
            "missing_values": df.isnull().sum().to_dict()
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading dataset: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
