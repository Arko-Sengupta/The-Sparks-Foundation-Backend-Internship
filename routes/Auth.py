from fastapi import APIRouter, HTTPException
from services.AuthService import LoginUser, SignupUser
from models.Auth import LoginRequest, SignUpRequest, TokenResponse

Router = APIRouter(prefix="/auth", tags=["Authentication"])

@Router.post("/signup", response_model=TokenResponse, status_code=201)
async def Signup(Data: SignUpRequest):
    try:
        return await SignupUser(Data)
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Signup error: {str(E)}")

@Router.post("/login", response_model=TokenResponse)
async def Login(Data: LoginRequest):
    try:
        return await LoginUser(Data)
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Login error: {str(E)}")