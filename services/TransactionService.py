from fastapi import HTTPException
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from config.Firebase import GetDb
from models.Transaction import CreateTransactionRequest, TransactionListResponse, TransactionResponse

def FormatTransaction(Doc) -> TransactionResponse:
    try:
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
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to format transaction: {str(E)}")

async def GetTransactions(UserId: str) -> TransactionListResponse:
    try:
        Db   = GetDb()
        Docs = Db.collection("transactions") \
                 .where("userId", "==", UserId) \
                 .get()

        Transactions = sorted(
            [FormatTransaction(D) for D in Docs],
            key=lambda t: t.date or "",
            reverse=True
        )
        return TransactionListResponse(transactions=Transactions, total=len(Transactions))
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to fetch transactions: {str(E)}")

async def CreateTransaction(UserId: str, Data: CreateTransactionRequest) -> TransactionResponse:
    try:
        Db       = GetDb()
        UserSnap = Db.collection("users").document(UserId).get()

        if not UserSnap.exists:
            raise HTTPException(404, "User not found")

        SenderBalance = UserSnap.to_dict().get("balance", 0.0)
        if SenderBalance < Data.amount:
            raise HTTPException(400, "Insufficient balance")

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

        Db.collection("users").document(UserId).update({
            "balance": SenderBalance - Data.amount
        })

        BeneficiaryResults = Db.collection("users").where("accountNumber", "==", Data.accountNumber).get()
        if BeneficiaryResults:
            Beneficiary        = BeneficiaryResults[0]
            BeneficiaryBalance = Beneficiary.to_dict().get("balance", 0.0)
            Db.collection("users").document(Beneficiary.id).update({
                "balance": BeneficiaryBalance + Data.amount
            })
            Db.collection("transactions").add({
                "userId":          Beneficiary.id,
                "beneficiaryName": UserSnap.to_dict().get("fullName", ""),
                "bankName":        Data.bankName,
                "accountNumber":   UserSnap.to_dict().get("accountNumber", ""),
                "category":        Data.category.value,
                "amount":          Data.amount,
                "type":            "Credit",
                "date":            SERVER_TIMESTAMP,
            })

        Ref = Db.collection("transactions").add(TxnDoc)
        Doc = Ref[1].get()
        return FormatTransaction(Doc)
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to create transaction: {str(E)}")