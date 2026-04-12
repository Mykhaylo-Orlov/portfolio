from src.pipeline import MLPipeline

if __name__ == "__main__":
    pipeline = MLPipeline()
    results = pipeline.run()

    print("Best model:", results["best_model_name"])
    print("RMSE:", results["rmse"])