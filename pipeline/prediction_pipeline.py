import joblib
import numpy as np
import pandas as pd
from config.paths_config import *
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

model = joblib.load(MODEL_OUTPUT_PATH)
logger.info("Model loaded successfully")


def predict(input_data: dict) -> dict:
    """
    Makes a prediction for a single patient.

    Parameters
    ----------
    input_data : dict
        Dictionary of feature names and their values.
        Example:
        {
            "age": 48,
            "blood_pressure": 80,
            "specific_gravity": 1.020,
            ...
        }

    Returns
    -------
    dict
        {
            "prediction": 0 or 1,
            "label": "CKD" or "Not CKD",
            "confidence": float  # highest class probability from the model
        }
    """
    try:
        logger.info(f"Received input for prediction: {input_data}")

        input_df = pd.DataFrame([input_data])

        prediction = model.predict(input_df)[0]
        confidence = float(np.max(model.predict_proba(input_df)))

        label = "CKD" if prediction == 0 else "Not CKD"

        result = {
            "prediction": int(prediction),
            "label": label,
            "confidence": round(confidence, 4),
        }

        logger.info(f"Prediction result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise CustomException("Failed to make prediction", e)


if __name__ == "__main__":
    # Sample input — values must be in processed format (encoded + imputed)
    sample_input = {
        "age": 48,
        "blood_pressure": 80,
        "specific_gravity": 1.020,
        "albumin": 1,
        "sugar": 0,
        "red_blood_cells": 1,
        "pus_cell": 1,
        "pus_cell_clumps": 0,
        "bacteria": 0,
        "blood_glucose_random": 121,
        "blood_urea": 36,
        "serum_creatinine": 1.2,
        "sodium": 137,
        "potassium": 4.5,
        "haemoglobin": 15.4,
        "packed_cell_volume": 44,
        "white_blood_cell_count": 7800,
        "red_blood_cell_count": 5.2,
        "hypertension": 1,
        "diabetes_mellitus": 0,
        "coronary_artery_disease": 0,
        "appetite": 1,
        "peda_edema": 0,
        "aanemia": 0,
    }

    result = predict(sample_input)
    print(f"\nPrediction : {result['label']}")
    print(f"Confidence : {result['confidence']:.2%}")