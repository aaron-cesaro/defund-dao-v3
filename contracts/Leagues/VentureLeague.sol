//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "@openzeppelin/contracts/access/AccessControlEnumerable.sol";
import "../Pass/DefundPass.sol";

contract VentureLeague is AccessControlEnumerable {
    bytes32 public constant ANALYST_ROLE = keccak256("ANALYST_ROLE");
    DefundPass public defundPass;

    string private ventureLeagueImg;
    address[] private members;
    bytes32[] private roles;
    mapping(address => bytes32) private memberRoles;

    string public constant LEAGUE_NAME = "VENTURE_LEAGUE";

    event RoleAdded(string indexed _role);
    event RoleRemoved(string indexed _role);
    event MemberAdded(address indexed _member);
    event MemberRemoved(address indexed _member);

    constructor(address _defundPass, string memory _ventureLeagueImg) {
        defundPass = DefundPass(_defundPass);
        ventureLeagueImg = _ventureLeagueImg;

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ANALYST_ROLE, msg.sender);
    }

    function addLeagueMember(address _member)
        external
        onlyRole(DEFAULT_ADMIN_ROLE)
        returns (uint256)
    {
        require(
            !hasRole(ANALYST_ROLE, _member),
            "addLeagueMember: address is already a member"
        );

        uint256 tokenId = defundPass.mintLeaguePass(
            _member,
            ventureLeagueImg,
            LEAGUE_NAME,
            "ANALYST"
        );

        emit MemberAdded(_member);

        return tokenId;
    }

    function removeLeagueMember(uint256 _tokenId) external returns (uint256) {
        address member = defundPass.ownerOf(_tokenId);
        require(
            hasRole(ANALYST_ROLE, member),
            "addLeagueMember: address is already a member"
        );

        defundPass.burnLeaguePass(_tokenId);

        emit MemberRemoved(member);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
