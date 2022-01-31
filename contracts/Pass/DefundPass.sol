// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/AccessControlEnumerable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@brechtpd/base64.sol";

/** @title DeFund Pass */
contract DefundPass is
    ERC721URIStorage,
    ERC721Burnable,
    Pausable,
    AccessControlEnumerable
{
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    string private standardPassImg;

    bytes32 public constant LEAGUE_ROLE = keccak256("LEAGUE_ROLE");

    mapping(address => bool) private members;
    uint256 private membersCount;

    event PassMinted(address indexed _to, uint256 indexed _tokenId);
    event PassBurned(uint256 indexed _tokenId);
    event LeaguePassMinted(address indexed _member, uint256 indexed _tokenId);
    event LeaguePassBurned(uint256 indexed _tokenId);

    /** @dev Contructor takes one arguments, initializes all basic roles, and pause the contract
     * @param _standardPassImg the ipfs url used by the standard Pass images
     */

    constructor(string memory _standardPassImg) ERC721("DeFund Pass", "DFPS") {
        standardPassImg = _standardPassImg;

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(LEAGUE_ROLE, msg.sender);

        _pause();
    }

    /**
     * @notice Use this function to buy (mint) a standard DeFund Pass.
     *         No one can own more than one Standard Pass and cost of each Standard Pass is 1 AVAX.
     * @dev mint a new DeFund Pass, using the standardPassImage used by this contract.
     * @param to the address that will have ownership on the minted Pass
     * @return the Pass Token Id
     */
    function buyPass(address to) external payable returns (uint256) {
        require(!isMember(to), "buyPass: address is already a member");
        require(
            !hasRole(LEAGUE_ROLE, to),
            "buyPass: members cannot have more than one role"
        );
        require(
            msg.value == 1,
            "buyPass: wrong amount. DeFund Passes cost 1 AVAX each"
        );

        uint256 tokenId = _tokenIdCounter.current();

        _safeMint(to, tokenId);

        string memory _tokenURI = formatTokenURI(
            standardPassImg,
            "STANDARD",
            "MEMBER"
        );
        _setTokenURI(tokenId, _tokenURI);

        members[to] = true;
        membersCount++;

        _tokenIdCounter.increment();

        emit PassMinted(to, tokenId);

        return tokenId;
    }

    /**
     * @notice Use this function to burn mint a standard DeFund Pass.
     *         Only the Pass owner or the Admin can burn a Pass.
     * @dev if '_tokenId' does not exists the function reverts.
     * @param _tokenId the Token Id to burn
     */
    function burnPass(uint256 _tokenId) public {
        address passOwner = ownerOf(_tokenId);
        require(
            msg.sender == passOwner || hasRole(DEFAULT_ADMIN_ROLE, msg.sender),
            "burnPass: pass cannot be burned by this address"
        );
        require(isMember(passOwner), "burnPass: invalid member");

        _burn(_tokenId);

        delete members[passOwner];
        membersCount--;

        emit PassBurned(_tokenId);
    }

    /**
     * @notice Use this function to mint a League DeFund Pass.
     *         All League members must own a Standard Pass before been able to be awarded a League Pass.
     *         No one can own more than one League Pass and League Passes have no costs.
     * @dev mint a new DeFund Pass, using the standardPassImage used by this contract.
     * @param to the address that will have ownership on the minted Pass
     * @param _leaguePassImg the ipfs url of the image representing the league that is minting the pass
     * @param _league league that is minting the pass
     * @param _role role that the new member will assume within the League
     * @return the League Pass Token Id
     */
    function mintLeaguePass(
        address to,
        string calldata _leaguePassImg,
        string calldata _league,
        string calldata _role
    ) public onlyRole(LEAGUE_ROLE) returns (uint256) {
        require(isMember(to), "mintLeaguePass: address is not a member");
        require(
            !hasRole(LEAGUE_ROLE, to),
            "mintLeaguePass: address is already a league member"
        );

        uint256 tokenId = _tokenIdCounter.current();

        _safeMint(to, tokenId);

        string memory _tokenURI = formatTokenURI(
            _leaguePassImg,
            _league,
            _role
        );
        _setTokenURI(tokenId, _tokenURI);

        _tokenIdCounter.increment();

        _grantRole(LEAGUE_ROLE, to);

        emit LeaguePassMinted(to, tokenId);

        return tokenId;
    }

    function burnLeaguePass(uint256 _tokenId) public onlyRole(LEAGUE_ROLE) {
        address _member = ownerOf(_tokenId);

        require(
            msg.sender == _member || hasRole(DEFAULT_ADMIN_ROLE, msg.sender),
            "burnLeaguePass: pass cannot be burned by this address"
        );

        require(
            hasRole(LEAGUE_ROLE, _member),
            "burnLeaguePass: invalid member"
        );

        _burn(_tokenId);

        _revokeRole(LEAGUE_ROLE, _member);

        emit LeaguePassBurned(_tokenId);
    }

    function isMember(address _address) public view returns (bool) {
        return members[_address];
    }

    function getMembersCount() public view returns (uint256) {
        return membersCount;
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, tokenId);
        // preventing transfer
        if (from != address(0) && to != address(0)) {
            require(
                hasRole(DEFAULT_ADMIN_ROLE, msg.sender),
                "_beforeTokenTransfer: only admin can transfer passes"
            );
        }
    }

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override {
        super._afterTokenTransfer(from, to, tokenId);
        _pause();
    }

    function formatTokenURI(
        string memory imageURI,
        string memory _membership,
        string memory _role
    ) internal pure returns (string memory) {
        string memory json = string(
            abi.encodePacked(
                '{"name":"Defund Pass - ',
                _membership,
                '","description":"DeFund Pass","image":"',
                imageURI,
                '","attributes":[{"trait_type":"Membership","value":"',
                _membership,
                '"},{"trait_type":"Role","value":"',
                _role,
                '"}]}'
            )
        );
        string memory _tokenURI = string(
            abi.encodePacked(
                "data:application/json;base64,",
                Base64.encode(bytes(json))
            )
        );

        return _tokenURI;
    }

    function pause() public onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, AccessControlEnumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    receive() external payable {
        // Thank you for your donation! Unfortunately we cannot accept it :)
        payable(msg.sender).transfer(msg.value);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function _safeMint(address to, uint256 tokenId) internal virtual override {
        _unpause();

        super._safeMint(to, tokenId);
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        _unpause();

        super._burn(tokenId);
    }
}
