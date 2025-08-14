import { NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST() {
  try {
    const supabase = await createServerSupabaseClient();

    // Create the get_friend_suggestions function
    const { error } = await supabase.rpc('query', {
      query: `
        CREATE OR REPLACE FUNCTION get_friend_suggestions(user_id UUID)
        RETURNS TABLE (
          suggested_user_id UUID,
          common_groups BIGINT,
          common_nodes BIGINT
        ) 
        LANGUAGE plpgsql
        AS $$
        BEGIN
          RETURN QUERY
          SELECT DISTINCT
            u2.id as suggested_user_id,
            COUNT(DISTINCT sgm2.group_id) as common_groups,
            COUNT(DISTINCT up2.knowledge_node_id) as common_nodes
          FROM auth.users u1
          CROSS JOIN auth.users u2
          LEFT JOIN study_group_members sgm1 ON sgm1.user_id = u1.id
          LEFT JOIN study_group_members sgm2 ON sgm2.user_id = u2.id AND sgm2.group_id = sgm1.group_id
          LEFT JOIN user_progress up1 ON up1.user_id = u1.id
          LEFT JOIN user_progress up2 ON up2.user_id = u2.id AND up2.knowledge_node_id = up1.knowledge_node_id
          WHERE u1.id = $1
            AND u2.id != $1
            AND NOT EXISTS (
              SELECT 1 FROM friends f WHERE f.user_id = $1 AND f.friend_id = u2.id
            )
            AND NOT EXISTS (
              SELECT 1 FROM friend_requests fr 
              WHERE (fr.sender_id = $1 AND fr.receiver_id = u2.id)
                 OR (fr.sender_id = u2.id AND fr.receiver_id = $1)
            )
          GROUP BY u1.id, u2.id
          HAVING COUNT(DISTINCT sgm2.group_id) > 0 OR COUNT(DISTINCT up2.knowledge_node_id) > 3
          ORDER BY COUNT(DISTINCT sgm2.group_id) DESC, COUNT(DISTINCT up2.knowledge_node_id) DESC
          LIMIT 10;
        END;
        $$;
        
        GRANT EXECUTE ON FUNCTION get_friend_suggestions(UUID) TO authenticated;
      `
    });

    if (error) {
      console.error('Error creating function:', error);
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ success: true, message: 'Friend suggestions function created successfully' });
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json({ error: 'Failed to create function' }, { status: 500 });
  }
}