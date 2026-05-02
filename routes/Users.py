from fastapi import APIRouter, Depends, HTTPException

from config.Jwt import GetCurrentUser
from models.Auth import UserResponse, UserUpdateRequest
from services.UserService import DeleteUser, GetUser, UpdateUser

Router = APIRouter(prefix="/users", tags=["Users"])

@Router.get("/profile", response_model=UserResponse)
async def GetProfile(CurrentUser: dict = Depends(GetCurrentUser)):
    try:
        return await GetUser(CurrentUser["sub"])
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(E)}")

@Router.patch("/update", response_model=UserResponse)
async def UpdateProfile(Data: UserUpdateRequest, CurrentUser: dict = Depends(GetCurrentUser)):
    try:
        return await UpdateUser(CurrentUser["sub"], Data)
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(E)}")

@Router.delete("/delete")
async def DeleteAccount(CurrentUser: dict = Depends(GetCurrentUser)):
    try:
        return await DeleteUser(CurrentUser["sub"])
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to delete account: {str(E)}")