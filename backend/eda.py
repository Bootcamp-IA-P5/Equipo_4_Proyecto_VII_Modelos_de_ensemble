"""
Exploratory Data Analysis (EDA) for Fetal Health Dataset
This script performs comprehensive EDA including:
- Data loading and overview
- Missing values and duplicates analysis
- Target variable distribution
- Class imbalance evaluation
- Feature correlations
Note: Visualization code removed for containerized execution
"""

import pandas as pd
import numpy as np
import warnings

from configure import RAW_DATA, DATA_DIR
from src.load_data import load_data

# Suppress warnings
warnings.filterwarnings('ignore')


def print_section_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def analyze_dataset_overview(df):
    """Analyze basic dataset information"""
    print_section_header("1. OVERVIEW OF THE DATASET")
    
    # Display first rows
    print("First 5 rows:")
    print(df.head())
    
    # Basic information
    print("\n" + "-" * 80)
    print("Dataset Information:")
    df.info()
    
    # Dimensions
    print("\n" + "-" * 80)
    print(f"Dataset Shape: {df.shape[0]} rows and {df.shape[1]} columns")
    
    return df


def analyze_missing_values(df):
    """Check for missing values"""
    print_section_header("2. MISSING VALUES ANALYSIS")
    
    # Print missing values count
    missing_count = df.isnull().sum()
    print("\nMissing values per column:")
    if missing_count.any():
        print(missing_count[missing_count > 0])
    else:
        print("No missing values found ✅")


def analyze_duplicates(df):
    """Check for duplicate rows"""
    print_section_header("3. DUPLICATE ROWS ANALYSIS")
    
    duplicates_count = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates_count}")
    
    if duplicates_count > 0:
        print(f"Percentage of duplicates: {(duplicates_count / len(df)) * 100:.2f}%")
        print("\nNote: These duplicates are likely valid data (different cardiotocograms")
        print("      with the same values), so we will keep them in the dataset.")
    else:
        print("✅ No duplicates found")


def analyze_descriptive_stats(df):
    """Generate descriptive statistics"""
    print_section_header("4. DESCRIPTIVE STATISTICS")
    
    print("Statistical summary (transposed):")
    print(df.describe().T)


def plot_feature_distributions(df):
    """Print feature distribution statistics"""
    print_section_header("5. FEATURE DISTRIBUTIONS")
    
    print("Feature distribution statistics:")
    print(df.describe().T[['mean', 'std', 'min', '25%', '50%', '75%', 'max']])


def analyze_target_variable(df):
    """Analyze target variable distribution and class balance"""
    print_section_header("6. TARGET VARIABLE ANALYSIS (fetal_health)")
    
    # Calculate class counts and percentages
    class_counts = df['fetal_health'].value_counts().sort_index()
    class_percentages = df['fetal_health'].value_counts(normalize=True).sort_index() * 100
    
    print(f"\nTotal observations: {len(df)}")
    print("\nClass distribution:")
    for idx, (count, pct) in enumerate(zip(class_counts, class_percentages), 1):
        class_name = {1: 'Normal', 2: 'Sospechoso', 3: 'Patológico'}.get(idx, f'Class {idx}')
        print(f"  Class {idx} ({class_name}): {count} ({pct:.2f}%)")


def evaluate_class_balance(df):
    """Evaluate class imbalance and provide recommendations"""
    print_section_header("7. CLASS BALANCE EVALUATION")
    
    class_counts = df['fetal_health'].value_counts().sort_index()
    class_percentages = df['fetal_health'].value_counts(normalize=True).sort_index() * 100
    
    # Calculate imbalance metrics
    max_class = class_counts.max()
    min_class = class_counts.min()
    imbalance_ratio = max_class / min_class
    
    print("EVALUACIÓN DE BALANCE DE CLASES")
    print("-" * 60)
    print(f"\nClase mayoritaria: {class_counts.idxmax()} con {max_class} observaciones ({class_percentages.max():.2f}%)")
    print(f"Clase minoritaria: {class_counts.idxmin()} con {min_class} observaciones ({class_percentages.min():.2f}%)")
    print(f"\nRatio de desbalance: {imbalance_ratio:.2f}:1")
    print("-" * 60)
    
    # Interpretation
    print("\nINTERPRETACIÓN:")
    if imbalance_ratio < 1.5:
        print("✅ Dataset BALANCEADO - No se requieren técnicas especiales de balanceo")
        print("   Puedes usar accuracy como métrica principal")
    elif 1.5 <= imbalance_ratio < 3:
        print("⚠️  Desbalance MODERADO - Considerar técnicas de balanceo")
        print("   Usar métricas: F1-score, Precision, Recall")
        print("   Técnicas sugeridas: class_weight='balanced' en modelos")
    else:
        print("🔴 Desbalance SEVERO - Técnicas de balanceo NECESARIAS")
        print("    - Usar métricas: F1-score macro/weighted, ROC-AUC")
        print("    - Técnicas sugeridas: SMOTE, undersampling, o class_weight")
        print("    - Usar stratified split en train/test")
    
    print("-" * 60)


