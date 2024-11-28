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

class DiffRpcSeq:
    def __init__(self, configObj):
        self.config = configObj
        self.rpc = rpc.RpcClient(self.config["rpc"])
        self.seq = rpc.RpcClient(self.config["seq"])
        return
        
    def latest_block(self):
        rpc_result = self.rpc.get_latest_block()
        seq_result = self.seq.get_latest_block()
        rpc = int(rpc_result["result"]["number"], 16)
        seq = int(seq_result["result"]["number"], 16)
        diff = seq - rpc
        logging.info("[block] rpc: " + str(rpc) + ", seq: " + str(seq) + ", diff: " + str(diff))

    def get_batch_bumber(self):
        rpc_result = self.rpc.get_batch_bumber()
        seq_result = self.seq.get_batch_bumber()
        rpc = int(rpc_result["result"], 16)
        seq = int(seq_result["result"], 16)
        diff = seq - rpc
        logging.info("[batch] rpc: " + str(rpc) + ", seq: " + str(seq) + ", diff: " + str(diff))
        return
 
    def get_virtual_batch_bumber(self):
        rpc_result = self.rpc.get_virtual_batch_bumber()
        seq_result = self.seq.get_virtual_batch_bumber()
        rpc = int(rpc_result["result"], 16)
        seq = int(seq_result["result"], 16)
        diff = seq - rpc
        logging.info("[virtual] rpc: " + str(rpc) + ", seq: " + str(seq) + ", diff: " + str(diff))
        return
    
    def get_verified_batch_number(self):
        rpc_result = self.rpc.get_verified_batch_number()
        seq_result = self.seq.get_verified_batch_number()
        rpc = int(rpc_result["result"], 16)
        seq = int(seq_result["result"], 16)
        diff = seq - rpc
        logging.info("[verified] rpc: " + str(rpc) + ", seq: " + str(seq) + ", diff: " + str(diff))
        return

if __name__ == '__main__':
    pybase = pybase.Pybase()
    strlist = os.path.basename(__file__).split('.') 
    file = open('config/' + strlist[0] + '.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = DiffRpcSeq(moduleConfig)

    if len(sys.argv) < 2:
        case.latest_block()
        case.get_batch_bumber()
        case.get_virtual_batch_bumber()
        case.get_verified_batch_number()
        exit(1)

    opt = sys.argv[1]
    if opt == "block":
        block = int(sys.argv[2])
        case.block(block)
    else:
        logging.error("Invalid option")

