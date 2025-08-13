const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

// Create a Supabase client with the anon key
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

async function createTestUsers() {
  console.log('🌱 Creating test users for social features...\n');

  // Test user data
  const testUsers = [
    {
      email: 'alice.neuro.test@gmail.com',
      password: 'Test123!',
      profile: {
        username: 'alice_neuro',
        full_name: 'Alice Johnson',
        avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=alice',
        bio: 'Neuroscience enthusiast | PhD student | Love learning about the brain! 🧠'
      }
    },
    {
      email: 'bob.brain.test@gmail.com', 
      password: 'Test123!',
      profile: {
        username: 'bob_brain',
        full_name: 'Bob Smith',
        avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=bob',
        bio: 'Medical student exploring neurology | Coffee addict ☕'
      }
    },
    {
      email: 'charlie.cortex.test@gmail.com',
      password: 'Test123!',
      profile: {
        username: 'charlie_cortex',
        full_name: 'Charlie Davis',
        avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=charlie',
        bio: 'Cognitive science researcher | AI & Brain intersection'
      }
    }
  ];

  for (const userData of testUsers) {
    try {
      // Create user account
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: userData.email,
        password: userData.password,
        options: {
          data: {
            username: userData.profile.username,
            full_name: userData.profile.full_name
          }
        }
      });

      if (authError) {
        if (authError.message.includes('already registered')) {
          console.log(`⚠️  User ${userData.email} already exists`);
          
          // Try to update their profile instead
          const { data: existingUser } = await supabase.auth.signInWithPassword({
            email: userData.email,
            password: userData.password
          });
          
          if (existingUser?.user) {
            const { error: profileError } = await supabase
              .from('profiles')
              .upsert({
                id: existingUser.user.id,
                ...userData.profile,
                updated_at: new Date().toISOString()
              });
              
            if (!profileError) {
              console.log(`✅ Updated profile for ${userData.profile.username}`);
            }
          }
        } else {
          console.error(`❌ Error creating ${userData.email}:`, authError.message);
        }
      } else if (authData?.user) {
        console.log(`✅ Created user ${userData.profile.username} (${userData.email})`);
        
        // Create/update profile
        const { error: profileError } = await supabase
          .from('profiles')
          .upsert({
            id: authData.user.id,
            ...userData.profile,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          });
          
        if (profileError) {
          console.error(`  ❌ Error creating profile:`, profileError.message);
        } else {
          console.log(`  ✅ Profile created`);
        }
      }
    } catch (error) {
      console.error(`❌ Unexpected error:`, error.message);
    }
  }

  console.log('\n📝 Test User Credentials:');
  console.log('------------------------');
  testUsers.forEach(user => {
    console.log(`${user.profile.username}:`);
    console.log(`  Email: ${user.email}`);
    console.log(`  Password: ${user.password}`);
    console.log('');
  });

  console.log('🎉 Test users are ready!');
  console.log('You can now log in with any of these accounts to test social features.');
  console.log('\n💡 Tip: Open multiple browser windows/incognito to test interactions between users!');
}

createTestUsers();