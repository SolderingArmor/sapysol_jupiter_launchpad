# ================================================================================
#
from __future__            import annotations
import typing
from   solders.pubkey      import Pubkey
from   spl.token.constants import TOKEN_PROGRAM_ID
from   solders.instruction import Instruction, AccountMeta
from ..program_id          import PROGRAM_ID

# ================================================================================
#
class CloseDistributorAccounts(typing.TypedDict):
    distributor:               Pubkey
    token_vault:               Pubkey
    admin:                     Pubkey
    destination_token_account: Pubkey

# ================================================================================
#
def close_distributor(accounts:           CloseDistributorAccounts,
                      program_id:         Pubkey = PROGRAM_ID,
                      remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["distributor"],               is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["token_vault"],               is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["admin"],                     is_signer=True,  is_writable=True ),
        AccountMeta(pubkey=accounts["destination_token_account"], is_signer=False, is_writable=True ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID,                      is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\xca8\xb4\x8f.hjp"
    encoded_args = b""
    data         = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
