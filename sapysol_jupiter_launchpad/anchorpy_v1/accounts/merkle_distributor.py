# ================================================================================
#
import typing
from   dataclasses              import dataclass
from   solders.pubkey           import Pubkey
from   solana.rpc.api           import Client
from   solana.rpc.commitment    import Commitment
import borsh_construct          as borsh
from   anchorpy.coder.accounts  import ACCOUNT_DISCRIMINATOR_SIZE
from   anchorpy.error           import AccountInvalidDiscriminator
from   anchorpy.utils.rpc       import get_multiple_accounts
from   anchorpy.borsh_extension import BorshPubkey
from ..program_id               import PROGRAM_ID
from   sapysol                  import MakePubkey, FetchAccount, FetchAccounts

# ================================================================================
#
class MerkleDistributorJSON(typing.TypedDict):
    bump:                 int
    version:              int
    root:                 list[int]
    mint:                 str
    token_vault:          str
    max_total_claim:      int
    max_num_nodes:        int
    total_amount_claimed: int
    num_nodes_claimed:    int
    start_ts:             int
    end_ts:               int
    clawback_start_ts:    int
    clawback_receiver:    str
    admin:                str
    clawed_back:          bool
    enable_slot:          int
    closable:             bool
    buffer0:              list[int]
    buffer1:              list[int]
    buffer2:              list[int]

# ================================================================================
#
@dataclass
class MerkleDistributor:
    discriminator: typing.ClassVar = b"Mw\x8bFT\xf7\x0c\x1a"
    layout: typing.ClassVar = borsh.CStruct(
        "bump"                 / borsh.U8,
        "version"              / borsh.U64,
        "root"                 / borsh.U8[32],
        "mint"                 / BorshPubkey,
        "token_vault"          / BorshPubkey,
        "max_total_claim"      / borsh.U64,
        "max_num_nodes"        / borsh.U64,
        "total_amount_claimed" / borsh.U64,
        "num_nodes_claimed"    / borsh.U64,
        "start_ts"             / borsh.I64,
        "end_ts"               / borsh.I64,
        "clawback_start_ts"    / borsh.I64,
        "clawback_receiver"    / BorshPubkey,
        "admin"                / BorshPubkey,
        "clawed_back"          / borsh.Bool,
        "enable_slot"          / borsh.U64,
        "closable"             / borsh.Bool,
        "buffer0"              / borsh.U8[32],
        "buffer1"              / borsh.U8[32],
        "buffer2"              / borsh.U8[32],
    )
    bump:                 int
    version:              int
    root:                 list[int]
    mint:                 Pubkey
    token_vault:          Pubkey
    max_total_claim:      int
    max_num_nodes:        int
    total_amount_claimed: int
    num_nodes_claimed:    int
    start_ts:             int
    end_ts:               int
    clawback_start_ts:    int
    clawback_receiver:    Pubkey
    admin:                Pubkey
    clawed_back:          bool
    enable_slot:          int
    closable:             bool
    buffer0:              list[int]
    buffer1:              list[int]
    buffer2:              list[int]

    # ========================================
    #
    @classmethod
    def fetch(cls,
              conn:       Client,
              address:    Pubkey,
              commitment: typing.Optional[Commitment] = None,
              program_id: Pubkey = PROGRAM_ID) -> typing.Optional["MerkleDistributor"]:
    
        resp = FetchAccount(connection    = conn, 
                            pubkey        = address,
                            requiredOwner = program_id,
                            commitment    = commitment)
        return None if resp is None else cls.decode(resp.data)

    # ========================================
    #
    @classmethod
    def fetch_multiple(cls,
                       conn:       Client,
                       addresses:  list[Pubkey],
                       commitment: typing.Optional[Commitment] = None,
                       program_id: Pubkey = PROGRAM_ID) -> typing.List[typing.Optional["MerkleDistributor"]]:

        entries = FetchAccounts(connection   = conn, 
                                pubkeys      = addresses,
                                requiredOwner= program_id,
                                commitment   = commitment)
        return [ MerkleDistributor.decode(entry.data) if entry else None for entry in entries ]

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "MerkleDistributor":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = MerkleDistributor.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(bump                 = dec.bump,
                   version              = dec.version,
                   root                 = dec.root,
                   mint                 = dec.mint,
                   token_vault          = dec.token_vault,
                   max_total_claim      = dec.max_total_claim,
                   max_num_nodes        = dec.max_num_nodes,
                   total_amount_claimed = dec.total_amount_claimed,
                   num_nodes_claimed    = dec.num_nodes_claimed,
                   start_ts             = dec.start_ts,
                   end_ts               = dec.end_ts,
                   clawback_start_ts    = dec.clawback_start_ts,
                   clawback_receiver    = dec.clawback_receiver,
                   admin                = dec.admin,
                   clawed_back          = dec.clawed_back,
                   enable_slot          = dec.enable_slot,
                   closable             = dec.closable,
                   buffer0              = dec.buffer0,
                   buffer1              = dec.buffer1,
                   buffer2              = dec.buffer2)

    # ========================================
    #
    def to_json(self) -> MerkleDistributorJSON:
        return {
            "bump":                 self.bump,
            "version":              self.version,
            "root":                 self.root,
            "mint":             str(self.mint),
            "token_vault":      str(self.token_vault),
            "max_total_claim":      self.max_total_claim,
            "max_num_nodes":        self.max_num_nodes,
            "total_amount_claimed": self.total_amount_claimed,
            "num_nodes_claimed":    self.num_nodes_claimed,
            "start_ts":             self.start_ts,
            "end_ts":               self.end_ts,
            "clawback_start_ts":    self.clawback_start_ts,
            "clawback_receiver":str(self.clawback_receiver),
            "admin":            str(self.admin),
            "clawed_back":          self.clawed_back,
            "enable_slot":          self.enable_slot,
            "closable":             self.closable,
            "buffer0":              self.buffer0,
            "buffer1":              self.buffer1,
            "buffer2":              self.buffer2,
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: MerkleDistributorJSON) -> "MerkleDistributor":
        return cls(bump                 =            obj["bump"],
                   version              =            obj["version"],
                   root                 =            obj["root"],
                   mint                 = MakePubkey(obj["mint"]),
                   token_vault          = MakePubkey(obj["token_vault"]),
                   max_total_claim      =            obj["max_total_claim"],
                   max_num_nodes        =            obj["max_num_nodes"],
                   total_amount_claimed =            obj["total_amount_claimed"],
                   num_nodes_claimed    =            obj["num_nodes_claimed"],
                   start_ts             =            obj["start_ts"],
                   end_ts               =            obj["end_ts"],
                   clawback_start_ts    =            obj["clawback_start_ts"],
                   clawback_receiver    = MakePubkey(obj["clawback_receiver"]),
                   admin                = MakePubkey(obj["admin"]),
                   clawed_back          =            obj["clawed_back"],
                   enable_slot          =            obj["enable_slot"],
                   closable             =            obj["closable"],
                   buffer0              =            obj["buffer0"],
                   buffer1              =            obj["buffer1"],
                   buffer2              =            obj["buffer2"])

# ================================================================================
#
