# The Sparks Foundation — Banking Backend

FastAPI + Firestore Backend For The Sparks Foundation Banking Application. Provides Secure REST APIs For User Authentication, Account Management, And Fund Transfers.

## How It Works

The Backend Exposes Three Route Groups — Auth, Users, And Transactions. JWT Tokens Are Issued On Login And Signup And Must Be Passed As Bearer Tokens For Protected Routes. Firebase Firestore Is Used As The Database. All Credentials Are Loaded From `.env` Via A Centralized `config/Secrets.py` Module. Transfers Automatically Debit The Sender, Credit The Beneficiary (If Their Account Exists In The System), And Record Transaction Entries For Both Parties.

## Setup

1. Clone Repository And Navigate To The Project Directory:

```bash
cd The-Sparks-Foundation-Internship-Backend
```

2. Create And Activate A Virtual Environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Environment Variables In `.env`:

```env
JWT_SECRET=<your_secret>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=<your_project_id>
FIREBASE_PRIVATE_KEY_ID=<your_private_key_id>
FIREBASE_PRIVATE_KEY=<your_private_key>
FIREBASE_CLIENT_EMAIL=<your_client_email>
FIREBASE_CLIENT_ID=<your_client_id>
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_CERT_URL=<your_client_cert_url>
FIREBASE_UNIVERSE_DOMAIN=googleapis.com
```

5. Start The Server:

```bash
uvicorn main:App --reload
```

API Starts At `http://localhost:8000`. Interactive Docs At `http://localhost:8000/docs`.

## Dependencies

| Package                  | Version  |
| ------------------------ | -------- |
| fastapi                  | 0.111.0  |
| uvicorn[standard]        | 0.29.0   |
| python-multipart         | 0.0.9    |
| firebase-admin           | 6.5.0    |
| python-jose[cryptography]| 3.3.0    |
| passlib[bcrypt]          | 1.7.4    |
| python-dotenv            | 1.0.1    |
| pytest                   | 8.2.2    |
| httpx                    | 0.27.0   |
| pytest-asyncio           | 0.23.7   |

## API Endpoints

| Method | Endpoint                | Auth     | Description                  |
| ------ | ----------------------- | -------- | ---------------------------- |
| POST   | `/auth/signup`          | No       | Register A New User          |
| POST   | `/auth/login`           | No       | Login And Receive JWT Token  |
| GET    | `/users/profile`        | Required | Get Logged-In User Profile   |
| PATCH  | `/users/update`         | Required | Update User Profile Fields   |
| DELETE | `/users/delete`         | Required | Delete Account And All Data  |
| GET    | `/transactions/history` | Required | Get User Transaction History |
| POST   | `/transactions/initiate`| Required | Initiate A Fund Transfer     |
| GET    | `/`                     | No       | Health Check                 |
| GET    | `/health`               | No       | Health Check                 |

## Project Structure

```
The-Sparks-Foundation-Internship-Backend/
├── main.py                            — FastAPI App, CORS, Router Registration
├── config/
│   ├── Secrets.py                     — Centralized Env Loader (JWT + Firebase Creds)
│   ├── Firebase.py                    — Firestore Client Singleton
│   └── Jwt.py                         — Token Creation, Decoding, Auth Dependency
├── models/
│   ├── Auth.py                        — Pydantic Models: Signup, Login, Token, User
│   └── Transaction.py                 — Pydantic Models: Transaction Request & Response
├── routes/
│   ├── Auth.py                        — POST /auth/signup, /auth/login
│   ├── Users.py                       — GET/PATCH/DELETE /users/*
│   └── Transactions.py                — GET/POST /transactions/*
├── services/
│   ├── AuthService.py                 — Signup & Login Business Logic
│   ├── UserService.py                 — Get, Update, Delete User Logic
│   └── TransactionService.py         — Format, Fetch & Create Transactions
├── requirements.txt                   — Python Dependencies
├── .env                               — Environment Variables (Git Ignored)
├── .gitignore
└── README.md
```

## Contribution

If You'd Like To Contribute, Follow The Guidelines:
- Create A Branch Using The Format `TSF-Backend_<YourUsername>` When Contributing To The Project.
- Add The Label `Contributor` To Your Contributions To Distinguish Them Within The Project.