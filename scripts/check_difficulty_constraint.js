const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function checkConstraint() {
  // Check what difficulties are in the generated content
  const fs = require('fs');
  const content = JSON.parse(fs.readFileSync('scripts/content_generation/output/math_content/visual_fixed/money_counting_visual.json', 'utf8'));
  
  const difficulties = new Set();
  content.questions.forEach(q => {
    difficulties.add(q.difficulty);
  });
  
  console.log('Difficulties in generated content:', Array.from(difficulties));
  
  // Check existing questions to see valid difficulties
  const { data, error } = await supabase
    .from('questions')
    .select('difficulty')
    .limit(10);
  
  if (!error && data) {
    const validDifficulties = new Set(data.map(q => q.difficulty));
    console.log('Valid difficulties from existing questions:', Array.from(validDifficulties));
  }
  
  process.exit(0);
}

checkConstraint();