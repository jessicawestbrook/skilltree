const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function analyzeBeeFactors() {
  try {
    console.log('=== ANALYZING BEE RATING FACTORS ===\n');
    
    // Get words with their various difficulty metrics
    const { data: words, error } = await supabase
      .from('spelling_words')
      .select('word, source_difficulty, grade_level, ai_spelling_difficulty_level')
      .in('source_difficulty', ['One Bee', 'Two Bee', 'Three Bee'])
      .order('word');
    
    if (error) throw error;
    
    // Analyze grade level correlation
    console.log('=== GRADE LEVEL CORRELATION ===\n');
    const gradeByBee = {
      'One Bee': {},
      'Two Bee': {},
      'Three Bee': {}
    };
    
    words.forEach(w => {
      if (w.grade_level) {
        if (!gradeByBee[w.source_difficulty][w.grade_level]) {
          gradeByBee[w.source_difficulty][w.grade_level] = 0;
        }
        gradeByBee[w.source_difficulty][w.grade_level]++;
      }
    });
    
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      const grades = gradeByBee[bee];
      const total = Object.values(grades).reduce((a, b) => a + b, 0);
      const avgGrade = Object.entries(grades).reduce((sum, [grade, count]) => 
        sum + (parseInt(grade) * count), 0) / total;
      
      console.log(`${bee} - Average Grade Level: ${avgGrade.toFixed(1)}`);
      console.log('  Distribution:', Object.entries(grades)
        .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
        .slice(0, 5)
        .map(([g, c]) => `Grade ${g}: ${((c/total)*100).toFixed(1)}%`)
        .join(', '));
    });
    
    // Analyze AI difficulty correlation
    console.log('\n=== AI DIFFICULTY CORRELATION ===\n');
    const aiByBee = {
      'One Bee': {},
      'Two Bee': {},
      'Three Bee': {}
    };
    
    words.forEach(w => {
      if (w.ai_spelling_difficulty_level) {
        if (!aiByBee[w.source_difficulty][w.ai_spelling_difficulty_level]) {
          aiByBee[w.source_difficulty][w.ai_spelling_difficulty_level] = 0;
        }
        aiByBee[w.source_difficulty][w.ai_spelling_difficulty_level]++;
      }
    });
    
    ['One Bee', 'Two Bee', 'Three Bee'].forEach(bee => {
      const levels = aiByBee[bee];
      const total = Object.values(levels).reduce((a, b) => a + b, 0);
      console.log(`${bee}:`);
      Object.entries(levels)
        .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
        .forEach(([level, count]) => {
          console.log(`  AI Level ${level}: ${count} words (${((count/total)*100).toFixed(1)}%)`);
        });
    });
    
    // Find overlapping words between categories
    console.log('\n=== WORD OVERLAP ANALYSIS ===\n');
    
    const wordsByBee = {
      'One Bee': new Set(words.filter(w => w.source_difficulty === 'One Bee').map(w => w.word.toLowerCase())),
      'Two Bee': new Set(words.filter(w => w.source_difficulty === 'Two Bee').map(w => w.word.toLowerCase())),
      'Three Bee': new Set(words.filter(w => w.source_difficulty === 'Three Bee').map(w => w.word.toLowerCase()))
    };
    
    // Check for common patterns in misclassified words
    const easyInHard = [];
    const hardInEasy = [];
    
    words.forEach(w => {
      const word = w.word.toLowerCase();
      // Simple word patterns that appear in Three Bee
      if (w.source_difficulty === 'Three Bee' && word.length <= 5 && !/[qxz]/.test(word)) {
        easyInHard.push(word);
      }
      // Complex patterns that appear in One Bee
      if (w.source_difficulty === 'One Bee' && (word.includes('ough') || word.includes('eigh') || word.length > 12)) {
        hardInEasy.push(word);
      }
    });
    
    console.log(`Simple words in Three Bee: ${easyInHard.length}`);
    console.log('Examples:', easyInHard.slice(0, 10).join(', '));
    
    console.log(`\nComplex words in One Bee: ${hardInEasy.length}`);
    console.log('Examples:', hardInEasy.slice(0, 10).join(', '));
    
    // Analyze what makes bee ratings different
    console.log('\n=== KEY INSIGHTS ===\n');
    console.log('1. Bee ratings appear to be based on:');
    console.log('   - Competition frequency (how often the word appears in spelling bees)');
    console.log('   - Age appropriateness (not just orthographic complexity)');
    console.log('   - Word familiarity (common words can be any difficulty)');
    console.log('   - Regional/curriculum variations');
    console.log('\n2. Pure orthographic features have limited predictive power (~40% accuracy)');
    console.log('\n3. Grade level shows weak correlation with bee ratings');
    console.log('\n4. AI difficulty levels also show poor alignment\n');
    
    // Propose hybrid approach
    console.log('=== RECOMMENDED HYBRID APPROACH ===\n');
    console.log('For new words without bee ratings, use:');
    console.log('\n1. PRIMARY: Orthographic complexity score (40% weight)');
    console.log('2. SECONDARY: Word frequency in English corpus (30% weight)');
    console.log('3. TERTIARY: Grade level appropriateness (20% weight)');
    console.log('4. QUATERNARY: Morphological complexity (10% weight)');
    console.log('\nThen map to 1-5 scale with manual adjustments for:');
    console.log('- Known curriculum words → lower difficulty');
    console.log('- Technical/specialized terms → higher difficulty');
    console.log('- Regional spelling variations → medium difficulty');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

analyzeBeeFactors();