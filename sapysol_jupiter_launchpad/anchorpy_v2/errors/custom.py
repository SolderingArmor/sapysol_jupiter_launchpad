# ================================================================================
#
import typing
from  anchorpy.error import ProgramError

# ================================================================================
#
class InsufficientUnlockedTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "Insufficient unlocked tokens")

    code = 6000
    name = "InsufficientUnlockedTokens"
    msg = "Insufficient unlocked tokens"


class StartTooFarInFuture(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Deposit Start too far in future")

    code = 6001
    name = "StartTooFarInFuture"
    msg = "Deposit Start too far in future"


class InvalidProof(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Invalid Merkle proof.")

    code = 6002
    name = "InvalidProof"
    msg = "Invalid Merkle proof."


class ExceededMaxClaim(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "Exceeded maximum claim amount")

    code = 6003
    name = "ExceededMaxClaim"
    msg = "Exceeded maximum claim amount"


class MaxNodesExceeded(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Exceeded maximum node count")

    code = 6004
    name = "MaxNodesExceeded"
    msg = "Exceeded maximum node count"


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "Account is not authorized to execute this instruction")

    code = 6005
    name = "Unauthorized"
    msg = "Account is not authorized to execute this instruction"


class OwnerMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "Token account owner did not match intended owner")

    code = 6006
    name = "OwnerMismatch"
    msg = "Token account owner did not match intended owner"


class ClawbackDuringVesting(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "Clawback cannot be before vesting ends")

    code = 6007
    name = "ClawbackDuringVesting"
    msg = "Clawback cannot be before vesting ends"


class ClawbackBeforeStart(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "Attempted clawback before start")

    code = 6008
    name = "ClawbackBeforeStart"
    msg = "Attempted clawback before start"


class ClawbackAlreadyClaimed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Clawback already claimed")

    code = 6009
    name = "ClawbackAlreadyClaimed"
    msg = "Clawback already claimed"


class InsufficientClawbackDelay(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6010, "Clawback start must be at least one day after vesting end"
        )

    code = 6010
    name = "InsufficientClawbackDelay"
    msg = "Clawback start must be at least one day after vesting end"


class SameClawbackReceiver(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "New and old Clawback receivers are identical")

    code = 6011
    name = "SameClawbackReceiver"
    msg = "New and old Clawback receivers are identical"


class SameAdmin(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "New and old admin are identical")

    code = 6012
    name = "SameAdmin"
    msg = "New and old admin are identical"


class ClaimExpired(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "Claim window expired")

    code = 6013
    name = "ClaimExpired"
    msg = "Claim window expired"


class ArithmeticError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "Arithmetic Error (overflow/underflow)")

    code = 6014
    name = "ArithmeticError"
    msg = "Arithmetic Error (overflow/underflow)"


class StartTimestampAfterEnd(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "Start Timestamp cannot be after end Timestamp")

    code = 6015
    name = "StartTimestampAfterEnd"
    msg = "Start Timestamp cannot be after end Timestamp"


class TimestampsNotInFuture(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, "Timestamps cannot be in the past")

    code = 6016
    name = "TimestampsNotInFuture"
    msg = "Timestamps cannot be in the past"


class InvalidVersion(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, "Airdrop Version Mismatch")

    code = 6017
    name = "InvalidVersion"
    msg = "Airdrop Version Mismatch"


class ClaimingIsNotStarted(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, "Claiming is not started")

    code = 6018
    name = "ClaimingIsNotStarted"
    msg = "Claiming is not started"


class CannotCloseDistributor(ProgramError):
    def __init__(self) -> None:
        super().__init__(6019, "Cannot close distributor")

    code = 6019
    name = "CannotCloseDistributor"
    msg = "Cannot close distributor"


class CannotCloseClaimStatus(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, "Cannot close claim status")

    code = 6020
    name = "CannotCloseClaimStatus"
    msg = "Cannot close claim status"

# ================================================================================
#
CustomError = typing.Union[
    InsufficientUnlockedTokens,
    StartTooFarInFuture,
    InvalidProof,
    ExceededMaxClaim,
    MaxNodesExceeded,
    Unauthorized,
    OwnerMismatch,
    ClawbackDuringVesting,
    ClawbackBeforeStart,
    ClawbackAlreadyClaimed,
    InsufficientClawbackDelay,
    SameClawbackReceiver,
    SameAdmin,
    ClaimExpired,
    ArithmeticError,
    StartTimestampAfterEnd,
    TimestampsNotInFuture,
    InvalidVersion,
    ClaimingIsNotStarted,
    CannotCloseDistributor,
    CannotCloseClaimStatus,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: InsufficientUnlockedTokens(),
    6001: StartTooFarInFuture(),
    6002: InvalidProof(),
    6003: ExceededMaxClaim(),
    6004: MaxNodesExceeded(),
    6005: Unauthorized(),
    6006: OwnerMismatch(),
    6007: ClawbackDuringVesting(),
    6008: ClawbackBeforeStart(),
    6009: ClawbackAlreadyClaimed(),
    6010: InsufficientClawbackDelay(),
    6011: SameClawbackReceiver(),
    6012: SameAdmin(),
    6013: ClaimExpired(),
    6014: ArithmeticError(),
    6015: StartTimestampAfterEnd(),
    6016: TimestampsNotInFuture(),
    6017: InvalidVersion(),
    6018: ClaimingIsNotStarted(),
    6019: CannotCloseDistributor(),
    6020: CannotCloseClaimStatus(),
}

# ================================================================================
#
def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err

# ================================================================================
#
