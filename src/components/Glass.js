import './Glass.css'
import { useState } from 'react'
import axios from 'axios'
import parse from "html-react-parser";
import {abi,contractAddress} from './sc_config'
import Web3 from 'web3'
import UploadPage from './UploadPage'

function Glass() {
  const [x, setx] = useState('')
  // const [first, setfirst] = useState('')
  const [train, setTrain] = useState(false)
  const [server, setServer] = useState(false)
  const [approve, setApprove] = useState(false)

  
  const web3 = new Web3("http://localhost:7545")
  const fedLearning = new web3.eth.Contract(abi,contractAddress) 
  const accounts = [] 
  


  const handleSubmit = async (e) => {
    e.preventDefault()
    const params = { x }
    const data = await axios.post('http://localhost:8080/train', params)
    console.log("Here", data.data.data)
    // const web3 = new Web3(
    //   new Web3.providers.HttpProvider(
    //     'https://goerli.infura.io/v3/5e882437de844dd481b7cdc0939fdcda'
    //   )
    // );

    // const signer = web3.eth.accounts.privateKeyToAccount(
    //   'd7cabcce4d3d9fc9ecfa6b41c216bd503cdee72c56ede3a332fa73d91d4ca0e6'
    // );
    // web3.eth.accounts.wallet.add(signer);
    const account_addr = await web3.eth.getAccounts()
    console.log(account_addr)
    for(let element in account_addr){
      accounts.push(account_addr[element])
    }
    console.log("Accounts List: ",accounts[1])
    fedLearning.methods.sendWeights(accounts[1], data.data.data.client0).send({from:accounts[0], gas: 3000000}); 
    fedLearning.methods.sendWeights(accounts[2], data.data.data.client1).send({from:accounts[0], gas: 3000000}); 
    fedLearning.methods.sendWeights(accounts[3], data.data.data.client2).send({from:accounts[0], gas: 3000000}); 
    // fedLearning.methods.sendWeights('0x3FFDA8413d779d5CB1d6505eDd21495761c1d4a3', data.data.data.client0).send({from:'0x8Ec8de8f504Ea59ecf000Ce359ae142409184ECc', gas: 3000000});
    // fedLearning.methods.sendWeights('0x21A073ce074aC1beB1E0a1F3Ab9BAEB42F1E253E', data.data.data.client1).send({from:'0x8Ec8de8f504Ea59ecf000Ce359ae142409184ECc', gas: 3000000});
    // fedLearning.methods.sendWeights('0xaBBCFcEA36e6EC40A08faBDaC3cd0fD06177E3C5', data.data.data.client2).send({from:'0x8Ec8de8f504Ea59ecf000Ce359ae142409184ECc', gas: 3000000});
    setTrain(true)
  }

  const handleAggregate = async() => {
    console.log("aggregation")
    const payload = []
    const client = await fedLearning.methods.getWeights(accounts[1]).call()
    console.log(client)
    payload.push(client)
    console.log("test")
    // await fedLearning.methods.getWeights('0x3FFDA8413d779d5CB1d6505eDd21495761c1d4a3').call().then((data)=>{
    //   payload.push(data)
    // });
    // console.log("aggregation1")
    // await fedLearning.methods.getWeights('0x21A073ce074aC1beB1E0a1F3Ab9BAEB42F1E253E').call().then((data) => {
    //   payload.push(data)
    // });
    // await fedLearning.methods.getWeights('0xaBBCFcEA36e6EC40A08faBDaC3cd0fD06177E3C5').call().then((data) => {
    //   payload.push(data)
    // });
    console.log("Client Hashes",payload)
    const data_agg = await axios.post('http://localhost:8080/aggregate', payload)
    console.log("Server data",data_agg.data.data)
    setServer(true)
    let chk;
    await fedLearning.methods.accuracyChecker(data_agg.data.data.hash, data_agg.data.data.accuracy).call().then(console.log)
    console.log("check", chk)
  }

  // const reset = () => {
  //   setx('')
  //   setfirst('')
  // }

  const sc = () => {
    console.log("Helloo")
    const web3 = new Web3("http://localhost:7545")
    const fedLearning = new web3.eth.Contract(abi,contractAddress)
    console.log(web3.eth.getAccounts())
  }
 
  return (
    <>
    {!train &&
    <div className="glass">
      <form onSubmit={(e) => handleSubmit(e)} className="glass__form">
        <h4>Train Clients</h4>
        <div className="glass__form__group">
          <input
            id="Client_count"
            className="glass__form__input"
            placeholder="Number of Clients"
            required
            autoFocus
            min="2"
            // max="1"
            pattern="[0-9]{0,1}"
            title="Client count"
            type="number"
            value={x}
            onChange={(e) => setx(e.target.value)}
          />
        </div>

        {/* <div className="glass__form__group">
          <input
            id="bsc"
            className="glass__form__input"
            placeholder="True or False"
            required
            // min="0"
            // max="5"
            type="bool"
            title="First time?"
            // pattern="[0-9]+([\.,][0-9]+)?"
            // step="0.01"
            value={first}
            onChange={(e) => setfirst(e.target.value)}
          />
        </div> */}

        <div className="glass__form__group">
          <button type="submit" className="glass__form__btn">
            Train Clients and Upload Gradients
          </button>
        </div>
      </form>
    </div>}

    {train && !server &&
    <div className="glass">
      <form onSubmit={() => handleAggregate()} className="glass__form">
        <h4>Aggregate Clients</h4>
        <div className="glass__form__group">
          <button type="submit" className="glass__form__btn">
            Approve
          </button>
        </div>
      </form>
    </div>}
    {server &&
      <div>
          <h4>Congratulations, your model has been approved!</h4>
      </div>}

    

    {train && server && !approve &&
    <div className="glass">
        <h4>Please improve your model and try again!</h4>
    </div>}

    </>)
}

export default Glass