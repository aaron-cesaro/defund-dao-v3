//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "../Pass/DefundPassManager.sol";

contract ComplianceLeague {
    DefundPassManager public defundPassManager;

    constructor(address _defundPassManager) {
        defundPassManager = DefundPassManager(_defundPassManager);
    }
}
