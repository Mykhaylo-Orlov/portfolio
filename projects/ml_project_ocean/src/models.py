from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


def get_models():
    return {
        "random_forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42
        ),
        "linear_regression": LinearRegression()
    }