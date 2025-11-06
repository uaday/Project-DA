# predictor.py
import numpy as np
import joblib

# Load once (module-level)
_lr = joblib.load("models/lr_model.pkl")
_rf = joblib.load("models/rf_model.pkl")
_xgb = joblib.load("models/xgb_model.pkl")
_scaler = joblib.load("models/scaler.pkl")
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

    # Linear uses scaled features
    pred_lr  = float(_lr.predict(_scaler.transform(feats))[0])
    pred_rf  = float(_rf.predict(feats)[0])
    pred_xgb = float(_xgb.predict(feats)[0])

    pred_ensemble = pred_lr*0.2 + pred_rf*0.3 + pred_xgb*0.5

    margin_xgb = (pred_xgb - mmr) / mmr * 100
    margin_ens = (pred_ensemble - mmr) / mmr * 100

    preds = [pred_lr, pred_rf, pred_xgb]
    std = float(np.std(preds))
    ci_low  = pred_ensemble - 1.96*std
    ci_high = pred_ensemble + 1.96*std

    return {
        "predictions": {
            "Linear Regression": pred_lr,
            "Random Forest": pred_rf,
            "XGBoost": pred_xgb,
            "Ensemble (Recommended)": pred_ensemble
        },
        "confidence_interval": {"lower_95": ci_low, "upper_95": ci_high, "std_dev": std},
        "business_metrics": {
            "mmr_baseline": mmr,
            "predicted_profit_ensemble": pred_ensemble - mmr,
            "profit_margin_ensemble": margin_ens
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
