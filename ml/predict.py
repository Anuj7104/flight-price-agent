import joblib

model = joblib.load("ml/flight_price_model.pkl")

def predict_price(days, stops, airline):
    prediction = model.predict([[days, stops, airline]])
    return round(prediction[0], 2)