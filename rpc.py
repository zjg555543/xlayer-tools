# /usr/bin/env python3
# --coding:utf-8 --
import json
import logging
import os
import time
import json

class CLI:
    def __init__(self, rpc):
        self.node_rpc = rpc

    def get_ledger_seq(self, rpc = ""):
        cmd = 'exchaincli status '
        if len(rpc) > 0:
            cmd = cmd + " --node " + rpc
        else:
            cmd = cmd + self.node_rpc
        
        result = os.popen(cmd).read().rstrip()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)
        return int(result_obj["sync_info"]["latest_block_height"])
