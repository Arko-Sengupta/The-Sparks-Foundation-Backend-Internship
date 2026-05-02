from fastapi import APIRouter, Depends
from models.Auth import UserResponse, UserUpdateRequest
from services.UserService import GetUser, UpdateUser, DeleteUser
from config.Jwt import GetCurrentUser

Router = APIRouter(prefix="/users", tags=["Users"])


@Router.get("/profile", response_model=UserResponse)
async def GetProfile(CurrentUser: dict = Depends(GetCurrentUser)):
    return await GetUser(CurrentUser["sub"])


@Router.patch("/update", response_model=UserResponse)
async def UpdateProfile(Data: UserUpdateRequest, CurrentUser: dict = Depends(GetCurrentUser)):
    return await UpdateUser(CurrentUser["sub"], Data)


@Router.delete("/delete")
async def DeleteAccount(CurrentUser: dict = Depends(GetCurrentUser)):
    return await DeleteUser(CurrentUser["sub"])
