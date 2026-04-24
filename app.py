from flask import Flask, render_template, request
from pipeline.prediction_pipeline import predict
from src.logger import get_logger
from src.custom_exception import CustomException

app = Flask(__name__)
logger = get_logger(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        try:
            input_data = {
                "age":                    float(request.form["age"]),
                "blood_pressure":         float(request.form["blood_pressure"]),
                "specific_gravity":       float(request.form["specific_gravity"]),
                "albumin":                float(request.form["albumin"]),
                "sugar":                  float(request.form["sugar"]),
                "red_blood_cells":        int(request.form["red_blood_cells"]),
                "pus_cell":               int(request.form["pus_cell"]),
                "pus_cell_clumps":        int(request.form["pus_cell_clumps"]),
                "bacteria":               int(request.form["bacteria"]),
                "blood_glucose_random":   float(request.form["blood_glucose_random"]),
                "blood_urea":             float(request.form["blood_urea"]),
                "serum_creatinine":       float(request.form["serum_creatinine"]),
                "sodium":                 float(request.form["sodium"]),
                "potassium":              float(request.form["potassium"]),
                "haemoglobin":            float(request.form["haemoglobin"]),
                "packed_cell_volume":     float(request.form["packed_cell_volume"]),
                "white_blood_cell_count": float(request.form["white_blood_cell_count"]),
                "red_blood_cell_count":   float(request.form["red_blood_cell_count"]),
                "hypertension":           int(request.form["hypertension"]),
                "diabetes_mellitus":      int(request.form["diabetes_mellitus"]),
                "coronary_artery_disease":int(request.form["coronary_artery_disease"]),
                "appetite":               int(request.form["appetite"]),
                "peda_edema":             int(request.form["peda_edema"]),
                "aanemia":                int(request.form["aanemia"]),
            }

            result = predict(input_data)
            logger.info(f"Prediction served: {result}")

        except CustomException as ce:
            error = str(ce)
            logger.error(f"CustomException in /: {error}")
        except Exception as e:
            error = "An unexpected error occurred. Please check your inputs."
            logger.error(f"Unexpected error in /: {e}")

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)