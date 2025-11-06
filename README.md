# Vehicle Price Analytics Platform

A professional ML-powered predictive analytics platform for vehicle price optimization built with Streamlit.

## Features

- 📊 **Analytics Dashboard**: Market insights and profitability analysis
- 💰 **Price Prediction**: ML-based vehicle price predictions using ensemble models
- 📈 **Interactive Visualizations**: Colorful charts powered by Plotly
- 🎨 **Modern UI**: Clean, professional interface inspired by shadcn/ui

## Tech Stack

- Python 3.x
- Streamlit
- Scikit-learn
- XGBoost
- Pandas & NumPy
- Plotly

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Project-DA
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Model Files

**Important**: The trained model files are not included in the repository due to their large size (>250MB). You need to train the models first.

Run the Jupyter notebook to train the models:

```bash
jupyter notebook final_project_da.ipynb
```

Execute all cells in the notebook. This will:
- Load and process the dataset
- Train the ML models (Linear Regression, Random Forest, XGBoost)
- Save the trained models to the `models/` directory:
  - `lr_model.pkl`
  - `rf_model.pkl`
  - `xgb_model.pkl`
  - `label_encoders.pkl`
  - `scaler.pkl`

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
Project-DA/
├── app.py                  # Main Streamlit application
├── predictor.py            # Prediction logic
├── final_project_da.ipynb  # Model training notebook
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── data/                   # Business intelligence data
│   ├── bi_make.csv
│   ├── bi_condition.csv
│   └── bi_margin_sample.csv
├── dataset/               # Raw dataset (not in git)
│   └── car_prices.csv
└── models/                # Trained models (not in git)
    ├── lr_model.pkl
    ├── rf_model.pkl
    ├── xgb_model.pkl
    ├── label_encoders.pkl
    └── scaler.pkl
```

## Dataset

The platform uses 558,837 real-world auction records with 16 features including vehicle specifications, condition metrics, and pricing data.

## Model Performance

- **Linear Regression**: R² = 0.954, RMSE = $1,123
- **Random Forest**: R² = 0.963, RMSE = $1,011  
- **XGBoost**: R² = 0.971, RMSE = $892
- **Ensemble Model**: R² = 0.969, RMSE = $924

## Academic Information

- **Course**: Data Analytics and Intelligence
- **Institution**: Unitec
- **Platform**: ML-powered vehicle price analytics with 96.9% accuracy
