//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "../Pass/DeFundPassManager.sol";

contract TreasuryLeague {
    DeFundPassManager public defundPassManager;

    constructor(address _defundPassManager) {
        defundPassManager = DeFundPassManager(_defundPassManager);
    }
}
