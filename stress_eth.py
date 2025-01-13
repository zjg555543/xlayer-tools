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
from solcx import compile_source
from web3 import Web3
from solcx import get_installable_solc_versions
from solcx import install_solc
from solcx import set_solc_version
from solcx import get_solc_version

class StressETH:
    def __init__(self, configObj):
        self.config = configObj
        self.rpc = rpc.RpcClient(self.config["rpc"])
        self.seq = rpc.RpcClient(self.config["seq"])
        return
        
    def depoly(self):
        install_solc('0.8.20')
        set_solc_version('0.8.20')  # 替换为你的版本

        # 合约代码
        # 读取整个文件内容
        file = open("./contract/batchTransfer.sol", "r")
        contract_source_code = file.read()
        logging.info(self.config["rpc"])
        # 编译合约
        compiled_sol = compile_source(contract_source_code, output_values=["abi", "bin"])
        contract_interface = compiled_sol["<stdin>:BatchTransfer"]
        abi = contract_interface["abi"]
        bytecode = contract_interface["bin"]

        # 连接到本地节点
        w3 = Web3(Web3.HTTPProvider(self.config["rpc"]))
        assert w3.is_connected(), "Failed to connect to Ethereum node."

        # 设置默认账户
        private_key = "815405dddb0e2a99b12af775fd2929e526704e1d1aea6a0b4e74dc33e2f7fcd2"
        account = w3.eth.account.from_key(private_key)
        w3.eth.default_account = account

        # 创建合约对象
        SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

        # 构造交易
        transaction = SimpleStorage.constructor().build_transaction({
            "from": account.address,  # 显式指定发送者地址
            "gas": 2000000,  # 设置合理的 gas limit
            "gasPrice": w3.to_wei(20, "gwei"),
            "nonce": w3.eth.get_transaction_count(account.address),
            "chainId": 195  # 指定 chainId (主网是1)
        })

        signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent with hash: {tx_hash.hex()}")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        print(f"Contract deployed at address: {contract_address}")
        
        # 获取合约实例
        contract_instance = w3.eth.contract(address=contract_address, abi=abi)
        
        recipients = self.getAccounts()
        amounts = []
        for i in range(len(recipients)):
            amounts.append(10000000000000)
        total_amount = sum(amounts) 

        # 调用 set() 函数
        transaction = contract_instance.functions.batchTransfer(recipients, amounts).build_transaction({
            "from": account.address,  # 显式指定发送者地址
            "gas": 30000000,  # 设置合理的 gas limit
            "gasPrice": w3.to_wei(20, "gwei"),
            "nonce": w3.eth.get_transaction_count(account.address),  # 获取当前账户的 nonce
            "chainId": 195,  # 指定 chainId (主网是1)
            "value": total_amount  # 设置交易发送的总金额（单位：Wei）
        })

        signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
        gas_estimate = w3.eth.estimate_gas(transaction)
        print(f"Estimated gas: {gas_estimate}")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent with hash: {tx_hash.hex()}")

        # 等待交易收据
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # 打印收据
        print(tx_receipt)
        return
    
    def getPrivate(self):
        file = open("./config/account_20000", "r")
        privateList = file.read().splitlines()  # 使用 splitlines() 来去除行尾的换行符
        return privateList

    def getAccounts(self):
        file = open("./config/account_20000", "r")
        privateList = file.read().splitlines()  # 使用 splitlines() 来去除行尾的换行符
        acc_lists = []
        for acc in privateList:
            w3 = Web3(Web3.HTTPProvider(self.config["rpc"]))
            account = w3.eth.account.from_key(acc)
            acc_lists.append(account.address)
        return acc_lists


if __name__ == '__main__':
    pybase = pybase.Pybase()
    strlist = os.path.basename(__file__).split('.') 
    file = open('config/' + strlist[0] + '.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = StressETH(moduleConfig)

    opt = sys.argv[1]
    if opt == "depoly":
        case.depoly()
    else:
        logging.error("Invalid option")

