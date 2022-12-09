// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./fedLearning.sol";

contract Flockie is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    mapping(address => bool) public isRegistered;
    mapping(address => bool) public hasVoted;

    uint voterCount = 0;
    uint update = 0; 
    uint noUpdate = 0;

    constructor() ERC721("Flockie", "FLK") {}

    // modifier onlyVoter() {
    //     require(isRegistered[msg.sender] == true);
    //     _;
    // }

    function mintNFT(address recipient, string memory tokenURI)
        public
        returns (uint256)
    {
        _tokenIds.increment();

        uint256 newItemId = _tokenIds.current();
        _mint(recipient, newItemId);
        _setTokenURI(newItemId, tokenURI);
        
        isRegistered[recipient] = true;
        hasVoted[recipient] = false;
        voterCount += 1;

        return newItemId;
    }

    function vote(address voter, uint acc) public payable {
        assert(isRegistered[voter]==true); //voter == msg.sender
        if(acc > 7500000){
            update += 1;
        }
        else{
            noUpdate += 1;
        }
        hasVoted[voter] = true;
    }

    function getVoteUpdate() public view returns(bool){
        assert(update + noUpdate == voterCount);
        if(update > noUpdate){
            return true;
        }
        return false;
    }


}