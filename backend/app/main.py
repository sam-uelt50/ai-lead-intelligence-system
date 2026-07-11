from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
uri = 'mongodb+srv://samueltesema56_db_user:sam123@cluster0.4dfoa3f.mongodb.net/agency_intel?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true'
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client['agency_intel']

@app.get("/")
def home():
    return {"message": "Dashboard API", "status": "running"}

@app.get("/dashboard")
def dashboard():
    companies = db.companies.count_documents({})
    signals = db.signals.count_documents({})
    
    # Companies by priority
    priorities = {}
    for priority in ["hot", "warm", "cold"]:
        count = db.companies.count_documents({"priority": priority})
        priorities[priority] = count
    
    return {
        "total_companies": companies,
        "total_signals": signals,
        "priorities": priorities,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/companies")
def get_companies(limit: int = 10):
    companies = list(db.companies.find(
        {},
        {"_id": 0, "name": 1, "score": 1, "priority": 1, "industry": 1, "signal_count": 1}
    ).limit(limit))
    
    return {"companies": companies, "count": len(companies)}

@app.get("/signals")
def get_signals(limit: int = 10):
    signals = list(db.signals.find(
        {},
        {"_id": 0, "company_name": 1, "signal_type": 1, "description": 1, "detected_at": 1}
    ).sort("detected_at", -1).limit(limit))
    
    return {"signals": signals, "count": len(signals)}

@app.get("/priority/{priority}")
def get_by_priority(priority: str):
    companies = list(db.companies.find(
        {"priority": priority},
        {"_id": 0, "name": 1, "score": 1, "industry": 1}
    ))
    
    return {"priority": priority, "companies": companies, "count": len(companies)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)