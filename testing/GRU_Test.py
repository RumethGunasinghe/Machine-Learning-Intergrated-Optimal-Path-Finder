from tensorflow.keras.models import Sequential #type: ignore
from tensorflow.keras.layers import GRU, Dense #type: ignore

def testingGRU_Model(X_train, X_test, y_train, y_test, scaler, epochs):
    model = Sequential()
    model.add(GRU(64, input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_split=0.2)

    predictions = model.predict(X_test)
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
    preds_actual = scaler.inverse_transform(predictions)

    return preds_actual, y_test_actual, model
