// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract FedLearning{
    mapping(address => uint256[][][]) public client_weights;
    mapping(uint256 => bool) public class_cnt;
    address[] client_address;
    uint256[][][] aggregate_weights;

    function sendWeight(uint256[][][] memory x) public {
        client_weights[msg.sender] = x;
        client_address.push(msg.sender);
    }

    function aggregate() public {
        uint256[][] memory coef = client_weights[client_address[0]][0];
        uint256[][] memory intercept = client_weights[client_address[0]][1];
        uint256[] storage classes = client_weights[client_address[0]][2][0];
        for(uint256 i=0;i<client_weights[client_address[0]][2][0].length;i++){
            classes.push(client_weights[client_address[0]][2][0][i]);
            class_cnt[client_weights[client_address[0]][2][0][i]]=true;
        }
        for(uint i=1;i<client_address.length;i++){
            coef = add(coef,client_weights[client_address[i]][0]);
            intercept = add(intercept, client_weights[client_address[i]][1]);
            for(uint j=0;j<client_weights[client_address[i]][2][0].length;j++){
                if(class_cnt[client_weights[client_address[i]][2][0][j]] == false){
                    classes.push(client_weights[client_address[i]][2][0][j]);
                    class_cnt[client_weights[client_address[i]][2][0][j]] = true;
                }
            }
        }
        coef = div(coef, client_address.length);
        intercept = div(intercept, client_address.length);
        uint256[][] memory temp = new uint256[][](1);
        temp[0] = classes;
        aggregate_weights.push(coef);
        aggregate_weights.push(intercept);
        aggregate_weights.push(temp);
    }

    function add(uint256[][] memory x, uint256[][] memory y) public view returns (uint256[][] memory){
        for(uint i=0;i<x.length;i++){
            for(uint j=0;j<x[0].length;j++){
                x[i][j] += y[i][j];
            }
        }
        return x;
    }

    function div(uint256[][] memory x, uint256 n) public view returns(uint256[][] memory){
        for(uint i=0;i<x.length;i++){
            for(uint j=0;j<x[0].length;j++){
                x[i][j] /= n;
            }
        }
        return x;
    }

}