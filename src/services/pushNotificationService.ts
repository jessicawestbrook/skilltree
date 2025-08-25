import { supabase } from './supabase'

// VAPID public key (you'll need to generate this and store in environment)
const VAPID_PUBLIC_KEY = process.env.REACT_APP_VAPID_PUBLIC_KEY || ''

export interface PushSubscriptionData {
  endpoint: string
  keys: {
    p256dh: string
    auth: string
  }
}

class PushNotificationService {
  private swRegistration: ServiceWorkerRegistration | null = null

  /**
   * Check if push notifications are supported
   */
  isSupported(): boolean {
    return 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window
  }

  /**
   * Get current notification permission status
   */
  getPermissionStatus(): NotificationPermission {
    return Notification.permission
  }

  /**
   * Request notification permission from user
   */
  async requestPermission(): Promise<NotificationPermission> {
    if (!this.isSupported()) {
      console.warn('Push notifications are not supported in this browser')
      return 'denied'
    }

    try {
      const permission = await Notification.requestPermission()
      console.log('Notification permission:', permission)
      return permission
    } catch (error) {
      console.error('Error requesting notification permission:', error)
      return 'denied'
    }
  }

  /**
   * Register service worker and initialize push notifications
   */
  async initialize(): Promise<boolean> {
    if (!this.isSupported()) {
      console.warn('Push notifications are not supported')
      return false
    }

    try {
      // Register service worker
      const registration = await navigator.serviceWorker.ready
      this.swRegistration = registration
      console.log('Service worker registered:', registration)

      // Check permission
      if (this.getPermissionStatus() === 'granted') {
        await this.subscribeToPush()
      }

      return true
    } catch (error) {
      console.error('Error initializing push notifications:', error)
      return false
    }
  }

  /**
   * Subscribe to push notifications
   */
  async subscribeToPush(): Promise<PushSubscription | null> {
    if (!this.swRegistration) {
      console.error('Service worker not registered')
      return null
    }

    if (this.getPermissionStatus() !== 'granted') {
      console.warn('Notification permission not granted')
      return null
    }

    try {
      // Check for existing subscription
      let subscription = await this.swRegistration.pushManager.getSubscription()

      if (!subscription) {
        // Create new subscription
        const vapidKey = this.urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
        
        subscription = await this.swRegistration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: vapidKey
        })

        console.log('Push subscription created:', subscription)
      }

      // Save subscription to database
      await this.saveSubscription(subscription)

      return subscription
    } catch (error) {
      console.error('Error subscribing to push notifications:', error)
      return null
    }
  }

  /**
   * Unsubscribe from push notifications
   */
  async unsubscribe(): Promise<boolean> {
    if (!this.swRegistration) {
      return false
    }

    try {
      const subscription = await this.swRegistration.pushManager.getSubscription()
      
      if (subscription) {
        await subscription.unsubscribe()
        await this.removeSubscription(subscription.endpoint)
        console.log('Unsubscribed from push notifications')
        return true
      }

      return false
    } catch (error) {
      console.error('Error unsubscribing from push notifications:', error)
      return false
    }
  }

  /**
   * Save push subscription to database
   */
  private async saveSubscription(subscription: PushSubscription): Promise<void> {
    try {
      const { data: { session } } = await (supabase.auth as any).getSession()
      if (!session?.user) return
      const user = session.user

      const subscriptionData = subscription.toJSON()
      
      const { error } = await supabase
        .from('push_subscriptions')
        .upsert({
          user_id: user.id,
          endpoint: subscriptionData.endpoint,
          p256dh: subscriptionData.keys?.p256dh,
          auth: subscriptionData.keys?.auth,
          user_agent: navigator.userAgent,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }, {
          onConflict: 'user_id,endpoint'
        })

      if (error) {
        console.error('Error saving push subscription:', error)
      }
    } catch (error) {
      console.error('Error saving push subscription:', error)
    }
  }

  /**
   * Remove push subscription from database
   */
  private async removeSubscription(endpoint: string): Promise<void> {
    try {
      const { data: { session } } = await (supabase.auth as any).getSession()
      if (!session?.user) return
      const user = session.user

      const { error } = await supabase
        .from('push_subscriptions')
        .delete()
        .eq('user_id', user.id)
        .eq('endpoint', endpoint)

      if (error) {
        console.error('Error removing push subscription:', error)
      }
    } catch (error) {
      console.error('Error removing push subscription:', error)
    }
  }

  /**
   * Show local notification (for testing)
   */
  async showNotification(title: string, options?: NotificationOptions): Promise<void> {
    if (!this.swRegistration || this.getPermissionStatus() !== 'granted') {
      console.warn('Cannot show notification')
      return
    }

    try {
      await this.swRegistration.showNotification(title, {
        icon: '/icon-192x192.png',
        badge: '/icon-72x72.png',
        vibrate: [200, 100, 200],
        tag: 'study-reminder',
        renotify: true,
        requireInteraction: true,
        ...options
      })
    } catch (error) {
      console.error('Error showing notification:', error)
    }
  }

  /**
   * Convert VAPID key from base64 to Uint8Array
   */
  private urlBase64ToUint8Array(base64String: string): Uint8Array {
    const padding = '='.repeat((4 - base64String.length % 4) % 4)
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/')

    const rawData = window.atob(base64)
    const outputArray = new Uint8Array(rawData.length)

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i)
    }
    
    return outputArray
  }

  /**
   * Check if push notifications are enabled for current user
   */
  async isPushEnabled(): Promise<boolean> {
    if (!this.swRegistration) return false

    try {
      const subscription = await this.swRegistration.pushManager.getSubscription()
      return subscription !== null
    } catch (error) {
      console.error('Error checking push subscription:', error)
      return false
    }
  }

  /**
   * Handle incoming push notification click
   */
  async handleNotificationClick(event: any): Promise<void> {
    const notification = event.notification
    const data = notification.data || {}

    // Close the notification
    notification.close()

    // Handle different notification types
    if (data.reminder_id) {
      // Open the study page for this reminder
      const url = `/study?reminder=${data.reminder_id}`
      await this.openUrl(url)
    } else if (data.url) {
      // Open custom URL
      await this.openUrl(data.url)
    } else {
      // Open app homepage
      await this.openUrl('/')
    }
  }

  /**
   * Open URL in app window
   * Note: This method is intended to be called from a service worker context
   */
  private async openUrl(url: string): Promise<void> {
    // This function would be called from service worker context
    // where 'self' refers to ServiceWorkerGlobalScope
    // For now, we'll just open in a new window from the browser context
    window.open(url, '_blank')
  }
}

export const pushNotificationService = new PushNotificationService()