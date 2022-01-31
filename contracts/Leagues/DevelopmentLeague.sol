//SPDX-License-Identifier: MIT

pragma solidity ^0.8;

import "../Pass/DefundPass.sol";

contract DevelopmentLeague {
    DefundPass public defundPass;

    constructor(address payable _defundPass) {
        defundPass = DefundPass(_defundPass);
    }
}
