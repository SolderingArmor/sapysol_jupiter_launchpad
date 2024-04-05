# ================================================================================
#
from __future__            import annotations
import typing
from   solders.pubkey      import Pubkey
from   solders.instruction import Instruction, AccountMeta
import borsh_construct     as borsh
from ..program_id          import PROGRAM_ID

# ================================================================================
#
class SetEnableSlotArgs(typing.TypedDict):
    enable_slot: int

# ================================================================================
#
layout = borsh.CStruct(
    "enable_slot" / borsh.U64
)

# ================================================================================
#
class SetEnableSlotAccounts(typing.TypedDict):
    distributor: Pubkey
    admin:       Pubkey

# ================================================================================
#
def set_enable_slot(args:               SetEnableSlotArgs,
                    accounts:           SetEnableSlotAccounts,
                    program_id:         Pubkey = PROGRAM_ID,
                    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["distributor"], is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["admin"],       is_signer=True,  is_writable=True ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\x054I!\x96sa\xce"
    encoded_args = layout.build({
        "enable_slot": args["enable_slot"],
    })
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
