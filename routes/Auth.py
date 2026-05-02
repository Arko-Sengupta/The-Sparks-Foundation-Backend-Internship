from fastapi import APIRouter
from models.Auth import SignUpRequest, LoginRequest, TokenResponse
from services.AuthService import SignupUser, LoginUser

Router = APIRouter(prefix="/auth", tags=["Authentication"])


@Router.post("/signup", response_model=TokenResponse, status_code=201)
async def Signup(Data: SignUpRequest):
    return await SignupUser(Data)


@Router.post("/login", response_model=TokenResponse)
async def Login(Data: LoginRequest):
    return await LoginUser(Data)
