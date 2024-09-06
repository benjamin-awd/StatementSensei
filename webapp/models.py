from dataclasses import dataclass

from monopoly.statements import Transaction


@dataclass
class Config:
    show_banks: bool


@dataclass
class TransactionMetadata:
    bank_name: str


@dataclass
class Transactions:
    transactions: list[Transaction]
    metadata: TransactionMetadata

    def __iter__(self):
        return iter(self.transactions)
