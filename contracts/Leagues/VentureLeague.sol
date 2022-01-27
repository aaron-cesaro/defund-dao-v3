//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "../Pass/DefundPassManager.sol";

contract VentureLeague {
    DefundPassManager public defundPassManager;

    string private leagueImg;
    address[] private members;
    bytes32[] private roles;
    mapping(address => bytes32) private memberRoles;

    string public constant LEAGUE_NAME = "VENTURE_LEAGUE";

    event RoleAdded(string indexed _role);
    event RoleRemoved(string indexed _role);
    event MemberAdded(address indexed _member, string indexed _role);
    event MemberRemoved(address indexed _member);

    constructor(
        address _defundPassManager,
        string memory _leagueImg,
        string[] memory _roles
    ) {
        defundPassManager = DefundPassManager(_defundPassManager);
        leagueImg = _leagueImg;

        for (uint256 index = 0; index < _roles.length; index++) {
            roles.push(keccak256(bytes(_roles[index])));
        }
    }

    function addLeagueMember(address _member, string memory _role)
        external
        returns (uint256)
    {
        require(
            bytes(_role).length >= 2,
            "addLeagueMember: invalid role format"
        );
        (bool roleExists, int256 rolePosition) = hasRole(_role);
        require(roleExists, "addLeagueMember: invalid role");
        require(
            !memberExists(_member),
            "addLeagueMember: member already present"
        );

        uint256 tokenId = defundPassManager.addLeagueMember(
            _member,
            leagueImg,
            LEAGUE_NAME,
            _role
        );

        members.push(_member);
        memberRoles[_member] = roles[uint256(rolePosition)];

        emit MemberAdded(_member, _role);

        return tokenId;
    }

    function removeLeagueMember(address _member) external returns (uint256) {
        (bool found, int256 memberPosition) = findLeagueMember(_member);
        require(found, "removeLeagueMember: member does not exists");

        defundPassManager.removeMember(_member);

        for (
            uint256 index = uint256(memberPosition);
            index < members.length - 1;
            index++
        ) {
            members[index] = members[index + 1];
        }
        members.pop();
        delete memberRoles[_member];

        emit MemberRemoved(_member);
    }

    function addRole(string memory _role) external {
        (bool exists, ) = hasRole(_role);
        require(!exists, "addRole: role already exists");
        roles.push(keccak256(bytes(_role)));

        emit RoleAdded(_role);
    }

    function removeRole(string memory _role) external {
        (bool exists, int256 rolePosition) = hasRole(_role);
        require(
            exists &&
                rolePosition >= 0 &&
                uint256(rolePosition) <= roles.length,
            "removeRole: role does not exist"
        );
        for (
            uint256 index = uint256(rolePosition);
            index < roles.length - 1;
            index++
        ) {
            roles[index] = roles[index + 1];
        }
        roles.pop();
    }

    function hasRole(string memory _role) public view returns (bool, int256) {
        require(bytes(_role).length > 4, "hasRole: invalid role");
        bool found = false;
        int256 roleIndex = -1;
        for (uint256 index = 0; index < roles.length && !found; index++) {
            if (roles[index] == keccak256(bytes(_role))) {
                found = true;
                roleIndex = int256(index);
            }
        }
        return (found, roleIndex);
    }

    function memberExists(address _member) public view returns (bool) {
        (bool exists, ) = findLeagueMember(_member);

        return exists;
    }

    function findLeagueMember(address _member)
        public
        view
        returns (bool, int256)
    {
        require(_member != address(0), "findLeagueMember: invalid address");
        bool found = false;
        int256 memberPosition = -1;
        for (uint256 index = 0; index < members.length && !found; index++) {
            if (members[index] == _member) {
                found = true;
                memberPosition = int256(index);
            }
        }

        return (found, memberPosition);
    }
}
