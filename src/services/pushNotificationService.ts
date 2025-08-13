import { supabase } from '@/lib/supabase';

interface PushSubscription {
  endpoint: string;
  keys: {
    p256dh: string;
    auth: string;
  };
}

interface NotificationOptions {
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

class PushNotificationService {
  private static instance: PushNotificationService;
  private swRegistration: ServiceWorkerRegistration | null = null;
  private isSupported: boolean = false;

  private constructor() {
    // Check if we're in a browser environment
    if (typeof window !== 'undefined') {
      this.isSupported = 'Notification' in window && 'serviceWorker' in navigator && 'PushManager' in window;
    }
  }

  static getInstance(): PushNotificationService {
    if (!PushNotificationService.instance) {
      PushNotificationService.instance = new PushNotificationService();
    }
    return PushNotificationService.instance;
  }

  async initialize(): Promise<boolean> {
    if (!this.isSupported) {
      console.log('Push notifications are not supported in this browser');
      return false;
    }

    try {
      // Wait for service worker to be ready
      this.swRegistration = await navigator.serviceWorker.ready;
      console.log('Push notification service initialized');
      return true;
    } catch (error) {
      console.error('Failed to initialize push notifications:', error);
      return false;
    }
  }

  async requestPermission(): Promise<NotificationPermission> {
    if (!this.isSupported) {
      return 'denied';
    }

    try {
      const permission = await Notification.requestPermission();
      console.log('Notification permission:', permission);
      
      if (permission === 'granted') {
        await this.subscribeUser();
      }
      
      return permission;
    } catch (error) {
      console.error('Error requesting notification permission:', error);
      return 'denied';
    }
  }

  async subscribeUser(): Promise<PushSubscription | null> {
    if (!this.swRegistration) {
      await this.initialize();
    }

    if (!this.swRegistration) {
      console.error('Service worker not registered');
      return null;
    }

    try {
      // Check if already subscribed
      let subscription = await this.swRegistration.pushManager.getSubscription();
      
      if (!subscription) {
        // Create new subscription
        const vapidPublicKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;
        
        if (!vapidPublicKey) {
          console.warn('VAPID public key not configured. Using local notifications only.');
          return null;
        }

        const convertedVapidKey = this.urlBase64ToUint8Array(vapidPublicKey);
        
        subscription = await this.swRegistration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: convertedVapidKey as BufferSource
        });
      }

