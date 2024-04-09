#!/usr/bin/python
# =============================================================================
# 
from solana.rpc.api             import Client, Pubkey, Keypair
from solders.instruction        import Instruction
from sapysol                    import *
from sapysol.token_cache        import *
from   sapysol.snippets.batcher import SapysolBatcher
from .anchorpy_v1.program_id    import PROGRAM_ID as PROGRAM_ID_V1
from .anchorpy_v2.program_id    import PROGRAM_ID as PROGRAM_ID_V2
from .anchorpy_v1.accounts      import ClaimStatus as ClaimStatus_v1, MerkleDistributor as MerkleDistributor_v1
from .anchorpy_v2.accounts      import ClaimStatus as ClaimStatus_v2, MerkleDistributor as MerkleDistributor_v2
from .anchorpy_v1.instructions  import new_claim, NewClaimArgs, NewClaimAccounts
from .anchorpy_v1.derive        import DeriveClaimStatus as DeriveClaimStatus_v1
from .anchorpy_v2.derive        import DeriveClaimStatus as DeriveClaimStatus_v2

# =============================================================================
# 
class SapysolJupiterDistributor:
    def __init__(self,
                 connection:         Client,
                 distributorAddress: SapysolPubkey):

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
    def GetClaimStatusAddress(self, walletAddress: SapysolPubkey) -> Pubkey:
        func = DeriveClaimStatus_v1 if self.VERSION == "v1" else DeriveClaimStatus_v2
        return func(walletAddress=MakePubkey(walletAddress), distributorAddress=self.PUBKEY)

    # ========================================
    #
    def GetClaimStatus(self, walletAddress: SapysolPubkey) -> Union[ClaimStatus_v1, ClaimStatus_v1]:
        address = self.GetClaimStatusAddress(walletAddress=walletAddress)
        return ClaimStatus_v1.fetch(conn=self.CONNECTION, address=address) if self.VERSION == "v1" else \
               ClaimStatus_v2.fetch(conn=self.CONNECTION, address=address)

    # ========================================
    #
    def GetClaimIx(self,
                   walletAddress: SapysolPubkey,
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
