/**
 * Script to update Money Counting HTML content with inline CSS
 * =============================================================
 */

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs').promises;
const path = require('path');

require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function updateHtmlWithCss() {
  try {
    console.log('Loading Money Counting content from file...');
    
    // Load the original content from the file
    const contentPath = path.join(__dirname, 'content_generation', 'output', 'math_content', 'visual_fixed', 'money_counting_visual.json');
    const data = JSON.parse(await fs.readFile(contentPath, 'utf-8'));
    const originalContent = data.content.content;
    
    // Add embedded CSS styles at the beginning
    const cssStyles = `
<style>
  /* Learning Content Styles */
  .intro-section {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border-left: 4px solid #22c55e;
  }
  
  .intro-section h2 {
    color: #166534;
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
  }
  
  .intro-section p {
    color: #15803d;
    font-size: 1.1rem;
    margin: 0;
  }
  
  /* Coin Guide Section */
  .coin-guide {
    margin: 2rem 0;
  }
  
  .coin-guide h2 {
    color: #059669;
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .coin-card {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .coin-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
  
  .coin-card h3 {
    color: #059669;
    margin-bottom: 1rem;
    font-size: 1.25rem;
  }
  
  .coin-display {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
  }
  
  .coin-svg {
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
  }
  
  .coin-card p {
    color: #374151;
    line-height: 1.6;
    margin: 0.5rem 0;
  }
  
  .coin-card strong {
    color: #059669;
    font-weight: 600;
  }
  
  /* Skip Counting Section */
  .skip-counting-section {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
  }
  
  .skip-counting-section h2 {
    color: #92400e;
    font-size: 1.75rem;
    margin-bottom: 1rem;
    text-align: center;
  }
  
  .skip-counting-section .intro {
    color: #78350f;
    font-size: 1.1rem;
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .skip-count-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .skip-count-card h3 {
    color: #92400e;
    margin-bottom: 1rem;
    font-size: 1.25rem;
  }
  
  .coin-row {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin: 1rem 0;
    flex-wrap: wrap;
  }
  
  .counting-sequence {
    background: #fef3c7;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    font-size: 1.25rem;
    color: #92400e;
    margin: 1rem 0;
    font-family: 'Courier New', monospace;
  }
  
  .counting-sequence strong {
    color: #dc2626;
    font-size: 1.5rem;
  }
  
  .tip {
    background: #dbeafe;
    border-left: 4px solid #3b82f6;
    border-radius: 4px;
    padding: 0.75rem;
    margin-top: 0.5rem;
    color: #1e40af;
    font-style: italic;
  }
  
  /* Practice Section */
  .practice-section {
    background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
  }
  
  .practice-section h2 {
    color: #6b21a8;
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .practice-problem {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .practice-problem h3 {
    color: #6b21a8;
    margin-bottom: 1rem;
  }
  
  .problem-coins {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin: 1rem 0;
    flex-wrap: wrap;
  }
  
  .solution {
    background: #f3e8ff;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
  }
  
  .solution strong {
    color: #6b21a8;
    font-size: 1.25rem;
  }
  
  /* Money Facts Section */
  .money-facts {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
  }
  
  .money-facts h2 {
    color: #991b1b;
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .fact-card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    border-left: 4px solid #dc2626;
  }
  
  .fact-card h4 {
    color: #991b1b;
    margin-bottom: 0.5rem;
  }
  
  .fact-card p {
    color: #7f1d1d;
    margin: 0;
  }
  
  /* Summary Section */
  .summary-section {
    background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
  }
  
  .summary-section h2 {
    color: #075985;
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .summary-card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .summary-card h4 {
    color: #075985;
    margin-bottom: 0.5rem;
  }
  
  .summary-card p {
    color: #0c4a6e;
    font-size: 1.25rem;
    font-weight: bold;
    margin: 0;
  }
  
  /* Dark mode support */
  @media (prefers-color-scheme: dark) {
    .coin-card,
    .skip-count-card,
    .practice-problem,
    .fact-card,
    .summary-card {
      background: #1f2937;
      border-color: #374151;
      color: #e5e7eb;
    }
    
    .coin-card p,
    .fact-card p {
      color: #d1d5db;
    }
    
    .coin-card h3,
    .skip-count-card h3,
    .practice-problem h3 {
      color: #34d399;
    }
    
    .intro-section {
      background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
    }
    
    .intro-section h2 {
      color: #34d399;
    }
    
    .intro-section p {
      color: #6ee7b7;
    }
    
    .skip-counting-section {
      background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
    }
    
    .skip-counting-section h2 {
      color: #fbbf24;
    }
    
    .skip-counting-section .intro {
      color: #fde68a;
    }
    
    .counting-sequence {
      background: #451a03;
      color: #fbbf24;
    }
    
    .solution {
      background: #4c1d95;
      color: #e9d5ff;
    }
  }
  
  /* Responsive design */
  @media (max-width: 640px) {
    .coin-row,
    .problem-coins {
      gap: 0.25rem;
    }
    
    .coin-svg {
      width: 50px !important;
      height: 50px !important;
    }
    
    .summary-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
`;
    
    // Combine CSS with the original HTML content
    const updatedContent = cssStyles + originalContent;
    
    console.log('\nUpdating learning content in database...');
    
    // Update the learning content in the database
    const { error } = await supabase
      .from('learning_content')
      .update({ content: updatedContent })
      .eq('id', 1991);
    
    if (error) {
      console.error('Error updating content:', error.message);
      return;
    }
    
    console.log('✅ Successfully updated Money Counting content with embedded CSS!');
    
    // Save a preview file
    const previewPath = path.join(__dirname, 'money_counting_preview_with_css.html');
    const previewHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Money Counting Learning Content Preview</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f9fafb;">
    ${updatedContent}
</body>
</html>`;
    
    await fs.writeFile(previewPath, previewHtml);
    console.log(`\nPreview file saved to: ${previewPath}`);
    console.log('You can open this file in a browser to see how the content will look.');
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  process.exit(0);
}

updateHtmlWithCss();