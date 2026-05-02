import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

_db = None

def GetDb():
    global _db
    if _db is None:
        ServiceAccountPath = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "serviceAccount.json")
        if not firebase_admin._apps:
            Cred = credentials.Certificate(ServiceAccountPath)
            firebase_admin.initialize_app(Cred)
        _db = firestore.client()
    return _db
