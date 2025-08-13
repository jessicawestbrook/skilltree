-- Sample data for social features in NeuroQuest
-- This script adds test data for development and testing purposes

-- First, ensure we have some test users (if not already present)
INSERT INTO auth.users (id, email, email_confirmed_at, created_at, updated_at)
SELECT * FROM (VALUES 
  ('11111111-1111-1111-1111-111111111111'::uuid, 'alice@example.com', NOW(), NOW(), NOW()),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'bob@example.com', NOW(), NOW(), NOW()),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'charlie@example.com', NOW(), NOW(), NOW()),
  ('44444444-4444-4444-4444-444444444444'::uuid, 'diana@example.com', NOW(), NOW(), NOW()),
  ('55555555-5555-5555-5555-555555555555'::uuid, 'eve@example.com', NOW(), NOW(), NOW())
) AS v(id, email, email_confirmed_at, created_at, updated_at)
WHERE NOT EXISTS (SELECT 1 FROM auth.users WHERE id = v.id);

-- Add user profiles
INSERT INTO public.profiles (id, username, full_name, avatar_url, bio, created_at, updated_at)
SELECT * FROM (VALUES
  ('11111111-1111-1111-1111-111111111111'::uuid, 'alice_neuro', 'Alice Johnson', 'https://api.dicebear.com/7.x/avataaars/svg?seed=alice', 'Neuroscience enthusiast | PhD student | Love learning about the brain! 🧠', NOW(), NOW()),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'bob_brain', 'Bob Smith', 'https://api.dicebear.com/7.x/avataaars/svg?seed=bob', 'Medical student exploring neurology | Coffee addict ☕', NOW(), NOW()),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'charlie_cortex', 'Charlie Davis', 'https://api.dicebear.com/7.x/avataaars/svg?seed=charlie', 'Cognitive science researcher | AI & Brain intersection', NOW(), NOW()),
  ('44444444-4444-4444-4444-444444444444'::uuid, 'diana_dendrite', 'Diana Wilson', 'https://api.dicebear.com/7.x/avataaars/svg?seed=diana', 'Neuropsychologist | Mental health advocate | 🌱', NOW(), NOW()),
  ('55555555-5555-5555-5555-555555555555'::uuid, 'eve_electric', 'Eve Martinez', 'https://api.dicebear.com/7.x/avataaars/svg?seed=eve', 'Biomedical engineer | Neural interfaces | Tech meets biology', NOW(), NOW())
) AS v(id, username, full_name, avatar_url, bio, created_at, updated_at)
ON CONFLICT (id) DO UPDATE SET
  username = EXCLUDED.username,
  full_name = EXCLUDED.full_name,
  avatar_url = EXCLUDED.avatar_url,
  bio = EXCLUDED.bio,
  updated_at = NOW();

-- Add some friendships/connections
INSERT INTO public.friendships (user_id, friend_id, status, created_at)
SELECT * FROM (VALUES
  -- Alice's connections
  ('11111111-1111-1111-1111-111111111111'::uuid, '22222222-2222-2222-2222-222222222222'::uuid, 'accepted', NOW() - INTERVAL '30 days'),
  ('11111111-1111-1111-1111-111111111111'::uuid, '33333333-3333-3333-3333-333333333333'::uuid, 'accepted', NOW() - INTERVAL '25 days'),
  ('11111111-1111-1111-1111-111111111111'::uuid, '44444444-4444-4444-4444-444444444444'::uuid, 'pending', NOW() - INTERVAL '2 days'),
  
  -- Bob's connections
  ('22222222-2222-2222-2222-222222222222'::uuid, '11111111-1111-1111-1111-111111111111'::uuid, 'accepted', NOW() - INTERVAL '30 days'),
  ('22222222-2222-2222-2222-222222222222'::uuid, '33333333-3333-3333-3333-333333333333'::uuid, 'accepted', NOW() - INTERVAL '20 days'),
  ('22222222-2222-2222-2222-222222222222'::uuid, '55555555-5555-5555-5555-555555555555'::uuid, 'accepted', NOW() - INTERVAL '15 days'),
  
  -- Charlie's connections
  ('33333333-3333-3333-3333-333333333333'::uuid, '11111111-1111-1111-1111-111111111111'::uuid, 'accepted', NOW() - INTERVAL '25 days'),
  ('33333333-3333-3333-3333-333333333333'::uuid, '22222222-2222-2222-2222-222222222222'::uuid, 'accepted', NOW() - INTERVAL '20 days'),
  ('33333333-3333-3333-3333-333333333333'::uuid, '44444444-4444-4444-4444-444444444444'::uuid, 'accepted', NOW() - INTERVAL '10 days'),
  
  -- Diana's connections
  ('44444444-4444-4444-4444-444444444444'::uuid, '33333333-3333-3333-3333-333333333333'::uuid, 'accepted', NOW() - INTERVAL '10 days'),
  ('44444444-4444-4444-4444-444444444444'::uuid, '55555555-5555-5555-5555-555555555555'::uuid, 'pending', NOW() - INTERVAL '1 day'),
  
  -- Eve's connections
  ('55555555-5555-5555-5555-555555555555'::uuid, '22222222-2222-2222-2222-222222222222'::uuid, 'accepted', NOW() - INTERVAL '15 days')
) AS v(user_id, friend_id, status, created_at)
ON CONFLICT (user_id, friend_id) DO NOTHING;

