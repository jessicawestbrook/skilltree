# Notification System Documentation

## Overview
The SkillTree application includes a comprehensive notification system that supports both in-app notifications and browser push notifications. The system integrates with spaced repetition learning and allows users to set custom study reminders.

## System Architecture

### Core Components

1. **NotificationContext** (`src/contexts/NotificationContext.tsx`)
   - Manages notification state across the application
   - Handles fetching, marking as read, and deleting notifications
   - Provides offline support with retry logic

2. **NotificationService** (`src/services/notificationService.ts`)
   - Core service for CRUD operations on notifications
   - Implements retry logic for failed requests
   - Caches notifications locally for offline access

3. **StudyReminderService** (`src/services/studyReminderService.ts`)
   - Manages study reminders and schedules
   - Creates spaced repetition reminders
   - Handles recurring reminders

4. **PushNotificationService** (`src/services/pushNotificationService.ts`)
   - Manages browser push notification subscriptions
   - Handles service worker registration
   - Requires VAPID keys for authentication

## Database Schema

### Tables

1. **notifications**
   - Stores all user notifications
   - Fields: `id`, `user_id`, `type`, `title`, `message`, `data`, `is_read`, `created_at`, `expires_at`
   - Types: `achievement`, `progress`, `reminder`, `system`, `social`

2. **notification_preferences**
   - User notification settings
   - Controls which notification types are enabled
   - Fields include toggles for each notification type

3. **study_reminders**
   - Scheduled study sessions
   - Supports one-time and recurring reminders
   - Fields: `scheduled_for`, `reminder_sent`, `reminder_sent_at`, `completed_at`, `dismissed_at`
   - Recurrence patterns: `daily`, `weekly`, `custom`

4. **study_schedules**
   - User's preferred study times
   - Fields: `preferred_days`, `preferred_time`, `timezone`, `auto_schedule_reviews`

5. **push_subscriptions**
   - Browser push notification endpoints
   - Fields: `endpoint`, `p256dh`, `auth`, `user_agent`

6. **notification_queue**
   - Queue for processing scheduled notifications
   - Tracks delivery status and retry attempts
   - Fields: `scheduled_for`, `status`, `sent_at`, `attempts`, `error_message`

## Automatic Notifications

### 1. Spaced Repetition Review Reminders
- **Trigger**: After completing a flashcard review with a correct answer (quality ≥ 3)
- **Timing**: Based on SM-2 algorithm intervals (1, 3, 7, 14, 30, 90 days)
- **Condition**: User must have `auto_schedule_reviews` enabled in their study schedule
- **Implementation**: `spacedRepetitionService.ts` - `createNextReviewReminder()` method

### 2. Recurring Study Reminders
- **Trigger**: When a user completes a recurring reminder
- **Timing**: Based on user-defined recurrence pattern
  - Daily: Next day at the same time
  - Weekly: Next week at the same time
  - Custom: Next selected day of the week
- **Implementation**: `studyReminderService.ts` - `createNextRecurrence()` method

### 3. Due Reminder Processing
- **Trigger**: Edge Function (`supabase/functions/process-reminders`)
- **Timing**: Should run every minute via cron job
- **Process**: 
  1. Queries reminders where `scheduled_for` ≤ current time
  2. Creates notification in `notifications` table
  3. Sends push notification if user has subscription
  4. Marks reminder as sent
  5. Creates next occurrence for recurring reminders

## Notification Types

### Available Types
- **achievement**: Unlocked achievements, milestones
- **progress**: Learning progress updates, streaks
- **reminder**: Study session reminders, review notifications
- **system**: App updates, maintenance notices
- **social**: Future use for social features

### Helper Methods
Each type has a dedicated helper method in `notificationService.ts`:
- `notifyAchievement(userId, title, message, data)`
- `notifyProgress(userId, title, message, data)`
- `notifyReminder(userId, title, message, data)`
- `notifySystem(userId, title, message, data)`

These methods automatically check user preferences before creating notifications.

