# /usr/bin/env python3
# --coding:utf-8 --
import json
import logging
import os
import time
import json
import requests

class RpcClient:
    def __init__(self, rpc):
        self.node_rpc = rpc

    def get_block_by_number(self, block_number):
        # 设置 RPC URL（这里以 Infura 为例）

        # 构造 JSON-RPC 请求数据
        headers = {'Content-Type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), True],
            "id": 1
        }

        # 发送 POST 请求
        response = requests.post(self.node_rpc, headers=headers, data=json.dumps(payload))

        # 检查响应状态码
        if response.status_code == 200:
            result = response.json()
            return json.dumps(result, indent=4)
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
        
    def get_value(self, str_object, key):
        object = json.loads(str_object)
        if "result" in object and key in object["result"]:
            return object["result"][key]
        else:
            return None
    


