import logging
from os.path import join, dirname, abspath


def create_logger():
    path = join(dirname(dirname(dirname(abspath(__file__)))))

    logging.basicConfig(filename=path + '/alibaba_app.log', level=logging.ERROR,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    return logging.getLogger('alibaba_logger')
