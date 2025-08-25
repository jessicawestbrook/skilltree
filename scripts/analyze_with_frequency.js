const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });
const fs = require('fs');

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

/**
 * Analyze how word frequency correlates with bee ratings
 * This will help us understand if common words tend to be easier in spelling bees
 */
async function analyzeWordFrequency() {
  try {
    console.log('=== ANALYZING WORD FREQUENCY vs BEE RATINGS ===\n');
    
    // Get all words with bee ratings and frequency data
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty, frequency')
      .in('source_difficulty', ['One Bee', 'Two Bee', 'Three Bee'])
      .order('word');
    
    if (error) throw error;
    
    console.log(`Analyzing ${words.length} words...\n`);
    
    // Check if we have frequency data
    const wordsWithFreq = words.filter(w => w.frequency !== null && w.frequency !== undefined);
    console.log(`Words with frequency data: ${wordsWithFreq.length} (${(wordsWithFreq.length/words.length*100).toFixed(1)}%)\n`);
    
    if (wordsWithFreq.length === 0) {
      console.log('NO FREQUENCY DATA FOUND IN DATABASE!\n');
      console.log('The "frequency" field exists but appears to be empty.');
      console.log('\n=== RECOMMENDATION ===');
      console.log('To properly predict difficulty, we need to:');
      console.log('1. Install wordfreq: pip install wordfreq');
      console.log('2. Create a script to populate the frequency field using wordfreq.zipf_frequency()');
      console.log('3. Use Zipf scale: 0-8 where higher = more common');
      console.log('   - 6+ = very common (the, a, and)');
      console.log('   - 4-6 = common (house, friend)');
      console.log('   - 2-4 = uncommon (peculiar, monastery)');
      console.log('   - 0-2 = rare (sesquipedalian)');
      console.log('\n=== PROPOSED PYTHON SCRIPT ===\n');
      
      const pythonScript = `import psycopg2
from wordfreq import zipf_frequency
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

# Connect to Supabase PostgreSQL
conn = psycopg2.connect(
    host=os.getenv('SUPABASE_HOST'),
    database=os.getenv('SUPABASE_DB'),
    user=os.getenv('SUPABASE_USER'),
    password=os.getenv('SUPABASE_PASSWORD')
)

cur = conn.cursor()

# Get all words
cur.execute("SELECT id, word FROM spelling_words WHERE frequency IS NULL")
words = cur.fetchall()

print(f"Updating frequency for {len(words)} words...")

# Update frequencies in batches
batch_size = 100
for i in range(0, len(words), batch_size):
    batch = words[i:i+batch_size]
    updates = []
    
    for word_id, word in batch:
        # Get Zipf frequency (0-8 scale, higher = more common)
        freq = zipf_frequency(word.lower(), 'en')
        updates.append((freq, word_id))
    
    # Batch update
    cur.executemany(
        "UPDATE spelling_words SET frequency = %s WHERE id = %s",
        updates
    )
    
    if (i + batch_size) % 1000 == 0:
        conn.commit()
        print(f"Updated {i + batch_size} words...")

conn.commit()
print("Done!")
conn.close()`;

      console.log(pythonScript);
      
      // Save the script
      fs.writeFileSync('populate_word_frequency.py', pythonScript);
      console.log('\n✓ Script saved to populate_word_frequency.py');
      
    } else {
      // Analyze the frequency data we have
      console.log('=== FREQUENCY DISTRIBUTION BY BEE RATING ===\n');
      
      const freqByBee = {
        'One Bee': [],
        'Two Bee': [],
        'Three Bee': []
      };
      
      wordsWithFreq.forEach(w => {
        freqByBee[w.source_difficulty].push(w.frequency);
      });
      
      ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
        const freqs = freqByBee[bee].sort((a, b) => a - b);
        if (freqs.length > 0) {
          const avg = freqs.reduce((a, b) => a + b, 0) / freqs.length;
          const median = freqs[Math.floor(freqs.length / 2)];
          const p25 = freqs[Math.floor(freqs.length * 0.25)];
          const p75 = freqs[Math.floor(freqs.length * 0.75)];
          
          console.log(`${bee}:`);
          console.log(`  Average frequency: ${avg.toFixed(2)}`);
          console.log(`  Median: ${median.toFixed(2)}`);
          console.log(`  25th-75th percentile: ${p25.toFixed(2)} - ${p75.toFixed(2)}`);
          console.log();
        }
      });
      
      // Check correlation
      console.log('=== CORRELATION ANALYSIS ===\n');
      
      // If higher frequency = easier, we expect:
      // One Bee to have highest frequency
      // Three Bee to have lowest frequency
      
      const avgFreqs = {};
      ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
        const freqs = freqByBee[bee];
        avgFreqs[bee] = freqs.length > 0 ? freqs.reduce((a, b) => a + b, 0) / freqs.length : 0;
      });
      
      console.log('Average frequencies:');
      Object.entries(avgFreqs).forEach(([bee, avg]) => {
        console.log(`  ${bee}: ${avg.toFixed(2)}`);
      });
      
      if (avgFreqs['One Bee'] > avgFreqs['Three Bee']) {
        console.log('\n✓ Correlation confirmed: easier words are more frequent');
      } else {
        console.log('\n✗ No clear correlation between frequency and difficulty');
      }
    }
    
    // Check for other frequency-related fields
    console.log('\n=== CHECKING OTHER FREQUENCY FIELDS ===\n');
    
    const sampleWord = words[0];
    if (sampleWord) {
      const { data: fullWord, error: fullError } = await supabase
        .from('spelling_words')
        .select('*')
        .eq('word', sampleWord.word)
        .single();
      
      if (!fullError && fullWord) {
        const fields = Object.keys(fullWord);
        const freqFields = fields.filter(f => 
          f.toLowerCase().includes('freq') || 
          f.toLowerCase().includes('common') ||
          f.toLowerCase().includes('usage')
        );
        
        if (freqFields.length > 0) {
          console.log('Found frequency-related fields:');
          freqFields.forEach(field => {
            console.log(`  - ${field}: ${fullWord[field]}`);
          });
        } else {
          console.log('No frequency-related fields found besides "frequency"');
        }
        
        // Check specific fields that might contain frequency data
        if (fullWord.frequency_score !== undefined) {
          console.log(`\nfrequency_score field exists: ${fullWord.frequency_score}`);
        }
        if (fullWord.word_frequency_score !== undefined) {
          console.log(`word_frequency_score field exists: ${fullWord.word_frequency_score}`);
        }
      }
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

analyzeWordFrequency();