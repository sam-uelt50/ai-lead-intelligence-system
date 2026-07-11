from pymongo import MongoClient

# MongoDB connection
uri = 'mongodb+srv://samueltesema56_db_user:sam123@cluster0.4dfoa3f.mongodb.net/agency_intel?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true'
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client['agency_intel']

# Test connection
try:
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")