## User Preferences

### Preference Settings
Users can control notifications through `notification_preferences` table:
- `email_notifications`: Email digest (future feature)
- `push_notifications`: Browser push notifications
- `achievement_notifications`: Achievement unlocks
- `progress_notifications`: Progress updates
- `reminder_notifications`: Study reminders
- `system_notifications`: System updates

### Study Schedule Settings
Users can set their preferred study times:
- Preferred days of the week
- Preferred time of day
- Session duration (minutes)
- Cards per session
- Auto-schedule spaced repetition reviews
- Include overdue cards

## User Interface Components

### Components
1. **StudyReminderModal** - Create/edit reminders
2. **StudyRemindersPanel** - View upcoming and overdue reminders
3. **NotificationSettingsPage** - Manage all notification preferences
4. **NotificationDropdown** - View recent notifications

### Features
- One-time and recurring reminders
- Custom day selection for recurring reminders
- Priority levels (low, medium, high)
- Duration estimates
- Complete/dismiss/delete actions

## Push Notifications

### Setup Requirements
1. Generate VAPID keys:
   ```bash
   npx web-push generate-vapid-keys
   ```

2. Add to environment variables:
   ```
   REACT_APP_VAPID_PUBLIC_KEY=your_public_key_here
   ```

3. Service worker must be registered (handled automatically)

### Browser Support
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Limited support (no background notifications)

## Notification History

The system maintains comprehensive history through multiple tables:

### What's Tracked
1. **Notification Creation**: When each notification was created (`notifications.created_at`)
2. **Read Status**: Whether user has seen the notification (`notifications.is_read`)
3. **Reminder Delivery**: When reminder was sent (`study_reminders.reminder_sent_at`)
4. **User Actions**: 
   - Completed (`study_reminders.completed_at`)
   - Dismissed (`study_reminders.dismissed_at`)
5. **Delivery Status**: Success/failure of push notifications (`notification_queue.status`)
6. **Retry Attempts**: Failed delivery attempts (`notification_queue.attempts`)

### Analytics Capabilities
- Track notification engagement rates
- Monitor delivery success rates
- Analyze user study patterns
- Identify optimal reminder times

## Edge Function Processing

The `process-reminders` Edge Function handles:
1. Querying due reminders
2. Creating in-app notifications
3. Sending push notifications
4. Marking reminders as sent
5. Creating recurring reminder instances

### Deployment
```bash
supabase functions deploy process-reminders
```

### Scheduling
Set up a cron job to run every minute:
- Processes all due reminders
- Handles retries for failed deliveries
- Creates audit trail in notification_queue

## Best Practices

### Performance
- Notifications are cached locally for offline access
- Exponential backoff for failed requests
- Batch processing in Edge Function

### User Experience
- Respect user preferences for notification types
- Use appropriate notification priorities
- Provide clear opt-out options
- Include actionable content in notifications

### Security
- RLS policies ensure users only see their own notifications
- VAPID keys authenticate push subscriptions
- Endpoints are validated before sending

## Troubleshooting

### Common Issues

1. **Push notifications not working**
   - Check browser permissions
   - Verify VAPID keys are set
   - Ensure service worker is registered

2. **Reminders not triggering**
   - Verify Edge Function is deployed
   - Check cron job is running
   - Review notification_queue for errors

3. **Notifications not syncing**
   - Check network connectivity
   - Review browser console for errors
   - Verify Supabase connection

### Debug Tools
- Check `notification_queue` table for delivery status
- Review `study_reminders.reminder_sent_at` for timing issues
- Monitor Edge Function logs in Supabase dashboard

## Future Enhancements

### Planned Features
- Email notification digests
- SMS notifications (via Twilio)
- In-app notification sounds
- Notification grouping/bundling
- Smart reminder timing based on user activity
- Achievement celebration animations

### Integration Opportunities
- Calendar app integration
- Mobile app push notifications
- Slack/Discord webhooks
- Parent/teacher notification options