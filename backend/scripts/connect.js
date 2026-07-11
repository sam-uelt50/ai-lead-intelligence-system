// diagnostic.js
const { MongoClient } = require('mongodb');

async function diagnose() {
  console.log("=== MongoDB Diagnostic Test ===\n");
  
  const testCases = [
    {
      name: "Basic connection",
      uri: "mongodb+srv://samueltesema56_db_user:sam123@cluster0.4dfoa3f.mongodb.net/"
    },
    {
      name: "With appName only",
      uri: "mongodb+srv://samueltesema56_db_user:sam123@cluster0.4dfoa3f.mongodb.net/?appName=Cluster0"
    },
    {
      name: "Full connection string",
      uri: "mongodb+srv://samueltesema56_db_user:sam123@cluster0.4dfoa3f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    }
  ];
  
  let success = false;
  
  for (const test of testCases) {
    console.log(`Testing: ${test.name}`);
    console.log(`URI: ${test.uri.substring(0, 55)}...`);
    
    const client = new MongoClient(test.uri, {
      serverSelectionTimeoutMS: 8000,
      connectTimeoutMS: 8000
    });
    
    try {
      await client.connect();
      console.log("✅ SUCCESS!\n");
      
      // Test further
      const ping = await client.db("admin").command({ ping: 1 });
      console.log(`   Ping response: ${JSON.stringify(ping)}`);
      
      const dbs = await client.db().admin().listDatabases();
      console.log(`   Found ${dbs.databases.length} databases`);
      
      await client.close();
      success = true;
      break;
      
    } catch (err) {
      console.log(`❌ FAILED: ${err.message}\n`);
    }
  }
  
  if (!success) {
    console.log("\n💡 TROUBLESHOOTING STEPS:");
    console.log("1. Verify password is correct in MongoDB Atlas");
    console.log("2. Check Network Access → Add your IP address");
    console.log("3. Try creating a new database user:");
    console.log("   - Go to Database Access → Add New User");
    console.log("   - Username: test_user");
    console.log("   - Password: test123");
    console.log("   - Atlas Admin role");
  }
}

diagnose();
      
    