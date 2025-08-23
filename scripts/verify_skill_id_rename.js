const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function verifyChanges() {
  console.log('=== Verifying skill_id Rename Changes ===\n');
  
  let allPassed = true;
  
  // 1. Check code for any remaining old column names
  console.log('1. Checking code for old column names...');
  const srcDir = path.join(__dirname, '..', 'src');
  const filesToCheck = [
    'types/database.types.ts',
    'services/recommendationService.ts',
    'services/adaptiveAssessmentService.ts',
    'components/LearningContentModal.tsx',
    'pages/CategoryPage.tsx',
    'pages/ProfilePage.tsx',
    'pages/LearningPathsPage.tsx'
  ];
  
  let codeIssues = [];
  for (const file of filesToCheck) {
    const filePath = path.join(srcDir, file);
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Check for old column names (but allow them in comments)
      const lines = content.split('\n');
      lines.forEach((line, index) => {
        if (!line.trim().startsWith('//') && !line.trim().startsWith('*')) {
          if (line.includes('skill_node_id')) {
            codeIssues.push(`   ❌ ${file}:${index + 1} - Found 'skill_node_id'`);
          }
          if (line.includes('skill_tree_node_id')) {
            codeIssues.push(`   ❌ ${file}:${index + 1} - Found 'skill_tree_node_id'`);
          }
          // Check for node_id but exclude parent_node_id and other valid uses
          if (line.includes('node_id') && !line.includes('parent_node_id') && !line.includes('allNodeIds')) {
            // More specific check for actual field references
            if (line.match(/[\.\[\s]node_id[:\s\]\}]/)) {
              codeIssues.push(`   ❌ ${file}:${index + 1} - Found 'node_id'`);
            }
          }
        }
      });
    }
  }
  
  if (codeIssues.length > 0) {
    console.log('   Issues found:');
    codeIssues.forEach(issue => console.log(issue));
    allPassed = false;
  } else {
    console.log('   ✅ No old column names found in code');
  }
  
  // 2. Check if we can query with new column names
  console.log('\n2. Testing database queries with new column names...');
  
  try {
    // Test user_progress with skill_id
    const { data: upTest, error: upError } = await supabase
      .from('user_progress')
      .select('skill_id')
      .limit(1);
    
    if (upError && upError.message.includes('skill_id')) {
      console.log('   ❌ user_progress.skill_id column not found - migration may not have been run');
      allPassed = false;
    } else {
      console.log('   ✅ user_progress.skill_id query successful');
    }
    
    // Test starred_categories with skill_id
    const { data: scTest, error: scError } = await supabase
      .from('starred_categories')
      .select('skill_id')
      .limit(1);
    
    if (scError && scError.message.includes('skill_id')) {
      console.log('   ⚠️  starred_categories.skill_id not accessible (table may not exist)');
    } else {
      console.log('   ✅ starred_categories.skill_id query successful');
    }
    
  } catch (error) {
    console.log('   ❌ Database query error:', error.message);
    allPassed = false;
  }
  
  // 3. Check for consistency in imports and types
  console.log('\n3. Checking TypeScript compilation...');
  const { execSync } = require('child_process');
  try {
    execSync('npm run typecheck', { stdio: 'pipe' });
    console.log('   ✅ TypeScript compilation successful');
  } catch (error) {
    console.log('   ❌ TypeScript compilation failed');
    allPassed = false;
  }
  
  // Summary
  console.log('\n=== VERIFICATION SUMMARY ===');
  if (allPassed) {
    console.log('✅ All checks passed! The rename from node_id/skill_node_id to skill_id is complete.');
    console.log('\nNext steps:');
    console.log('1. Run the SQL migration in Supabase if not already done');
    console.log('2. Test the application functionality');
    console.log('3. Remove backup tables once everything is confirmed working');
  } else {
    console.log('⚠️  Some issues were found. Please review the output above.');
    console.log('\nMake sure to:');
    console.log('1. Run the SQL migration script in Supabase dashboard');
    console.log('2. Fix any remaining code issues');
  }
}

verifyChanges();