-- Add user achievements
INSERT INTO public.user_achievements (user_id, achievement_id, unlocked_at, progress)
SELECT * FROM (VALUES
  -- Alice's achievements
  ('11111111-1111-1111-1111-111111111111'::uuid, 'first_quiz_completed', NOW() - INTERVAL '29 days', 100),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'neural_navigator', NOW() - INTERVAL '28 days', 100),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'synapse_specialist', NOW() - INTERVAL '20 days', 100),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'week_streak', NOW() - INTERVAL '15 days', 100),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'perfect_score', NOW() - INTERVAL '10 days', 100),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'knowledge_seeker', NOW() - INTERVAL '5 days', 75),
  
  -- Bob's achievements
  ('22222222-2222-2222-2222-222222222222'::uuid, 'first_quiz_completed', NOW() - INTERVAL '25 days', 100),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'neural_navigator', NOW() - INTERVAL '22 days', 100),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'quick_learner', NOW() - INTERVAL '18 days', 100),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'social_learner', NOW() - INTERVAL '12 days', 100),
  
  -- Charlie's achievements
  ('33333333-3333-3333-3333-333333333333'::uuid, 'first_quiz_completed', NOW() - INTERVAL '24 days', 100),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'neural_navigator', NOW() - INTERVAL '23 days', 100),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'synapse_specialist', NOW() - INTERVAL '15 days', 100),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'cortex_master', NOW() - INTERVAL '8 days', 100),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'month_streak', NOW() - INTERVAL '2 days', 100),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'brain_expert', NOW() - INTERVAL '1 day', 90),
  
  -- Diana's achievements
  ('44444444-4444-4444-4444-444444444444'::uuid, 'first_quiz_completed', NOW() - INTERVAL '15 days', 100),
  ('44444444-4444-4444-4444-444444444444'::uuid, 'neural_navigator', NOW() - INTERVAL '14 days', 100),
  ('44444444-4444-4444-4444-444444444444'::uuid, 'helpful_peer', NOW() - INTERVAL '7 days', 100),
  
  -- Eve's achievements
  ('55555555-5555-5555-5555-555555555555'::uuid, 'first_quiz_completed', NOW() - INTERVAL '10 days', 100),
  ('55555555-5555-5555-5555-555555555555'::uuid, 'quick_learner', NOW() - INTERVAL '8 days', 100)
) AS v(user_id, achievement_id, unlocked_at, progress)
ON CONFLICT (user_id, achievement_id) DO UPDATE SET
  unlocked_at = EXCLUDED.unlocked_at,
  progress = EXCLUDED.progress;

