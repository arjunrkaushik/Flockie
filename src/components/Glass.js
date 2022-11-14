import './Glass.css'
import React, { useState } from 'react'
import { Routes, Route, useNavigate  } from 'react-router-dom'
import axios from 'axios'
import parse from "html-react-parser";
import {abi,contractAddress} from './sc_config'
import Web3 from 'web3'
import UploadPage from './UploadPage'
import Congrats from "./Congrats";

let myHtml=""
//let congrats=""
  const tempFunc = () => {
      let count = document.getElementById('gender').value;
      console.log(count);
      //let myHtml = '';
      for(let i = 1; i <= count; i++) {
          myHtml+="<br>Client " +i + " trained ";
      }

  }

  //const history = useHistory();

//const navigateToCongrats = () => {
    // 👇️ navigate to /contacts
   // history.push("/Congrats");
 // };

  //const result = () => {
  //  alert("Congratulations, weights uploaded");
  //}
//const Congrats = () => {
            //alert("Congratulations, weights uploaded");
    //congrats = "<p> HEAD </p>";

//};
//function Congrats(){
   // return <h2>Contacts</h2>;
//}

function Glass() {
  const [x, setx] = useState('')
  const [first, setfirst] = useState('')
  const [train, setTrain] = useState(false)
  const [grads, setGrads] = useState('')



  //const [active, setActive] = useState(false)

 // function printCongrats(){
     // setActive(Congrats)
  //}
//const navigate = useNavigate();

//const navigateCongrats = () => {
    // 👇️ navigate to /contacts
   //navigate('./Congrats');
 // };






//   const [workex, setWorkex] = useState('')
//   const [etest_p, setEtest_p] = useState('')
//   const [msc, setMsc] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const params = { x, first }

    axios
      .post('http://localhost:8080/train', params)
      .then((res) => {
        const data = res.data.data
        const parameters = JSON.stringify(params)
        // const msg = `weights: ${data.weights}`
        // alert(data)
        // upload(msg)
        //setGrads(data)
        console.log(data.client0)
        console.log(data.client1)
        console.log(data.client1)
        setTrain(true)
        // reset()
      })
      .catch((error) => alert(`Error: ${error.message}`))

  }

  const reset = () => {
    setx('')
    setfirst('')
  }

  const sc = () => {
    console.log("Helloo")
    // const web3 = new Web3("http://localhost:7545")
    // const fedLearning = new web3.eth.Contract(abi,contractAddress)
    // console.log(web3.eth.getAccounts())
  }


  return (
    <>
            <div className="glass">
                <form onSubmit={(e) => handleSubmit(e)} className="glass__form">
                    <h4>Train Clients</h4>
                    <div className="glass__form__group">
                        <input
                            id="gender"
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

                    <div className="glass__form__group">
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
                    </div>

                    <div className="glass__form__group">
                        <button type="submit" className="glass__form__btn" onClick={() => tempFunc()}>
                            Train
                        </button>
                    </div>
                </form>
            </div>

        {train && (         <div className="glass">
                <h1>Congrats</h1>
            </div>) }

    </>)
}

export default Glass
