import firebase_admin

from fastapi import HTTPException
from firebase_admin import credentials, firestore

from config.Secrets import FirebaseCredentials

Db = None

def GetDb():
    global Db
    try:
        if Db is None:
            if not firebase_admin._apps:
                Cred = credentials.Certificate(FirebaseCredentials)
                firebase_admin.initialize_app(Cred)
            Db = firestore.client()
        return Db
    except Exception as E:
        raise HTTPException(status_code=500, detail=f"Firebase initialization failed: {str(E)}")