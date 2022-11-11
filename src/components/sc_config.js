
export const contractAddress = '0x6f192172563615fE2Ca84DBd54d6FaE8A36ECa82'
export const abi = [
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "class_cnt",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": true
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "client_weights",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": true
    },
    {
      "inputs": [
        {
          "internalType": "uint256[][][]",
          "name": "x",
          "type": "uint256[][][]"
        }
      ],
      "name": "sendWeight",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "aggregate",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256[][]",
          "name": "x",
          "type": "uint256[][]"
        },
        {
          "internalType": "uint256[][]",
          "name": "y",
          "type": "uint256[][]"
        }
      ],
      "name": "add",
      "outputs": [
        {
          "internalType": "uint256[][]",
          "name": "",
          "type": "uint256[][]"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": true
    },
    {
      "inputs": [
        {
          "internalType": "uint256[][]",
          "name": "x",
          "type": "uint256[][]"
        },
        {
          "internalType": "uint256",
          "name": "n",
          "type": "uint256"
        }
      ],
      "name": "div",
      "outputs": [
        {
          "internalType": "uint256[][]",
          "name": "",
          "type": "uint256[][]"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": true
    }
  ];

