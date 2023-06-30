import logging
from logging.handlers import RotatingFileHandler

def configure_logger(app):
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
