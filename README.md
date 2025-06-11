# Cyclone Intensity Prediction

## Introduction

This project predicts cyclone intensity using machine learning. It integrates a Flutter application for user interaction, a FastAPI backend for processing and model serving, and a Weather API for real-time data.

## Features

- Real-time cyclone intensity prediction.
- User-friendly Flutter interface.
- Robust FastAPI backend.
- Integration with Weather API for up-to-date information.

## Tech Stack

- **Frontend:** Flutter
- **Backend:** FastAPI (Python)
- **Machine Learning:** Scikit-learn, Pandas, Numpy
- **Data Source:** Weather API

## Data Flow (Flutter App Integration)

Flutter → (lat, lon) → FastAPI → Weather API → Feature preparation → ML Model (predict cyclone severity) → Response → Flutter shows prediction

## Installation

### Prerequisites

- Flutter SDK
- Python 3.8+
- Pip

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cyclone-intensity-prediction.git
   cd cyclone-intensity-prediction/backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Create a `.env` file in the `backend` directory with your Weather API key:
   ```env
   WEATHER_API_KEY=your_weather_api_key
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Run the Flutter app:
   ```bash
   flutter run
   ```

## Usage

- Open the Flutter app.
- Allow location access or manually input coordinates.
- View the cyclone intensity prediction.

## Machine Learning Model

- **Model:** [Specify model used, e.g., Random Forest, Gradient Boosting]
- **Features:** [List features used, e.g., temperature, humidity, wind speed]
- **Training:** [Briefly describe training data and process]

## API Endpoints

- `POST /predict`: Accepts latitude and longitude, returns cyclone intensity prediction.
  - Request: `{"lat": float, "lon": float}`
  - Response: `{"severity": str, "details": {}}`

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
