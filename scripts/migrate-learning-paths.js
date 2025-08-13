const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');
const path = require('path');

// Load .env.local file
dotenv.config({ path: path.join(__dirname, '..', '.env.local') });

console.log('🚀 NeuroQuest Learning Paths Migration Tool\n');
console.log('========================================\n');

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('❌ Missing Supabase environment variables!');
  process.exit(1);
}

console.log('✅ Environment variables loaded successfully\n');

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Learning paths data
const learningPaths = [
  {
    name: 'Beginner\'s Journey',
    icon: 'MapPin',
    description: 'Start your knowledge quest with foundational concepts',
    nodes: ['symbols-meaning', 'quantity-concept', 'self-care', 'sound-patterns']
  },
  {
    name: 'Math Master',
    icon: 'Brain',
    description: 'Master mathematics from basics to advanced calculus',
    nodes: ['quantity-concept', 'number-systems', 'operations', 'algebra-thinking', 'calculus-parent']
  },
  {
    name: 'Science Explorer',
    icon: 'Trophy',
    description: 'Explore the scientific world from method to advanced physics',
    nodes: ['scientific-method', 'matter-energy', 'living-systems', 'forces-motion']
  },
  {
    name: 'Digital Native',
    icon: 'Home',
    description: 'Master digital skills and computer science',
    nodes: ['digital-literacy', 'programming-basics', 'algorithms-parent', 'arrays-lists', 'trees-graphs']
  },
  {
    name: 'Polyglot Path',
    icon: 'MessageSquare',
    description: 'Learn multiple languages and communication skills',
    nodes: ['written-expression', 'language-fundamentals', 'spanish', 'french', 'chinese']
  },
  {
    name: 'Life Skills',
    icon: 'Heart',
    description: 'Essential practical skills for everyday life',
    nodes: ['self-care', 'safety-awareness', 'cooking-fundamentals', 'money-management', 'basic-repairs']
  },
  {
    name: 'Creative Mind',
    icon: 'ChartBar',
    description: 'Develop communication and expression skills',
    nodes: ['visual-literacy', 'written-expression', 'digital-literacy', 'language-fundamentals', 'languages-parent']
  }
];

async function migrateLearningPaths() {
  console.log('📚 Starting learning paths migration to Supabase...\n');

  let totalPaths = 0;
  let totalPathNodes = 0;
  let failedPaths = 0;
  let failedPathNodes = 0;

  for (const pathData of learningPaths) {
    try {
      console.log(`📝 Migrating path: ${pathData.name}`);
      
      // Insert learning path
      const { data: pathResult, error: pathError } = await supabase
        .from('learning_paths')
        .insert([{
          name: pathData.name,
          description: pathData.description,
          icon_name: pathData.icon,
          created_at: new Date().toISOString()
        }])
        .select()
        .single();

      if (pathError) {
        console.error(`  ❌ Failed to insert path: ${pathError.message}`);
        failedPaths++;
        continue;
      }

      console.log(`  ✅ Created learning path: ${pathData.name}`);
      totalPaths++;

      // Insert nodes for this path
      for (let i = 0; i < pathData.nodes.length; i++) {
        const nodeId = pathData.nodes[i];
        
        try {
          const { error: nodeError } = await supabase
            .from('learning_path_nodes')
            .insert([{
              path_id: pathResult.id,
              node_id: nodeId,
              order_index: i,
              created_at: new Date().toISOString()
            }]);

          if (nodeError) {
            console.error(`    ❌ Failed to link node ${nodeId}: ${nodeError.message}`);
            failedPathNodes++;
          } else {
            console.log(`    ✅ Linked node: ${nodeId} (position ${i + 1})`);
            totalPathNodes++;
          }
        } catch (err) {
          console.error(`    ❌ Error linking node ${nodeId}: ${err.message}`);
          failedPathNodes++;
        }
      }
    } catch (err) {
      console.error(`  ❌ Error processing path ${pathData.name}: ${err.message}`);
      failedPaths++;
    }
  }

  console.log('\n========================================');
  console.log('📊 Migration Summary:');
  console.log(`✅ Learning paths created: ${totalPaths}`);
  console.log(`✅ Path nodes linked: ${totalPathNodes}`);
  console.log(`❌ Failed paths: ${failedPaths}`);
  console.log(`❌ Failed path nodes: ${failedPathNodes}`);
  console.log('========================================\n');

  // Verify the migration
  console.log('🔍 Verifying migration...');
  const { count: pathCount, error: pathCountError } = await supabase
    .from('learning_paths')
    .select('*', { count: 'exact', head: true });

  const { count: nodeCount, error: nodeCountError } = await supabase
    .from('learning_path_nodes')
    .select('*', { count: 'exact', head: true });

  if (!pathCountError && pathCount !== null) {
    console.log(`✅ Total learning paths in database: ${pathCount}`);
  }
  if (!nodeCountError && nodeCount !== null) {
    console.log(`✅ Total path nodes in database: ${nodeCount}`);
  }
}

// Run the migration
migrateLearningPaths()
  .then(() => {
    console.log('\n✨ Learning paths migration completed successfully!');
    process.exit(0);
  })
  .catch((err) => {
    console.error('\n❌ Migration failed:', err.message);
    process.exit(1);
  });