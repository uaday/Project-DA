# predictor.py
import numpy as np
import joblib

# Load once (module-level) - Using only XGBoost for deployment
_xgb = joblib.load("models/xgb_model.pkl")
_label_encoders = joblib.load("models/label_encoders.pkl")

LUXURY_BRANDS = ['Mercedes-Benz','BMW','Audi','Lexus','Porsche','Jaguar','Land Rover','Cadillac','Tesla','Maserati']
CURRENT_YEAR = 2015

def safe_encode(col, value):
    le = _label_encoders[col]
    if value in le.classes_:
        return le.transform([value])[0]
    # Handle unseen categories by mapping to a fallback
    # Add a temporary extended classes_ if needed
    try:
        le.classes_ = np.append(le.classes_, value)
        return le.transform([value])[0]
    except:
        # fallback to the first class
        return le.transform([le.classes_[0]])[0]

def predict_vehicle_price(year, make, body, transmission, odometer, condition, mmr, is_luxury=None):
    vehicle_age = CURRENT_YEAR - int(year)
    if is_luxury is None:
        is_luxury = 1 if make in LUXURY_BRANDS else 0

    make_enc = safe_encode('make', str(make))
    # body_simplified in your training—if body is unseen, push to 'Other'
    body_classes = list(_label_encoders['body_simplified'].classes_)
    body = body if body in body_classes else 'Other'
    body_enc = safe_encode('body_simplified', str(body))

    transmission = str(transmission).lower()
    trans_enc = safe_encode('transmission', transmission)

    feats = np.array([[vehicle_age, odometer, condition, mmr, is_luxury,
                       make_enc, body_enc, trans_enc]])

    # XGBoost prediction (R² = 0.971, RMSE = $892)
    pred_xgb = float(_xgb.predict(feats)[0])

    margin_xgb = (pred_xgb - mmr) / mmr * 100

    # Confidence interval based on model RMSE
    rmse = 892  # From model evaluation
    ci_low  = pred_xgb - 1.96 * rmse
    ci_high = pred_xgb + 1.96 * rmse

    return {
        "predictions": {
            "XGBoost": pred_xgb,
        },
        "confidence_interval": {"lower_95": ci_low, "upper_95": ci_high, "rmse": rmse},
        "business_metrics": {
            "mmr_baseline": mmr,
            "predicted_profit": pred_xgb - mmr,
            "profit_margin": margin_xgb
        },
        "vehicle_info": {
            "year": year, "make": make, "body": body, "transmission": transmission,
            "odometer": odometer, "condition": condition, "age": vehicle_age, "is_luxury": bool(is_luxury)
        }
    }

def get_encoder_classes():
    return {
        "make": list(_label_encoders["make"].classes_),
        "body": list(_label_encoders["body_simplified"].classes_),
        "transmission": list(_label_encoders["transmission"].classes_)
    }
