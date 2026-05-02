from fastapi import HTTPException

from config.Firebase import GetDb
from models.Auth import UserResponse, UserUpdateRequest

async def GetUser(UserId: str) -> UserResponse:
    try:
        Db   = GetDb()
        Snap = Db.collection("users").document(UserId).get()

        if not Snap.exists:
            raise HTTPException(404, "User not found")

        D = Snap.to_dict()
        return UserResponse(
            id            = Snap.id,
            fullName      = D.get("fullName", ""),
            email         = D.get("email", ""),
            phone         = D.get("phone", ""),
            address       = D.get("address", ""),
            accountNumber = D.get("accountNumber", ""),
            accountType   = D.get("accountType", "Savings"),
            balance       = D.get("balance", 0.0),
        )
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(E)}")

async def UpdateUser(UserId: str, Data: UserUpdateRequest) -> UserResponse:
    try:
        Db      = GetDb()
        Updates = {K: V for K, V in Data.dict().items() if V is not None}

        if not Updates:
            raise HTTPException(400, "No fields provided to update")

        Db.collection("users").document(UserId).update(Updates)
        return await GetUser(UserId)
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(E)}")

async def DeleteUser(UserId: str) -> dict:
    try:
        Db = GetDb()

        UserSnap = Db.collection("users").document(UserId).get()
        if not UserSnap.exists:
            raise HTTPException(404, "User not found")

        Transactions = Db.collection("transactions").where("userId", "==", UserId).get()
        for Txn in Transactions:
            Txn.reference.delete()

        Db.collection("users").document(UserId).delete()

        return {"message": "Account deleted successfully"}
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(E)}")