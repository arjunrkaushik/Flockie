var fedLearning = artifacts.require("FedLearning");
var flockie = artifacts.require("Flockie");

module.exports = function(deployer) {
    deployer.deploy(fedLearning);
    deployer.deploy(flockie);
};