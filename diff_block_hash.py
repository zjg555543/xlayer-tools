# /usr/bin/env python3
# --coding:utf-8 --
from cmath import log
import json
import logging
from os import system
from pickletools import long1
import sys
import time
import pybase
import rpc
import sys
import os

class DiffBlockHash:
    def __init__(self, configObj):
        self.config = configObj
        self.zkevm_rpc = rpc.RpcClient(self.config["zkevm_rpc"])
        self.erigon_rpc = rpc.RpcClient(self.config["erigon_rpc"])
        return

    def format_decimal(self, num):
        str_num = str(num)
        if "." in str_num:
            a, b = str(str_num).split('.')
            return int(a)
        else:
            return int(str_num)

    def block(self, block):
        logging.info("test start")
        zkevm_result = self.zkevm_rpc.get_block_by_number(block)
        erigon_result = self.erigon_rpc.get_block_by_number(block)
        zkevm_hash = self.zkevm_rpc.get_value(zkevm_result, "hash")
        erigon_hash = self.erigon_rpc.get_value(erigon_result, "hash")
        if zkevm_hash != erigon_hash:
            logging.error("!!!!!!!!!!!!!!!!!!Block hash is different!!!!!!!!!!!!!!!!!!")
            logging.error("zkevm hash: " + zkevm_hash + ", erigon hash: " + erigon_hash)
            exit(1)
        else:
            logging.info("Block number: " + str(block) + ", hash: " + zkevm_hash)
        return

if __name__ == '__main__':
    pybase = pybase.Pybase()
    strlist = os.path.basename(__file__).split('.') 
    file = open('config/' + strlist[0] + '.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = DiffBlockHash(moduleConfig)

    opt = sys.argv[1]
    if opt == "block":
        block = int(sys.argv[2])
        case.block(block)
    else:
        logging.error("Invalid option")

