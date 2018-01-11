import React, { Component } from 'react';
import axios from 'axios'

import RaisedButton from 'material-ui/RaisedButton';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';

import './App.css';

const PREFIX = 'http://'
const LIVE_NODE = 'https://blockchain-node-0.herokuapp.com'

class App extends Component {
  constructor() {
    super()
    this.state = {
      chain: [],
      nodes: [],
      selectedNodeIdx: -1
    }

    this.handleNodeChange = this.handleNodeChange.bind(this)
    this.handleChainRefresh = this.handleChainRefresh.bind(this)
  }

  componentWillMount() {
    axios.get(`${LIVE_NODE}/nodes/list`)
      .then((response) => {
        this.setState({
          nodes: response.data.total_nodes
        })
      })
      .catch((error) => {
        console.log(error)
      })
  }

  handleNodeChange(event, index, value) {
    this.setState({
      selectedNodeIdx: index
    })
  }

  handleChainRefresh() {
    const currentNode = this.state.nodes[this.state.selectedNodeIdx]

    if (currentNode) {
      axios.get(PREFIX + currentNode + '/chain')
        .then(response => {
          this.setState({
            chain: response.data.chain
          })
        })
        .catch(error => {
          console.log(error)
        })
    }
  }

  render() {
    let blockchain
    if (this.state.chain) {
      blockchain = this.state.chain.map(b => {
        return <Block
                key={b.index}
                index={b.index}
                previousHash={b.previous_hash}
                proof={b.proof}
                timestamp={b.timestamp}
                transactions={b.transactions} />
      })
    }

    let nodeMenuItems
    if (this.state.nodes.length > 0) {
      nodeMenuItems = this.state.nodes.map((n, i) => {
        return  <MenuItem key={i} value={i} primaryText={n} />
      })
    }

    return (
      <div className="App">
        <h1 className="App-title">Blockchain Explorer</h1>
        <SelectField
          floatingLabelText="Node"
          value={this.state.selectedNodeIdx}
          onChange={this.handleNodeChange}>
          {nodeMenuItems}
        </SelectField>
        <div className='spacer-div'></div>
        <RaisedButton label="Refresh Chain" onClick={this.handleChainRefresh} />
        <div className='spacer-div'></div>
        <div className='blockchain-container'>
          {blockchain}
        </div>
      </div>
    );
  }
}

const Block = (props) => {
  return (
    <div className="block-container">
      <div>{`Index: ${props.index}`}</div>
      <div>{`Previous Hash: ${props.previousHash}`}</div>
      <div>{`Proof: ${props.proof}`}</div>
      <div>{`Timestamp: ${props.timestamp}`}</div>
      <div>{`Transaction Count: ${props.transactions.length}`}</div>
    </div>
  )
}

export default App;
