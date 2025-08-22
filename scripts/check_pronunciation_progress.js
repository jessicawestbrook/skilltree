const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

async function checkProgress() {
  try {
    console.log('=== PRONUNCIATION UPDATE PROGRESS CHECK ===');
    console.log(`Checked at: ${new Date().toISOString()}\n`);
    
    // Check current database state
    const { count: totalWords, error: totalError } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true });
    
    if (totalError) {
      console.error('Error getting total count:', totalError);
      return;
    }
    
    // Check missing pronunciations
    const { count: missingCount, error: missingError } = await supabase
      .from('spelling_words')
      .select('*', { count: 'exact', head: true })
      .or('pronunciation_guide.is.null,pronunciation_guide.eq.');
    
    if (missingError) {
      console.error('Error getting missing count:', missingError);
      return;
    }
    
    // Check recent progress files
    const progressFiles = fs.readdirSync('scripts')
      .filter(file => file.startsWith('pronunciation_progress_'))
      .map(file => ({
        file: file,
        path: path.join('scripts', file),
        timestamp: fs.statSync(path.join('scripts', file)).mtime
      }))
      .sort((a, b) => b.timestamp - a.timestamp);
    
    console.log(`Database Status:`);
    console.log(`- Total spelling words: ${totalWords}`);
    console.log(`- Words missing pronunciations: ${missingCount}`);
    console.log(`- Words with pronunciations: ${totalWords - missingCount}`);
    console.log(`- Completion percentage: ${Math.round(((totalWords - missingCount) / totalWords) * 100)}%`);
    
    if (progressFiles.length > 0) {
      console.log(`\nLatest Progress File: ${progressFiles[0].file}`);
      try {
        const latestProgress = JSON.parse(fs.readFileSync(progressFiles[0].path, 'utf8'));
        console.log(`- Timestamp: ${latestProgress.timestamp}`);
        console.log(`- Batch: ${latestProgress.batchIndex}/${latestProgress.totalBatches}`);
        console.log(`- Words processed: ${latestProgress.processed}/${latestProgress.total}`);
        console.log(`- Success rate: ${Math.round((latestProgress.successful / latestProgress.processed) * 100)}%`);
        console.log(`- Progress: ${latestProgress.progress_percentage}%`);
      } catch (error) {
        console.log('- Could not read progress file details');
      }
    }
    
    console.log(`\nProgress files found: ${progressFiles.length}`);
    if (progressFiles.length > 5) {
      console.log('(Showing most recent 5)');
    }
    
    progressFiles.slice(0, 5).forEach(pf => {
      console.log(`- ${pf.file} (${pf.timestamp.toLocaleString()})`);
    });
    
    // Show some recent pronunciation examples
    console.log('\nRecent pronunciation updates (last 10):');
    const { data: recentUpdates, error: recentError } = await supabase
      .from('spelling_words')
      .select('word, pronunciation_guide, updated_at')
      .not('pronunciation_guide', 'is', null)
      .neq('pronunciation_guide', '')
      .order('updated_at', { ascending: false })
      .limit(10);
    
    if (!recentError && recentUpdates) {
      recentUpdates.forEach(update => {
        console.log(`- ${update.word} -> ${update.pronunciation_guide}`);
      });
    }
    
  } catch (error) {
    console.error('Progress check failed:', error);
  }
}

// Run the progress check
checkProgress();