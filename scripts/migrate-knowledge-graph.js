const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');
const path = require('path');

// Load .env.local file
dotenv.config({ path: path.join(__dirname, '..', '.env.local') });

// Check environment variables
console.log('🚀 NeuroQuest Knowledge Graph Migration Tool\n');
console.log('========================================\n');

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing Supabase environment variables!');
  console.error('Please ensure your .env.local file contains:');
  console.error('  NEXT_PUBLIC_SUPABASE_URL=your_supabase_url');
  console.error('  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key\n');
  process.exit(1);
}

console.log('✅ Environment variables loaded successfully\n');

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Import the knowledge graph data
const hierarchicalKnowledgeGraph = {
  foundation: {
    communication: [
      { id: 'symbols-meaning', name: 'Symbols & Meaning', prereqs: [], category: 'foundation', domain: 'communication', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'sound-patterns', name: 'Sound Patterns', prereqs: [], category: 'foundation', domain: 'communication', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'visual-literacy', name: 'Visual Literacy', prereqs: ['symbols-meaning'], category: 'foundation', domain: 'communication', difficulty: 1, points: 75, level: 0, isParent: false },
      { id: 'written-expression', name: 'Written Expression', prereqs: ['symbols-meaning'], category: 'foundation', domain: 'communication', difficulty: 2, points: 100, level: 0, isParent: false }
    ],
    quantitative: [
      { id: 'quantity-concept', name: 'Quantity & Counting', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'patterns-sequences', name: 'Pattern Recognition', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'spatial-reasoning', name: 'Spatial Reasoning', prereqs: [], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75, level: 0, isParent: false },
      { id: 'measurement-basics', name: 'Basic Measurement', prereqs: ['quantity-concept'], category: 'foundation', domain: 'quantitative', difficulty: 2, points: 75, level: 0, isParent: false }
    ],
    practical: [
      { id: 'self-care', name: 'Personal Care', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 25, level: 0, isParent: false },
      { id: 'tool-use-basic', name: 'Basic Tool Use', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50, level: 0, isParent: false },
      { id: 'safety-awareness', name: 'Safety Awareness', prereqs: [], category: 'foundation', domain: 'practical', difficulty: 1, points: 50, level: 0, isParent: false }
    ]
  },
  fundamentals: {
    mathematics: [
      { id: 'number-systems', name: 'Number Systems', prereqs: ['quantity-concept'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'operations', name: 'Math Operations', prereqs: ['number-systems'], category: 'fundamentals', domain: 'mathematics', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'algebra-thinking', name: 'Algebraic Thinking', prereqs: ['operations'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'geometric-thinking', name: 'Geometric Thinking', prereqs: ['spatial-reasoning'], category: 'fundamentals', domain: 'mathematics', difficulty: 3, points: 150, level: 0, isParent: false }
    ],
    science: [
      { id: 'scientific-method', name: 'Scientific Method', prereqs: [], category: 'fundamentals', domain: 'science', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'matter-energy', name: 'Matter & Energy', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'living-systems', name: 'Living Systems', prereqs: ['scientific-method'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150, level: 0, isParent: false },
      { id: 'forces-motion', name: 'Forces & Motion', prereqs: ['matter-energy'], category: 'fundamentals', domain: 'science', difficulty: 3, points: 150, level: 0, isParent: false }
    ],
    practical_skills: [
      { id: 'cooking-fundamentals', name: 'Cooking Basics', prereqs: ['measurement-basics', 'safety-awareness'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'digital-literacy', name: 'Digital Literacy', prereqs: [], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'money-management', name: 'Money Management', prereqs: ['operations'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false },
      { id: 'basic-repairs', name: 'Basic Repairs', prereqs: ['tool-use-basic'], category: 'fundamentals', domain: 'practical', difficulty: 2, points: 100, level: 0, isParent: false }
    ]
  },
  domains: {
    mathematics: [
      {
        id: 'calculus-parent',
        name: 'Calculus',
        prereqs: ['algebra-thinking'],
        category: 'domains',
        domain: 'mathematics',
        difficulty: 4,
        points: 50,
        level: 0,
        isParent: true,
        subnodes: [
          { id: 'limits', name: 'Limits & Continuity', parentId: 'calculus-parent', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'derivatives', name: 'Derivatives', parentId: 'calculus-parent', prereqs: ['limits'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'integrals', name: 'Integrals', parentId: 'calculus-parent', prereqs: ['derivatives'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'differential-equations', name: 'Differential Equations', parentId: 'calculus-parent', prereqs: ['integrals'], category: 'domains', domain: 'mathematics', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'multivariable-calc', name: 'Multivariable Calculus', parentId: 'calculus-parent', prereqs: ['integrals'], category: 'domains', domain: 'mathematics', difficulty: 5, points: 300, level: 1, isParent: false }
        ]
      },
      {
        id: 'statistics-parent',
        name: 'Statistics & Probability',
        prereqs: ['algebra-thinking'],
        category: 'domains',
        domain: 'mathematics',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        subnodes: [
          { id: 'descriptive-stats', name: 'Descriptive Statistics', parentId: 'statistics-parent', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 2, points: 125, level: 1, isParent: false },
          { id: 'probability-theory', name: 'Probability Theory', parentId: 'statistics-parent', prereqs: ['descriptive-stats'], category: 'domains', domain: 'mathematics', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'hypothesis-testing', name: 'Hypothesis Testing', parentId: 'statistics-parent', prereqs: ['probability-theory'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'regression-analysis', name: 'Regression Analysis', parentId: 'statistics-parent', prereqs: ['hypothesis-testing'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 1, isParent: false },
          { id: 'bayesian-stats', name: 'Bayesian Statistics', parentId: 'statistics-parent', prereqs: ['probability-theory'], category: 'domains', domain: 'mathematics', difficulty: 5, points: 250, level: 1, isParent: false }
        ]
      },
      { id: 'linear-systems', name: 'Linear Algebra', prereqs: ['algebra-thinking'], category: 'domains', domain: 'mathematics', difficulty: 4, points: 200, level: 0, isParent: false }
    ],
    computer_science: [
      { id: 'programming-basics', name: 'Programming Fundamentals', prereqs: ['digital-literacy'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150, level: 0, isParent: false },
      {
        id: 'algorithms-parent',
        name: 'Algorithms & Data Structures',
        prereqs: ['programming-basics'],
        category: 'domains',
        domain: 'computer_science',
        difficulty: 4,
        points: 50,
        level: 0,
        isParent: true,
        subnodes: [
          { id: 'arrays-lists', name: 'Arrays & Lists', parentId: 'algorithms-parent', prereqs: ['programming-basics'], category: 'domains', domain: 'computer_science', difficulty: 2, points: 100, level: 1, isParent: false },
          { id: 'trees-graphs', name: 'Trees & Graphs', parentId: 'algorithms-parent', prereqs: ['arrays-lists'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 175, level: 1, isParent: false },
          { id: 'sorting-algorithms', name: 'Sorting Algorithms', parentId: 'algorithms-parent', prereqs: ['arrays-lists'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'search-algorithms', name: 'Search Algorithms', parentId: 'algorithms-parent', prereqs: ['trees-graphs'], category: 'domains', domain: 'computer_science', difficulty: 3, points: 150, level: 1, isParent: false },
          { id: 'dynamic-programming', name: 'Dynamic Programming', parentId: 'algorithms-parent', prereqs: ['sorting-algorithms'], category: 'domains', domain: 'computer_science', difficulty: 5, points: 250, level: 1, isParent: false },
          { id: 'graph-algorithms', name: 'Graph Algorithms', parentId: 'algorithms-parent', prereqs: ['trees-graphs'], category: 'domains', domain: 'computer_science', difficulty: 4, points: 200, level: 1, isParent: false }
        ]
      }
    ],
    languages: [
      { id: 'language-fundamentals', name: 'Language Learning Basics', prereqs: ['written-expression'], category: 'domains', domain: 'languages', difficulty: 2, points: 100, level: 0, isParent: false },
      {
        id: 'languages-parent',
        name: 'World Languages',
        prereqs: ['language-fundamentals'],
        category: 'domains',
        domain: 'languages',
        difficulty: 3,
        points: 50,
        level: 0,
        isParent: true,
        subnodes: [
          { id: 'spanish', name: 'Spanish', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200, level: 1, isParent: false },
          { id: 'french', name: 'French', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 3, points: 200, level: 1, isParent: false },
          { id: 'german', name: 'German', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 4, points: 225, level: 1, isParent: false },
          { id: 'chinese', name: 'Chinese (Mandarin)', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300, level: 1, isParent: false },
          { id: 'japanese', name: 'Japanese', parentId: 'languages-parent', prereqs: ['language-fundamentals'], category: 'domains', domain: 'languages', difficulty: 5, points: 300, level: 1, isParent: false }
        ]
      }
    ]
  },
  mastery: [
    { id: 'quantum-computing', name: 'Quantum Computing', prereqs: ['quantum-mechanics', 'algorithms-parent'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500, level: 0, isParent: false },
    { id: 'artificial-general-intelligence', name: 'AGI', prereqs: ['machine-learning-parent'], category: 'mastery', domain: 'advanced', difficulty: 6, points: 500, level: 0, isParent: false }
  ]
};

async function migrateKnowledgeGraph() {
  console.log('📊 Starting knowledge graph migration to Supabase...\n');

  let totalNodes = 0;
  let totalPrereqs = 0;
  let failedNodes = 0;
  let failedPrereqs = 0;

  // Process all nodes first (without prerequisites)
  console.log('📝 Migrating nodes...\n');
  
  for (const [categoryName, categoryData] of Object.entries(hierarchicalKnowledgeGraph)) {
    if (typeof categoryData === 'object') {
      if (Array.isArray(categoryData)) {
        // Process array directly (like mastery)
        for (const node of categoryData) {
          await insertNode(node);
        }
      } else {
        // Process nested domains
        for (const [domainName, domainNodes] of Object.entries(categoryData)) {
          for (const node of domainNodes) {
            await insertNode(node);
            
            // Process subnodes if they exist
            if (node.subnodes) {
              for (const subnode of node.subnodes) {
                await insertNode(subnode);
              }
            }
          }
        }
      }
    }
  }

  // Now process all prerequisites
  console.log('\n🔗 Migrating prerequisites...\n');
  
  for (const [categoryName, categoryData] of Object.entries(hierarchicalKnowledgeGraph)) {
    if (typeof categoryData === 'object') {
      if (Array.isArray(categoryData)) {
        for (const node of categoryData) {
          await insertPrerequisites(node);
        }
      } else {
        for (const [domainName, domainNodes] of Object.entries(categoryData)) {
          for (const node of domainNodes) {
            await insertPrerequisites(node);
            
            if (node.subnodes) {
              for (const subnode of node.subnodes) {
                await insertPrerequisites(subnode);
              }
            }
          }
        }
      }
    }
  }

  async function insertNode(node) {
    try {
      const nodeData = {
        id: node.id,
        name: node.name,
        domain: node.domain,
        difficulty: node.difficulty,
        points: node.points,
        level: node.level || 0,
        is_parent: node.isParent || false,
        parent_id: node.parentId || null,
        position_x: null, // Will be calculated by the app
        position_y: null,
        created_at: new Date().toISOString()
      };

      const { error } = await supabase
        .from('knowledge_nodes')
        .upsert([nodeData], { onConflict: 'id' });

      if (error) {
        console.error(`  ❌ Failed to insert node ${node.id}: ${error.message}`);
        failedNodes++;
      } else {
        console.log(`  ✅ Inserted node: ${node.name}`);
        totalNodes++;
      }
    } catch (err) {
      console.error(`  ❌ Error inserting node ${node.id}: ${err.message}`);
      failedNodes++;
    }
  }

  async function insertPrerequisites(node) {
    if (!node.prereqs || node.prereqs.length === 0) return;

    for (const prereqId of node.prereqs) {
      try {
        const prereqData = {
          node_id: node.id,
          prerequisite_id: prereqId,
          created_at: new Date().toISOString()
        };

        const { error } = await supabase
          .from('node_prerequisites')
          .upsert([prereqData], { onConflict: 'node_id,prerequisite_id' });

        if (error) {
          console.error(`  ❌ Failed to insert prerequisite ${prereqId} for ${node.id}: ${error.message}`);
          failedPrereqs++;
        } else {
          console.log(`  ✅ Linked prerequisite: ${prereqId} → ${node.id}`);
          totalPrereqs++;
        }
      } catch (err) {
        console.error(`  ❌ Error inserting prerequisite: ${err.message}`);
        failedPrereqs++;
      }
    }
  }

  console.log('\n========================================');
  console.log('📊 Migration Summary:');
  console.log(`✅ Nodes inserted: ${totalNodes}`);
  console.log(`✅ Prerequisites linked: ${totalPrereqs}`);
  console.log(`❌ Failed nodes: ${failedNodes}`);
  console.log(`❌ Failed prerequisites: ${failedPrereqs}`);
  console.log('========================================\n');

  // Verify the migration
  console.log('🔍 Verifying migration...');
  const { count: nodeCount, error: nodeError } = await supabase
    .from('knowledge_nodes')
    .select('*', { count: 'exact', head: true });

  const { count: prereqCount, error: prereqError } = await supabase
    .from('node_prerequisites')
    .select('*', { count: 'exact', head: true });

  if (!nodeError && nodeCount !== null) {
    console.log(`✅ Total nodes in database: ${nodeCount}`);
  }
  if (!prereqError && prereqCount !== null) {
    console.log(`✅ Total prerequisites in database: ${prereqCount}`);
  }
}

// Run the migration
migrateKnowledgeGraph()
  .then(() => {
    console.log('\n✨ Knowledge graph migration completed successfully!');
    process.exit(0);
  })
  .catch((err) => {
    console.error('\n❌ Migration failed:', err.message);
    process.exit(1);
  });