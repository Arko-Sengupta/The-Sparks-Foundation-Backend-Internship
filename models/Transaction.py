from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class TransactionType(str, Enum):
    Credit = "Credit"
    Debit  = "Debit"

class TransactionCategory(str, Enum):
    IMPS = "IMPS"
    RTGS = "RTGS"
    NEFT = "NEFT"

class CreateTransactionRequest(BaseModel):
    beneficiaryName: str = Field(..., min_length=2)
    bankName:        str
    accountNumber:   str = Field(..., min_length=11, max_length=17)
    category:        TransactionCategory
    amount:          float = Field(..., gt=0)

class TransactionResponse(BaseModel):
    id:              str
    userId:          str
    beneficiaryName: str
    bankName:        str
    accountNumber:   str
    category:        str
    amount:          float
    type:            str
    date:            Optional[str]

class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total:        int