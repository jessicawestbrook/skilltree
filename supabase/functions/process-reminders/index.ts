import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.0'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Create Supabase client with service role key
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
      {
        auth: {
          autoRefreshToken: false,
          persistSession: false
        }
      }
    )

    const now = new Date()

    // Get all due reminders
    const { data: dueReminders, error: remindersError } = await supabaseClient
      .from('study_reminders')
      .select('*')
      .lte('scheduled_for', now.toISOString())
      .eq('reminder_sent', false)
      .is('completed_at', null)
      .is('dismissed_at', null)

    if (remindersError) {
      throw remindersError
    }

    if (!dueReminders || dueReminders.length === 0) {
      return new Response(
        JSON.stringify({ message: 'No due reminders to process' }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const processedCount = 0
    const errors = []

    // Process each reminder
    for (const reminder of dueReminders) {
      try {
        // Create notification
        const { error: notificationError } = await supabaseClient
          .from('notifications')
          .insert({
            user_id: reminder.user_id,
            type: 'reminder',
            title: reminder.title || 'Study Reminder',
            message: reminder.description || 'Time for your study session!',
            data: {
              reminder_id: reminder.id,
              content_type: reminder.content_type,
              content_ids: reminder.content_ids,
              duration_minutes: reminder.study_duration_minutes
            },
            is_read: false,
            created_at: now.toISOString()
          })

        if (notificationError) {
          errors.push({ reminder_id: reminder.id, error: notificationError })
          continue
        }

        // Get user's push subscriptions
        const { data: subscriptions, error: subError } = await supabaseClient
          .from('push_subscriptions')
          .select('*')
          .eq('user_id', reminder.user_id)

        if (!subError && subscriptions && subscriptions.length > 0) {
          // Send push notification to each subscription
          for (const subscription of subscriptions) {
            await sendPushNotification(
              subscription,
              reminder.title || 'Study Reminder',
              reminder.description || 'Time for your study session!',
              {
                reminder_id: reminder.id,
                url: `/study?reminder=${reminder.id}`
              }
            )
          }
        }

        // Mark reminder as sent
        const { error: updateError } = await supabaseClient
          .from('study_reminders')
          .update({
            reminder_sent: true,
            reminder_sent_at: now.toISOString()
          })
          .eq('id', reminder.id)

        if (updateError) {
          errors.push({ reminder_id: reminder.id, error: updateError })
        } else {
          processedCount++
        }

        // Handle recurring reminders
        if (reminder.is_recurring && reminder.recurrence_pattern) {
          await createNextRecurrence(supabaseClient, reminder)
        }

      } catch (error) {
        errors.push({ reminder_id: reminder.id, error })
      }
    }

    return new Response(
      JSON.stringify({
        message: `Processed ${processedCount} reminders`,
        errors: errors.length > 0 ? errors : undefined
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    )
  }
})

/**
 * Send push notification using Web Push Protocol
 */
async function sendPushNotification(
  subscription: any,
  title: string,
  body: string,
  data: any
) {
  try {
    const payload = JSON.stringify({
      title,
      body,
      icon: '/icon-192x192.png',
      badge: '/icon-72x72.png',
      data,
      requireInteraction: true,
      vibrate: [200, 100, 200]
    })

    // This is a simplified version - in production, you'd use web-push library
    // with VAPID keys for authentication
    const response = await fetch(subscription.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'TTL': '86400', // 24 hours
      },
      body: payload
    })

    if (!response.ok) {
      console.error('Failed to send push notification:', response.statusText)
    }
  } catch (error) {
    console.error('Error sending push notification:', error)
  }
}

/**
 * Create next occurrence of a recurring reminder
 */
async function createNextRecurrence(supabaseClient: any, reminder: any) {
  const scheduledFor = new Date(reminder.scheduled_for)
  
  // Check if we've reached the end date
  if (reminder.recurrence_end_date) {
    const endDate = new Date(reminder.recurrence_end_date)
    if (scheduledFor >= endDate) return
  }

  // Calculate next occurrence
  switch (reminder.recurrence_pattern) {
    case 'daily':
      scheduledFor.setDate(scheduledFor.getDate() + 1)
      break
    
    case 'weekly':
      scheduledFor.setDate(scheduledFor.getDate() + 7)
      break
    
    case 'custom':
      if (reminder.recurrence_days && reminder.recurrence_days.length > 0) {
        // Find next day in recurrence_days
        let daysToAdd = 1
        const currentDay = scheduledFor.getDay()
        
        for (let i = 1; i <= 7; i++) {
          const nextDay = (currentDay + i) % 7
          if (reminder.recurrence_days.includes(nextDay)) {
            daysToAdd = i
            break
          }
        }
        
        scheduledFor.setDate(scheduledFor.getDate() + daysToAdd)
      }
      break
  }

  // Create new reminder
  await supabaseClient
    .from('study_reminders')
    .insert({
      ...reminder,
      id: undefined, // Let database generate new ID
      scheduled_for: scheduledFor.toISOString(),
      reminder_sent: false,
      reminder_sent_at: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    })
}