-- Add leaderboard entries
INSERT INTO public.leaderboard (user_id, score, quizzes_completed, accuracy_rate, streak_days, rank, period, created_at, updated_at)
SELECT * FROM (VALUES
  -- Weekly leaderboard
  ('33333333-3333-3333-3333-333333333333'::uuid, 2850, 38, 95.0, 28, 1, 'weekly', NOW(), NOW()),
  ('11111111-1111-1111-1111-111111111111'::uuid, 2650, 35, 92.5, 21, 2, 'weekly', NOW(), NOW()),
  ('22222222-2222-2222-2222-222222222222'::uuid, 2200, 28, 88.0, 14, 3, 'weekly', NOW(), NOW()),
  ('44444444-4444-4444-4444-444444444444'::uuid, 1500, 18, 85.5, 7, 4, 'weekly', NOW(), NOW()),
  ('55555555-5555-5555-5555-555555555555'::uuid, 1000, 12, 82.0, 5, 5, 'weekly', NOW(), NOW()),
  
  -- Monthly leaderboard
  ('33333333-3333-3333-3333-333333333333'::uuid, 12500, 150, 94.5, 28, 1, 'monthly', NOW(), NOW()),
  ('11111111-1111-1111-1111-111111111111'::uuid, 11200, 135, 91.0, 21, 2, 'monthly', NOW(), NOW()),
  ('22222222-2222-2222-2222-222222222222'::uuid, 9800, 110, 87.5, 14, 3, 'monthly', NOW(), NOW()),
  ('44444444-4444-4444-4444-444444444444'::uuid, 5500, 65, 84.0, 7, 4, 'monthly', NOW(), NOW()),
  ('55555555-5555-5555-5555-555555555555'::uuid, 3200, 38, 80.5, 5, 5, 'monthly', NOW(), NOW()),
  
  -- All-time leaderboard
  ('33333333-3333-3333-3333-333333333333'::uuid, 45000, 450, 93.5, 28, 1, 'all_time', NOW(), NOW()),
  ('11111111-1111-1111-1111-111111111111'::uuid, 38500, 380, 90.0, 21, 2, 'all_time', NOW(), NOW()),
  ('22222222-2222-2222-2222-222222222222'::uuid, 32000, 310, 86.5, 14, 3, 'all_time', NOW(), NOW()),
  ('44444444-4444-4444-4444-444444444444'::uuid, 15000, 150, 83.0, 7, 4, 'all_time', NOW(), NOW()),
  ('55555555-5555-5555-5555-555555555555'::uuid, 8000, 85, 79.5, 5, 5, 'all_time', NOW(), NOW())
) AS v(user_id, score, quizzes_completed, accuracy_rate, streak_days, rank, period, created_at, updated_at)
ON CONFLICT (user_id, period) DO UPDATE SET
  score = EXCLUDED.score,
  quizzes_completed = EXCLUDED.quizzes_completed,
  accuracy_rate = EXCLUDED.accuracy_rate,
  streak_days = EXCLUDED.streak_days,
  rank = EXCLUDED.rank,
  updated_at = NOW();

