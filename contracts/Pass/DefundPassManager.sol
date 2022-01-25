//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "@brechtpd/base64.sol";
import "./DefundPass.sol";

contract DefundPassManager {
    DefundPass public defundPass;

    mapping(address => uint256) public membersIds;

    constructor(address _defundPass) {
        defundPass = DefundPass(_defundPass);
    }

    function isMember(address _member) public view returns (bool) {
        return defundPass.balanceOf(_member) > 0;
    }

    function ownerOf(uint256 _tokenId) public view returns (address) {
        return defundPass.ownerOf(_tokenId);
    }

    function addStandardMember(address _member, string memory _passImg)
        external
        returns (uint256)
    {
        require(
            !isMember(_member),
            "addStandardMember: address is already a member"
        );
        string memory tokenURI = formatTokenURI(
            _passImg,
            "Standard",
            "Investor"
        );

        uint256 tokenId = defundPass.mintPass(_member, tokenURI);

        membersIds[_member] = tokenId;

        return tokenId;
    }

    function addLeagueMember(
        address _member,
        string memory _passImg,
        string memory _league,
        string memory _role
    ) external returns (uint256) {
        require(bytes(_role).length > 0, "addLeagueMember: invalid role");
        require(
            isMember(_member),
            "addLeagueMember: only members can access leagues"
        );

        // remove current membership
        removeMember(_member);

        string memory tokenURI = formatTokenURI(_passImg, _league, _role);

        uint256 tokenId = defundPass.mintPass(_member, tokenURI);

        membersIds[_member] = tokenId;

        return tokenId;
    }

    function removeMember(address _member) public {
        require(isMember(_member), "removeMember: address is not a member");
        uint256 tokenId = membersIds[_member];
        defundPass.burnPass(tokenId);

        delete membersIds[_member];
    }

    function formatTokenURI(
        string memory imageURI,
        string memory _league,
        string memory _role
    ) internal pure returns (string memory) {
        string memory json = string(
            abi.encodePacked(
                '{"name":"'
                "Defund Pass"
                '", "description":"DeFund Pass", "image":"',
                imageURI,
                '", "attributes": [ {"trait_type":"Membership", "value":"',
                _league,
                '"},{"trait_type":"Role", "value":"',
                _role,
                '"}]}'
            )
        );
        string memory tokenURI = string(
            abi.encodePacked(
                "data:application/json;base64,",
                Base64.encode(bytes(json))
            )
        );

        return tokenURI;
    }
}