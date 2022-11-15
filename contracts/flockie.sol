// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

contract FedLearning{
    mapping(address => string) public client_weights;
    address[] client_address;
    string server;

    function sendWeights(address x, string memory y) public {
        client_weights[x] = y;
        client_address.push(x);
    }

    function getServer() public view returns(string memory){
        return server;
    }

    function getWeights(address a) public view returns(string memory){
        return client_weights[a];
    }    

    function accuracyChecker(string memory z, uint acc) public returns (bool){
        if(acc > 8000000){
            server = z;
            return true;
        }
        return false;
    }    


}