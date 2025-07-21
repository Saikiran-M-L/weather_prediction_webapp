"""Flask API"""
import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR,  "models")

app = Flask(__name__, static_folder='static', template_folder='templates')

CORS(app)

# Load models and encoders
stage1_model = joblib.load(os.path.join(MODELS_DIR, "stage1_model.pkl"))
regressor = joblib.load(os.path.join(MODELS_DIR, "regressor.pkl"))
clf_desc = joblib.load(os.path.join(MODELS_DIR, "description_classifier.pkl"))
clf_icon = joblib.load(os.path.join(MODELS_DIR, "icon_classifier.pkl"))
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
le_desc = joblib.load(os.path.join(MODELS_DIR, "label_encoder_description.pkl"))
le_icon = joblib.load(os.path.join(MODELS_DIR, "label_encoder_icon.pkl"))
city_encoder = joblib.load(os.path.join(MODELS_DIR, "stage1_city_encoder.pkl"))

target_columns = [
    "tempmax",
    "tempmin",
    "feelslikemax",
    "feelslikemin",
    "dew",
    "precipprob",
    "precipcover",
    "snow",
    "snowdepth",
    "windgust",
    "winddir",
    "cloudcover",
    "solarradiation",
    "solarenergy",
    "uvindex",
]

cities = [
    "city_Berlin",
    "city_Cologne",
    "city_Frankfurt",
    "city_Hamburg",
    "city_Munich",
]

regression_targets = [
    "temp",
    "humidity",
    "precip",
    "windspeed",
    "feelslike",
    "sealevelpressure",
]

city_columns = city_encoder.get_feature_names_out(["city"])


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
def predict():
    """Prediction of weather with the given inputs City and Date

    Returns:
        _type_: _description_
    """
    try:
        data = request.get_json()
        dt = datetime.strptime(data["datetime"], "%Y-%m-%d")
        year = dt.year
        month = dt.month
        dayofyear = dt.timetuple().tm_yday
        sin_dayofyear = np.sin(2 * np.pi * dayofyear / 365)
        cos_dayofyear = np.cos(2 * np.pi * dayofyear / 365)

        # One-hot encode city
        city_encoded = city_encoder.transform([[data["city"]]])

        # Prepare input DataFrame
        X_new = pd.DataFrame(
            city_encoded, columns=city_encoder.get_feature_names_out(["city"])
        )
        X_new["year"] = year
        X_new["month"] = month
        X_new["sin_dayofyear"] = sin_dayofyear
        X_new["cos_dayofyear"] = cos_dayofyear

        # Predict stage 1 outputs
        y_pred = stage1_model.predict(X_new)

        stage1_predict = dict(zip(target_columns, y_pred[0]))
        stage1_predict["date"] = data["datetime"]
        stage1_predict["name"] = data["city"]

        # Stage 2 predict
        city_vector = [
            1 if f"city_{stage1_predict['name']}" ==
            city else 0 for city in cities
        ]

        X_input = np.array(
            [
                stage1_predict["tempmax"],
                stage1_predict["tempmin"],
                stage1_predict["feelslikemax"],
                stage1_predict["feelslikemin"],
                stage1_predict["dew"],
                stage1_predict["precipprob"],
                stage1_predict["precipcover"],
                stage1_predict["snow"],
                stage1_predict["snowdepth"],
                stage1_predict["windgust"],
                stage1_predict["winddir"],
                stage1_predict["cloudcover"],
                stage1_predict["solarradiation"],
                stage1_predict["solarenergy"],
                stage1_predict["uvindex"],
                year,
                month,
                sin_dayofyear,
                cos_dayofyear,
            ]
            + city_vector
        ).reshape(1, -1)

        # Scale
        X_scaled = scaler.transform(X_input)

        # Stage 2 prediction process

        # Regression prediction
        y_reg_pred = regressor.predict(X_scaled)

        # Classification predictions
        y_desc_pred = clf_desc.predict(X_scaled)
        y_icon_pred = clf_icon.predict(X_scaled)

        # Decode class labels
        description_label = le_desc.inverse_transform(y_desc_pred)[0]
        icon_label = le_icon.inverse_transform(y_icon_pred)[0]

        # Convert regression output to dict
        reg_output = dict(zip(regression_targets, y_reg_pred[0]))

        # Combine with classification
        reg_output["description"] = description_label
        reg_output["icon"] = icon_label

        # Rounding of values to 2 decimal places
        reg_output["feelslike"] = round(reg_output["feelslike"], 2)
        reg_output["humidity"] = round(reg_output["humidity"], 2)
        reg_output["precip"] = round(reg_output["precip"], 2)
        reg_output["sealevelpressure"] = round(reg_output["sealevelpressure"],
                                               2)
        reg_output["temp"] = round(reg_output["temp"], 2)
        reg_output["windspeed"] = round(reg_output["windspeed"], 2)

        return jsonify({"weather_metrics": reg_output})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4500, debug=True)
