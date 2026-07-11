# backend/scripts/test_api.py
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    """Test the API endpoints"""
    print("🧪 Testing Agency Lead Intelligence API...")
    
    # 1. Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # 2. Create a company
    print("\n2. Creating test company...")
    company_data = {
        "name": "Test Tech Co",
        "website": "https://testtech.example.com",
        "industry": "SaaS",
        "size": "51-200 employees"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/companies", json=company_data)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Response: {data}")
        
        if response.status_code == 200:
            company_id = data.get("company_id")
            
            # 3. Get the company
            print("\n3. Getting company...")
            response = requests.get(f"{BASE_URL}/companies/{company_id}")
            print(f"   Status: {response.status_code}")
            
            # 4. Get all companies
            print("\n4. Getting all companies...")
            response = requests.get(f"{BASE_URL}/companies")
            companies = response.json()
            print(f"   Found {len(companies)} companies")
            
            # 5. Get leads
            print("\n5. Getting leads...")
            response = requests.get(f"{BASE_URL}/leads")
            leads = response.json()
            print(f"   Found {len(leads)} leads")
            
            # 6. Get stats
            print("\n6. Getting statistics...")
            response = requests.get(f"{BASE_URL}/leads/stats")
            stats = response.json()
            print(f"   Stats: {json.dumps(stats, indent=2)}")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")

if __name__ == "__main__":
    test_api()