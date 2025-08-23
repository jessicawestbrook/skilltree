/**
 * Test script to verify Money Counting content displays properly
 * ================================================================
 */

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs').promises;
const path = require('path');

require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function testDisplay() {
  try {
    console.log('=== MONEY COUNTING MODULE TEST ===\n');
    
    // 1. Check the node
    const { data: node, error: nodeError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('name', 'Money Counting')
      .single();
    
    if (nodeError) throw nodeError;
    
    console.log('✅ Node found:');
    console.log('   ID:', node.id);
    console.log('   Name:', node.name);
    console.log('   Learning Content IDs:', node.learning_content_ids);
    
    // 2. Check the learning content
    if (node.learning_content_ids && node.learning_content_ids.length > 0) {
      const { data: content, error: contentError } = await supabase
        .from('learning_content')
        .select('id, title, content, question_ids')
        .eq('id', node.learning_content_ids[0])
        .single();
      
      if (contentError) throw contentError;
      
      console.log('\n✅ Learning Content found:');
      console.log('   ID:', content.id);
      console.log('   Title:', content.title);
      console.log('   Content length:', content.content.length, 'characters');
      console.log('   Has embedded CSS:', content.content.includes('<style>'));
      console.log('   Question IDs:', content.question_ids?.length || 0, 'questions linked');
      
      // 3. Check questions
      if (content.question_ids && content.question_ids.length > 0) {
        const { data: questions, error: questionsError } = await supabase
          .from('questions')
          .select('id, question_text, difficulty')
          .in('id', content.question_ids);
        
        if (questionsError) throw questionsError;
        
        console.log('\n✅ Questions found:', questions.length);
        
        // Group by difficulty
        const byDifficulty = {};
        questions.forEach(q => {
          byDifficulty[q.difficulty] = (byDifficulty[q.difficulty] || 0) + 1;
        });
        
        console.log('   Difficulty distribution:');
        Object.entries(byDifficulty).forEach(([diff, count]) => {
          console.log(`     ${diff}: ${count} questions`);
        });
      }
      
      // 4. Create a preview file
      const previewPath = path.join(__dirname, 'money_counting_full_preview.html');
      const previewHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Money Counting - Full Preview</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f9fafb;
        }
        .header {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 2rem;
        }
        .header p {
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
        }
        .content-wrapper {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        .info-box {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #10b981;
        }
        .info-box h2 {
            color: #059669;
            margin-top: 0;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        .stat {
            background: #f0fdf4;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #059669;
        }
        .stat-label {
            color: #6b7280;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        .learning-content-container {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Money Counting Learning Module</h1>
        <p>Interactive preview with embedded CSS styling</p>
    </div>
    
    <div class="content-wrapper">
        <div class="info-box">
            <h2>Module Information</h2>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">${content.question_ids?.length || 0}</div>
                    <div class="stat-label">Questions</div>
                </div>
                <div class="stat">
                    <div class="stat-value">✅</div>
                    <div class="stat-label">CSS Embedded</div>
                </div>
                <div class="stat">
                    <div class="stat-value">🎨</div>
                    <div class="stat-label">Interactive</div>
                </div>
            </div>
        </div>
        
        <div class="learning-content-container">
            ${content.content}
        </div>
    </div>
</body>
</html>`;
      
      await fs.writeFile(previewPath, previewHtml);
      console.log('\n📄 Preview file created:', previewPath);
      console.log('   Open this file in a browser to see the styled content');
      
    } else {
      console.log('\n❌ No learning content IDs found for Money Counting node');
    }
    
    console.log('\n=== TEST COMPLETE ===');
    console.log('\nTo test in the app:');
    console.log('1. Go to http://localhost:3000');
    console.log('2. Navigate to: Mathematics → Early Mathematics → Arithmetic Basics → Money Counting');
    console.log('3. Click on Money Counting to open the learning modal');
    console.log('\nThe content should display with all embedded CSS styles (no external CSS needed).');
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  process.exit(0);
}

testDisplay();