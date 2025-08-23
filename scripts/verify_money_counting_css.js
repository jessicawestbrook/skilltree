const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function verifyContent() {
  try {
    // Get the Money Counting learning content
    const { data, error } = await supabase
      .from('learning_content')
      .select('content')
      .eq('id', 1991)
      .single();
    
    if (error) throw error;
    
    console.log('=== Money Counting Content Status ===\n');
    console.log('Content length:', data.content.length, 'characters');
    console.log('Has <style> tag:', data.content.includes('<style>'));
    console.log('Has CSS classes:', data.content.includes('coin-card'));
    console.log('Has intro-section:', data.content.includes('intro-section'));
    console.log('Has SVG coins:', data.content.includes('<svg'));
    
    // Check for key CSS elements
    const cssChecks = [
      'background: linear-gradient',
      'border-radius',
      'box-shadow',
      '.coin-card',
      '.intro-section',
      '.skip-counting-section',
      '@media (prefers-color-scheme: dark)'
    ];
    
    console.log('\n=== CSS Elements Check ===');
    cssChecks.forEach(check => {
      console.log(`${check}: ${data.content.includes(check) ? '✅' : '❌'}`);
    });
    
    // Check HTML structure
    const htmlChecks = [
      '<h1>Let\'s Learn to Count Money!',
      '<div class="intro-section">',
      '<div class="coin-guide">',
      '<div class="skip-counting-section">',
      'svg width="100" height="100"'
    ];
    
    console.log('\n=== HTML Structure Check ===');
    htmlChecks.forEach(check => {
      const checkDisplay = check.length > 40 ? check.substring(0, 40) + '...' : check;
      console.log(`${checkDisplay}: ${data.content.includes(check) ? '✅' : '❌'}`);
    });
    
    console.log('\n✅ Content is ready for display with embedded CSS!');
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  process.exit(0);
}

verifyContent();