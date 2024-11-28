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
        
    def diff(self, zkevm_result, erigon_result, key):
        zkevm = self.zkevm_rpc.get_value(zkevm_result, key)
        erigon = self.erigon_rpc.get_value(erigon_result, key)
        # logging.info("zkevm_result" + json.dumps(zkevm_result, indent=4) + "Key, " + key)
        if zkevm != erigon:
            logging.error("!!!!!!!!!!!!!!!!!!Different!!!!!!!!!!!!!!!!!!")
            logging.error(key + ", zkevm: " + json.dumps(zkevm, indent=4) + ", erigon: " + json.dumps(erigon, indent=4))

            exit(1)
        else:
            logging.info("Same " + key + ", " + str(zkevm))

    def block(self, block):
        logging.info("Compare block hash start")
        zkevm_result = self.zkevm_rpc.get_block_by_number(block)
        erigon_result = self.erigon_rpc.get_block_by_number(block)
        self.diff(zkevm_result, erigon_result, "hash")

        logging.info("Compare block hash end")
        return
    
    def receipt(self, hash):
        logging.info("Compare receipt start")
        zkevm_result = self.zkevm_rpc.get_transaction_receipt(hash)
        erigon_result = self.erigon_rpc.get_transaction_receipt(hash)
        for i in range(len(zkevm_result["result"]["logs"])):
            self.diff(zkevm_result["result"]["logs"][i], erigon_result["result"]["logs"][i], "address")
            # self.diff(zkevm_result["result"]["logs"][i], erigon_result["result"]["logs"][i], "data")
            self.diff(zkevm_result["result"]["logs"][i], erigon_result["result"]["logs"][i], "blockNumber")
            self.diff(zkevm_result["result"]["logs"][i], erigon_result["result"]["logs"][i], "transactionHash")
            self.diff(zkevm_result["result"]["logs"][i], erigon_result["result"]["logs"][i], "transactionIndex")
            # self.diff(zkevm_result["result"]["logs"][i], erigon_result["result"]["logs"][i], "logIndex")
        
        self.diff(zkevm_result, erigon_result, "status")
        self.diff(zkevm_result, erigon_result, "transactionHash")
        self.diff(zkevm_result, erigon_result, "transactionIndex")
        self.diff(zkevm_result, erigon_result, "blockNumber")
        self.diff(zkevm_result, erigon_result, "gasUsed")
        self.diff(zkevm_result, erigon_result, "from")
        self.diff(zkevm_result, erigon_result, "to")
        self.diff(zkevm_result, erigon_result, "contractAddress")
        self.diff(zkevm_result, erigon_result, "type")
        self.diff(zkevm_result, erigon_result, "effectiveGasPrice")
        self.diff(zkevm_result, erigon_result, "logsBloom")

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
    elif opt == "receipt":
        hash = sys.argv[2]
        case.receipt(hash)
    else:
        logging.error("Invalid option")

