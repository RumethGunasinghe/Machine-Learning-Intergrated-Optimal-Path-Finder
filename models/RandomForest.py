import preprocessing
from sklearn.ensemble import RandomForestRegressor
import numpy as np 

def RF_Model(X, y, scaler):
    Xrf = X.reshape(X.shape[0], X.shape[1])

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(Xrf, y)

    latest_sequence = X[-1].reshape(1, X.shape[1])
    predicted_scaled = model.predict(latest_sequence).reshape(-1, 1)
    predicted_actual = scaler.inverse_transform(predicted_scaled)
    return predicted_actual[0][0]

# X, y, scaler, TOD = preprocessing("./csv/ScatsReformed.csv", "WARRIGAL_RD N of HIGH STREET_RD", 10, "Night")
# prediction = RF_Model(X, y, scaler)
# print(f"Random Forest Model pred for volume: {prediction}")

