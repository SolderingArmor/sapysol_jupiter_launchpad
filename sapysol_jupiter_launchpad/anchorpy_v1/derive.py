# ================================================================================
# 
from    solana.rpc.api        import Pubkey
from ..anchorpy_v1.program_id import PROGRAM_ID as DISTRIBUTOR_PROGRAM_ID

V2_ROOT_MERKLE_TREE = Pubkey.from_string("A8ftiUspopUk8zX1Y85mJ2Vngqte8KnesapRpdkTvSry")

# =============================================================================
# 
def DeriveClaimStatus(walletAddress: Pubkey, distributorAddress: Pubkey):
    return Pubkey.find_program_address(seeds      = [bytes(b"ClaimStatus"), 
                                                     bytes(walletAddress),
                                                     bytes(distributorAddress)],
                                       program_id = DISTRIBUTOR_PROGRAM_ID)[0]

# =============================================================================
# 
#def DeriveASAA():
#    pass
#    f.PublicKey.findProgramAddressSync([p.from("MerkleDistributor"), e.toBuffer(), p.alloc(8)], this.mdProgram.programId);