# ================================================================================
#
from __future__            import annotations
import typing
from   solders.pubkey      import Pubkey
from   solders.instruction import Instruction, AccountMeta
from ..program_id          import PROGRAM_ID

# ================================================================================
#
class CloseClaimStatusAccounts(typing.TypedDict):
    claim_status: Pubkey
    claimant: Pubkey
    admin: Pubkey

# ================================================================================
#
def close_claim_status(accounts:           CloseClaimStatusAccounts,
                       program_id:         Pubkey = PROGRAM_ID,
                       remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["claim_status"], is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["claimant"],     is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["admin"],        is_signer=True,  is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\xa3\xd6\xbf\xa5\xf5\xbc\x11\xb9"
    encoded_args = b""
    data         = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
