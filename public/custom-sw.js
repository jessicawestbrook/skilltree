// Push notification event listeners
self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');
  
  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data = { title: 'NeuroQuest', body: event.data.text() };
    }
  }

  const title = data.title || 'NeuroQuest';
  const options = {
    body: data.body || 'You have a new notification',
    icon: data.icon || '/icon-192x192.png',
    badge: data.badge || '/icon-192x192.png',
    vibrate: data.vibrate || [200, 100, 200],
    data: data.data || {},
    tag: data.tag || 'default',
    requireInteraction: data.requireInteraction || false,
    actions: data.actions || [],
    image: data.image,
    timestamp: data.timestamp || Date.now()
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', function(event) {
  console.log('[Service Worker] Notification click received.');
  
  event.notification.close();

  const action = event.action;
  const notification = event.notification;
  const data = notification.data || {};

  let targetUrl = '/';

  // Handle different actions
  if (action === 'open' || !action) {
    // Default action - open the app
    if (data.url) {
      targetUrl = data.url;
    } else if (data.nodeId) {
      targetUrl = `/?node=${data.nodeId}`;
    }
  } else if (action === 'later') {
    // Schedule a reminder for later
    scheduleReminder();
    return;
  }

  // Open or focus the app
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(function(clientList) {
        // Check if app is already open
        for (let client of clientList) {
          if (client.url.includes(self.registration.scope) && 'focus' in client) {
            client.focus();
            if (targetUrl !== '/') {
              client.navigate(targetUrl);
            }
            return;
          }
        }
        // App not open, open new window
        if (clients.openWindow) {
          return clients.openWindow(targetUrl);
        }
      })
  );
});

// Handle notification close
self.addEventListener('notificationclose', function(event) {
  console.log('[Service Worker] Notification closed', event);
  
  // Track notification dismissal if needed
  const data = event.notification.data || {};
  if (data.trackDismissal) {
    // Send analytics event
    fetch('/api/analytics/notification-dismissed', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tag: event.notification.tag,
        timestamp: Date.now()
      })
    }).catch(err => console.error('Failed to track dismissal:', err));
  }
});

// Background sync for offline notifications
self.addEventListener('sync', function(event) {
  if (event.tag === 'send-notifications') {
    event.waitUntil(sendQueuedNotifications());
  }
});

// Helper function to schedule a reminder
function scheduleReminder() {
  // Store reminder request in IndexedDB or similar
  // This would be implemented based on your needs
  console.log('Reminder scheduled for later');
}

// Helper function to send queued notifications
async function sendQueuedNotifications() {
  // Implement logic to send queued notifications
  // when connection is restored
  console.log('Sending queued notifications');
}

// Periodic background sync for daily reminders
self.addEventListener('periodicsync', function(event) {
  if (event.tag === 'daily-reminder') {
    event.waitUntil(
      self.registration.showNotification('🧠 Time to Learn!', {
        body: 'Continue your journey in NeuroQuest!',
        icon: '/icon-192x192.png',
        badge: '/icon-192x192.png',
        tag: 'daily-reminder',
        requireInteraction: false,
        actions: [
          { action: 'open', title: 'Start Learning', icon: '/icon-192x192.png' }
        ]
      })
    );
  }
});

// Message handler for communication with the app
self.addEventListener('message', function(event) {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'TEST_NOTIFICATION') {
    self.registration.showNotification('Test Notification', {
      body: 'Push notifications are working!',
      icon: '/icon-192x192.png',
      badge: '/icon-192x192.png'
    });
  }
});