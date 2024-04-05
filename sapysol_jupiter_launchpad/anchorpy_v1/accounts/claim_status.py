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
from   sapysol.helpers          import MakePubkey, FetchAccount, FetchAccounts

# ================================================================================
#
class ClaimStatusJSON(typing.TypedDict):
    claimant:                str
    locked_amount:           int
    locked_amount_withdrawn: int
    unlocked_amount:         int
    closable:                bool
    admin:                   str

# ================================================================================
#
@dataclass
class ClaimStatus:
    discriminator: typing.ClassVar = b"B8'\\\xc7F) "
    layout: typing.ClassVar = borsh.CStruct(
        "claimant"                / BorshPubkey,
        "locked_amount"           / borsh.U64,
        "locked_amount_withdrawn" / borsh.U64,
        "unlocked_amount"         / borsh.U64,
        "closable"                / borsh.Bool,
        "admin"                   / BorshPubkey,
    )
    claimant:                Pubkey
    locked_amount:           int
    locked_amount_withdrawn: int
    unlocked_amount:         int
    closable:                bool
    admin:                   Pubkey

    # ========================================
    #
    @classmethod
    def fetch(cls,
              conn:       Client,
              address:    Pubkey,
              commitment: typing.Optional[Commitment] = None,
              program_id: Pubkey = PROGRAM_ID) -> typing.Optional["ClaimStatus"]:

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
                       program_id: Pubkey = PROGRAM_ID) -> typing.List[typing.Optional["ClaimStatus"]]:

        entries = FetchAccounts(connection   = conn, 
                                pubkeys      = addresses,
                                requiredOwner= program_id,
                                commitment   = commitment)
        return [ ClaimStatus.decode(entry.data) if entry else None for entry in entries ]

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "ClaimStatus":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = ClaimStatus.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(claimant                = dec.claimant,
                   locked_amount           = dec.locked_amount,
                   locked_amount_withdrawn = dec.locked_amount_withdrawn,
                   unlocked_amount         = dec.unlocked_amount,
                   closable                = dec.closable,
                   admin                   = dec.admin)

    # ========================================
    #
    def to_json(self) -> ClaimStatusJSON:
        return {
            "claimant":            str(self.claimant),
            "locked_amount":           self.locked_amount,
            "locked_amount_withdrawn": self.locked_amount_withdrawn,
            "unlocked_amount":         self.unlocked_amount,
            "closable":                self.closable,
            "admin":               str(self.admin),
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: ClaimStatusJSON) -> "ClaimStatus":
        return cls(claimant     = MakePubkey(obj["claimant"]),
                   locked_amount           = obj["locked_amount"],
                   locked_amount_withdrawn = obj["locked_amount_withdrawn"],
                   unlocked_amount         = obj["unlocked_amount"],
                   closable                = obj["closable"],
                   admin        = MakePubkey(obj["admin"]))

# ================================================================================
#
