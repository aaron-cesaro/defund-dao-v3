//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "./DeFundPass.sol";

contract DeFundPassManager {
    DeFundPass public deFundPass;

    mapping(string => string) private tokenURIs;
    mapping(address => uint256) public membersIds;
    mapping(address => string) public leagueMembers;

    constructor(address _deFundPass) {
        deFundPass = DeFundPass(_deFundPass);
    }

    function isMember(address _member) public view returns (bool) {
        return deFundPass.balanceOf(_member) > 0;
    }

    function ownerOf(uint256 _tokenId) public view returns (address) {
        return deFundPass.ownerOf(_tokenId);
    }

    function addSimpleMember(address _member) public returns (uint256) {
        require(
            !isMember(_member),
            "addSimpleMember: address is already a member"
        );
        string memory tokenURI = tokenURIs["member"];
        uint256 tokenId = deFundPass.mintPass(_member, tokenURI);

        membersIds[_member] = tokenId;

        return tokenId;
    }

    function removeSimpleMember(address _member) public {
        require(
            isMember(_member),
            "removeSimpleMember: address is not a member"
        );
        uint256 tokenId = membersIds[_member];
        deFundPass.burnPass(tokenId);

        delete membersIds[_member];
    }

    function addLeagueMember(address _member, string memory _league)
        public
        returns (uint256)
    {
        require(isMember(_member), "addLeagueMember: address is not a member");
        require(
            bytes(leagueMembers[_member]).length <= 0,
            "addLeagueMember: address already belongs to a League"
        );

        string memory tokenURI = tokenURIs[_league];

        require(
            bytes(tokenURI).length > 0,
            "addLeagueMember: League not valid"
        );
        uint256 tokenId = deFundPass.mintPass(_member, tokenURI);

        membersIds[_member] = tokenId;
        leagueMembers[_member] = _league;

        return tokenId;
    }

    function removeLeagueMember(address _member, string memory _league) public {
        require(
            isMember(_member),
            "removeLeagueMember: address is not a member"
        );
        require(
            bytes(leagueMembers[_member]).length > 0,
            "removeLeagueMember: address does not belong to the League"
        );

        uint256 tokenId = membersIds[_member];
        deFundPass.burnPass(tokenId);

        delete membersIds[_member];
        delete leagueMembers[_member];
    }
}
