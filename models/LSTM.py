import preprocessing
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense # type: ignore

def LSTM_Model(X, y, scaler):
    model = Sequential()
    model.add(LSTM(64, input_shape=(X.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.3)

    latest_sequence = X[-1].reshape(1, X.shape[1], 1)
    predicted_next_scaled = model.predict(latest_sequence)
    predicted_next_actual = scaler.inverse_transform(predicted_next_scaled)
    print(predicted_next_actual[0][0])
    return predicted_next_actual[0][0]

# X, y, scaler, TOD = preprocessing("./csv/ScatsReformed.csv", "WARRIGAL_RD N of HIGH STREET_RD", 10, "Morning")
# prediction = LSTM_Model(X, y, scaler)
# print(f"LSTM Model pred for volume: {prediction}")

