## Educational Blockchain

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/facebook/react/blob/master/LICENSE)
[![CircleCI Status](https://circleci.com/gh/facebook/react.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/facebook/react)

A fun project to explore the wonders of the blockchain.

### Short description of what you attempted to build

In this project we built a blockchain, that is, a distributed ledger maintained
by independent nodes in the network. Rather than have one central database or entity
keep track of the network activity and state, it is maintained by the entire network.

For many years, computer scientists had pondered whether it was possible
to create a trustless, but trustworthy, network; a great number declared such a system of decentralized currency and transactions was impossible. In 2008,
a solution to this problem was proposed in the Bitcoin whitepaper. We have sought to understand this solution by implementing the kind of network it describes from the ground up.

Our starting point was [this tutorial on building a blockchain]( https://hackernoon.com/learn-blockchains-by-building-one-117428612f46).
Using this and building on top of it, we created three submodules for this project
that together create a functional blockchain network (though also a very naive one).

Submodules:

* blockchain-node: the 'miners' in the network, who maintain a record of the blockchain and who compete to put new transactions on the blockchain by racing to perform Proof of Work (PoW). They are rewarded with coins if they succeed in placing transactions on the blockchain.

* blockchain-wallet: in order to make a new transaction, you need a public address to send from, and a private key to sign transactions with so that nodes can verify
only you can send money from your account address (which acts as the public key).
This module manages your keys for you and abstracts away all this hashing and signature complication. Sending money is as easy as specifying a recipient and an amount!

* blockchain-client: website where anyone can inspect the current state of the ledger.


### Who did what (if you worked with someone else)

Partners: Kyle and Robin

Step 1: Tutorial. Done together

https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

This was done as partner programming (we switched computers halfway to split the commits). This basically got the blockchain-node set up in a basic form, to the
point where you could run it locally and hit it with postman requests to do transactions and mining (but no security measures or digital signatures to stop people from spending other people's money).


Step 2: Securing transactions by setting up public key / private key system. Primarily by Robin

To create an 'account' on the blockchain, you create a public/private keypair. Your public key is your address that is used to send and receive money. To make a transaction you now send along with the transaction a digital signature, basically the contents of the transaction signed with your private key. The nodes were to changed so that they would use the transaction and the public key to verify the digital signature attached, ensuring the sender of this transaction actually has access to the private key associated with this address.


Step 3: Wallet wrapper for making this private key signature stuff user friendly. Primarily by Robin

Users obviously do not want to mess around with creating their own digital signature of a transaction each time they want to send some money. The blockchain-wallet module gives you command line scripts that let you easily send money as long as your set your public and private keys in the environment variables. There are also some tests here to make sure that a malicious transaction is rejected by the nodes. It passes.

Step 4: Making the blockchain-node module work 'out-of-the-box' and on heroku. Primarily by Kyle.

The network relies on many nodes/miners running. It therefore must be easy to spin up your own node. The addition of a Pipfile, Procfile, and changes to the project structure make it so that anyone can clone the code and deploy to Heroku in a matter of minutes! Now anyone can easily become a miner and start earning coins, and more miners in turn makes the network faster and more secure!

Step 5: Make a website where anyone can see the blockchain state. Primarily by Kyle.

If you are running a node, you can easily see the entire blockchain since your
node maintains it. But if you just a have a wallet, or are interested in the network, you cannot see the state of the chain. This site changes it. It shows what its node believes to be the state of the chain. Remember there is no central authority, so this site could represent something different than other nodes think the blockchain is at that moment. In the long it is accurate though, since nodes come to consensus on the blockchain repeatedly.


### What you learned

We learned an immense amount about the blockchain, and the underlying tech of all the current cryptocurrency hype. It is easy to focus on the speculative bubble surrounding it, but it is super interesting to realize that underlying these coins is a significant computer science breakthrough that can remove middlemen for online transactions and establish a system where you need not trust anyone but the network as a whole.

In addition, we learned about making Flask apps deployable to heroku and distributable. For example, we had never used Pipfiles before, as usually we have just run our flask apps locally for fun.

We also touched up on our cryptography, using hashing algorithms and RSA keys to
ensure security on our network.


### What didn’t work

We did not have time to finish some important features. There is no balance checking, so right now you can send any amount from your account to another account and it will go through. This makes the supply infinite, and it is quite possibly the most inflationary currency in history as anyone can print money anytime they want.

Nodes do not take backups of the chain, which means if all the nodes went down at the same time, and could not ask each other for the chain when they come up, the blockchain would be lost. Probably not something people will put their money in yet.


### Running the Code

To start a node, run `python blockchain-node/app.py`. It should listen on port 5000 or 5001.

Now, you can send a transaction to that node using the wallet. Create your account with `python blockchain-wallet/generate_wallet.py`. This will give you public and private keys. Save these as environment variables ('COIN_PRIVATE' and 'COIN_PUBLIC').
Now edit `wallet.py` at the bottom of the file to change the amount and recipient. Run `python wallet.py` and this transaction will be sent to your locally running node. Now, next time you use postman to hit your node's mining endpoint, this transaction will be included in its next block and you will see it on the blockchain.

### Acknowledgements

The implementation of the blockchain node is adapted from a tutorial by Daniel van Flymen that can be found [here](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46).
