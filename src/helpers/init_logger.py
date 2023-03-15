import logging


def create_logger():
    return logging.basicConfig(filename='/tmp/myapp.log', level=logging.DEBUG,
                               format='%(asctime)s %(levelname)s %(name)s %(message)s')
