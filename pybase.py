# /usr/bin/env python3
# --coding:utf-8 --
import json
import time
import sys
import os
# import case_simulate_sendtx
# import case_demo_sendtx
import logging
import signal

def quit(signum, frame):
    print('You choose to stop me.')
    sys.exit()

class Pybase:
    def __init__(self):
        # 设置log
        log_type = "file"
        log_level = "INFO"
        log_path = "./log/pytest.log"

        logger = logging.getLogger()
        logger.setLevel(log_level)
        rht = logging.FileHandler(log_path, encoding='utf-8', mode='a')
        fmt = logging.Formatter(
            '%(asctime)s - %(filename)s[line:%(lineno)d](%(funcName)s) - %(levelname)s: %(message)s',
            '%Y-%m-%d %H:%M:%S')
        rht.setFormatter(fmt)
        logging.basicConfig(
            format='%(asctime)s - %(filename)s[line:%(lineno)d](%(funcName)s) - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        logger.addHandler(rht)
        
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        return
    
