// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DragonToken {
    string public name = "DragonToken";
    string public symbol = "DGN";
    uint8 public decimals = 18;
    uint256 public totalSupply = 10_000_000 ether;
    mapping(address => uint256) public balanceOf;
    event Transfer(address indexed from, address indexed to, uint256 value);
    constructor() { balanceOf[msg.sender] = totalSupply; emit Transfer(address(0), msg.sender, totalSupply); }
    function transfer(address to, uint256 value) external returns (bool) {
        require(balanceOf[msg.sender] >= value, "bal");
        balanceOf[msg.sender] -= value; balanceOf[to] += value; emit Transfer(msg.sender, to, value); return true;
    }
}

contract DragonDAO {
    struct Proposal { string title; string description; uint64 endTs; int256 votes; bool executed; }
    Proposal[] public proposals;
    mapping(uint256 => mapping(address => bool)) public voted;
    event Proposed(uint256 id, string title);
    event Voted(uint256 id, int256 votes);
    event Executed(uint256 id);

    function propose(string memory title, string memory description, uint64 votingPeriod) external returns (uint256) {
        proposals.push(Proposal(title, description, uint64(block.timestamp) + votingPeriod, 0, false));
        emit Proposed(proposals.length - 1, title);
        return proposals.length - 1;
    }

    function vote(uint256 id, bool support) external {
        require(id < proposals.length, "id");
        require(!voted[id][msg.sender], "dup");
        require(block.timestamp < proposals[id].endTs, "ended");
        voted[id][msg.sender] = true;
        proposals[id].votes += support ? int256(1) : int256(-1);
        emit Voted(id, proposals[id].votes);
    }

    function execute(uint256 id) external {
        Proposal storage p = proposals[id];
        require(block.timestamp >= p.endTs, "not ended");
        require(!p.executed, "done");
        p.executed = true;
        emit Executed(id);
    }

    function submitZKProof(bytes calldata /*proof*/, bytes32 /*signal*/) external pure returns (bool) {
        return true;
    }
}
