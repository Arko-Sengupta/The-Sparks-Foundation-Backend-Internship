
import re
import random
from fastapi import HTTPException
from config.Firebase import GetDb
from config.Jwt import CreateAccessToken
from models.Auth import SignUpRequest, LoginRequest, TokenResponse


def GenerateAccountNumber() -> str:
    return str(random.randint(10000000000, 99999999999))


def ValidateSignup(Data: SignUpRequest):
    if not re.match(r'^[a-zA-Z\s]{4,}$', Data.fullName):
        raise HTTPException(400, "Invalid full name — min 4 letters only")
    if not re.match(r'^\d{10}$', Data.phone):
        raise HTTPException(400, "Phone must be exactly 10 digits")
    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', Data.pan.upper()):
        raise HTTPException(400, "Invalid PAN format (e.g. ABCDE1234F)")
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', Data.password):
        raise HTTPException(400, "Password must be 8+ chars with uppercase, number & special character")


async def SignupUser(Data: SignUpRequest) -> TokenResponse:
    ValidateSignup(Data)
    Db = GetDb()

    Existing = Db.collection("users").where("email", "==", Data.email).get()
    if Existing:
        raise HTTPException(409, "An account with this email already exists")

    UserDoc = {
        "fullName":      Data.fullName,
        "email":         Data.email,
        "phone":         Data.phone,
        "pan":           Data.pan.upper(),
        "password":      Data.password,
        "address":       Data.address or "",
        "accountNumber": GenerateAccountNumber(),
        "accountType":   "Savings",
        "balance":       0.0,
    }

    Ref    = Db.collection("users").add(UserDoc)
    UserId = Ref[1].id
    Token  = CreateAccessToken({"sub": UserId, "email": Data.email})

    return TokenResponse(
        access_token   = Token,
        user_id        = UserId,
        full_name      = Data.fullName,
        email          = Data.email,
        account_number = UserDoc["accountNumber"],
    )


async def LoginUser(Data: LoginRequest) -> TokenResponse:
    Db = GetDb()

    Results = Db.collection("users") \
                .where("email",    "==", Data.email) \
                .where("password", "==", Data.password) \
                .get()

    if not Results:
        raise HTTPException(401, "Invalid email or password")

    User     = Results[0]
    UserId   = User.id
    UserData = User.to_dict()
    Token    = CreateAccessToken({"sub": UserId, "email": Data.email})

    return TokenResponse(
        access_token   = Token,
        user_id        = UserId,
        full_name      = UserData.get("fullName", ""),
        email          = UserData.get("email", ""),
        account_number = UserData.get("accountNumber", ""),
    )
