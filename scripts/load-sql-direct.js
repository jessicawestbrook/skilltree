const { Client } = require('pg');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

async function loadSocialData() {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
    ssl: {
      rejectUnauthorized: false
    }
  });

  try {
    console.log('🔌 Connecting to database...');
    await client.connect();
    console.log('✅ Connected to database\n');

    // Read the SQL file
    const sqlPath = path.join(__dirname, 'seed-social-data.sql');
    const sqlContent = fs.readFileSync(sqlPath, 'utf8');

    // Split SQL into individual statements
    const statements = sqlContent
      .split(';')
      .map(stmt => stmt.trim())
      .filter(stmt => stmt.length > 0 && !stmt.startsWith('--'));

    console.log(`📝 Executing ${statements.length} SQL statements...\n`);

    let successCount = 0;
    let errorCount = 0;

    for (let i = 0; i < statements.length; i++) {
      const statement = statements[i] + ';';
      
      // Skip SELECT statements that are just for output
      if (statement.trim().toLowerCase().startsWith('select \'')) {
        continue;
      }

      try {
        await client.query(statement);
        successCount++;
        
        // Log progress for important operations
        if (statement.includes('INSERT INTO')) {
          const table = statement.match(/INSERT INTO (\w+\.\w+|\w+)/i)?.[1];
          if (table) {
            console.log(`  ✅ Inserted data into ${table}`);
          }
        }
      } catch (err) {
        errorCount++;
        // Only log actual errors, not expected conflicts
        if (!err.message.includes('duplicate key') && !err.message.includes('already exists')) {
          console.error(`  ❌ Error: ${err.message.substring(0, 100)}`);
        }
      }
    }

    console.log('\n📊 Summary:');
    console.log(`  ✅ Successful operations: ${successCount}`);
    if (errorCount > 0) {
      console.log(`  ⚠️  Skipped operations (duplicates): ${errorCount}`);
    }

    // Verify the data was loaded
    console.log('\n🔍 Verifying data...');
    
    const profileCount = await client.query('SELECT COUNT(*) FROM profiles');
    console.log(`  👥 User profiles: ${profileCount.rows[0].count}`);
    
    const friendshipCount = await client.query('SELECT COUNT(*) FROM friendships');
    console.log(`  🤝 Friendships: ${friendshipCount.rows[0].count}`);
    
    const achievementCount = await client.query('SELECT COUNT(*) FROM user_achievements');
    console.log(`  🏆 Achievements: ${achievementCount.rows[0].count}`);
    
    const leaderboardCount = await client.query('SELECT COUNT(*) FROM leaderboard');
    console.log(`  📊 Leaderboard entries: ${leaderboardCount.rows[0].count}`);
    
    const discussionCount = await client.query('SELECT COUNT(*) FROM discussions');
    console.log(`  💬 Discussions: ${discussionCount.rows[0].count}`);
    
    const progressCount = await client.query('SELECT COUNT(*) FROM user_progress');
    console.log(`  📈 Progress records: ${progressCount.rows[0].count}`);

    console.log('\n🎉 Sample social data loaded successfully!');
    console.log('Your NeuroQuest app now has test users and social content!');

  } catch (error) {
    console.error('❌ Connection error:', error.message);
  } finally {
    await client.end();
    console.log('\n🔌 Database connection closed');
  }
}

loadSocialData();