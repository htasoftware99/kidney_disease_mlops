import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import load_data

logger = get_logger(__name__)


RANDOM_FOREST_PARAMS = {
    "criterion": ["gini", "entropy"],
    "max_depth": [3, 5, 7, 9],
    "max_features": ["sqrt", "log2"],
    "min_samples_leaf": [1, 2, 3, 4, 5],
    "min_samples_split": [2, 3, 4, 5],
    "n_estimators": [100, 200, 300, 500],
}

GRID_SEARCH_PARAMS = {
    "cv": 5,
    "n_jobs": -1,
    "verbose": 1,
    "scoring": "accuracy",
}


class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path


    def load_and_split_data(self):
        try:
            logger.info(f"Loading train data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading test data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["class"])
            y_train = train_df["class"]

            X_test = test_df.drop(columns=["class"])
            y_test = test_df["class"]

            logger.info("Data loaded and split successfully")
            return X_train, y_train, X_test, y_test

        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            raise CustomException("Failed to load and split data", e)


    def train_random_forest(self, X_train, y_train):
        try:
            logger.info("Initializing Random Forest model")
            rf_model = RandomForestClassifier(random_state=42)

            logger.info("Starting hyperparameter tuning with GridSearchCV")
            grid_search = GridSearchCV(
                estimator=rf_model,
                param_grid=RANDOM_FOREST_PARAMS,
                cv=GRID_SEARCH_PARAMS["cv"],
                n_jobs=GRID_SEARCH_PARAMS["n_jobs"],
                verbose=GRID_SEARCH_PARAMS["verbose"],
                scoring=GRID_SEARCH_PARAMS["scoring"],
            )

            grid_search.fit(X_train, y_train)

            best_params = grid_search.best_params_
            best_model = grid_search.best_estimator_

            logger.info(f"Best parameters found: {best_params}")
            logger.info(f"Best CV score: {grid_search.best_score_:.4f}")

            return best_model

        except Exception as e:
            logger.error(f"Error while training model: {e}")
            raise CustomException("Failed to train Random Forest model", e)


    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating model on test set")

            y_pred = model.predict(X_test)

            accuracy  = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall    = recall_score(y_test, y_pred)
            f1        = f1_score(y_test, y_pred)

            logger.info(f"Accuracy  : {accuracy:.4f}")
            logger.info(f"Precision : {precision:.4f}")
            logger.info(f"Recall    : {recall:.4f}")
            logger.info(f"F1 Score  : {f1:.4f}")

            return {
                "accuracy":  accuracy,
                "precision": precision,
                "recall":    recall,
                "f1":        f1,
            }

        except Exception as e:
            logger.error(f"Error while evaluating model: {e}")
            raise CustomException("Failed to evaluate model", e)


    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")

        except Exception as e:
            logger.error(f"Error while saving model: {e}")
            raise CustomException("Failed to save model", e)


    def run(self):
        try:
            logger.info("Starting Model Training pipeline")

            X_train, y_train, X_test, y_test = self.load_and_split_data()

            best_model = self.train_random_forest(X_train, y_train)

            metrics = self.evaluate_model(best_model, X_test, y_test)

            self.save_model(best_model)

            logger.info("Model Training pipeline completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Model Training pipeline: {e}")
            raise CustomException("Failed during Model Training pipeline", e)


if __name__ == "__main__":
    trainer = ModelTraining(
        PROCESSED_TRAIN_DATA_PATH,
        PROCESSED_TEST_DATA_PATH,
        MODEL_OUTPUT_PATH,
    )
    trainer.run()