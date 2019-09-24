# -*- coding: utf-8 -*-

from common.log import logger
import time

def execute_time(func):
    def __decorator(*args, **args2):
        t_start = time.time()
        rt = func(*args, **args2)
        t_end = time.time()
        logger.info('INFO: Excuting %s takes %.3fs' % (func.__name__, t_end - t_start))
        return rt
    return __decorator