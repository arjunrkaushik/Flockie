var fedLearning = artifacts.require("FedLearning");

module.exports = function(deployer) {
    deployer.deploy(fedLearning);
};