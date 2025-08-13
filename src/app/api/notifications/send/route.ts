import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import webpush from 'web-push';
import { withRateLimit } from '@/lib/rateLimit';

// Initialize web-push with VAPID keys
const vapidKeys = {
  publicKey: process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY || '',
  privateKey: process.env.VAPID_PRIVATE_KEY || '',
  subject: process.env.VAPID_SUBJECT || 'mailto:admin@neuroquest.com'
};

// Configure web-push only if keys are available
if (vapidKeys.publicKey && vapidKeys.privateKey) {
  webpush.setVapidDetails(
    vapidKeys.subject,
    vapidKeys.publicKey,
    vapidKeys.privateKey
  );
}

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

interface NotificationPayload {
  userId?: string;
  title: string;
  body: string;
  icon?: string;
  badge?: string;
  tag?: string;
  data?: any;
  requireInteraction?: boolean;
  actions?: Array<{
    action: string;
    title: string;
    icon?: string;
  }>;
}

export async function POST(request: NextRequest) {
  return withRateLimit(request, async () => {
  try {
    const payload: NotificationPayload = await request.json();
    
    // If no VAPID keys, return early with local notification instruction
    if (!vapidKeys.publicKey || !vapidKeys.privateKey) {
      return NextResponse.json({
        success: false,
        message: 'Push notifications not configured. Use local notifications instead.',
        useLocal: true
      });
    }

    // Get user's push subscription
    let subscriptions;
    if (payload.userId) {
      // Send to specific user
      const { data, error } = await supabase
        .from('push_subscriptions')
        .select('*')
        .eq('user_id', payload.userId);
      
      if (error) {
        console.error('Failed to fetch subscription:', error);
        return NextResponse.json({ 
          success: false, 
          error: 'Failed to fetch subscription' 
        }, { status: 500 });
      }
      
      subscriptions = data;
    } else {
      // Broadcast to all users (admin feature)
      const { data, error } = await supabase
        .from('push_subscriptions')
        .select('*');
      
      if (error) {
        console.error('Failed to fetch subscriptions:', error);
        return NextResponse.json({ 
          success: false, 
          error: 'Failed to fetch subscriptions' 
        }, { status: 500 });
      }
      
      subscriptions = data;
    }

    if (!subscriptions || subscriptions.length === 0) {
      return NextResponse.json({
        success: false,
        message: 'No push subscriptions found'
      });
    }

    // Prepare notification payload
    const notificationPayload = JSON.stringify({
      title: payload.title,
      body: payload.body,
      icon: payload.icon || '/icon-192x192.png',
      badge: payload.badge || '/icon-192x192.png',
      tag: payload.tag,
      data: payload.data,
      requireInteraction: payload.requireInteraction || false,
      actions: payload.actions || []
    });

    // Send push notifications
    const results = await Promise.allSettled(
      subscriptions.map(async (subscription) => {
        const pushSubscription = {
          endpoint: subscription.endpoint,
          keys: {
            p256dh: subscription.p256dh,
            auth: subscription.auth
          }
        };

        try {
          await webpush.sendNotification(pushSubscription, notificationPayload);
          return { success: true, userId: subscription.user_id };
        } catch (error: any) {
          console.error('Failed to send notification:', error);
          
          // Handle expired subscriptions
          if (error.statusCode === 410) {
            // Remove expired subscription
            await supabase
              .from('push_subscriptions')
              .delete()
              .eq('id', subscription.id);
          }
          
          return { success: false, userId: subscription.user_id, error: error.message };
        }
      })
    );

    // Count successful sends
    const successCount = results.filter(r => r.status === 'fulfilled' && r.value.success).length;
    const failCount = results.filter(r => r.status === 'rejected' || (r.status === 'fulfilled' && !r.value.success)).length;

    return NextResponse.json({
      success: true,
      sent: successCount,
      failed: failCount,
      total: subscriptions.length
    });

    } catch (error) {
      console.error('Push notification error:', error);
      return NextResponse.json({ 
        success: false, 
        error: 'Failed to send push notification' 
      }, { status: 500 });
    }
  }, 'notifications');
}