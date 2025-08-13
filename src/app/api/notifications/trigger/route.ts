import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { withRateLimit } from '@/lib/rateLimit';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

interface TriggerRequest {
  userId: string;
  type: 'achievement' | 'levelup' | 'streak' | 'friend_activity' | 'new_content' | 'reminder';
  data: any;
}

export async function POST(request: NextRequest) {
  return withRateLimit(request, async () => {
  try {
    const { userId, type, data }: TriggerRequest = await request.json();
    
    // Check user's notification preferences
    const { data: preferences, error: prefError } = await supabase
      .from('user_notification_preferences')
      .select('*')
      .eq('user_id', userId)
      .single();
    
    if (prefError || !preferences) {
      // Default preferences if not found
      console.log('No preferences found, using defaults');
    }
    
    // Prepare notification based on type
    let notification;
    switch (type) {
      case 'achievement':
        if (preferences?.achievement_alerts === false) {
          return NextResponse.json({ success: false, message: 'User disabled achievement notifications' });
        }
        notification = {
          userId,
          title: '🏆 Achievement Unlocked!',
          body: `${data.name}: ${data.description}`,
          tag: 'achievement',
          data: { type: 'achievement', achievementId: data.id }
        };
        break;
        
      case 'levelup':
        if (preferences?.achievement_alerts === false) {
          return NextResponse.json({ success: false, message: 'User disabled achievement notifications' });
        }
        notification = {
          userId,
          title: '⚡ Level Up!',
          body: `Congratulations! You've reached Neural Level ${data.level}`,
          tag: 'levelup',
          data: { type: 'levelup', level: data.level }
        };
        break;
        
      case 'streak':
        if (preferences?.streak_notifications === false) {
          return NextResponse.json({ success: false, message: 'User disabled streak notifications' });
        }
        notification = {
          userId,
          title: '🔥 Streak Milestone!',
          body: `Amazing! You've maintained a ${data.days}-day learning streak`,
          tag: 'streak',
          data: { type: 'streak', days: data.days }
        };
        break;
        
      case 'friend_activity':
        if (preferences?.friend_activity === false) {
          return NextResponse.json({ success: false, message: 'User disabled friend notifications' });
        }
        notification = {
          userId,
          title: '👥 Friend Activity',
          body: `${data.friendName} ${data.activity}`,
          tag: 'friend-activity',
          data: { type: 'friend_activity', friendId: data.friendId }
        };
        break;
        
      case 'new_content':
        if (preferences?.new_content === false) {
          return NextResponse.json({ success: false, message: 'User disabled content notifications' });
        }
        notification = {
          userId,
          title: '✨ New Content Available!',
          body: `New ${data.contentType}: ${data.contentName} is now available`,
          tag: 'new-content',
          data: { type: 'new_content', contentId: data.contentId }
        };
        break;
        
      case 'reminder':
        if (preferences?.daily_reminders === false) {
          return NextResponse.json({ success: false, message: 'User disabled reminder notifications' });
        }
        notification = {
          userId,
          title: '🧠 Time to Learn!',
          body: 'Continue your journey in NeuroQuest and keep your streak alive!',
          tag: 'reminder',
          actions: [
            { action: 'open', title: 'Start Learning' },
            { action: 'later', title: 'Remind Later' }
          ],
          data: { type: 'reminder' }
        };
        break;
        
      default:
        return NextResponse.json({ 
          success: false, 
          error: 'Invalid notification type' 
        }, { status: 400 });
    }
    
    // Send the notification via the send endpoint
    const response = await fetch(`${process.env.NEXT_PUBLIC_APP_URL}/api/notifications/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(notification)
    });
    
    const result = await response.json();
    return NextResponse.json(result);
    
    } catch (error) {
      console.error('Trigger notification error:', error);
      return NextResponse.json({ 
        success: false, 
        error: 'Failed to trigger notification' 
      }, { status: 500 });
    }
  }, 'notifications');
}