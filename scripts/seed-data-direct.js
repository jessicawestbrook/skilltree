const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

async function seedData() {
  console.log('🌱 Seeding social data...\n');

  try {
    // Test users
    const users = [
      { id: '11111111-1111-1111-1111-111111111111', username: 'alice_neuro', full_name: 'Alice Johnson', avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=alice', bio: 'Neuroscience enthusiast | PhD student | Love learning about the brain! 🧠' },
      { id: '22222222-2222-2222-2222-222222222222', username: 'bob_brain', full_name: 'Bob Smith', avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=bob', bio: 'Medical student exploring neurology | Coffee addict ☕' },
      { id: '33333333-3333-3333-3333-333333333333', username: 'charlie_cortex', full_name: 'Charlie Davis', avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=charlie', bio: 'Cognitive science researcher | AI & Brain intersection' },
      { id: '44444444-4444-4444-4444-444444444444', username: 'diana_dendrite', full_name: 'Diana Wilson', avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=diana', bio: 'Neuropsychologist | Mental health advocate | 🌱' },
      { id: '55555555-5555-5555-5555-555555555555', username: 'eve_electric', full_name: 'Eve Martinez', avatar_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=eve', bio: 'Biomedical engineer | Neural interfaces | Tech meets biology' }
    ];

    // Insert profiles
    console.log('Creating user profiles...');
    const { error: profileError } = await supabase
      .from('profiles')
      .upsert(users, { onConflict: 'id' });
    
    if (profileError) {
      console.error('Error creating profiles:', profileError.message);
    } else {
      console.log('✅ User profiles created');
    }

    // Friendships
    const friendships = [
      { user_id: '11111111-1111-1111-1111-111111111111', friend_id: '22222222-2222-2222-2222-222222222222', status: 'accepted' },
      { user_id: '11111111-1111-1111-1111-111111111111', friend_id: '33333333-3333-3333-3333-333333333333', status: 'accepted' },
      { user_id: '22222222-2222-2222-2222-222222222222', friend_id: '33333333-3333-3333-3333-333333333333', status: 'accepted' },
      { user_id: '33333333-3333-3333-3333-333333333333', friend_id: '44444444-4444-4444-4444-444444444444', status: 'accepted' },
      { user_id: '44444444-4444-4444-4444-444444444444', friend_id: '55555555-5555-5555-5555-555555555555', status: 'pending' }
    ];

    console.log('Creating friendships...');
    const { error: friendError } = await supabase
      .from('friendships')
      .upsert(friendships, { onConflict: 'user_id,friend_id', ignoreDuplicates: true });
    
    if (friendError) {
      console.error('Error creating friendships:', friendError.message);
    } else {
      console.log('✅ Friendships created');
    }

    // Achievements
    const achievements = [
      { user_id: '11111111-1111-1111-1111-111111111111', achievement_id: 'first_quiz_completed', progress: 100 },
      { user_id: '11111111-1111-1111-1111-111111111111', achievement_id: 'neural_navigator', progress: 100 },
      { user_id: '22222222-2222-2222-2222-222222222222', achievement_id: 'first_quiz_completed', progress: 100 },
      { user_id: '33333333-3333-3333-3333-333333333333', achievement_id: 'first_quiz_completed', progress: 100 },
      { user_id: '33333333-3333-3333-3333-333333333333', achievement_id: 'synapse_specialist', progress: 100 },
      { user_id: '33333333-3333-3333-3333-333333333333', achievement_id: 'month_streak', progress: 100 }
    ];

    console.log('Unlocking achievements...');
    const { error: achievementError } = await supabase
      .from('user_achievements')
      .upsert(achievements, { onConflict: 'user_id,achievement_id' });
    
    if (achievementError) {
      console.error('Error creating achievements:', achievementError.message);
    } else {
      console.log('✅ Achievements unlocked');
    }

    // Leaderboard
    const leaderboard = [
      { user_id: '33333333-3333-3333-3333-333333333333', score: 2850, quizzes_completed: 38, accuracy_rate: 95.0, streak_days: 28, rank: 1, period: 'weekly' },
      { user_id: '11111111-1111-1111-1111-111111111111', score: 2650, quizzes_completed: 35, accuracy_rate: 92.5, streak_days: 21, rank: 2, period: 'weekly' },
      { user_id: '22222222-2222-2222-2222-222222222222', score: 2200, quizzes_completed: 28, accuracy_rate: 88.0, streak_days: 14, rank: 3, period: 'weekly' },
      { user_id: '44444444-4444-4444-4444-444444444444', score: 1500, quizzes_completed: 18, accuracy_rate: 85.5, streak_days: 7, rank: 4, period: 'weekly' },
      { user_id: '55555555-5555-5555-5555-555555555555', score: 1000, quizzes_completed: 12, accuracy_rate: 82.0, streak_days: 5, rank: 5, period: 'weekly' }
    ];

    console.log('Updating leaderboard...');
    const { error: leaderboardError } = await supabase
      .from('leaderboard')
      .upsert(leaderboard, { onConflict: 'user_id,period' });
    
    if (leaderboardError) {
      console.error('Error creating leaderboard:', leaderboardError.message);
    } else {
      console.log('✅ Leaderboard updated');
    }

    // Discussions
    const discussions = [
      {
        id: 'd1111111-1111-1111-1111-111111111111',
        user_id: '11111111-1111-1111-1111-111111111111',
        title: 'Understanding Neurotransmitters: A Beginner\'s Guide',
        content: 'Hey everyone! I\'ve been studying neurotransmitters and wanted to share my notes...',
        category: 'study-tips',
        tags: ['neurotransmitters', 'biochemistry', 'study-guide'],
        upvotes: 45,
        views: 320
      },
      {
        id: 'd2222222-2222-2222-2222-222222222222',
        user_id: '33333333-3333-3333-3333-333333333333',
        title: 'The Fascinating World of Mirror Neurons',
        content: 'Just learned about mirror neurons in my cognitive neuroscience class! Mind = blown! 🤯',
        category: 'discoveries',
        tags: ['mirror-neurons', 'cognitive-neuroscience', 'empathy'],
        upvotes: 67,
        views: 450,
        is_pinned: true
      }
    ];

    console.log('Creating discussions...');
    const { error: discussionError } = await supabase
      .from('discussions')
      .upsert(discussions, { onConflict: 'id' });
    
    if (discussionError) {
      console.error('Error creating discussions:', discussionError.message);
    } else {
      console.log('✅ Discussions created');
    }

    // Progress data
    const progress = [
      { user_id: '11111111-1111-1111-1111-111111111111', node_id: 'neuron-structure', progress_percentage: 100, quizzes_completed: 5, quizzes_passed: 5, total_score: 475 },
      { user_id: '11111111-1111-1111-1111-111111111111', node_id: 'action-potential', progress_percentage: 100, quizzes_completed: 4, quizzes_passed: 4, total_score: 380 },
      { user_id: '22222222-2222-2222-2222-222222222222', node_id: 'neuron-structure', progress_percentage: 100, quizzes_completed: 4, quizzes_passed: 4, total_score: 360 },
      { user_id: '33333333-3333-3333-3333-333333333333', node_id: 'neuron-structure', progress_percentage: 100, quizzes_completed: 6, quizzes_passed: 6, total_score: 600 },
      { user_id: '33333333-3333-3333-3333-333333333333', node_id: 'synaptic-transmission', progress_percentage: 100, quizzes_completed: 5, quizzes_passed: 5, total_score: 495 }
    ];

    console.log('Adding progress data...');
    const { error: progressError } = await supabase
      .from('user_progress')
      .upsert(progress, { onConflict: 'user_id,node_id' });
    
    if (progressError) {
      console.error('Error creating progress:', progressError.message);
    } else {
      console.log('✅ Progress data added');
    }

    console.log('\n🎉 Sample social data loaded successfully!');
    console.log('You now have:');
    console.log('  • 5 test users with profiles');
    console.log('  • Friend connections');
    console.log('  • Achievement unlocks');
    console.log('  • Leaderboard rankings');
    console.log('  • Discussion posts');
    console.log('  • Learning progress data');

  } catch (error) {
    console.error('Error seeding data:', error);
  }
}

seedData();