# Fetal Health Classification - Ensemble Models Project

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-orange.svg)

A machine learning project for fetal health classification using ensemble models, featuring automated hyperparameter optimization, containerized deployment, and interactive web interfaces.

**[📋 Project Management](https://github.com/orgs/Bootcamp-IA-P5/projects/5)** | **[📊 Dataset on Kaggle](https://www.kaggle.com/datasets/andrewmvd/fetal-health-classification/data)**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Model Training](#model-training)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Results](#results)
- [Team](#team)

## 🎯 Overview

This project implements a multiclass classification system to predict fetal health status from cardiotocographic (CTG) data. The system uses ensemble machine learning models with automated hyperparameter optimization to classify fetal health into three categories:

1. **Normal** (Class 1)
2. **Suspect** (Class 2)
3. **Pathological** (Class 3)

The project includes:
- Automated EDA (Exploratory Data Analysis)
- Model training with GridSearchCV optimization
- RESTful API for predictions
- Interactive Streamlit dashboard
- Fully containerized deployment with Docker

## ✨ Features

### Machine Learning
- **Ensemble Models**: Random Forest, Gradient Boosting, AdaBoost, Bagging, XGBoost
- **Baseline Models**: Logistic Regression, Decision Tree, KNN, Naive Bayes, SVM
- **Automated Optimization**: GridSearchCV for hyperparameter tuning
- **Class Imbalance Handling**: SMOTE oversampling
- **Cross-Validation**: Stratified K-Fold validation

### Application
- **FastAPI Backend**: RESTful API with automatic documentation
- **Streamlit Frontend**: Interactive web interface for predictions
- **Docker Deployment**: Multi-container orchestration
- **Model Persistence**: Serialized models with joblib
- **Comprehensive Logging**: Training metrics and reports

## 📁 Project Structure

```
Equipo_4_Proyecto_VII_Modelos_de_ensemble/
├── backend/                    # FastAPI backend service
│   ├── app/
│   │   ├── main.py            # API endpoints
│   │   ├── routes/            # API route handlers (modular structure)
│   │   └── services/          # Business logic services
│   ├── configure.py           # Path configuration
│   ├── eda.py                 # Exploratory Data Analysis script
│   ├── setup.py               # Package setup
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend container definition
├── frontend/                   # Streamlit frontend service
│   ├── app.py                 # Streamlit dashboard
│   ├── requirements.txt       # Frontend dependencies
│   └── Dockerfile             # Frontend container definition
├── src/                        # Source code
│   ├── train_model.py         # Model training pipeline
│   └── load_data.py           # Data loading utilities
├── data/                       # Data directory (mounted volume)
│   ├── raw/                   # Original dataset
│   └── processed/             # Cleaned/processed data
├── models/                     # Trained models (mounted volume)
│   ├── fetal_health_model.pkl
│   └── scaler.pkl
├── reports/                    # Training reports and metrics (mounted volume)
│   ├── metrics_*.json
│   ├── model_comparison_*.csv
│   └── best_model_report_*.txt
├── notebooks/                  # Jupyter notebooks for analysis
├── docker-compose.yml          # Multi-container orchestration
└── README.md                   # This file
```

## 🛠 Technologies

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for FastAPI
- **Pydantic** - Data validation using Python type annotations
- **scikit-learn** - Machine learning library
- **XGBoost** - Gradient boosting framework
- **imbalanced-learn** - SMOTE for handling class imbalance
- **SHAP** - Model explainability

### Frontend
- **Streamlit** - Framework for data science web apps
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Data visualization

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Python 3.11** - Programming language

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- Git (for cloning the repository)
- At least 4GB of available RAM

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bootcamp-IA-P5/Equipo_4_Proyecto_VII_Modelos_de_ensemble.git
   cd Equipo_4_Proyecto_VII_Modelos_de_ensemble
   ```

2. **Ensure the dataset is in place**
   ```bash
   # The dataset should be at:
   data/raw/fetal_health.csv
   ```

3. **Build and start the services**
   ```bash
   docker compose up --build
   ```

4. **Access the applications**
   - **Frontend (Streamlit)**: http://localhost:8501
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

## 📊 Usage

### Using the Web Interface (Streamlit)

1. Navigate to http://localhost:8501
2. Enter the CTG parameters in the input fields
3. Click "Predict" to get the classification result
4. View the prediction confidence and class label

### Using the API

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Make a Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "baseline_value": 120.0,
    "accelerations": 0.0,
    "fetal_movement": 0.0,
    "uterine_contractions": 0.0,
    "light_decelerations": 0.0,
    "severe_decelerations": 0.0,
    "prolongued_decelerations": 0.0,
    ...
  }'
```

#### Get Dataset Info
```bash
curl http://localhost:8000/dataset/info
```

## 🎓 Model Training

### Running the Complete Training Pipeline

The training pipeline includes EDA, data preprocessing, model training with hyperparameter optimization, and evaluation:

```bash
docker compose --profile training up train-model
```

This will:
1. **Install dependencies** in editable mode
2. **Run EDA script** (`backend/eda.py`)
   - Analyze data quality
   - Generate statistics
   - Save cleaned dataset to `data/processed/`
3. **Train models** (`src/train_model.py`)
   - Train baseline models
   - Optimize ensemble models with GridSearchCV
   - Evaluate and compare all models
   - Save best model to `models/`
   - Generate reports in `reports/`

### Training Configuration

The training pipeline uses:
- **Test Split**: 20% of data
- **Cross-Validation**: 5-fold Stratified K-Fold
- **SMOTE**: Applied to balance training classes
- **Optimization**: GridSearchCV for ensemble models
- **Metrics**: Accuracy, Precision, Recall, F1-Score

### Models Trained

**Baseline Models** (default hyperparameters):
- Logistic Regression
- Decision Tree
- K-Nearest Neighbors
- Naive Bayes
- Support Vector Machine

**Ensemble Models** (with GridSearchCV optimization):
- Random Forest
- Gradient Boosting
- AdaBoost
- Bagging Classifier
- Voting Classifier (ensemble of ensembles)
- Stacking Classifier

### Output Files

After training, you'll find:
- `models/fetal_health_model.pkl` - Best trained model
- `models/scaler.pkl` - Fitted StandardScaler
- `reports/metrics_*.json` - All model metrics
- `reports/model_comparison_*.csv` - Model comparison table
- `reports/best_model_report_*.txt` - Detailed best model report
- `data/processed/fetal_health_clean.csv` - Cleaned dataset
- `data/processed/eda_summary.txt` - EDA summary report

## 📖 API Documentation

### Interactive Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### `GET /`
Root endpoint with API information.

#### `GET /health`
Health check endpoint.

#### `POST /predict`
Make a fetal health prediction.

**Request Body**: 21 CTG features including baseline value, accelerations, decelerations, variability, and histogram features.

**Response**:
```json
{
  "prediction": 1,
  "prediction_label": "Normal",
  "confidence": 0.95
}
```

#### `GET /dataset/info`
Get information about the dataset including total samples, features, class distribution, and missing values.

## 🔧 Development

### Running Individual Services

**Backend only:**
```bash
docker compose up backend
```

**Frontend only:**
```bash
docker compose up frontend
```

**Training only:**
```bash
docker compose --profile training up train-model
```

### Rebuilding After Changes

```bash
docker compose up --build
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f train-model
```

### Stopping Services

```bash
# Stop and remove containers
docker compose down

# Stop, remove containers and volumes
docker compose down -v
```

### Local Development (Without Docker)

1. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   ```

2. **Run backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Run frontend** (in another terminal)
   ```bash
   streamlit run frontend/app.py --server.port 8501
   ```

4. **Run training**
   ```bash
   python src/train_model.py
   ```

## 📈 Results

### Model Performance

The best performing model (typically AdaBoost or Random Forest) achieves:
- **Test Accuracy**: ~95%
- **Cross-Validation Score**: ~98%
- **Precision**: ~95%
- **Recall**: ~95%
- **F1-Score**: ~95%

Detailed results are available in:
- `reports/model_comparison_*.csv` - Comparison of all models
- `reports/best_model_report_*.txt` - Detailed best model metrics

### Class Distribution

The dataset shows class imbalance:
- **Normal (Class 1)**: ~78% (1655 samples)
- **Suspect (Class 2)**: ~14% (295 samples)
- **Pathological (Class 3)**: ~8% (176 samples)

SMOTE is applied during training to handle this imbalance.

## 👥 Team

**Equipo 4** - Bootcamp IA P5

## 📝 License

This project is part of an educational bootcamp and is intended for learning purposes.

## 🙏 Acknowledgments

- Dataset: [Fetal Health Classification from CTG data](https://www.kaggle.com/datasets/andrewmvd/fetal-health-classification/data)
- Bootcamp IA P5 instructors and mentors
- scikit-learn and FastAPI communities

---

**Note**: This is a machine learning project for educational purposes. Medical decisions should always be made by qualified healthcare professionals.

