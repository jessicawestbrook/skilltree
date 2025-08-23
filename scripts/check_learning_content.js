const fs = require('fs');
const path = require('path');

// Check all money counting content files for learning content
const files = [
  'scripts/content_generation/output/math_content/visual_fixed/money_counting_visual.json',
  'scripts/content_generation/output/math_content/age_appropriate/money_counting_elementary.json',
  'scripts/content_generation/output/math_content/visual/money_counting_visual.json'
];

files.forEach(filePath => {
  try {
    if (fs.existsSync(filePath)) {
      const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      console.log(`\n=== ${path.basename(filePath)} ===`);
      console.log('Has learningContent field:', 'learningContent' in content);
      console.log('Learning content value:', content.learningContent);
      
      if (content.content) {
        console.log('Has "content" field instead:', true);
        console.log('Content preview:', content.content.substring(0, 200) + '...');
      }
    }
  } catch (err) {
    console.log(`Error reading ${filePath}:`, err.message);
  }
});