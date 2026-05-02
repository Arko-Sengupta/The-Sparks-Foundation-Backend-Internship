from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.Secrets import JwtAlgorithm, JwtExpireMinutes, JwtSecret
Bearer = HTTPBearer()

def CreateAccessToken(Data: dict) -> str:
    try:
        Payload = Data.copy()
        Payload["exp"] = datetime.utcnow() + timedelta(minutes=JwtExpireMinutes)
        return jwt.encode(Payload, JwtSecret, algorithm=JwtAlgorithm)
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Token creation failed: {str(E)}")

def DecodeToken(Token: str) -> dict:
    try:
        return jwt.decode(Token, JwtSecret, algorithms=[JwtAlgorithm])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Token decoding failed: {str(E)}")

def GetCurrentUser(Credentials: HTTPAuthorizationCredentials = Security(Bearer)) -> dict:
    try:
        return DecodeToken(Credentials.credentials)
    except HTTPException:
        raise
    except Exception as E:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(E)}")