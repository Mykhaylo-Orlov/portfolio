from models.ml_project.config import TRAIN_PATH, TARGET
from models.ml_project.src.data_loader import load_data
from models.ml_project.src.processor import clean_data
from models.ml_project.src.models import get_models
from models.ml_project.src.evaluate import evaluate
from pathlib import Path
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
import pandas as pd


class MLPipeline:
    def __init__(self):
        self.results = {}

        BASE_DIR = Path(__file__).resolve().parent.parent

        self.output_dir = BASE_DIR / "outputs"
        self.fig_dir = self.output_dir / "figures"

        self.output_dir.mkdir(exist_ok=True)
        self.fig_dir.mkdir(parents=True, exist_ok=True)

    def load_and_prepare(self):
        df = load_data(TRAIN_PATH)
        df = clean_data(df)

        X = df.drop(columns=[TARGET])
        y = df[TARGET]

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_and_evaluate(self, X_train, X_val, y_train, y_val):
        models = get_models()

        for name, model in models.items():
            model.fit(X_train, y_train)
            rmse = evaluate(model, X_val, y_val)

            self.results[name] = {
                "model": model,
                "rmse": rmse
            }

    def select_best_model(self):
        best_model_name = min(
            self.results, key=lambda x: self.results[x]["rmse"]
        )

        self.best_model = self.results[best_model_name]["model"]
        self.best_rmse = self.results[best_model_name]["rmse"]
        self.best_model_name = best_model_name

    def get_feature_importance(self, X_columns):
        if hasattr(self.best_model, "feature_importances_"):
            return pd.Series(
                self.best_model.feature_importances_,
                index=X_columns
            )
        else:
            return None  # e.g. LinearRegression

    def run(self):
        X_train, X_val, y_train, y_val = self.load_and_prepare()

        self.train_and_evaluate(X_train, X_val, y_train, y_val)
        self.select_best_model()

        preds = self.best_model.predict(X_val)

        pd.DataFrame({
            "actual": y_val,
            "predicted": preds
        }).to_csv(self.output_dir / "predictions.csv", index=False)

        feature_importance = self.get_feature_importance(X_train.columns)

        if feature_importance is not None:
            feature_importance.sort_values().plot(kind="barh")
            plt.tight_layout()
            plt.savefig(self.fig_dir / "feature_importance.png")
            plt.close()

        return {
            "best_model_name": self.best_model_name,
            "rmse": self.best_rmse,
            "all_results": self.results,
            "feature_importance": feature_importance
        }