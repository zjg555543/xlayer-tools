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
            return result
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
        
    def get_transaction_receipt(self, transaction_hash):
        # 构造 JSON-RPC 请求数据
        headers = {'Content-Type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [transaction_hash],
            "id": 1
        }

        # 发送 POST 请求
        response = requests.post(self.node_rpc, headers=headers, data=json.dumps(payload))

        # 检查响应状态码
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
        
    def get_value(self, object, key):
        if "result" in object and key in object["result"]:
            # logging.info("key: " + key + ", value: " + json.dumps(object["result"][key], indent=4))
            return object["result"][key]
        elif key in object:
            # logging.info("key: " + key + ", value: " + json.dumps(object[key], indent=4))
            return object[key]
        else:
            logging.info("key: " + key + ", value: " + object)
            exit(1)
    
    


