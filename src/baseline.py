
from sklearn.preprocessing import StandardScaler
import pandas as pd

def escalar_features(X):
    '''
    Escala las características utilizando StandardScaler.
    '''
    col_names = list(X.columns)
    s_scaler = StandardScaler()
    X_scaled= s_scaler.fit_transform(X)
    return pd.DataFrame(X_scaled, columns=col_names)