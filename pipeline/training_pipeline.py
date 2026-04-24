from config.paths_config import *
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml

if __name__ == "__main__":


    data_processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH,
    )
    data_processor.process()

    model_trainer = ModelTraining(
        train_path=PROCESSED_TRAIN_DATA_PATH,
        test_path=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH,
    )
    model_trainer.run()