const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

// Words that were likely incorrectly filtered and should receive pronunciations
const LEGITIMATE_WORDS = [
  'overweening',
  'peregrination', 
  'preserving',
  'professionally',
  'proffered',
  'proselytiser',
  'proselytizer',
  'puerilely',
  'pulverised',
  'pulverized',
  'puttering',
  'redingote',
  'referred',
  'refrigerated',
  'reverberant',
  'ringing',
  'singing',
  'smoldering',
  'smouldering',
  'unacknowledged',
  'understanding',
  'unexpectedly',
  'unilaterally',
  'veered',
  'versiera',
  'vertere'
];

// Obviously combined words to keep filtered
const DEFINITELY_COMBINED = [
  'nostrilsthe',
  'nulliusnoun',
  'obligeviscount',
  'obviouspulse',
  'oceaniancharitable',
  'ogivalnoun',
  'referralaerials',
  'reiterateremorseful',
  'renvoinoun',
  'rescissiblejungian',
  'rescissiblereveille',
  'resuscitateretina',
  'revelationarithmetic',
  'runesancestors',
  'ryeland',
  'ryelanddomesticity',
  'sherifftarry',
  'shrivellimbering',
  'shutterscorner',
  'solderinterim',
  'solitairedishevel',
  'soppinesssousaphone'
];

// Words with invalid characters (accents) to keep filtered
const INVALID_CHARACTERS = [
  'pâtissier',
  'regnalattaché',
  'résumé',
  'reykjavík',
  'soirée',
  'soupçon',
  'velouté'
];

async function reviewFilteredWords() {
  try {
    console.log('🔍 REVIEWING FILTERED WORDS\n');
    
    // Load the analysis results
    const analysis = JSON.parse(fs.readFileSync('scripts/word_analysis_results.json', 'utf8'));
    
    console.log('=== ANALYSIS SUMMARY ===');
    console.log(`Total invalid words: ${analysis.invalid.length}`);
    console.log(`- Combined words: ${analysis.invalid.filter(w => w.reason === 'combined-word').length}`);
    console.log(`- Likely combined words: ${analysis.invalid.filter(w => w.reason === 'likely-combined-word').length}`);
    console.log(`- Invalid characters: ${analysis.invalid.filter(w => w.reason === 'invalid-characters').length}`);
    console.log(`- Nonsense words: ${analysis.invalid.filter(w => w.reason === 'nonsense-word').length}`);
    
    // Categorize the invalid words
    const legitimateToRestore = [];
    const properlyFiltered = [];
    const needsManualReview = [];
    
    for (const word of analysis.invalid) {
      if (LEGITIMATE_WORDS.includes(word.word)) {
        legitimateToRestore.push(word);
      } else if (DEFINITELY_COMBINED.includes(word.word) || 
                 INVALID_CHARACTERS.includes(word.word) || 
                 word.reason === 'nonsense-word') {
        properlyFiltered.push(word);
      } else {
        needsManualReview.push(word);
      }
    }
    
    console.log('\n=== CATEGORIZATION RESULTS ===');
    console.log(`✅ Legitimate words to restore: ${legitimateToRestore.length}`);
    console.log(`❌ Properly filtered words: ${properlyFiltered.length}`);
    console.log(`🤔 Need manual review: ${needsManualReview.length}`);
    
    // Show legitimate words to restore
    if (legitimateToRestore.length > 0) {
      console.log('\n📝 LEGITIMATE WORDS TO RESTORE:');
      legitimateToRestore.forEach(word => {
        console.log(`   - "${word.word}" (was filtered as: ${word.reason})`);
      });
    }
    
    // Show words needing manual review
    if (needsManualReview.length > 0) {
      console.log('\n🤔 WORDS NEEDING MANUAL REVIEW:');
      needsManualReview.forEach(word => {
        console.log(`   - "${word.word}" (${word.reason})`);
      });
    }
    
    // Generate detailed report
    const report = {
      summary: {
        totalFiltered: analysis.invalid.length,
        legitimateToRestore: legitimateToRestore.length,
        properlyFiltered: properlyFiltered.length,
        needsManualReview: needsManualReview.length
      },
      legitimateWords: legitimateToRestore.map(w => ({
        word: w.word,
        id: w.id,
        originalReason: w.reason
      })),
      properlyFiltered: properlyFiltered.map(w => ({
        word: w.word,
        reason: w.reason
      })),
      needsManualReview: needsManualReview.map(w => ({
        word: w.word,
        id: w.id,
        reason: w.reason
      }))
    };
    
    fs.writeFileSync('scripts/filtered_words_review.json', JSON.stringify(report, null, 2));
    console.log('\n📄 Detailed report saved to scripts/filtered_words_review.json');
    
    return report;
    
  } catch (error) {
    console.error('Review failed:', error);
    return null;
  }
}

// Run if called directly
if (require.main === module) {
  reviewFilteredWords()
    .then(report => {
      if (report) {
        console.log('\n🎯 RECOMMENDATIONS:');
        if (report.legitimateWords.length > 0) {
          console.log(`1. Restore pronunciations for ${report.legitimateWords.length} legitimate words`);
        }
        if (report.needsManualReview.length > 0) {
          console.log(`2. Manually review ${report.needsManualReview.length} borderline cases`);
        }
        console.log('3. Keep current filtering for obviously combined/invalid words');
      }
    })
    .catch(error => {
      console.error('Process failed:', error);
      process.exit(1);
    });
}

module.exports = { reviewFilteredWords, LEGITIMATE_WORDS };