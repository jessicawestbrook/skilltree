const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function analyzeSkillTreeOrdering() {
  console.log('=== SKILL TREE ORDERING ANALYSIS ===\n');

  try {
    // 1. First, let's examine the table structure
    console.log('1. EXAMINING TABLE STRUCTURE:');
    const { data: columns, error: schemaError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .limit(1);
    
    if (schemaError) {
      console.error('Error getting schema:', schemaError);
      return;
    }

    if (columns && columns.length > 0) {
      console.log('Table columns:', Object.keys(columns[0]));
    }

    // 2. Find the root node
    console.log('\n2. FINDING ROOT NODE:');
    const { data: rootNodes, error: rootError } = await supabase
      .from('skill_tree_nodes')
      .select('*')
      .is('parent_id', null);

    if (rootError) {
      console.error('Error finding root:', rootError);
      return;
    }

    console.log('Root nodes found:', rootNodes?.length || 0);
    if (rootNodes && rootNodes.length > 0) {
      rootNodes.forEach(node => {
        console.log(`- ${node.name} (ID: ${node.id})`);
      });
    }

    // 3. Get top-level categories (direct children of root)
    console.log('\n3. TOP-LEVEL CATEGORIES:');
    let rootId = null;
    if (rootNodes && rootNodes.length > 0) {
      rootId = rootNodes[0].id;
      
      const { data: topCategories, error: topError } = await supabase
        .from('skill_tree_nodes')
        .select('*')
        .eq('parent_id', rootId)
        .order('id', { ascending: true });

      if (topError) {
        console.error('Error getting top categories:', topError);
        return;
      }

      console.log(`Found ${topCategories?.length || 0} top-level categories:`);
      if (topCategories) {
        topCategories.forEach((cat, index) => {
          console.log(`${index + 1}. ${cat.name} (ID: ${cat.id})`);
        });
      }

      // 4. Check for ordering fields
      console.log('\n4. CHECKING FOR ORDERING FIELDS:');
      if (topCategories && topCategories.length > 0) {
        const sample = topCategories[0];
        const orderingFields = Object.keys(sample).filter(key => 
          key.toLowerCase().includes('order') || 
          key.toLowerCase().includes('sort') ||
          key.toLowerCase().includes('sequence') ||
          key.toLowerCase().includes('position')
        );
        
        if (orderingFields.length > 0) {
          console.log('Potential ordering fields found:', orderingFields);
          
          // Show ordering field values for top categories
          console.log('\nOrdering field values for top categories:');
          topCategories.forEach(cat => {
            const orderingInfo = orderingFields.map(field => `${field}: ${cat[field]}`).join(', ');
            console.log(`- ${cat.name}: ${orderingInfo}`);
          });
        } else {
          console.log('No explicit ordering fields found in the table structure.');
          console.log('Categories appear to be ordered by ID or creation time.');
        }
      }

      // 5. Analyze specific subject areas
      console.log('\n5. ANALYZING SPECIFIC SUBJECT AREAS:');
      
      // Look for Languages category
      const languagesCategory = topCategories?.find(cat => 
        cat.name.toLowerCase().includes('language') || 
        cat.name.toLowerCase().includes('linguistic')
      );
      
      if (languagesCategory) {
        console.log(`\nFOUND LANGUAGES CATEGORY: ${languagesCategory.name}`);
        await analyzeSubcategory(languagesCategory.id, languagesCategory.name, 2);
      }

      // Look for Mathematics category
      const mathCategory = topCategories?.find(cat => 
        cat.name.toLowerCase().includes('math') || 
        cat.name.toLowerCase().includes('quantitative')
      );
      
      if (mathCategory) {
        console.log(`\nFOUND MATHEMATICS CATEGORY: ${mathCategory.name}`);
        await analyzeSubcategory(mathCategory.id, mathCategory.name, 2);
      }

      // Look for Science category
      const scienceCategory = topCategories?.find(cat => 
        cat.name.toLowerCase().includes('science') || 
        cat.name.toLowerCase().includes('natural')
      );
      
      if (scienceCategory) {
        console.log(`\nFOUND SCIENCE CATEGORY: ${scienceCategory.name}`);
        await analyzeSubcategory(scienceCategory.id, scienceCategory.name, 2);
      }

      // 6. Look for problematic ordering examples
      console.log('\n6. IDENTIFYING PROBLEMATIC ORDERING EXAMPLES:');
      await identifyOrderingProblems(topCategories);
    }

  } catch (error) {
    console.error('Error in analysis:', error);
  }
}

async function analyzeSubcategory(parentId, parentName, depth = 1, maxDepth = 3) {
  if (depth > maxDepth) return;

  const { data: children, error } = await supabase
    .from('skill_tree_nodes')
    .select('*')
    .eq('parent_id', parentId)
    .order('id', { ascending: true });

  if (error) {
    console.error(`Error getting children of ${parentName}:`, error);
    return;
  }

  if (children && children.length > 0) {
    const indent = '  '.repeat(depth);
    console.log(`${indent}Children of ${parentName} (${children.length} items):`);
    
    children.forEach((child, index) => {
      console.log(`${indent}${index + 1}. ${child.name} (ID: ${child.id})`);
    });

    // If this is Languages, look for specific ordering issues
    if (parentName.toLowerCase().includes('language')) {
      await checkLanguageOrdering(children, indent);
    }

    // If this is Mathematics, look for progression issues
    if (parentName.toLowerCase().includes('math')) {
      await checkMathOrdering(children, indent);
    }
  }
}

async function checkLanguageOrdering(languages, indent = '') {
  console.log(`${indent}Language ordering analysis:`);
  
  const commonLanguages = ['spanish', 'french', 'german', 'italian', 'portuguese'];
  const ancientLanguages = ['latin', 'greek', 'ancient', 'classical'];
  
  languages.forEach((lang, index) => {
    const name = lang.name.toLowerCase();
    const isCommon = commonLanguages.some(common => name.includes(common));
    const isAncient = ancientLanguages.some(ancient => name.includes(ancient));
    
    if (isAncient && index < languages.length / 2) {
      console.log(`${indent}⚠️  POTENTIAL ISSUE: "${lang.name}" appears early (position ${index + 1}) - ancient languages should typically come after modern ones`);
    }
    
    if (isCommon && index > languages.length / 2) {
      console.log(`${indent}⚠️  POTENTIAL ISSUE: "${lang.name}" appears late (position ${index + 1}) - common languages should typically come first`);
    }
  });
}

async function checkMathOrdering(mathTopics, indent = '') {
  console.log(`${indent}Mathematics ordering analysis:`);
  
  const basicMath = ['arithmetic', 'basic', 'elementary', 'addition', 'subtraction', 'multiplication', 'division'];
  const intermediateMath = ['algebra', 'geometry', 'trigonometry', 'statistics', 'probability'];
  const advancedMath = ['calculus', 'differential', 'integral', 'abstract', 'linear algebra', 'discrete', 'analysis'];
  
  mathTopics.forEach((topic, index) => {
    const name = topic.name.toLowerCase();
    const isBasic = basicMath.some(basic => name.includes(basic));
    const isIntermediate = intermediateMath.some(inter => name.includes(inter));
    const isAdvanced = advancedMath.some(adv => name.includes(adv));
    
    if (isAdvanced && index < mathTopics.length / 3) {
      console.log(`${indent}⚠️  POTENTIAL ISSUE: "${topic.name}" appears early (position ${index + 1}) - advanced topics should come after basics`);
    }
    
    if (isBasic && index > mathTopics.length / 2) {
      console.log(`${indent}⚠️  POTENTIAL ISSUE: "${topic.name}" appears late (position ${index + 1}) - basic topics should come first`);
    }

    // Check for specific problematic cases
    if (name.includes('abstract') && mathTopics.some(t => t.name.toLowerCase().includes('elementary'))) {
      const elementaryIndex = mathTopics.findIndex(t => t.name.toLowerCase().includes('elementary'));
      if (index < elementaryIndex) {
        console.log(`${indent}⚠️  MAJOR ISSUE: "Abstract" topics (${topic.name}) before "Elementary" topics - this violates academic progression`);
      }
    }
  });
}

async function identifyOrderingProblems(categories) {
  console.log('Scanning for common academic ordering problems...');
  
  // Check if there's a pattern to the current ordering
  console.log('\nCurrent top-level category order:');
  categories.forEach((cat, index) => {
    console.log(`${index + 1}. ${cat.name}`);
  });

  // Look for obvious ordering issues
  const academicOrder = ['language', 'math', 'science', 'social', 'arts', 'practical'];
  const currentOrder = categories.map(cat => cat.name.toLowerCase());

  console.log('\nOrder analysis:');
  console.log('- Current ordering appears to be based on:', 
    categories[0]?.id < categories[categories.length - 1]?.id ? 'ID/Creation time (ascending)' : 'Custom ordering');

  // Check total node count
  const { count, error } = await supabase
    .from('skill_tree_nodes')
    .select('*', { count: 'exact', head: true });

  if (!error) {
    console.log(`\nTotal nodes in skill tree: ${count}`);
  }
}

// Run the analysis
analyzeSkillTreeOrdering().then(() => {
  console.log('\n=== ANALYSIS COMPLETE ===');
  process.exit(0);
}).catch(error => {
  console.error('Analysis failed:', error);
  process.exit(1);
});