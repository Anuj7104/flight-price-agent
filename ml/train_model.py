import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

data = pd.DataFrame({
    'days_before_departure':[30,20,10,5,2],
    'stops':[0,1,0,1,0],
    'airline_id':[1,2,1,2,1],
    'price':[4500,5200,5000,6000,7000]
})

X = data[['days_before_departure','stops','airline_id']]
y = data['price']

model = RandomForestRegressor()
model.fit(X,y)

joblib.dump(model,'ml/flight_price_model.pkl')

print("Model trained successfully")