def analyze_correlations(df):
    """Analyze feature correlations"""
    print_section_header("8. CORRELATION ANALYSIS")
    
    print("Calculating correlation matrix...")
    
    # Calculate correlation matrix
    corrmat = df.corr()
    
    # Find highly correlated features
    print("\nHighly correlated features (|correlation| > 0.7):")
    high_corr = []
    for i in range(len(corrmat.columns)):
        for j in range(i+1, len(corrmat.columns)):
            if abs(corrmat.iloc[i, j]) > 0.7:
                high_corr.append((corrmat.columns[i], corrmat.columns[j], corrmat.iloc[i, j]))
    
    if high_corr:
        for feat1, feat2, corr in sorted(high_corr, key=lambda x: abs(x[2]), reverse=True):
            print(f"  {feat1} <-> {feat2}: {corr:.3f}")
    else:
        print("  No features with correlation > 0.7 found")
    
    # Features with low correlation to target
    if 'fetal_health' in corrmat.columns:
        target_corr = corrmat['fetal_health'].abs().sort_values(ascending=True)
        print("\nFeatures with lowest correlation to target (|correlation| < 0.1):")
        low_corr_features = target_corr[target_corr < 0.1].drop('fetal_health', errors='ignore')
        if len(low_corr_features) > 0:
            for feat, corr in low_corr_features.items():
                print(f"  {feat}: {corrmat.loc[feat, 'fetal_health']:.3f}")
            print("\n  💡 Consider removing these features during feature selection")
        else:
            print("  All features show meaningful correlation with target")


def save_clean_dataset(df):
    """Save cleaned dataset"""
    print_section_header("9. SAVING CLEAN DATASET")
    
    processed_path = DATA_DIR / "processed" / "fetal_health_clean.csv"
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(processed_path, index=False)
    print(f"✅ Dataset guardado en: {processed_path}")
    print(f"   Filas: {df.shape[0]} | Columnas: {df.shape[1]}")


def generate_eda_summary(df):
    """Generate EDA summary report"""
    print_section_header("10. EDA SUMMARY")
    
    summary = f"""
EDA SUMMARY REPORT
{'=' * 80}

Dataset Characteristics:
- Total observations: {df.shape[0]}
- Total features: {df.shape[1] - 1} (predictors)
- Target variable: fetal_health
- Data types: All numeric (float64)
- Missing values: {df.isnull().sum().sum()}
- Duplicate rows: {df.duplicated().sum()}

Target Variable Distribution:
{df['fetal_health'].value_counts().sort_index().to_string()}

Class Balance:
- Imbalance ratio: {df['fetal_health'].value_counts().max() / df['fetal_health'].value_counts().min():.2f}:1

Key Findings:
1. Dataset is complete with no missing values
2. All features are numeric, ready for modeling
3. {df.duplicated().sum()} duplicate rows found (likely valid data)
4. Class distribution shows {'moderate' if 1.5 <= df['fetal_health'].value_counts().max() / df['fetal_health'].value_counts().min() < 3 else 'severe' if df['fetal_health'].value_counts().max() / df['fetal_health'].value_counts().min() >= 3 else 'balanced'} imbalance

Recommendations:
- Use stratified train-test split
- Consider SMOTE or class_weight for imbalance handling
- Use F1-score, Precision, Recall as primary metrics
- Monitor overfitting due to class imbalance

Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 80}
"""
    
    print(summary)
    
    # Save summary to file
    summary_path = DATA_DIR / "processed" / "eda_summary.txt"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w') as f:
        f.write(summary)
    print(f"\n✅ Summary saved to: {summary_path}")


def main():
    """Main EDA execution function"""
    print("\n" + "=" * 80)
    print("  EXPLORATORY DATA ANALYSIS - FETAL HEALTH DATASET")
    print("=" * 80)
    
    # Load data
    print("\nLoading dataset...")
    df = load_data(RAW_DATA / "fetal_health.csv")
    print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Execute all EDA steps
    analyze_dataset_overview(df)
    analyze_missing_values(df)
    analyze_duplicates(df)
    analyze_descriptive_stats(df)
    plot_feature_distributions(df)
    analyze_target_variable(df)
    evaluate_class_balance(df)
    analyze_correlations(df)
    save_clean_dataset(df)
    generate_eda_summary(df)
    
    print("\n" + "=" * 80)
    print("  EDA COMPLETED SUCCESSFULLY! ✅")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - datasets/processed/fetal_health_clean.csv")
    print("  - datasets/processed/eda_summary.txt")
    print("\n")


if __name__ == "__main__":
    main()
