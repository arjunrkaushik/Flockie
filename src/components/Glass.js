import './Glass.css'
import { useState } from 'react'
import axios from 'axios'
import parse from "html-react-parser";
import {abi_fedLearning,contractAddress_fedLearning, abi_flockie, contractAddress_flockie, FLK_wolf, FLK_elephant, FLK_tiger} from './sc_config'
import Web3 from 'web3'
import UploadPage from './UploadPage'

function Glass() {
  const [x, setx] = useState('')
  // const [first, setfirst] = useState('')
  const [train, setTrain] = useState(false)
  const [approve, setApprove] = useState(false)
  const [server, setServer] = useState(false)
  const [update, setUpdate] = useState(false)
  
  const web3 = new Web3("http://localhost:7545")
  const fedLearning = new web3.eth.Contract(abi_fedLearning,contractAddress_fedLearning)
  const flockie = new web3.eth.Contract(abi_flockie, contractAddress_flockie) 


  const handleSubmit = async (e) => {
    e.preventDefault()
    const params = { x }
    const data = await axios.post('http://localhost:8080/train', params)
    var accounts = []
    const account_addr = await web3.eth.getAccounts()
    console.log(account_addr)
    for(var element in account_addr){
      accounts.push(account_addr[element])
    }
    console.log("Accounts List: ",accounts[1])
    fedLearning.methods.sendWeights(accounts[1], data.data.data.client0).send({from:accounts[0], gas: 3000000}); 
    fedLearning.methods.sendWeights(accounts[2], data.data.data.client1).send({from:accounts[0], gas: 3000000}); 
    fedLearning.methods.sendWeights(accounts[3], data.data.data.client2).send({from:accounts[0], gas: 3000000}); 
    setTrain(true)
  }

  const handleAggregate = async(e) => {
    e.preventDefault()

    const accounts = []
    const account_addr = await web3.eth.getAccounts()
    for(const element in account_addr){
      accounts.push(account_addr[element])
    }

    const payload = []
    await fedLearning.methods.getWeights(accounts[1]).call().then((data)=>{
      payload.push(data)
    });
    console.log("aggregation1")
    await fedLearning.methods.getWeights(accounts[2]).call().then((data) => {
      payload.push(data)
    });
    await fedLearning.methods.getWeights(accounts[3]).call().then((data) => {
      payload.push(data)
    });

    //Mint NFT
    await flockie.methods.mintNFT(accounts[4], FLK_wolf).send({from:accounts[0], gas: 3000000});
    await flockie.methods.mintNFT(accounts[5], FLK_elephant).send({from:accounts[0], gas: 3000000});
    await flockie.methods.mintNFT(accounts[6], FLK_tiger).send({from:accounts[0], gas: 3000000});

    const data_agg = await axios.post('http://localhost:8080/aggregate', payload)
    setServer(true)
    await flockie.methods.vote(accounts[4], data_agg.data.data.accuracy[0]).send({from:accounts[0], gas: 3000000});
    await flockie.methods.vote(accounts[5], data_agg.data.data.accuracy[1]).send({from:accounts[0], gas: 3000000});
    await flockie.methods.vote(accounts[6], data_agg.data.data.accuracy[2]).send({from:accounts[0], gas: 3000000});

    const upd = await flockie.methods.getVoteUpdate().call()

    if(upd){
      await fedLearning.methods.setServer(data_agg.data.data.hash).call().then((data) => {
        setUpdate(true)
        setApprove(data)
      })
    }
  }

  // const reset = () => {
  //   setx('')
  //   setfirst('')
  // }

 
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
      <form onSubmit={(e) => handleAggregate(e)} className="glass__form">
        <h4>Aggregate Clients</h4>
        <div className="glass__form__group">
          <button type="submit" className="glass__form__btn">
            Approve
          </button>
        </div>
      </form>
    </div>}
    
    {train && server && approve &&
      <div className="glass">
          <h4>Congratulations, your model has been approved!</h4>
      </div>}

    

    {train && server && !approve &&
    <div className="glass">
        <h4>Please improve your model and try again!</h4>
    </div>}

    </>)
}

export default Glass