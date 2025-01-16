import logging

# Configure the logger
logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers = [logging.StreamHandler()]
)

# Logger will be used by every class
logger = logging.getLogger("Global_Logging_Tool")