      // Save subscription to database
      const subscriptionJSON = subscription.toJSON();
      if (subscriptionJSON) {
        await this.saveSubscription(subscriptionJSON);
        return subscriptionJSON as PushSubscription;
      }
      return null;
    } catch (error) {
      console.error('Failed to subscribe user:', error);
      return null;
    }
  }

  async unsubscribeUser(): Promise<boolean> {
    if (!this.swRegistration) {
      return false;
    }

    try {
      const subscription = await this.swRegistration.pushManager.getSubscription();
      
      if (subscription) {
        await subscription.unsubscribe();
        await this.removeSubscription();
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Failed to unsubscribe user:', error);
      return false;
    }
  }

  async getSubscription(): Promise<PushSubscription | null> {
    if (!this.swRegistration) {
      return null;
    }

    try {
      const subscription = await this.swRegistration.pushManager.getSubscription();
      return subscription ? subscription.toJSON() as PushSubscription : null;
    } catch (error) {
      console.error('Failed to get subscription:', error);
      return null;
    }
  }

  getPermissionStatus(): NotificationPermission {
    if (!this.isSupported) {
      return 'denied';
    }
    return Notification.permission;
  }

  // Show local notification (doesn't require server)
  async showLocalNotification(options: NotificationOptions): Promise<void> {
    if (!this.swRegistration || Notification.permission !== 'granted') {
      console.warn('Cannot show notification: permissions not granted or SW not ready');
      return;
    }

    try {
      const notificationOptions = {
        body: options.body,
        icon: options.icon || '/icon-192x192.png',
        badge: options.badge || '/icon-192x192.png',
        tag: options.tag,
        data: options.data,
        requireInteraction: options.requireInteraction || false,
        ...(options.actions && { actions: options.actions })
      };
      
      await this.swRegistration.showNotification(options.title, notificationOptions);
    } catch (error) {
      console.error('Failed to show notification:', error);
    }
  }

  // Save subscription to database
  private async saveSubscription(subscription: PushSubscriptionJSON): Promise<void> {
    const { data: { user } } = await supabase.auth.getUser();
    
    if (!user) {
      console.error('User not authenticated');
      return;
    }

    try {
      const { error } = await supabase
        .from('push_subscriptions')
        .upsert({
          user_id: user.id,
          endpoint: subscription.endpoint,
          p256dh: subscription.keys?.p256dh,
          auth: subscription.keys?.auth,
          updated_at: new Date().toISOString()
        }, {
          onConflict: 'user_id'
        });

      if (error) {
        console.error('Failed to save subscription:', error);
      }
    } catch (error) {
      console.error('Failed to save subscription:', error);
    }
  }

  // Remove subscription from database
  private async removeSubscription(): Promise<void> {
    const { data: { user } } = await supabase.auth.getUser();
    
    if (!user) {
      return;
    }

    try {
      await supabase
        .from('push_subscriptions')
        .delete()
        .eq('user_id', user.id);
    } catch (error) {
      console.error('Failed to remove subscription:', error);
    }
  }

  // Helper function to convert VAPID key
  private urlBase64ToUint8Array(base64String: string): Uint8Array {
    if (typeof window === 'undefined') {
      // Return empty array on server side
      return new Uint8Array(0);
    }
    
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const buffer = new ArrayBuffer(rawData.length);
    const outputArray = new Uint8Array(buffer);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  // Notification presets for common scenarios
  async notifyAchievement(achievement: string, description: string): Promise<void> {
    await this.showLocalNotification({
      title: '🏆 Achievement Unlocked!',
      body: `${achievement}: ${description}`,
      tag: 'achievement',
      icon: '/icon-192x192.png',
      requireInteraction: false
    });
  }

  async notifyLevelUp(level: number): Promise<void> {
    await this.showLocalNotification({
      title: '⚡ Level Up!',
      body: `Congratulations! You've reached Neural Level ${level}`,
      tag: 'levelup',
      icon: '/icon-192x192.png',
      requireInteraction: false
    });
  }

  async notifyStreak(days: number): Promise<void> {
    await this.showLocalNotification({
      title: '🔥 Streak Milestone!',
      body: `Amazing! You've maintained a ${days}-day learning streak`,
      tag: 'streak',
      icon: '/icon-192x192.png',
      requireInteraction: false
    });
  }

  async notifyDailyReminder(): Promise<void> {
    await this.showLocalNotification({
      title: '🧠 Time to Learn!',
      body: "Continue your journey in NeuroQuest and keep your streak alive!",
      tag: 'reminder',
      icon: '/icon-192x192.png',
      actions: [
        { action: 'open', title: 'Start Learning' },
        { action: 'later', title: 'Remind Later' }
      ]
    });
  }

  async notifyNewContent(contentType: string, contentName: string): Promise<void> {
    await this.showLocalNotification({
      title: '✨ New Content Available!',
      body: `New ${contentType}: ${contentName} is now available to explore`,
      tag: 'new-content',
      icon: '/icon-192x192.png'
    });
  }

  async notifyFriendActivity(friendName: string, activity: string): Promise<void> {
    await this.showLocalNotification({
      title: '👥 Friend Activity',
      body: `${friendName} ${activity}`,
      tag: 'friend-activity',
      icon: '/icon-192x192.png'
    });
  }
}

export const pushNotificationService = PushNotificationService.getInstance();