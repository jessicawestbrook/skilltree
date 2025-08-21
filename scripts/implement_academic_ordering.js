const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Academic ordering mappings based on educational progression
const TOP_LEVEL_ORDERING = {
  'Mathematics': 0,
  'Natural Sciences': 10,
  'Applied Sciences': 20,
  'Computer Science': 30,
  'Languages': 40,
  'Humanities': 50,
  'Social Sciences': 60,
  'Technical Skills': 70,
  'Professional Skills': 80,
  'Creative Skills': 90,
  'Life Skills': 100,
  'Test Preparation and Assessment': 110
};

const MATHEMATICS_ORDERING = {
  'Early Math Concepts': 10,
  'Arithmetic Foundations': 20,
  'Elementary Algebra': 30,
  'Geometry': 40,
  'Statistics and Probability': 50,
  'Algebra': 60, // Intermediate Algebra
  'Discrete Mathematics': 70,
  'Calculus': 80,
  'Applied Mathematics': 90,
  'Abstract Algebra': 100
};

const LANGUAGES_ORDERING = {
  'Spanish': 10,
  'French': 20,
  'Italian': 30,
  'Portuguese': 40,
  'German': 50,
  'Mandarin Chinese': 60,
  'Japanese': 70,
  'Korean': 80,
  'Arabic': 90,
  'Russian': 100,
  'Latin': 110,
  'Ancient Greek': 120
};

const NATURAL_SCIENCES_ORDERING = {
  'Scientific Method': 10,
  'Physics': 20,
  'Chemistry': 30,
  'Biology': 40,
  'Earth Science': 50,
  'Environmental Science': 60,
  'Astronomy': 70
};

const COMPUTER_SCIENCE_ORDERING = {
  'Computer Literacy': 10,
  'Introduction to Programming': 20,
  'Programming Fundamentals': 30,
  'Data Structures': 40,
  'Algorithms': 50,
  'Software Engineering': 60,
  'Database Systems': 70,
  'Computer Networks': 80,
  'Artificial Intelligence': 90,
  'Cybersecurity': 100
};

const HUMANITIES_ORDERING = {
  'History': 10,
  'Philosophy': 20,
  'Literature': 30,
  'Language Arts': 40,
  'Art History': 50,
  'Religious Studies': 60,
  'Cultural Studies': 70
};

const SOCIAL_SCIENCES_ORDERING = {
  'Psychology': 10,
  'Sociology': 20,
  'Economics': 30,
  'Political Science': 40,
  'Anthropology': 50,
  'Geography': 60,
  'International Relations': 70
};

// Function to create backup before making changes
async function createBackup() {
  console.log('Creating backup of current display_order values...');
  
  try {
    // Get all current display_order values
    const { data: currentState, error: fetchError } = await supabase
      .from('skill_tree_nodes')
      .select('id, name, display_order, parent_id');
    
    if (fetchError) {
      console.error('Error fetching current state:', fetchError);
      return false;
    }
    
    // Save backup to file
    const fs = require('fs');
    const path = require('path');
    const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
    const backupPath = path.join(__dirname, `skill_tree_backup_${timestamp}.json`);
    
    fs.writeFileSync(backupPath, JSON.stringify(currentState, null, 2));
    console.log(`✅ Backup saved to: ${backupPath}`);
    console.log(`📊 Backed up ${currentState.length} nodes`);
    
    return true;
    
  } catch (error) {
    console.error('Error creating backup:', error);
    return false;
  }
}

// Function to update display_order for a specific set of nodes
async function updateDisplayOrder(parentName, orderMapping, description) {
  console.log(`\nUpdating ${description}...`);
  
  let successCount = 0;
  let errorCount = 0;
  
  for (const [nodeName, order] of Object.entries(orderMapping)) {
    try {
      let query = supabase
        .from('skill_tree_nodes')
        .update({ display_order: order })
        .eq('name', nodeName);
      
      // If we have a parent name, filter by parent as well
      if (parentName) {
        // First get the parent ID
        const { data: parentData, error: parentError } = await supabase
          .from('skill_tree_nodes')
          .select('id')
          .eq('name', parentName)
          .single();
        
        if (parentError || !parentData) {
          console.warn(`Warning: Parent '${parentName}' not found for '${nodeName}'`);
          continue;
        }
        
        query = query.eq('parent_id', parentData.id);
      } else {
        // Top-level nodes have parent_id = null
        query = query.is('parent_id', null);
      }
      
      const { data, error } = await query;
      
      if (error) {
        console.error(`Error updating '${nodeName}':`, error.message);
        errorCount++;
      } else {
        console.log(`✓ Updated '${nodeName}' to display_order: ${order}`);
        successCount++;
      }
    } catch (err) {
      console.error(`Exception updating '${nodeName}':`, err.message);
      errorCount++;
    }
  }
  
  console.log(`${description} complete: ${successCount} updated, ${errorCount} errors`);
  return { successCount, errorCount };
}

