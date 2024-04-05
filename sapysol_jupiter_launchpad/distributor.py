#!/usr/bin/python
# =============================================================================
# 
from solana.rpc.types       import TxOpts, TokenAccountOpts, DataSliceOpts
from solana.rpc.api         import Client, Pubkey, Keypair
from solders.instruction    import Instruction
from sapysol import *
from sapysol.token_cache import *
from pprint import pprint

from .anchorpy_v1.program_id    import PROGRAM_ID as PROGRAM_ID_V1
from .anchorpy_v2.program_id    import PROGRAM_ID as PROGRAM_ID_V2
from .anchorpy_v2.accounts      import ClaimStatus as ClaimStatus_v2, MerkleDistributor as MerkleDistributor_v2
from .anchorpy_v1.accounts      import ClaimStatus as ClaimStatus_v1, MerkleDistributor as MerkleDistributor_v1
from .anchorpy_v2.accounts      import ClaimStatus as ClaimStatus_v2, MerkleDistributor as MerkleDistributor_v2
from .anchorpy_v1.instructions  import new_claim, NewClaimArgs, NewClaimAccounts
from .anchorpy_v1.derive        import DeriveClaimStatus as DeriveClaimStatus_v1
from .anchorpy_v2.derive        import DeriveClaimStatus as DeriveClaimStatus_v2

from   sapysol.helpers          import FetchAccount, FetchAccounts
from   sapysol.snippets.batcher import SapysolBatcher
import requests

# =============================================================================
# 
class SapysolJupiterDistributor:
    def __init__(self,
                 connection:         Client,
                 distributorAddress: Union[str, bytes, Pubkey]):

        self.CONNECTION:  Client              = connection
        self.PUBKEY:      Pubkey              = MakePubkey(distributorAddress)
        self.VERSION:     Literal["v1", "v2"] = None
        self.DISTRIBUTOR: Union[MerkleDistributor_v1, MerkleDistributor_v2] = None 
        account = FetchAccount(connection=connection, pubkey=self.PUBKEY)
        if account is None:
            raise ValueError(f"SapysolJupiterDistributor: {str(self.PUBKEY)} is an empty account!")

        if account.owner == PROGRAM_ID_V1:
            self.DISTRIBUTOR: MerkleDistributor_v1 = MerkleDistributor_v1.decode(data=account.data)
            self.VERSION = "v1"
        elif account.owner == PROGRAM_ID_V2:
            self.DISTRIBUTOR: MerkleDistributor_v2 = MerkleDistributor_v2.decode(data=account.data) 
            self.VERSION = "v2"

    # ========================================
    #
    def GetClaimStatusAddress(self, walletAddress: Union[str, bytes, Pubkey]) -> Pubkey:
        func = DeriveClaimStatus_v1 if self.VERSION == "v1" else DeriveClaimStatus_v2
        return func(walletAddress=MakePubkey(walletAddress), distributorAddress=self.PUBKEY)

    # ========================================
    #
    def GetClaimStatus(self, walletAddress: Union[str, bytes, Pubkey]) -> Union[ClaimStatus_v1, ClaimStatus_v1]:
        address = self.GetClaimStatusAddress(walletAddress=walletAddress)
        return ClaimStatus_v1.fetch(conn=self.CONNECTION, address=address) if self.VERSION == "v1" else \
               ClaimStatus_v2.fetch(conn=self.CONNECTION, address=address)

    # ========================================
    #
    def GetClaimIx(self,
                   walletAddress: Union[str, bytes, Pubkey], 
                   amount:        int,
                   proof:         List[List[int]],
                   computePrice:  int = 1) -> List[Instruction]:

        _walletAddress = MakePubkey(walletAddress)
        ataIx   = GetOrCreateAtaIx(connection=self.CONNECTION, tokenMint=self.DISTRIBUTOR.mint, owner=_walletAddress)

        args = NewClaimArgs(amount_unlocked = amount,
                            amount_locked   = 0,
                            proof           = proof)
        accounts = NewClaimAccounts(distributor  = self.PUBKEY,
                                    claim_status = self.GetClaimStatusAddress(walletAddress=_walletAddress),
                                    from_        = self.DISTRIBUTOR.token_vault,
                                    to           = ataIx.pubkey,
                                    claimant     = _walletAddress)
        claimIx = new_claim(args=args, accounts=accounts)

        result: List[Instruction] = []
        result.append(ComputeBudgetIx())
        result.append(ComputePriceIx(computePrice))
        if ataIx.ix:
            result.append(ataIx.ix)
        result.append(claimIx)
        return result

# =============================================================================
# 
class SapysolLfgProofParams:
    def __init__(self, tokenMint: Union[str, bytes, Pubkey], walletAddress: Union[str, bytes, Pubkey]):
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
                 tokenMint:          Union[str, bytes, Pubkey],
                 keypairsList:       List[Union[str, bytes, Keypair]],
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
    def GetDistributor(self, distributorAddress: Union[str, bytes, Pubkey]) -> SapysolJupiterDistributor:

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
