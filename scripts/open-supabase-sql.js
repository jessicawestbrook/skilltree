const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('📋 SOCIAL TABLES SETUP REQUIRED');
console.log('================================\n');

// Read the SQL file
const sqlPath = path.join(__dirname, '..', 'prisma', 'migrations', 'sql', '0002_social_features.sql');
const sqlContent = fs.readFileSync(sqlPath, 'utf8');

// Save a temporary HTML file with the SQL and instructions
const htmlContent = `<!DOCTYPE html>
<html>
<head>
  <title>NeuroQuest - Create Social Tables</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
    h1 { color: #0ea5e9; }
    .step { background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .sql-box { background: #1e293b; color: #e2e8f0; padding: 20px; border-radius: 8px; overflow-x: auto; font-family: 'Courier New', monospace; font-size: 14px; max-height: 400px; overflow-y: auto; }
    button { background: #0ea5e9; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; }
    button:hover { background: #0284c7; }
    .success { color: #10b981; font-weight: bold; }
    .link { color: #0ea5e9; text-decoration: none; font-weight: bold; }
    .link:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>🧠 NeuroQuest - Create Social Feature Tables</h1>
  
  <div class="step">
    <h2>Step 1: Open Supabase SQL Editor</h2>
    <p>Click the link below to open your Supabase project's SQL editor:</p>
    <a class="link" href="https://supabase.com/dashboard/project/bedcscnprmaztktgklko/sql" target="_blank">
      🚀 Open Supabase SQL Editor
    </a>
  </div>

  <div class="step">
    <h2>Step 2: Copy the SQL</h2>
    <p>Click the button below to copy the SQL code to your clipboard:</p>
    <button onclick="copySQL()">📋 Copy SQL to Clipboard</button>
    <span id="copyStatus"></span>
  </div>

  <div class="step">
    <h2>Step 3: SQL Code</h2>
    <p>Here's the SQL that will create all the social feature tables:</p>
    <div class="sql-box" id="sqlContent">${sqlContent.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
  </div>

  <div class="step">
    <h2>Step 4: Run in Supabase</h2>
    <p>1. Paste the SQL code in the Supabase SQL Editor</p>
    <p>2. Click "Run" to execute the SQL</p>
    <p>3. You should see <span class="success">Success. No rows returned</span></p>
  </div>

  <div class="step">
    <h2>Step 5: Load Sample Data</h2>
    <p>After creating the tables, return to the terminal and the data will be loaded automatically!</p>
  </div>

  <script>
    function copySQL() {
      const sql = document.getElementById('sqlContent').textContent;
      navigator.clipboard.writeText(sql).then(() => {
        document.getElementById('copyStatus').innerHTML = ' <span class="success">✅ Copied!</span>';
        setTimeout(() => {
          document.getElementById('copyStatus').innerHTML = '';
        }, 3000);
      });
    }
  </script>
</body>
</html>`;

const htmlPath = path.join(__dirname, 'setup-social-tables.html');
fs.writeFileSync(htmlPath, htmlContent);

console.log('Opening setup page in your browser...\n');

// Open in default browser
const url = `file:///${htmlPath.replace(/\\/g, '/')}`;
const start = (process.platform == 'darwin'? 'open': process.platform == 'win32'? 'start': 'xdg-open');

exec(`${start} "${url}"`, (err) => {
  if (err) {
    console.log('Could not open browser automatically.');
    console.log(`Please open manually: ${htmlPath}`);
  } else {
    console.log('✅ Setup page opened in your browser!');
    console.log('\nFollow the instructions on the page to:');
    console.log('1. Open Supabase SQL Editor');
    console.log('2. Copy the SQL code');
    console.log('3. Run it in Supabase');
    console.log('4. Return here to load sample data');
  }
});

console.log('\n⏳ Waiting for you to create the tables...');
console.log('Press Ctrl+C to exit or wait for confirmation...\n');

// Check periodically if tables exist
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

let checkCount = 0;
const checkInterval = setInterval(async () => {
  checkCount++;
  
  // Check if profiles table exists
  const { error } = await supabase.from('profiles').select('*').limit(1);
  
  if (!error || !error.message.includes('does not exist')) {
    clearInterval(checkInterval);
    console.log('\n🎉 Tables created successfully!');
    console.log('Now loading sample data...\n');
    
    // Clean up HTML file
    fs.unlinkSync(htmlPath);
    
    // Load the sample data
    exec('node scripts/seed-data-direct.js', (err, stdout, stderr) => {
      if (stdout) console.log(stdout);
      if (stderr) console.error(stderr);
      process.exit(0);
    });
  } else if (checkCount % 10 === 0) {
    console.log('Still waiting for tables to be created... (checking every 5 seconds)');
  }
}, 5000);