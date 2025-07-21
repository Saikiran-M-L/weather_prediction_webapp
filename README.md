# 🌤️ Weather Prediction Web Application

This is a full-stack machine learning project that predicts weather conditions (temperature, humidity, windspeed, etc.) for a specified city and date. It uses a two-stage ML pipeline and provides a web interface for interaction.

---

## Features

- Predicts:

  - Temperature
  - Humidity
  - Precipitation
  - Wind Speed
  - Feels Like Temperature
  - Sea Level Pressure
  - Weather Description
  - Weather Icon

- Two-stage ML model:

  - Stage 1: Generates engineered weather features using city and date
  - Stage 2: Predicts final outputs using generated features

- Flask backend with REST API

- Frontend using HTML, CSS, JavaScript, and Vue.js

- Deployment ready on Render (Docker or Python environment)

---

## 💠 Tech Stack

- Python 3.10
- Flask
- scikit-learn, XGBoost
- HTML, CSS, JS, Vue.js
- Render for deployment
- Git LFS for large model files

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
To clone the repository, you need to install Git LFS first, as the repository contains large files that are managed using Git LFS.
git clone https://github.com/your-username/weather-predictor.git
cd weather-predictor
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally (for testing)

```bash
python app/app.py
```

Then open: http\://localhost:4500/

---

## 🚀 Deployment on Render

Choose one of the following methods:

### Option 1: Python Environment

- Connect GitHub repo to Render
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn app:app`
- Set port using environment variable: `PORT=8000`

### Option 2: Docker Environment

- Add a Dockerfile with gunicorn command (bind to `${PORT}`)
- Set Render environment to Docker
- Set port to 8000 or use Render’s default `$PORT`

---

## 🌐 API Endpoint

### POST `/predict`

Request Body:

```json
{
  "city": "Berlin",
  "datetime": "2025-08-01"
}
```

Response:

```json
{
  "weather_metrics": {
    "temp": 24.5,
    "humidity": 60,
    "precip": 0.8,
    "windspeed": 15,
    "feelslike": 25.2,
    "sealevelpressure": 1012.3,
    "description": "Partly cloudy",
    "icon": "partly-cloudy-day"
  }
}
```

---

## ❗ Notes

- Use Git LFS to manage .pkl files over 100MB.
- CORS enabled globally via flask-cors for API access from frontend.
- Supports Vue.js frontend served from Flask or separately deployed.

---

## 📃 License

This project is licensed under the MIT License. See LICENSE file for details.

