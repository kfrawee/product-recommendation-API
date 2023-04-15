import datetime
import logging
import os
import pickle

logger = logging.getLogger(__name__)
current_dir = os.path.dirname(os.path.realpath(__file__))
data_path = "output"
model_name = "xgb_model.pkl"


def load_model():
    start_time = datetime.datetime.now()
    logger.info("Loading model..")

    # Load the saved model from file
    model = pickle.load(open(os.path.join(current_dir, data_path, model_name), "rb"))
    logger.info("Model loaded successfully")
    logger.info("Time taken to load model: %s", datetime.datetime.now() - start_time)
    return model
