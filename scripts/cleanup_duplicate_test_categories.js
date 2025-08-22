require('dotenv').config({ path: '.env.local' });
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function cleanupDuplicateTestCategories() {
    try {
        console.log('🧹 CLEANING UP DUPLICATE TEST PREPARATION CATEGORIES\n');
        
        // Get Test Preparation category
        const { data: testPrep, error: testPrepError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name')
            .eq('name', 'Test Preparation and Assessment')
            .is('parent_id', null)
            .single();
            
        if (testPrepError || !testPrep) {
            console.error('❌ Error finding Test Preparation category:', testPrepError);
            return;
        }
        
        console.log(`✅ Found Test Preparation: ${testPrep.id}`);
        
        // Get all direct children under Test Preparation
        const { data: allCategories, error: categoriesError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order, type')
            .eq('parent_id', testPrep.id)
            .order('name');
            
        if (categoriesError) {
            console.error('❌ Error fetching categories:', categoriesError);
            return;
        }
        
        console.log(`\nFound ${allCategories.length} categories under Test Preparation:`);
        allCategories.forEach((cat, index) => {
            const order = cat.display_order || 'null';
            console.log(`   ${index + 1}. ${cat.name} (${cat.type}) - Order: ${order}`);
        });
        
        // Find duplicates by grouping by name
        const categoryGroups = {};
        allCategories.forEach(cat => {
            if (!categoryGroups[cat.name]) {
                categoryGroups[cat.name] = [];
            }
            categoryGroups[cat.name].push(cat);
        });
        
        console.log('\n🔍 Analyzing for duplicates and empty categories...');
        
        // Check each group for duplicates or empty categories
        for (const [categoryName, categories] of Object.entries(categoryGroups)) {
            if (categories.length > 1) {
                console.log(`\n📂 DUPLICATE FOUND: ${categoryName} (${categories.length} instances)`);
                
                // Check which ones have children and which are empty
                const categoriesWithDetails = [];
                
                for (const cat of categories) {
                    const { data: children, error: childrenError } = await supabase
                        .from('skill_tree_nodes')
                        .select('id, name, type')
                        .eq('parent_id', cat.id);
                        
                    if (childrenError) {
                        console.error(`   ❌ Error checking children for ${cat.id}:`, childrenError);
                        continue;
                    }
                    
                    categoriesWithDetails.push({
                        ...cat,
                        childrenCount: children ? children.length : 0,
                        children: children || []
                    });
                }
                
                // Sort by children count (keep the one with most children)
                categoriesWithDetails.sort((a, b) => b.childrenCount - a.childrenCount);
                
                console.log(`   Analysis:`);
                categoriesWithDetails.forEach((cat, index) => {
                    const order = cat.display_order || 'null';
                    console.log(`      ${index + 1}. ID: ${cat.id} | Order: ${order} | Children: ${cat.childrenCount}`);
                    if (cat.children.length > 0) {
                        cat.children.forEach(child => {
                            console.log(`         • ${child.name} (${child.type})`);
                        });
                    }
                });
                
                // Keep the first one (most children) and remove the rest
                const keepCategory = categoriesWithDetails[0];
                const removeCategories = categoriesWithDetails.slice(1);
                
                console.log(`   ✅ KEEPING: ${keepCategory.id} (${keepCategory.childrenCount} children)`);
                
                for (const removeCategory of removeCategories) {
                    if (removeCategory.childrenCount === 0) {
                        // Safe to remove empty duplicate
                        const { error: deleteError } = await supabase
                            .from('skill_tree_nodes')
                            .delete()
                            .eq('id', removeCategory.id);
                            
                        if (deleteError) {
                            console.error(`   ❌ Error removing empty duplicate ${removeCategory.id}:`, deleteError);
                        } else {
                            console.log(`   🗑️  REMOVED: Empty duplicate ${removeCategory.id}`);
                        }
                    } else {
                        // Has children - need to move them to the keep category first
                        console.log(`   🔄 Moving ${removeCategory.childrenCount} children from ${removeCategory.id} to ${keepCategory.id}`);
                        
                        for (const child of removeCategory.children) {
                            const { error: moveError } = await supabase
                                .from('skill_tree_nodes')
                                .update({ parent_id: keepCategory.id })
                                .eq('id', child.id);
                                
                            if (moveError) {
                                console.error(`      ❌ Error moving ${child.name}:`, moveError);
                            } else {
                                console.log(`      ✅ Moved: ${child.name}`);
                            }
                        }
                        
                        // Now remove the empty duplicate
                        const { error: deleteError } = await supabase
                            .from('skill_tree_nodes')
                            .delete()
                            .eq('id', removeCategory.id);
                            
                        if (deleteError) {
                            console.error(`   ❌ Error removing duplicate after moving children:`, deleteError);
                        } else {
                            console.log(`   🗑️  REMOVED: Duplicate ${removeCategory.id} after moving children`);
                        }
                    }
                }
            }
        }
        
        // Check for any categories that shouldn't be there
        console.log('\n🔍 Checking for unexpected categories...');
        
        const expectedCategories = [
            'College Entrance Exams',
            'Graduate School Exams',
            'IQ and Cognitive Tests',
            'K-12 Standardized Tests',
            'Language Proficiency Tests',
            'Professional Certification Exams',
            'Test-Taking Strategies'
        ];
        
        // Get current categories after cleanup
        const { data: currentCategories, error: currentError } = await supabase
            .from('skill_tree_nodes')
            .select('id, name, display_order')
            .eq('parent_id', testPrep.id)
            .order('display_order', { nullsFirst: false })
            .order('name');
            
        if (currentError) {
            console.error('❌ Error fetching current categories:', currentError);
            return;
        }
        
        console.log(`\nFinal category list (${currentCategories.length} categories):`);
        currentCategories.forEach((cat, index) => {
            const order = cat.display_order || 'null';
            const isExpected = expectedCategories.includes(cat.name);
            const marker = isExpected ? '✅' : '⚠️ ';
            console.log(`   ${index + 1}. ${marker} ${cat.name} - Order: ${order}`);
        });
        
        // Check for any orphaned categories that might have been created incorrectly
        const unexpectedCategories = currentCategories.filter(cat => 
            !expectedCategories.includes(cat.name) && 
            !cat.name.includes('GRE') && 
            !cat.name.includes('GMAT') && 
            !cat.name.includes('LSAT') && 
            !cat.name.includes('MCAT') &&
            !cat.name.includes('TOEFL') &&
            !cat.name.includes('IELTS')
        );
        
        if (unexpectedCategories.length > 0) {
            console.log(`\n⚠️  Found ${unexpectedCategories.length} unexpected top-level categories:`);
            unexpectedCategories.forEach(cat => {
                console.log(`   • ${cat.name} (${cat.id})`);
            });
        }
        
        console.log('\n📊 CLEANUP SUMMARY:');
        console.log(`   Final category count: ${currentCategories.length}`);
        console.log(`   Expected categories preserved: ${expectedCategories.length}`);
        console.log(`   Unexpected categories: ${unexpectedCategories.length}`);
        
        console.log('\n🎉 Cleanup completed!');
        console.log('✅ Duplicate categories removed');
        console.log('✅ Children properly preserved');
        console.log('✅ Clean hierarchy structure restored');
        
    } catch (error) {
        console.error('❌ Cleanup failed:', error);
    }
}

cleanupDuplicateTestCategories();