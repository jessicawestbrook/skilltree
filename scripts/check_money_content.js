const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkMoneyContent() {
  try {
    // Check skill_tree_nodes for money counting
    const { data: nodes, error: nodesError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, learning_content_ids')
      .or('name.ilike.%money%,name.ilike.%counting%,name.ilike.%coin%,name.ilike.%currency%');
    
    if (nodesError) throw nodesError;
    
    console.log('=== Skill Tree Nodes with Money/Counting ===');
    if (nodes && nodes.length > 0) {
      const moneyCountingNode = nodes.find(n => n.name === 'Money Counting');
      if (moneyCountingNode) {
        console.log(`\nMoney Counting Node Found:`);
        console.log(`  ID: ${moneyCountingNode.id}`);
        console.log(`  Content IDs: ${JSON.stringify(moneyCountingNode.learning_content_ids)}`);
        console.log(`  Has content: ${moneyCountingNode.learning_content_ids && moneyCountingNode.learning_content_ids.length > 0}`);
      }
      
      console.log(`\nTotal nodes with money/counting keywords: ${nodes.length}`);
    } else {
      console.log('No money counting nodes found');
    }
    
    // Check questions table for money-related questions
    const { data: questions, error: questionsError } = await supabase
      .from('questions')
      .select('id, question_text, skill_node_id')
      .or('question_text.ilike.%money%,question_text.ilike.%coin%,question_text.ilike.%dollar%,question_text.ilike.%cent%,question_text.ilike.%quarter%,question_text.ilike.%dime%,question_text.ilike.%nickel%,question_text.ilike.%penny%')
      .limit(10);
    
    if (questionsError) throw questionsError;
    
    console.log('\n=== Money-related Questions ===');
    if (questions && questions.length > 0) {
      console.log(`Found ${questions.length} money-related questions`);
      
      // Check if any belong to Money Counting node
      const moneyCountingNode = nodes?.find(n => n.name === 'Money Counting');
      if (moneyCountingNode) {
        const moneyCountingQuestions = questions.filter(q => q.skill_node_id === moneyCountingNode.id);
        console.log(`Questions for Money Counting node: ${moneyCountingQuestions.length}`);
        
        if (moneyCountingQuestions.length > 0) {
          console.log('\nSample Money Counting questions:');
          moneyCountingQuestions.slice(0, 3).forEach((q, i) => {
            console.log(`${i+1}. ${q.question_text.substring(0, 100)}...`);
          });
        }
      }
      
      console.log('\nSample money-related questions (any node):');
      questions.slice(0, 3).forEach((q, i) => {
        console.log(`${i+1}. ${q.question_text.substring(0, 100)}...`);
      });
    } else {
      console.log('No money-related questions found');
    }
    
    // Check learning_content table
    const { data: content, error: contentError } = await supabase
      .from('learning_content')
      .select('id, title, content')
      .or('title.ilike.%money%,title.ilike.%counting%,content.ilike.%money counting%')
      .limit(5);
    
    if (contentError) throw contentError;
    
    console.log('\n=== Learning Content with Money/Counting ===');
    if (content && content.length > 0) {
      console.log(`Found ${content.length} money-related learning content items`);
      content.forEach((c, i) => {
        console.log(`${i+1}. ${c.title} (ID: ${c.id})`);
        if (c.content) {
          console.log(`   Preview: ${c.content.substring(0, 100)}...`);
        }
      });
    } else {
      console.log('No money counting learning content found');
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
  
  process.exit(0);
}

checkMoneyContent();