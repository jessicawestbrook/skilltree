#!/usr/bin/env node

/**
 * Fix references from user_progress to user_module_progress
 * The table was renamed but some code still references the old name
 */

const fs = require('fs');
const path = require('path');

const filesToFix = [
  'src/components/LearningContentModal.tsx',
  'src/pages/DiagnosticPage.tsx',
  'src/utils/checkTables.ts',
  'src/pages/SimpleLearningPage.tsx',
  'src/pages/CategoryPage.tsx',
  'src/services/achievementService.ts',
  'src/services/recommendationService.ts'
];

function fixFile(filePath) {
  const fullPath = path.join(__dirname, '..', filePath);
  
  if (!fs.existsSync(fullPath)) {
    console.log(`File not found: ${filePath}`);
    return;
  }
  
  let content = fs.readFileSync(fullPath, 'utf8');
  const originalContent = content;
  
  // Replace table references
  content = content.replace(/\.from\(['"]user_progress['"]\)/g, ".from('user_module_progress')");
  content = content.replace(/'user_progress'/g, "'user_module_progress'");
  content = content.replace(/"user_progress"/g, '"user_module_progress"');
  
  // Also update field names if needed
  // skill_id is now module_id in the new table
  content = content.replace(/\.eq\(['"]skill_id['"]/g, ".eq('module_id'");
  content = content.replace(/\.select\(['"]skill_id/g, ".select('module_id");
  
  if (content !== originalContent) {
    fs.writeFileSync(fullPath, content, 'utf8');
    console.log(`✓ Fixed: ${filePath}`);
  } else {
    console.log(`  No changes needed: ${filePath}`);
  }
}

console.log('Fixing user_progress table references...\n');

filesToFix.forEach(fixFile);

console.log('\nDone! All references have been updated.');
console.log('Note: You may need to restart the development server for changes to take effect.');