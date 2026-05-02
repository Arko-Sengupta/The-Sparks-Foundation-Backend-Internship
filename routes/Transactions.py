from fastapi import APIRouter, Depends
from models.Transaction import CreateTransactionRequest, TransactionResponse, TransactionListResponse
from services.TransactionService import GetTransactions, CreateTransaction
from config.Jwt import GetCurrentUser

Router = APIRouter(prefix="/transactions", tags=["Transactions"])


@Router.get("/history", response_model=TransactionListResponse)
async def TransactionHistory(CurrentUser: dict = Depends(GetCurrentUser)):
    return await GetTransactions(CurrentUser["sub"])


@Router.post("/initiate", response_model=TransactionResponse, status_code=201)
async def InitiateTransaction(Data: CreateTransactionRequest, CurrentUser: dict = Depends(GetCurrentUser)):
    return await CreateTransaction(CurrentUser["sub"], Data)
