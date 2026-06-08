import numpy as np
import polars as pl

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.detection.anomaly_features import (
    ANOMALY_FEATURE_COLUMNS,
)


def run_isolation_forest(
    anomaly_features: pl.DataFrame,
    contamination: float = 0.03,
    random_state: int = 42,
) -> pl.DataFrame:
    if anomaly_features.height == 0:
        return pl.DataFrame()

    pdf = anomaly_features.to_pandas()

    x = pdf[ANOMALY_FEATURE_COLUMNS].fillna(0)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    model = IsolationForest(
        n_estimators=300,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )

    model_labels = model.fit_predict(x_scaled)
    decision_scores = model.decision_function(x_scaled)

    raw_anomaly = -decision_scores

    min_score = float(np.min(raw_anomaly))
    max_score = float(np.max(raw_anomaly))

    if max_score == min_score:
        normalized = np.zeros_like(raw_anomaly)
    else:
        normalized = (
            (raw_anomaly - min_score)
            / (max_score - min_score)
        ) * 100

    pdf["isolation_forest_label"] = model_labels
    pdf["isolation_forest_decision_score"] = decision_scores
    pdf["anomaly_score"] = normalized
    pdf["is_anomalous"] = model_labels == -1

    return pl.from_pandas(pdf)