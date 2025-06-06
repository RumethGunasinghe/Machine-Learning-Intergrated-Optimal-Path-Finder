import preprocessing
from tensorflow.keras.layers import GRU # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore

def GRU_Model(X, y, scaler):
    model = Sequential()
    model.add(GRU(64, input_shape=(X.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.3)
    
    latest_sequence = X[-1].reshape(1, X.shape[1], 1)
    predicted_next_scaled = model.predict(latest_sequence)
    predicted_next_actual = scaler.inverse_transform(predicted_next_scaled)
    print(predicted_next_actual[0][0])
    return predicted_next_actual[0][0]

# X, y, scaler, TOD = preprocessing("./csv/ScatsReformed.csv", "WARRIGAL_RD N of HIGH STREET_RD", 10, "Afternoon")
# prediction = GRU_Model(X, y, scaler)
# print(f"GRU Model pred for volume: {prediction}")