// Function to verify current state
async function verifyCurrentState() {
  console.log('\nVerifying current state...');
  
  // Check top-level categories
  const { data: topLevel, error: topError } = await supabase
    .from('skill_tree_nodes')
    .select('name, display_order')
    .is('parent_id', null)
    .order('display_order', { nullsLast: true });
  
  if (topError) {
    console.error('Error fetching top-level nodes:', topError);
    return;
  }
  
  console.log('\nTop-level categories (current order):');
  topLevel.forEach((node, index) => {
    console.log(`${index + 1}. ${node.name} (display_order: ${node.display_order})`);
  });
  
  // Check how many nodes have display_order set
  const { data: stats, error: statsError } = await supabase
    .from('skill_tree_nodes')
    .select('display_order');
  
  if (!statsError && stats) {
    const withOrder = stats.filter(n => n.display_order !== null).length;
    const withoutOrder = stats.filter(n => n.display_order === null).length;
    console.log(`\nOrdering statistics:`);
    console.log(`- Nodes with display_order: ${withOrder}`);
    console.log(`- Nodes without display_order: ${withoutOrder}`);
    console.log(`- Total nodes: ${stats.length}`);
  }
}

// Main execution function
async function implementAcademicOrdering() {
  console.log('🎯 Implementing Academic Ordering System');
  console.log('=====================================\n');
  
  try {
    // Step 1: Create backup
    const backupSuccess = await createBackup();
    if (!backupSuccess) {
      console.error('❌ Failed to create backup. Aborting operation.');
      return;
    }
    
    // Step 2: Verify current state
    await verifyCurrentState();
    
    // Step 3: Update top-level categories
    const topLevelResults = await updateDisplayOrder(
      null,
      TOP_LEVEL_ORDERING,
      'top-level categories'
    );
    
    // Step 4: Update Mathematics subcategories
    const mathResults = await updateDisplayOrder(
      'Mathematics',
      MATHEMATICS_ORDERING,
      'Mathematics subcategories'
    );
    
    // Step 5: Update Languages subcategories
    const languageResults = await updateDisplayOrder(
      'Languages',
      LANGUAGES_ORDERING,
      'Languages subcategories'
    );
    
    // Step 6: Update Natural Sciences subcategories
    const scienceResults = await updateDisplayOrder(
      'Natural Sciences',
      NATURAL_SCIENCES_ORDERING,
      'Natural Sciences subcategories'
    );
    
    // Step 7: Update Computer Science subcategories
    const csResults = await updateDisplayOrder(
      'Computer Science',
      COMPUTER_SCIENCE_ORDERING,
      'Computer Science subcategories'
    );
    
    // Step 8: Update Humanities subcategories
    const humanitiesResults = await updateDisplayOrder(
      'Humanities',
      HUMANITIES_ORDERING,
      'Humanities subcategories'
    );
    
    // Step 9: Update Social Sciences subcategories
    const socialResults = await updateDisplayOrder(
      'Social Sciences',
      SOCIAL_SCIENCES_ORDERING,
      'Social Sciences subcategories'
    );
    
    // Step 10: Verify final state
    console.log('\n' + '='.repeat(50));
    console.log('📊 FINAL VERIFICATION');
    console.log('='.repeat(50));
    await verifyCurrentState();
    
    // Summary
    const totalUpdated = topLevelResults.successCount + mathResults.successCount + 
                        languageResults.successCount + scienceResults.successCount +
                        csResults.successCount + humanitiesResults.successCount +
                        socialResults.successCount;
    
    const totalErrors = topLevelResults.errorCount + mathResults.errorCount + 
                       languageResults.errorCount + scienceResults.errorCount +
                       csResults.errorCount + humanitiesResults.errorCount +
                       socialResults.errorCount;
    
    console.log('\n' + '='.repeat(50));
    console.log('🎉 ACADEMIC ORDERING IMPLEMENTATION COMPLETE');
    console.log('='.repeat(50));
    console.log(`✅ Total nodes updated: ${totalUpdated}`);
    console.log(`❌ Total errors: ${totalErrors}`);
    
    if (totalErrors === 0) {
      console.log('\n🌟 All updates completed successfully!');
      console.log('The skill tree now follows proper academic progression.');
    } else {
      console.log(`\n⚠️  Some updates failed. Please review the errors above.`);
    }
    
  } catch (error) {
    console.error('❌ Fatal error during implementation:', error);
    console.log('\n💾 You can restore from backup if needed:');
    console.log('   - skill_tree_nodes_bkp (main backup)');
    console.log('   - Or timestamped backup table created today');
  }
}

// Run the implementation
if (require.main === module) {
  implementAcademicOrdering()
    .then(() => {
      console.log('\n🏁 Script execution completed.');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Script failed:', error);
      process.exit(1);
    });
}

module.exports = {
  implementAcademicOrdering,
  TOP_LEVEL_ORDERING,
  MATHEMATICS_ORDERING,
  LANGUAGES_ORDERING,
  NATURAL_SCIENCES_ORDERING,
  COMPUTER_SCIENCE_ORDERING,
  HUMANITIES_ORDERING,
  SOCIAL_SCIENCES_ORDERING
};