// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

import "./flockie.sol";

contract FedLearning{
    string server;
    uint voterCount = 0;
    uint clientCount = 0;
    mapping(address => string) clientWeights;

    constructor() public {
        // Initilizing default values
        clientCount = 0;
        voterCount = 0;
    }

    function sendWeights(address x, string memory y) public {
        clientWeights[x] = y;
    }

    function setServer(string memory serverHash) public returns(bool){
        server = serverHash;
        return true;
    }


    function getServer() public view returns(string memory){
        return server;
    }

    function getWeights(address a) public view returns(string memory){
        // assert(msg.sender == a);
        return clientWeights[a];
    }    

    // function accuracyChecker(string memory z, uint acc) public returns (bool){
    //     if(acc > 8000000){
    //         server = z;
    //         return true;
    //     }
    //     return false;
    // }    


}