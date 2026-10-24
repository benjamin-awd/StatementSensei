from dataclasses import dataclass, field
from typing import Literal

from monopoly.statements import Transaction


@dataclass
class TransactionMetadata:
    bank_name: str


@dataclass
class Notice:
    level: Literal["error", "warning"]
    message: str


@dataclass
class ProcessedFile:
    transactions: list[Transaction]
    metadata: TransactionMetadata
    # stored with the file so they're shown again on every rerun, not just the first parse
    notices: list[Notice] = field(default_factory=list)

    def __iter__(self):
        return iter(self.transactions)
