//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "../Pass/DefundPassManager.sol";

contract VentureLeague {
    DefundPassManager public defundPassManager;

    string private leagueImg;
    address[] private members;
    mapping(address => string) private roles;

    constructor(address _defundPassManager, string memory _leagueImg) {
        defundPassManager = DefundPassManager(_defundPassManager);
        leagueImg = _leagueImg;
    }

    function addLeagueMember(address _member, string memory _role)
        external
        returns (uint256)
    {
        defundPassManager.addLeagueMember(
            _member,
            leagueImg,
            "Venture League",
            _role
        );

        members.push(_member);
        roles[_member] = _role;
    }

    function removeLeagueMember(address _member, string memory _role)
        external
        returns (uint256)
    {
        (bool exists, uint256 memberPosition) = isLeagueMember(_member);
        require(exists, "removeLeagueMember: member does not exists");

        defundPassManager.removeLeagueMember(_member);

        for (
            uint256 index = memberPosition;
            index < members.length - 1;
            index++
        ) {
            members[index] = members[index + 1];
        }
        members.pop();
        delete roles[_member];
    }

    function isLeagueMember(address _member)
        internal
        view
        returns (bool, uint256)
    {
        uint256 memberPosition = 0;
        bool found = false;
        for (uint256 index = 0; index < members.length && !found; index++) {
            if (members[index] == _member) {
                found = true;
                memberPosition = index;
            }
        }

        return (found, memberPosition);
    }
}
