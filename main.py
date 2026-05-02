from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes.Auth         import Router as AuthRouter
from routes.Users        import Router as UsersRouter
from routes.Transactions import Router as TransactionsRouter

load_dotenv()

App = FastAPI(
    title       = "TSF Bank API",
    description = "Backend API for The Sparks Foundation Banking Application",
    version     = "1.0.0",
)

App.add_middleware(
    CORSMiddleware,
    allow_origins     = [""],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

App.include_router(AuthRouter)
App.include_router(UsersRouter)
App.include_router(TransactionsRouter)


@App.get("/", tags=["Health"])
async def Root():
    return {"status": "ok", "message": "TSF Bank API is running"}


@App.get("/health", tags=["Health"])
async def Health():
    return {"status": "healthy"}
