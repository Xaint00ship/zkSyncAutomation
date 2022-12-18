from zksync_sdk.lib import ZkSyncLibrary
from zksync_sdk.zksync_provider import ZkSyncProviderV01
from zksync_sdk.network import goerli, mainnet
from zksync_sdk.transport.http import HttpJsonRPCTransport
from zksync_sdk.zksync_signer import ZkSyncSigner
from web3 import Web3, HTTPProvider, Account
from zksync_sdk.zksync import ZkSync
from zksync_sdk.ethereum_provider import  EthereumProvider
from zksync_sdk.wallet import Wallet
from zksync_sdk.ethereum_signer import EthereumSignerWeb3
from decimal import Decimal
import asyncio
import os
from ipfs2bytes32 import Ipfs2bytes32

class WalletFunction:

    def __init__(self, secretKey, endpointURL):
        __path = os.path.dirname(os.path.abspath(__file__)) 
        self.lib = ZkSyncLibrary(__path + "/src/zks-crypto-x86_64-pc-windows-gnu.dll") # сделать проверку ОСи для выбора нужного файла.
        self.account = Account.from_key(secretKey) # переписать под безопасное хранение 
        self.endpointURL = endpointURL# брать из файла-конфига
        self.network = goerli  
        self.loop = asyncio.get_event_loop()
        self.wallet = self.loop.run_until_complete(self.getWallet(self.account, self.endpointURL, self.network))    
 


    async def getWallet(self, account, endpointURL, network):
        ethereum_signer = EthereumSignerWeb3(account = account)
        w3 = Web3(HTTPProvider(endpoint_uri = endpointURL)) 
        provider = ZkSyncProviderV01(provider = HttpJsonRPCTransport(network = network))
        address = await provider.get_contract_address()
        zksync = ZkSync(account = account,
        web3 = w3,
        zksync_contract_address = address.main_contract)
        ethereum_provider = EthereumProvider(w3, zksync)
        signer = ZkSyncSigner.from_account(account, self.lib, network.chain_id)

        return Wallet(ethereum_provider=ethereum_provider, zk_signer=signer,eth_signer=ethereum_signer, provider=provider)



    def getBalance(self, token):
        committedETHBalance  = self.loop.run_until_complete(self.wallet.get_balance(token, "committed"))    
        verifiedETHBalance = self.loop.run_until_complete(self.wallet.get_balance(token, "verified"))

        return {"commited":committedETHBalance, "verified":verifiedETHBalance}



    def deposit(self, valueDeposit, token):
        token = self.loop.run_until_complete(self.wallet.resolve_token(token))
        deposit = self.loop.run_until_complete(self.wallet.ethereum_provider.deposit(token, Decimal(valueDeposit),  self.account.address))

        return deposit



    def mintingNFT(self, cid, recipientAddress, token):
        infNft = self.loop.run_until_complete(self.wallet.mint_nft(Ipfs2bytes32().byte32_to_ipfscidv0(cid), recipientAddress, token))

        return infNft

