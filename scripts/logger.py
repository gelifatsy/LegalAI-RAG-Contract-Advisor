import logging
import os

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define a common formatter
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# Set up log file paths
logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
error_log_file = os.path.join(logs_dir, 'error.log')
info_log_file = os.path.join(logs_dir, 'info.log')

# Configure file handlers
error_handler = logging.FileHandler(error_log_file)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

info_handler = logging.FileHandler(info_log_file)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

# Configure stream handler for console output
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(error_handler)
logger.addHandler(info_handler)
logger.addHandler(stream_handler)
