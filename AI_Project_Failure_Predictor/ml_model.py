# Placeholder for ML logic
# In full project: generate risk scores using trained ML model

def generate_risk_scores(df):
    """
    Placeholder function to generate risk scores.
    Returns the same dataframe with a RiskScore column (demo random scores).
    """
    import numpy as np
    df['RiskScore'] = np.round(np.random.uniform(0.1, 0.9, size=len(df)), 2)
    return df