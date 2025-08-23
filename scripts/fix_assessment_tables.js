const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env.local' });

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_SERVICE_ROLE_KEY
);

async function checkAndCreateTables() {
  console.log('Checking for assessment tables...');

  // Check if tables exist
  const { data: tables, error: tablesError } = await supabase
    .from('information_schema.tables')
    .select('table_name')
    .eq('table_schema', 'public')
    .in('table_name', ['user_category_scores', 'assessment_sessions', 'assessment_questions', 'assessment_responses']);

  if (tablesError) {
    // The information_schema approach might not work, let's try a different approach
    console.log('Checking tables directly...');
    
    // Try to query each table to see if it exists
    const tablesToCheck = ['user_category_scores', 'assessment_sessions', 'assessment_questions', 'assessment_responses'];
    const existingTables = [];
    const missingTables = [];

    for (const tableName of tablesToCheck) {
      const { error } = await supabase
        .from(tableName)
        .select('*')
        .limit(1);
      
      if (error && error.code === '42P01') {
        // Table does not exist
        missingTables.push(tableName);
      } else {
        existingTables.push(tableName);
      }
    }

    console.log('Existing tables:', existingTables);
    console.log('Missing tables:', missingTables);

    // Create missing tables
    if (missingTables.includes('user_category_scores')) {
      console.log('Creating user_category_scores table...');
      const { error } = await supabase.rpc('exec_sql', {
        sql: `
          CREATE TABLE IF NOT EXISTS public.user_category_scores (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
            category_id UUID NOT NULL REFERENCES public.skill_tree_nodes(id) ON DELETE CASCADE,
            current_ability_estimate DECIMAL(5,2) DEFAULT 0,
            confidence_interval DECIMAL(5,2) DEFAULT 1,
            total_questions_answered INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            last_assessment_date TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(user_id, category_id)
          );
          
          CREATE INDEX IF NOT EXISTS idx_user_category_scores_user_id ON public.user_category_scores(user_id);
          CREATE INDEX IF NOT EXISTS idx_user_category_scores_category_id ON public.user_category_scores(category_id);
        `
      });
      
      if (error) {
        console.error('Error creating user_category_scores table:', error);
      } else {
        console.log('user_category_scores table created successfully');
      }
    }

    if (missingTables.includes('assessment_sessions')) {
      console.log('Creating assessment_sessions table...');
      const { error } = await supabase.rpc('exec_sql', {
        sql: `
          CREATE TABLE IF NOT EXISTS public.assessment_sessions (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
            category_id UUID NOT NULL REFERENCES public.skill_tree_nodes(id) ON DELETE CASCADE,
            session_type VARCHAR(50) NOT NULL,
            status VARCHAR(50) DEFAULT 'active',
            current_ability_estimate DECIMAL(5,2) DEFAULT 0,
            confidence_interval DECIMAL(5,2) DEFAULT 1,
            total_questions INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            total_points INTEGER DEFAULT 0,
            streak_count INTEGER DEFAULT 0,
            max_streak INTEGER DEFAULT 0,
            started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            completed_at TIMESTAMP WITH TIME ZONE,
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
          );
          
          CREATE INDEX IF NOT EXISTS idx_assessment_sessions_user_id ON public.assessment_sessions(user_id);
          CREATE INDEX IF NOT EXISTS idx_assessment_sessions_category_id ON public.assessment_sessions(category_id);
          CREATE INDEX IF NOT EXISTS idx_assessment_sessions_status ON public.assessment_sessions(status);
        `
      });
      
      if (error) {
        console.error('Error creating assessment_sessions table:', error);
      } else {
        console.log('assessment_sessions table created successfully');
      }
    }

    if (missingTables.includes('assessment_questions')) {
      console.log('Creating assessment_questions table...');
      const { error } = await supabase.rpc('exec_sql', {
        sql: `
          CREATE TABLE IF NOT EXISTS public.assessment_questions (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            session_id UUID NOT NULL REFERENCES public.assessment_sessions(id) ON DELETE CASCADE,
            question_id UUID NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
            question_number INTEGER NOT NULL,
            difficulty_estimate DECIMAL(5,2),
            presented_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
          );
          
          CREATE INDEX IF NOT EXISTS idx_assessment_questions_session_id ON public.assessment_questions(session_id);
          CREATE INDEX IF NOT EXISTS idx_assessment_questions_question_id ON public.assessment_questions(question_id);
        `
      });
      
      if (error) {
        console.error('Error creating assessment_questions table:', error);
      } else {
        console.log('assessment_questions table created successfully');
      }
    }

    if (missingTables.includes('assessment_responses')) {
      console.log('Creating assessment_responses table...');
      const { error } = await supabase.rpc('exec_sql', {
        sql: `
          CREATE TABLE IF NOT EXISTS public.assessment_responses (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            assessment_question_id UUID NOT NULL REFERENCES public.assessment_questions(id) ON DELETE CASCADE,
            user_answer TEXT,
            is_correct BOOLEAN,
            points_earned INTEGER DEFAULT 0,
            time_spent_seconds INTEGER,
            responded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
          );
          
          CREATE INDEX IF NOT EXISTS idx_assessment_responses_question_id ON public.assessment_responses(assessment_question_id);
        `
      });
      
      if (error) {
        console.error('Error creating assessment_responses table:', error);
      } else {
        console.log('assessment_responses table created successfully');
      }
    }

    console.log('Table check and creation complete');
    
  } else {
    const tableNames = tables ? tables.map(t => t.table_name) : [];
    console.log('Found tables:', tableNames);
  }
}

checkAndCreateTables().catch(console.error);