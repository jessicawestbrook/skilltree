const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkMoneyContent() {
  try {
    console.log('=== MONEY COUNTING CONTENT CHECK ===\n');
    
    // 1. Check skill_tree_nodes for Money Counting
    const { data: moneyNode, error: nodeError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .eq('name', 'Money Counting')
      .single();
    
    if (nodeError) throw nodeError;
    
    console.log('1. Money Counting Node:');
    console.log(`   ID: ${moneyNode.id}`);
    console.log(`   Name: ${moneyNode.name}`);
    console.log(`   Learning Content IDs: ${JSON.stringify(moneyNode.learning_content_ids)}`);
    console.log(`   Has Content: ${moneyNode.learning_content_ids && moneyNode.learning_content_ids.length > 0 ? 'YES' : 'NO'}`);
    
    // 2. Check if learning content exists for those IDs
    if (moneyNode.learning_content_ids && moneyNode.learning_content_ids.length > 0) {
      const { data: content, error: contentError } = await supabase
        .from('learning_content')
        .select('id, title, content')
        .in('id', moneyNode.learning_content_ids);
      
      if (contentError) throw contentError;
      
      console.log('\n2. Learning Content for Money Counting:');
      if (content && content.length > 0) {
        content.forEach((c, i) => {
          console.log(`   ${i+1}. ${c.title} (ID: ${c.id})`);
          if (c.content) {
            console.log(`      Preview: ${c.content.substring(0, 150).replace(/\n/g, ' ')}...`);
          }
        });
      } else {
        console.log('   No learning content found for the IDs in learning_content_ids');
      }
    } else {
      console.log('\n2. Learning Content: NO CONTENT IDS ASSIGNED TO NODE');
    }
    
    // 3. Check for questions directly about money counting
    const { data: questions, error: questionsError } = await supabase
      .from('questions')
      .select('*')
      .or('question_text.ilike.%how many cents%,question_text.ilike.%how much money%,question_text.ilike.%count the coins%,question_text.ilike.%total value%,question_text.ilike.%quarters%,question_text.ilike.%dimes%,question_text.ilike.%nickels%,question_text.ilike.%pennies%')
      .limit(10);
    
    if (questionsError) throw questionsError;
    
    console.log('\n3. Money Counting Questions:');
    if (questions && questions.length > 0) {
      console.log(`   Found ${questions.length} money counting questions`);
      console.log('\n   Sample questions:');
      questions.slice(0, 5).forEach((q, i) => {
        console.log(`   ${i+1}. ${q.question_text}`);
        console.log(`      Options: ${JSON.stringify(q.options)}`);
        console.log(`      Answer: ${q.options[q.correct_answer]}`);
      });
    } else {
      console.log('   NO MONEY COUNTING QUESTIONS FOUND');
    }
    
    // 4. Summary
    console.log('\n=== SUMMARY ===');
    console.log(`Money Counting node exists: YES (ID: ${moneyNode.id})`);
    console.log(`Learning content IDs assigned: ${moneyNode.learning_content_ids && moneyNode.learning_content_ids.length > 0 ? 'YES' : 'NO'}`);
    console.log(`Questions exist: ${questions && questions.length > 0 ? `YES (${questions.length} found)` : 'NO'}`);
    
    if (!moneyNode.learning_content_ids || moneyNode.learning_content_ids.length === 0) {
      console.log('\n⚠️  Money Counting node has NO learning content assigned');
    }
    if (!questions || questions.length === 0) {
      console.log('⚠️  No money counting questions found in the database');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkMoneyContent();