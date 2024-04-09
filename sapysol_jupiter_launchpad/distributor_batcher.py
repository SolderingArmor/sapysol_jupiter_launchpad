#!/usr/bin/python
# =============================================================================
# 
from   solana.rpc.api           import Client, Pubkey, Keypair
from   solders.instruction      import Instruction
from   sapysol                  import *
from   sapysol.token_cache      import *
from   sapysol.snippets.batcher import SapysolBatcher
from  .distributor              import SapysolJupiterDistributor
import requests

# =============================================================================
# 
class SapysolLfgProofParams:
    def __init__(self, tokenMint: SapysolPubkey, walletAddress: SapysolPubkey):
        self.DISTRIBUTOR_PUBKEY: Pubkey          = None
        self.AMOUNT:             int             = None
        self.PROOF:              List[List[int]] = None

        r: requests.Response = requests.get(f"https://worker.jup.ag/jup-claim-proof/{str(tokenMint)}/{str(walletAddress)}")
        if r.text == "":
            return
        response = r.json()
        self.DISTRIBUTOR_PUBKEY: Pubkey          = MakePubkey(response["merkle_tree"])
        self.AMOUNT:             int             = response["amount"]
        self.PROOF:              List[List[int]] = response["proof"]

    def IsValid(self) -> bool:
        return self.DISTRIBUTOR_PUBKEY and self.AMOUNT and self.PROOF

# =============================================================================
# 
class SapysolJupiterDistributorBatcher:
    def __init__(self, 
                 connection:         Client,
                 tokenMint:          SapysolPubkey,
                 keypairsList:       List[SapysolKeypair],
                 connectionOverride: List[Union[str, Client]] = None,
                 numThreads:         int  = 20):

        self.CONNECTION:          Client                   = connection
        self.TOKEN_MINT:          Pubkey                   = MakePubkey(tokenMint)
        self.TOKEN:               SapysolToken             = SapysolToken(connection=connection, tokenMint=tokenMint)
        self.KEYPAIRS_LIST:       List[Keypair]            = [MakeKeypair(k) for k in keypairsList]
        self.CONNECTION_OVERRIDE: List[Union[str, Client]] = connectionOverride
        self.DISTRIBUTOR_LIST:    dict                     = {}
        self.BATCHER:             SapysolBatcher = SapysolBatcher(callback    = self.ClaimSingle,
                                                                  entityList  = self.KEYPAIRS_LIST,
                                                                  entityKwarg = "wallet",
                                                                  numThreads  = numThreads)

    # ========================================
    #
    def GetDistributor(self, distributorAddress: SapysolPubkey) -> SapysolJupiterDistributor:

        _distributorAddress: Pubkey = MakePubkey(distributorAddress)
        if _distributorAddress in self.DISTRIBUTOR_LIST:
            return self.DISTRIBUTOR_LIST[_distributorAddress]
        self.DISTRIBUTOR_LIST[_distributorAddress] = SapysolJupiterDistributor(connection         = self.CONNECTION,
                                                                               distributorAddress = distributorAddress)
        return self.DISTRIBUTOR_LIST[_distributorAddress]

    # ========================================
    #
    def ClaimSingle(self, wallet: Keypair) -> None:
        params: SapysolLfgProofParams = SapysolLfgProofParams(tokenMint=self.TOKEN_MINT, walletAddress=wallet.pubkey())
        if not params.IsValid():
            print(f"{str(wallet.pubkey()):>44}: No distribution, skipping...")
            return

        distributor: SapysolJupiterDistributor = self.GetDistributor(distributorAddress=params.DISTRIBUTOR_PUBKEY)
        claimStatus = distributor.GetClaimStatus(walletAddress=wallet.pubkey())
        if claimStatus:
            print(f"{str(wallet.pubkey()):>44}: Already claimed, skipping...")
            return

        ix: List[Instruction] = distributor.GetClaimIx(walletAddress=wallet.pubkey(), amount=params.AMOUNT, proof=params.PROOF)

        while True:
            delimiter: int = 10**self.TOKEN.TOKEN_INFO.decimals
            print(f"{str(wallet.pubkey()):>44}: Claiming {params.AMOUNT/delimiter} tokens...")
            tx: SapysolTx = SapysolTx(connection=self.CONNECTION, payer=wallet)
            tx.FromInstructionsLegacy(instructions=ix)
            result: SapysolTxStatus = tx.Sign([wallet]).WaitForTx(self.CONNECTION_OVERRIDE)
            if result == SapysolTxStatus.SUCCESS:
                return

    # ========================================
    #
    def Start(self, **kwargs) -> None:
        self.RESULTS = {}
        self.BATCHER.Start(**kwargs)

# =============================================================================
# 
