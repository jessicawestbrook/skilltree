const fs = require('fs');
const path = require('path');

// Check the generated money counting content
const contentPath = path.join('scripts', 'content_generation', 'output', 'math_content', 'visual_fixed', 'money_counting_visual.json');

try {
  const rawContent = fs.readFileSync(contentPath, 'utf8');
  const content = JSON.parse(rawContent);
  
  console.log('=== GENERATED MONEY COUNTING CONTENT ===\n');
  console.log('File:', contentPath);
  console.log('Content type:', typeof content);
  console.log('Is array:', Array.isArray(content));
  
  // Handle if content is an object instead of array
  const items = Array.isArray(content) ? content : [content];
  console.log('Total items:', items.length);
  
  if (items.length > 0) {
    const moneyItem = items[0];
    console.log('\nFirst item details:');
    console.log('  Node ID:', moneyItem.nodeId);
    console.log('  Node Name:', moneyItem.nodeName);
    console.log('  Has learning content:', !!moneyItem.learningContent);
    console.log('  Number of questions:', moneyItem.questions?.length || 0);
    
    if (moneyItem.learningContent) {
      console.log('  Learning content preview:', moneyItem.learningContent.substring(0, 200) + '...');
    }
    
    if (moneyItem.questions && moneyItem.questions.length > 0) {
      console.log('\n  Sample questions:');
      moneyItem.questions.slice(0, 3).forEach((q, i) => {
        console.log(`    ${i + 1}. ${q.question_text?.substring(0, 100)}...`);
      });
    }
  }
  
  // Check if this is for Money Counting node
  const moneyCountingItem = items.find(item => 
    item.nodeName === 'Money Counting' || 
    item.nodeId === 'fea1ba27-904d-4a1c-85d3-7e708a80727c'
  );
  
  if (moneyCountingItem) {
    console.log('\n=== MONEY COUNTING NODE FOUND ===');
    console.log('Node ID:', moneyCountingItem.nodeId);
    console.log('Node Name:', moneyCountingItem.nodeName);
    console.log('Has content:', !!moneyCountingItem.learningContent);
    console.log('Questions count:', moneyCountingItem.questions?.length || 0);
    console.log('\nThis content is READY to be inserted into the database.');
  } else {
    console.log('\n⚠️  No Money Counting node found in this file');
  }
  
} catch (error) {
  console.error('Error reading file:', error.message);
}