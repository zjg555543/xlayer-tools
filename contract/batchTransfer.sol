// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BatchTransfer {
    // 定义事件
    event BatchTransferEvent(address indexed sender, uint256 totalAmount);

    function batchTransfer(address[] calldata recipients, uint256[] calldata amounts) external payable {
        require(recipients.length == amounts.length, "Mismatched recipients and amounts");
        uint256 totalAmount = 0;

        // 计算总额
        for (uint256 i = 0; i < amounts.length; i++) {
            totalAmount += amounts[i];
        }

        // 验证是否提供了足够的 Ether
        require(msg.value >= totalAmount, "Insufficient Ether provided");

        // 进行转账
        for (uint256 i = 0; i < recipients.length; i++) {
            payable(recipients[i]).transfer(amounts[i]);
        }

        // 如果提供了超额的 Ether，则退还多余的部分
        if (msg.value > totalAmount) {
            payable(msg.sender).transfer(msg.value - totalAmount);
        }

        // 发出事件，记录总额
        emit BatchTransferEvent(msg.sender, totalAmount);
    }
}

