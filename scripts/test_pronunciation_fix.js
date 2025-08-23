const { createClient } = require('@supabase/supabase-js');
const Anthropic = require('@anthropic-ai/sdk');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function testPronunciationAPI() {
  console.log('Testing Anthropic API for pronunciation data...\n');
  
  const testWords = ['ringing', 'referred', 'redingote', 'proselytizer'];
  
  for (const word of testWords) {
    try {
      console.log(`Testing word: ${word}`);
      
      const message = await anthropic.messages.create({
        model: "claude-3-5-sonnet-20240620",
        max_tokens: 150,
        messages: [{
          role: "user",
          content: `Provide the phonetic respelling pronunciation for the word "${word}" in the format used for spelling bees (like AY-bul for "able" or KROH-kus for "crocus"). Return ONLY the pronunciation, nothing else. If the word is not a real English word, return "INVALID".`
        }]
      });
      
      const pronunciation = message.content[0].text.trim();
      console.log(`  Result: ${pronunciation}\n`);
      
      // Test delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
    } catch (error) {
      console.error(`Error with ${word}:`, error.message);
    }
  }
}

async function testDatabaseConnection() {
  console.log('Testing database connection...');
  
  try {
    const { data, error } = await supabase
      .from('spelling_words')
      .select('word, pronunciation_guide')
      .is('pronunciation_guide', null)
      .limit(3);
      
    if (error) throw error;
    
    console.log('Sample missing pronunciation words:');
    data.forEach(word => console.log(`- ${word.word}`));
    console.log('✓ Database connection successful\n');
    
  } catch (error) {
    console.error('Database connection failed:', error);
  }
}

async function main() {
  await testDatabaseConnection();
  await testPronunciationAPI();
}

main().catch(console.error);