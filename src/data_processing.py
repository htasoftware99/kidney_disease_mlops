import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data

logger = get_logger(__name__)


class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        os.makedirs(self.processed_dir, exist_ok=True)

        logger.info("DataProcessor initialized")

    def rename_columns(self, df):
        """Assign canonical column names (matches notebook ordering)."""
        try:
            logger.info("Renaming columns to canonical names")

            df.columns = [
                'age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar',
                'red_blood_cells', 'pus_cell', 'pus_cell_clumps', 'bacteria',
                'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                'potassium', 'haemoglobin', 'packed_cell_volume',
                'white_blood_cell_count', 'red_blood_cell_count',
                'hypertension', 'diabetes_mellitus', 'coronary_artery_disease',
                'appetite', 'peda_edema', 'aanemia', 'class'
            ]

            logger.info("Columns renamed successfully")
            return df

        except Exception as e:
            logger.error(f"Error while renaming columns: {e}")
            raise CustomException("Failed to rename columns", e)

    def fix_dtypes(self, df):
        """Convert object-encoded numeric columns to float."""
        try:
            logger.info("Fixing dtypes for packed_cell_volume, white_blood_cell_count, red_blood_cell_count")

            numeric_cols = ['packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            logger.info("Dtype fix completed")
            return df

        except Exception as e:
            logger.error(f"Error while fixing dtypes: {e}")
            raise CustomException("Failed to fix dtypes", e)

    def clean_dirty_values(self, df):
        """Fix known dirty values in categorical columns."""
        try:
            logger.info("Cleaning dirty values in categorical columns")

            df['diabetes_mellitus'] = df['diabetes_mellitus'].replace(
                {'\tno': 'no', '\tyes': 'yes', ' yes': 'yes'}
            )
            df['coronary_artery_disease'] = df['coronary_artery_disease'].replace(
                {'\tno': 'no'}
            )
            df['class'] = df['class'].replace(
                {'ckd\t': 'ckd', 'notckd': 'not ckd'}
            )

            logger.info("Dirty values cleaned")
            return df

        except Exception as e:
            logger.error(f"Error while cleaning dirty values: {e}")
            raise CustomException("Failed to clean dirty values", e)

    def encode_target(self, df):
        """Map target column: ckd → 0, not ckd → 1."""
        try:
            logger.info("Encoding target column 'class'")

            df['class'] = df['class'].map({'ckd': 0, 'not ckd': 1})
            df['class'] = pd.to_numeric(df['class'], errors='coerce')

            logger.info(f"Target distribution after encoding:\n{df['class'].value_counts()}")
            return df

        except Exception as e:
            logger.error(f"Error while encoding target: {e}")
            raise CustomException("Failed to encode target column", e)

    @staticmethod
    def _random_sample_impute(df, col):
        """In-place random sampling imputation for a single column."""
        null_count = df[col].isnull().sum()
        if null_count == 0:
            return df
        random_sample = df[col].dropna().sample(null_count, random_state=42)
        random_sample.index = df[df[col].isnull()].index
        df.loc[df[col].isnull(), col] = random_sample
        return df

    @staticmethod
    def _mode_impute(df, col):
        """In-place mode imputation for a single column."""
        mode_val = df[col].mode()[0]
        df[col] = df[col].fillna(mode_val)
        return df

    def impute_missing_values(self, df):
        """Apply random sampling for numerical cols, mode for categorical cols."""
        try:
            logger.info("Starting missing value imputation")

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            # Numerical – random sampling
            for col in num_cols:
                if col in df.columns:
                    df = self._random_sample_impute(df, col)

            # Two categorical cols also get random sampling (notebook pattern)
            df = self._random_sample_impute(df, 'red_blood_cells')
            df = self._random_sample_impute(df, 'pus_cell')

            # Remaining categorical cols – mode
            for col in cat_cols:
                if col in df.columns:
                    df = self._mode_impute(df, col)

            logger.info(f"Remaining nulls after imputation:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
            return df

        except Exception as e:
            logger.error(f"Error during imputation: {e}")
            raise CustomException("Failed to impute missing values", e)

    def encode_categoricals(self, df):
        try:
            logger.info("Applying Label Encoding to categorical columns")

            cat_cols = self.config["data_processing"]["categorical_columns"]
        
            # Config'e ek olarak, object dtype kalan tüm kolonları da yakala
            remaining_object_cols = df.select_dtypes(include=["object"]).columns.tolist()
            all_cat_cols = list(set(cat_cols + remaining_object_cols))

            le = LabelEncoder()
            mappings = {}

            for col in all_cat_cols:
                if col in df.columns:
                    df[col] = le.fit_transform(df[col].astype(str))
                    mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))

            logger.info("Label Encoding mappings:")
            for col, mapping in mappings.items():
                logger.info(f"  {col}: {mapping}")

            # Son kontrol — hâlâ object kalan kolon var mı?
            still_object = df.select_dtypes(include=["object"]).columns.tolist()
            if still_object:
                logger.warning(f"Still object dtype after encoding: {still_object}")

            return df

        except Exception as e:
            logger.error(f"Error during label encoding: {e}")
            raise CustomException("Failed to encode categorical columns", e)

    def drop_unwanted_columns(self, df):
        """Drop index / id columns that are not useful for modelling."""
        try:
            cols_to_drop = [c for c in ['Unnamed: 0', 'id'] if c in df.columns]
            if cols_to_drop:
                df.drop(columns=cols_to_drop, inplace=True)
                logger.info(f"Dropped columns: {cols_to_drop}")
            return df

        except Exception as e:
            logger.error(f"Error while dropping columns: {e}")
            raise CustomException("Failed to drop unwanted columns", e)

    def save_data(self, df, file_path):
        try:
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved to {file_path}")
        except Exception as e:
            logger.error(f"Error while saving data: {e}")
            raise CustomException("Failed to save data", e)

    def preprocess(self, df):
        """Run all preprocessing steps on a single dataframe."""
        df = self.drop_unwanted_columns(df)
        df = self.rename_columns(df)
        df = self.fix_dtypes(df)
        df = self.clean_dirty_values(df)
        df = self.encode_target(df)
        df = self.impute_missing_values(df)
        df = self.encode_categoricals(df)
        return df

    def process(self):
        try:
            logger.info("Loading raw train and test data")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            logger.info("Preprocessing train data")
            train_df = self.preprocess(train_df)

            logger.info("Preprocessing test data")
            test_df = self.preprocess(test_df)

            # Align test columns to train (safety guard)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing pipeline completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in processing pipeline: {e}")
            raise CustomException("Data processing pipeline failed", e)


if __name__ == "__main__":
    processor = DataProcessor(
        TRAIN_FILE_PATH,
        TEST_FILE_PATH,
        PROCESSED_DIR,
        CONFIG_PATH
    )
    processor.process()