-- Add some discussion posts
INSERT INTO public.discussions (id, user_id, title, content, category, tags, upvotes, views, is_pinned, is_locked, created_at, updated_at)
VALUES
  ('d1111111-1111-1111-1111-111111111111'::uuid, '11111111-1111-1111-1111-111111111111'::uuid, 
   'Understanding Neurotransmitters: A Beginner''s Guide',
   'Hey everyone! I''ve been studying neurotransmitters and wanted to share my notes. Neurotransmitters are chemical messengers that transmit signals between neurons. The major ones include dopamine (reward and motivation), serotonin (mood regulation), GABA (inhibitory), and glutamate (excitatory). What are your favorite mnemonics for remembering them?',
   'study-tips', ARRAY['neurotransmitters', 'biochemistry', 'study-guide'], 45, 320, false, false, NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 hours'),
   
  ('d2222222-2222-2222-2222-222222222222'::uuid, '33333333-3333-3333-3333-333333333333'::uuid,
   'The Fascinating World of Mirror Neurons',
   'Just learned about mirror neurons in my cognitive neuroscience class! These neurons fire both when we perform an action AND when we observe someone else performing that same action. They might be crucial for empathy, learning through imitation, and understanding others'' intentions. Mind = blown! 🤯',
   'discoveries', ARRAY['mirror-neurons', 'cognitive-neuroscience', 'empathy'], 67, 450, true, false, NOW() - INTERVAL '3 days', NOW() - INTERVAL '6 hours'),
   
  ('d3333333-3333-3333-3333-333333333333'::uuid, '22222222-2222-2222-2222-222222222222'::uuid,
   'Study Group for Neuroanatomy - Join Us!',
   'Starting a virtual study group for neuroanatomy! We meet every Tuesday and Thursday at 7 PM EST. Currently working through the limbic system and will move to the basal ganglia next week. Comment if interested!',
   'study-groups', ARRAY['neuroanatomy', 'study-group', 'collaboration'], 23, 180, false, false, NOW() - INTERVAL '2 days', NOW() - INTERVAL '12 hours'),
   
  ('d4444444-4444-4444-4444-444444444444'::uuid, '44444444-4444-4444-4444-444444444444'::uuid,
   'Question: Why do we dream? Latest neuroscience perspectives',
   'I''ve been researching the neuroscience of dreams and sleep. The activation-synthesis hypothesis, memory consolidation theory, and threat simulation theory all offer different perspectives. What''s the current scientific consensus? Would love to hear your thoughts!',
   'questions', ARRAY['dreams', 'sleep', 'consciousness'], 89, 612, false, false, NOW() - INTERVAL '4 days', NOW() - INTERVAL '8 hours'),
   
  ('d5555555-5555-5555-5555-555555555555'::uuid, '55555555-5555-5555-5555-555555555555'::uuid,
   'New Research: Brain-Computer Interfaces Show Promise',
   'Exciting news from the BCI field! Recent studies show significant improvements in neural decoding algorithms. We''re getting closer to thought-controlled prosthetics and direct brain-to-computer communication. Check out this paper: [link]. What are your thoughts on the ethical implications?',
   'research', ARRAY['BCI', 'neurotechnology', 'innovation'], 102, 780, true, false, NOW() - INTERVAL '1 day', NOW() - INTERVAL '3 hours');

-- Add comments to discussions
INSERT INTO public.discussion_comments (id, discussion_id, user_id, content, upvotes, created_at, updated_at)
VALUES
  -- Comments on neurotransmitters post
  ('c1111111-1111-1111-1111-111111111111'::uuid, 'd1111111-1111-1111-1111-111111111111'::uuid, '22222222-2222-2222-2222-222222222222'::uuid,
   'Great summary! For dopamine, I use "DOPE-amine = feeling dope/good". For GABA, I remember "GABA = Go Away Bad Activity" since it''s inhibitory!',
   12, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
   
  ('c1111112-1111-1111-1111-111111111112'::uuid, 'd1111111-1111-1111-1111-111111111111'::uuid, '33333333-3333-3333-3333-333333333333'::uuid,
   'Don''t forget about acetylcholine! It''s crucial for muscle movement and memory. I remember it as "A-SETTLE-choline" because it helps muscles settle into action.',
   8, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
   
  -- Comments on mirror neurons post
  ('c2222221-2222-2222-2222-222222222221'::uuid, 'd2222222-2222-2222-2222-222222222222'::uuid, '11111111-1111-1111-1111-111111111111'::uuid,
   'Mirror neurons are incredible! They might also explain why we yawn when others yawn. The contagious yawning phenomenon could be mirror neurons in action!',
   15, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
   
  ('c2222222-2222-2222-2222-222222222222'::uuid, 'd2222222-2222-2222-2222-222222222222'::uuid, '44444444-4444-4444-4444-444444444444'::uuid,
   'There''s still debate about mirror neurons in humans though. Most research was done on macaque monkeys. Still fascinating regardless!',
   6, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
   
  -- Comments on study group post
  ('c3333331-3333-3333-3333-333333333331'::uuid, 'd3333333-3333-3333-3333-333333333333'::uuid, '11111111-1111-1111-1111-111111111111'::uuid,
   'Count me in! I''ve been struggling with the hippocampus and could use a study buddy.',
   3, NOW() - INTERVAL '1 day 18 hours', NOW() - INTERVAL '1 day 18 hours'),
   
  ('c3333332-3333-3333-3333-333333333332'::uuid, 'd3333333-3333-3333-3333-333333333333'::uuid, '55555555-5555-5555-5555-555555555555'::uuid,
   'Interested! Do you use any specific textbook or resources?',
   2, NOW() - INTERVAL '1 day 12 hours', NOW() - INTERVAL '1 day 12 hours');

-- Add user messages (direct messages between users)
INSERT INTO public.messages (id, sender_id, recipient_id, content, is_read, created_at)
VALUES
  ('m1111111-1111-1111-1111-111111111111'::uuid, '11111111-1111-1111-1111-111111111111'::uuid, '22222222-2222-2222-2222-222222222222'::uuid,
   'Hey Bob! Thanks for the study tips on neurotransmitters. Really helped with my quiz!', true, NOW() - INTERVAL '3 days'),
   
  ('m1111112-1111-1111-1111-111111111112'::uuid, '22222222-2222-2222-2222-222222222222'::uuid, '11111111-1111-1111-1111-111111111111'::uuid,
   'No problem, Alice! Glad it helped. How did you do on the quiz?', true, NOW() - INTERVAL '3 days' + INTERVAL '30 minutes'),
   
  ('m1111113-1111-1111-1111-111111111113'::uuid, '11111111-1111-1111-1111-111111111111'::uuid, '22222222-2222-2222-2222-222222222222'::uuid,
   'Got 95%! The mnemonics really made a difference.', true, NOW() - INTERVAL '3 days' + INTERVAL '45 minutes'),
   
  ('m2222221-2222-2222-2222-222222222221'::uuid, '33333333-3333-3333-3333-333333333333'::uuid, '44444444-4444-4444-4444-444444444444'::uuid,
   'Diana, would you like to collaborate on the neuroplasticity module? I think our research interests align!', true, NOW() - INTERVAL '2 days'),
   
  ('m2222222-2222-2222-2222-222222222222'::uuid, '44444444-4444-4444-4444-444444444444'::uuid, '33333333-3333-3333-3333-333333333333'::uuid,
   'Absolutely! I''ve been researching adult neurogenesis. Let''s set up a time to discuss.', false, NOW() - INTERVAL '1 day'),
   
  ('m3333331-3333-3333-3333-333333333331'::uuid, '55555555-5555-5555-5555-555555555555'::uuid, '22222222-2222-2222-2222-222222222222'::uuid,
   'Your insights on BCIs in the discussion were spot on! Are you working in that field?', false, NOW() - INTERVAL '6 hours');

-- Add notifications
INSERT INTO public.notifications (id, user_id, type, title, message, data, is_read, created_at)
VALUES
  ('n1111111-1111-1111-1111-111111111111'::uuid, '11111111-1111-1111-1111-111111111111'::uuid, 'achievement',
   'New Achievement Unlocked!', 'You''ve earned the "Knowledge Seeker" badge!',
   '{"achievement_id": "knowledge_seeker", "points": 100}'::jsonb, false, NOW() - INTERVAL '2 hours'),
   
  ('n2222221-2222-2222-2222-222222222221'::uuid, '22222222-2222-2222-2222-222222222222'::uuid, 'friend_request',
   'New Friend Request', 'Diana wants to connect with you',
   '{"from_user_id": "44444444-4444-4444-4444-444444444444"}'::jsonb, false, NOW() - INTERVAL '1 hour'),
   
  ('n3333331-3333-3333-3333-333333333331'::uuid, '33333333-3333-3333-3333-333333333333'::uuid, 'leaderboard',
   'Leaderboard Update!', 'You''re now #1 on the weekly leaderboard!',
   '{"period": "weekly", "rank": 1, "previous_rank": 2}'::jsonb, true, NOW() - INTERVAL '3 hours'),
   
  ('n4444441-4444-4444-4444-444444444441'::uuid, '44444444-4444-4444-4444-444444444444'::uuid, 'message',
   'New Message', 'You have a new message from Charlie',
   '{"from_user_id": "33333333-3333-3333-3333-333333333333"}'::jsonb, false, NOW() - INTERVAL '1 day'),
   
  ('n5555551-5555-5555-5555-555555555551'::uuid, '55555555-5555-5555-5555-555555555555'::uuid, 'discussion_reply',
   'New Reply to Your Post', 'Someone commented on your BCI discussion',
   '{"discussion_id": "d5555555-5555-5555-5555-555555555555", "comment_id": "c5555551-5555-5555-5555-555555555551"}'::jsonb, false, NOW() - INTERVAL '30 minutes');

-- Add sample quiz progress data
INSERT INTO public.user_progress (user_id, node_id, progress_percentage, quizzes_completed, quizzes_passed, total_score, last_activity, created_at, updated_at)
SELECT * FROM (VALUES
  -- Alice's progress
  ('11111111-1111-1111-1111-111111111111'::uuid, 'neuron-structure', 100, 5, 5, 475, NOW() - INTERVAL '1 day', NOW() - INTERVAL '29 days', NOW() - INTERVAL '1 day'),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'action-potential', 100, 4, 4, 380, NOW() - INTERVAL '2 days', NOW() - INTERVAL '25 days', NOW() - INTERVAL '2 days'),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'synaptic-transmission', 85, 3, 3, 255, NOW() - INTERVAL '3 days', NOW() - INTERVAL '20 days', NOW() - INTERVAL '3 days'),
  ('11111111-1111-1111-1111-111111111111'::uuid, 'neurotransmitters', 75, 3, 2, 210, NOW() - INTERVAL '5 days', NOW() - INTERVAL '15 days', NOW() - INTERVAL '5 days'),
  
  -- Bob's progress
  ('22222222-2222-2222-2222-222222222222'::uuid, 'neuron-structure', 100, 4, 4, 360, NOW() - INTERVAL '2 days', NOW() - INTERVAL '24 days', NOW() - INTERVAL '2 days'),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'action-potential', 90, 3, 3, 270, NOW() - INTERVAL '4 days', NOW() - INTERVAL '20 days', NOW() - INTERVAL '4 days'),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'synaptic-transmission', 60, 2, 1, 110, NOW() - INTERVAL '7 days', NOW() - INTERVAL '15 days', NOW() - INTERVAL '7 days'),
  
  -- Charlie's progress (top performer)
  ('33333333-3333-3333-3333-333333333333'::uuid, 'neuron-structure', 100, 6, 6, 600, NOW() - INTERVAL '1 hour', NOW() - INTERVAL '24 days', NOW() - INTERVAL '1 hour'),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'action-potential', 100, 5, 5, 500, NOW() - INTERVAL '2 hours', NOW() - INTERVAL '22 days', NOW() - INTERVAL '2 hours'),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'synaptic-transmission', 100, 5, 5, 495, NOW() - INTERVAL '3 hours', NOW() - INTERVAL '18 days', NOW() - INTERVAL '3 hours'),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'neurotransmitters', 100, 4, 4, 395, NOW() - INTERVAL '4 hours', NOW() - INTERVAL '15 days', NOW() - INTERVAL '4 hours'),
  ('33333333-3333-3333-3333-333333333333'::uuid, 'brain-anatomy', 95, 4, 4, 370, NOW() - INTERVAL '6 hours', NOW() - INTERVAL '10 days', NOW() - INTERVAL '6 hours'),
  
  -- Diana's progress
  ('44444444-4444-4444-4444-444444444444'::uuid, 'neuron-structure', 100, 3, 3, 285, NOW() - INTERVAL '1 day', NOW() - INTERVAL '15 days', NOW() - INTERVAL '1 day'),
  ('44444444-4444-4444-4444-444444444444'::uuid, 'action-potential', 70, 2, 2, 140, NOW() - INTERVAL '3 days', NOW() - INTERVAL '12 days', NOW() - INTERVAL '3 days'),
  
  -- Eve's progress (newest user)
  ('55555555-5555-5555-5555-555555555555'::uuid, 'neuron-structure', 100, 2, 2, 190, NOW() - INTERVAL '2 days', NOW() - INTERVAL '10 days', NOW() - INTERVAL '2 days'),
  ('55555555-5555-5555-5555-555555555555'::uuid, 'action-potential', 50, 1, 1, 85, NOW() - INTERVAL '4 days', NOW() - INTERVAL '8 days', NOW() - INTERVAL '4 days')
) AS v(user_id, node_id, progress_percentage, quizzes_completed, quizzes_passed, total_score, last_activity, created_at, updated_at)
ON CONFLICT (user_id, node_id) DO UPDATE SET
  progress_percentage = EXCLUDED.progress_percentage,
  quizzes_completed = EXCLUDED.quizzes_completed,
  quizzes_passed = EXCLUDED.quizzes_passed,
  total_score = EXCLUDED.total_score,
  last_activity = EXCLUDED.last_activity,
  updated_at = NOW();

-- Output summary
SELECT 'Sample social data loaded successfully!' as status;
SELECT 'Users created/updated: ' || COUNT(DISTINCT id) FROM public.profiles;
SELECT 'Friendships created: ' || COUNT(*) FROM public.friendships;
SELECT 'Achievements unlocked: ' || COUNT(*) FROM public.user_achievements;
SELECT 'Leaderboard entries: ' || COUNT(*) FROM public.leaderboard;
SELECT 'Discussions created: ' || COUNT(*) FROM public.discussions;
SELECT 'Comments added: ' || COUNT(*) FROM public.discussion_comments;
SELECT 'Messages sent: ' || COUNT(*) FROM public.messages;
SELECT 'Notifications created: ' || COUNT(*) FROM public.notifications;