
import logging
import os


def configure_logger(logs_folder_path="/home/elias/Documents/10 Academy/WEEK 11/LegalAI-RAG-Contract-Advisor/logs"):


    error_log_file = os.path.join(logs_folder_path, "error.log")
    info_log_file = os.path.join(logs_folder_path, "info.log")

    error_handler = logging.FileHandler(error_log_file)
    info_handler = logging.FileHandler(info_log_file)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)

    return logger
