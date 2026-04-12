import numpy as np
from sklearn.metrics import mean_squared_error


def evaluate(model, X, y):
    preds = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, preds))
    return rmse