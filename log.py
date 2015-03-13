#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import logging

'''
a log method , using logging

from log import log

log.error('11')
log.info('22')
log.debug('33')
'''

def init():
    '''
    from log import log
    log.error('')
    log.debug('')
    log.info('')
    '''
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)

    debug = logging.StreamHandler()
    debug.setLevel(logging.DEBUG)

    info = logging.FileHandler('run.log')
    info.setLevel(logging.INFO)

    error = logging.FileHandler('error.log')
    error.setLevel(logging.ERROR)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    debug.setFormatter(formatter)
    info.setFormatter(formatter)
    error.setFormatter(formatter)

    log.addHandler(debug)
    log.addHandler(info)
    log.addHandler(error)

    return log

logging = init()
