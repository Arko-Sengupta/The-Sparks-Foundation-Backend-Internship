import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

SecretKey   = os.getenv("JWT_SECRET")
Algorithm   = os.getenv("JWT_ALGORITHM")
ExpireMinutes = int(os.getenv("JWT_EXPIRE_MINUTES"))

Security_ = HTTPBearer()


def CreateAccessToken(Data: dict) -> str:
    Payload = Data.copy()
    Payload["exp"] = datetime.utcnow() + timedelta(minutes=ExpireMinutes)
    return jwt.encode(Payload, SecretKey, algorithm=Algorithm)


def DecodeToken(Token: str) -> dict:
    try:
        return jwt.decode(Token, SecretKey, algorithms=[Algorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def GetCurrentUser(Credentials: HTTPAuthorizationCredentials = Security(Security_)) -> dict:
    return DecodeToken(Credentials.credentials)
