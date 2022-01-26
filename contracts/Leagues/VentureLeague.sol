//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "../Pass/DefundPassManager.sol";

contract VentureLeague {
    DefundPassManager public defundPassManager;

    string private leagueImg;
    address[] private members;
    string[] private roles;
    mapping(address => string) private memberRoles;

    string public constant LEAGUE_NAME = "Venture League";

    constructor(
        address _defundPassManager,
        string memory _leagueImg,
        string[] memory _roles
    ) {
        defundPassManager = DefundPassManager(_defundPassManager);
        leagueImg = _leagueImg;

        roles = _roles;
    }

    function addLeagueMember(address _member, uint256 _roleIndex)
        external
        returns (uint256)
    {
        require(_roleIndex <= roles.length, "addLeagueMember: invalid role");
        require(
            !memberExists(_member),
            "addLeagueMember: member already present"
        );

        string memory roleName = roles[_roleIndex];

        uint256 tokenId = defundPassManager.addLeagueMember(
            _member,
            leagueImg,
            LEAGUE_NAME,
            roleName
        );

        members.push(_member);
        memberRoles[_member] = roleName;

        return tokenId;
    }

    function removeLeagueMember(address _member) external returns (uint256) {
        (bool found, uint256 memberPosition) = findLeagueMember(_member);
        require(found, "removeLeagueMember: member does not exists");

        defundPassManager.removeMember(_member);

        for (
            uint256 index = memberPosition;
            index < members.length - 1;
            index++
        ) {
            members[index] = members[index + 1];
        }
        members.pop();
        delete memberRoles[_member];
    }

    function getRole(address _member) external view returns (string memory) {
        require(_member != address(0), "getRole: invalid address");
        return memberRoles[_member];
    }

    function memberExists(address _member) public view returns (bool) {
        (bool exists, ) = findLeagueMember(_member);

        return exists;
    }

    function findLeagueMember(address _member)
        internal
        view
        returns (bool, uint256)
    {
        require(_member != address(0), "findLeagueMember: invalid address");
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
