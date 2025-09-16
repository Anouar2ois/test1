// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DragonShieldToken {
    string public name = "DragonShieldToken";
    string public symbol = "DST";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor() {
        totalSupply = 1_000_000 ether;
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address to, uint256 value) external returns (bool) {
        require(balanceOf[msg.sender] >= value, "bal");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
}

contract DragonShieldSignatures {
    struct Sig {
        string id;
        string name;
        string sha256hex;
        string pattern;
        address publisher;
        uint64 ts;
        int32 votes;
    }

    Sig[] public signatures;

    event Published(uint256 index, string id, string name, address publisher);
    event Voted(uint256 index, int32 votes);

    function publish(string memory id, string memory name, string memory sha256hex, string memory pattern) external returns (uint256) {
        Sig memory s = Sig({
            id: id,
            name: name,
            sha256hex: sha256hex,
            pattern: pattern,
            publisher: msg.sender,
            ts: uint64(block.timestamp),
            votes: 0
        });
        signatures.push(s);
        emit Published(signatures.length - 1, id, name, msg.sender);
        return signatures.length - 1;
    }

    function vote(uint256 index, bool up) external {
        require(index < signatures.length, "idx");
        if (up) signatures[index].votes += 1; else signatures[index].votes -= 1;
        emit Voted(index, signatures[index].votes);
    }

    function get(uint256 index) external view returns (Sig memory) {
        require(index < signatures.length, "idx");
        return signatures[index];
    }

    function count() external view returns (uint256) {
        return signatures.length;
    }
}
