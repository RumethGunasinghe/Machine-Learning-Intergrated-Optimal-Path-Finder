from sklearn.ensemble import RandomForestRegressor

def testingRF_Model(X_train, X_test, y_train, y_test, scaler, estimator):
    X_train_flat = X_train.reshape((X_train.shape[0], X_train.shape[1]))
    X_test_flat = X_test.reshape((X_test.shape[0], X_test.shape[1]))

    model = RandomForestRegressor(n_estimators=estimator, random_state=42)
    model.fit(X_train_flat, y_train)

    predictions = model.predict(X_test_flat)
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
    preds_actual = scaler.inverse_transform(predictions.reshape(-1, 1))

    return preds_actual, y_test_actual, model
