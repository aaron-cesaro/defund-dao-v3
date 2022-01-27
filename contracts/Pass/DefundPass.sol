// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract DefundPass is ERC721URIStorage, ERC721Burnable, Pausable, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    event PassMinted(address indexed _to, uint256 indexed _tokenId);
    event PassBurned(uint256 indexed _tokenId);

    constructor() ERC721("DeFund Pass", "DFPS") {
        _pause();
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function mintPass(address to, string memory uri)
        public
        onlyOwner
        returns (uint256)
    {
        _unpause();

        _tokenIdCounter.increment();
        uint256 tokenId = _tokenIdCounter.current();

        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);

        emit PassMinted(to, tokenId);

        return tokenId;
    }

    function burnPass(uint256 _tokenId) public onlyOwner {
        _burn(_tokenId);

        emit PassBurned(_tokenId);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, tokenId);

        if (to != address(0)) {
            require(
                balanceOf(to) == 0,
                "_beforeTokenTransfer: members cannot have more than one badge"
            );
        }
    }

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override {
        super._afterTokenTransfer(from, to, tokenId);
        // Token has been minted
        if (from == address(0)) {
            _approve(msg.sender, tokenId);
        }
        // Token has been transferred, otherwise token has been burned
        else if (to != address(0)) {
            _approve(from, tokenId);
        }
        _pause();
    }

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        _unpause();

        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}
