from fastapi import APIRouter, Depends, HTTPException

from config.Jwt import GetCurrentUser
from services.TransactionService import CreateTransaction, GetTransactions
from models.Transaction import CreateTransactionRequest, TransactionListResponse, TransactionResponse

Router = APIRouter(prefix="/transactions", tags=["Transactions"])

@Router.get("/history", response_model=TransactionListResponse)
async def TransactionHistory(CurrentUser: dict = Depends(GetCurrentUser)):
    try:
        return await GetTransactions(CurrentUser["sub"])
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to fetch transaction history: {str(E)}")

@Router.post("/initiate", response_model=TransactionResponse, status_code=201)
async def InitiateTransaction(Data: CreateTransactionRequest, CurrentUser: dict = Depends(GetCurrentUser)):
    try:
        return await CreateTransaction(CurrentUser["sub"], Data)
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to initiate transaction: {str(E)}")