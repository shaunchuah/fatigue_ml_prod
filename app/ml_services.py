import base64
import pickle
from io import BytesIO

import keras
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import shap
from joblib import load

from .constants import NUMERICAL_FEATURES

matplotlib.use("agg")


def load_ml_resources():
    model = keras.saving.load_model("source_model/fatigue_model.keras")
    scaler = load("source_model/scaler.pkl")
    return model, scaler


def prepare_dataframe(formatted_data: dict, scaler) -> pd.DataFrame:
    """
    Takes in formatted data, loads it in the correct structure
    and scales the numerical features using standard scaler
    """
    df = pd.read_csv("source_model/X_train.csv")
    df = df.iloc[0:0]
    df = pd.DataFrame.from_records([formatted_data])
    df[NUMERICAL_FEATURES] = scaler.transform(df[NUMERICAL_FEATURES])
    return df


def generate_force_plot(df, scaler) -> str:
    """
    Takes in SHAP KernelExplainer object, input dataframe and sklearn standard scaler
    Returns a base64 encoded image of the force plot
    """
    # Inverse transform for clearer visualization
    with open("source_model/shap_explainer.pkl", "rb") as f:
        explainer = pickle.load(f)
    shap_values = explainer.shap_values(df.iloc[0])
    # Very important
    # Reverse transform needs to be performed after the shap values are calculated
    df[NUMERICAL_FEATURES] = scaler.inverse_transform(df[NUMERICAL_FEATURES])
    buf = BytesIO()
    shap.force_plot(
        base_value=explainer.expected_value[0],
        shap_values=shap_values[:, 0],
        features=df.iloc[0],
        matplotlib=True,
        contribution_threshold=0.05,
        text_rotation=30,
        show=False,
    )
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    return "data:image/png;base64," + base64.b64encode(buf.getbuffer()).decode("ascii")
