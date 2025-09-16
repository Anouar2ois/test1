// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StakingReputation {
    struct Validator {
        uint256 stake;
        int256 reputation;
    }

    mapping(address => Validator) public validators;
    uint256 public minStake = 100 ether;

    event Staked(address indexed v, uint256 amount);
    event Unstaked(address indexed v, uint256 amount);
    event Voted(address indexed v, bool up, int256 newRep);

    function stake() external payable {
        validators[msg.sender].stake += msg.value;
        require(validators[msg.sender].stake >= minStake, "low stake");
        emit Staked(msg.sender, msg.value);
    }

    function unstake(uint256 amount) external {
        require(validators[msg.sender].stake >= amount, "exceeds");
        validators[msg.sender].stake -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer fail");
        emit Unstaked(msg.sender, amount);
    }

    function vote(bool up) external {
        require(validators[msg.sender].stake >= minStake, "not validator");
        if (up) validators[msg.sender].reputation += 1; else validators[msg.sender].reputation -= 1;
        emit Voted(msg.sender, up, validators[msg.sender].reputation);
    }
}
