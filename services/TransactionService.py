from fastapi import HTTPException
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from config.Firebase import GetDb
from models.Transaction import CreateTransactionRequest, TransactionResponse, TransactionListResponse


def FormatTransaction(Doc) -> TransactionResponse:
    D    = Doc.to_dict()
    Date = D.get("date")
    return TransactionResponse(
        id              = Doc.id,
        userId          = D.get("userId", ""),
        beneficiaryName = D.get("beneficiaryName", ""),
        bankName        = D.get("bankName", ""),
        accountNumber   = D.get("accountNumber", ""),
        category        = D.get("category", ""),
        amount          = float(D.get("amount", 0)),
        type            = D.get("type", "Debit"),
        date            = Date.isoformat() if hasattr(Date, "isoformat") else str(Date) if Date else None,
    )


async def GetTransactions(UserId: str) -> TransactionListResponse:
    Db   = GetDb()
    Docs = Db.collection("transactions") \
             .where("userId", "==", UserId) \
             .order_by("date", direction="DESCENDING") \
             .get()

    Transactions = [FormatTransaction(D) for D in Docs]
    return TransactionListResponse(transactions=Transactions, total=len(Transactions))


async def CreateTransaction(UserId: str, Data: CreateTransactionRequest) -> TransactionResponse:
    Db       = GetDb()
    UserSnap = Db.collection("users").document(UserId).get()

    if not UserSnap.exists:
        raise HTTPException(404, "User not found")

    TxnDoc = {
        "userId":          UserId,
        "beneficiaryName": Data.beneficiaryName,
        "bankName":        Data.bankName,
        "accountNumber":   Data.accountNumber,
        "category":        Data.category.value,
        "amount":          Data.amount,
        "type":            "Debit",
        "date":            SERVER_TIMESTAMP,
    }

    Ref = Db.collection("transactions").add(TxnDoc)
    Doc = Ref[1].get()
    return FormatTransaction(Doc)
