import './Glass.css'
import { useState } from 'react'
import axios from 'axios'
import {abi,contractAddress} from './sc_config'
import Web3 from 'web3'


function UploadPage() {
  const [x, setx] = useState('')
  const [first, setfirst] = useState('')
//   const [workex, setWorkex] = useState('')
//   const [etest_p, setEtest_p] = useState('')
//   const [msc, setMsc] = useState('')

  



  return (
    <div className="glass">
      <button>
        Train
      </button>
      <button>
        Train
      </button>
      <button>
        Train
      </button>     
    </div>
  )
}

export default UploadPage