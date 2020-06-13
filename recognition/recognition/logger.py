import logging

logging.basicConfig(filename='/tmp/recognition/app.log', filemode='a',
                    format='[%(asctime)s] [%(name)s]  %(levelname)s  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger("RECOGNITION SERVICE")
