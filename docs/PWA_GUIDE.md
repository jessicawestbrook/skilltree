# Progressive Web App (PWA) Guide

NeuroQuest is now a fully-featured Progressive Web App (PWA) that provides a native app-like experience with offline functionality, push notifications, and installability across all platforms.

## Features

### ✨ **Core PWA Features**
- **📱 Installable**: Can be installed on any device (mobile, tablet, desktop)
- **🌐 Offline Support**: Works without internet connection
- **⚡ Fast Loading**: Optimized caching for instant loading
- **🔄 Background Sync**: Syncs data when connection is restored
- **🔔 Push Notifications**: Real-time notifications for learning reminders
- **🔄 Auto Updates**: Automatic updates with user notification

### 🎯 **Learning-Specific Features**
- **📚 Offline Content**: Download courses for offline learning
- **💾 Progress Sync**: Learning progress saved locally and synced
- **📊 Cached Analytics**: Track performance even offline
- **🎮 Quiz Continuity**: Complete quizzes offline, sync when online

## Installation

### 📱 **Mobile Installation**

#### iOS (Safari)
1. Open NeuroQuest in Safari
2. Tap the **Share** button (square with arrow)
3. Scroll down and tap **"Add to Home Screen"**
4. Tap **"Add"** to install

#### Android (Chrome)
1. Open NeuroQuest in Chrome
2. Tap the **menu** (three dots)
3. Tap **"Add to Home screen"** or **"Install app"**
4. Tap **"Install"** when prompted

### 💻 **Desktop Installation**

#### Chrome/Edge
1. Look for the **install icon** in the address bar
2. Click the icon and select **"Install NeuroQuest"**
3. Or use the **"Install NeuroQuest"** prompt when it appears

#### Firefox
1. Look for the **install icon** in the address bar
2. Click and follow the installation prompts

## Offline Functionality

### 🔄 **What Works Offline**

#### ✅ **Fully Available**
- Previously viewed courses and lessons
- Downloaded quizzes and assessments
- Learning progress tracking
- User profile and settings
- Cached knowledge graph
- Basic navigation

#### 📶 **Limited/Queued**
- New course downloads
- Quiz submissions (queued for sync)
- Progress updates (saved locally)
- Social features (friends, sharing)

### 💾 **Data Storage**
- **Local Storage**: User preferences and settings
- **IndexedDB**: Course content, quiz data, progress
- **Service Worker Cache**: Static assets, pages, API responses

### 🔄 **Background Sync**
When you go back online, the app automatically:
- Syncs quiz submissions
- Updates learning progress
- Downloads new content
- Refreshes cached data

## Caching Strategy

### 🚀 **Performance Optimizations**

#### **Cache First** (Fastest)
- Static assets (images, fonts, icons)
- Downloaded course content
- App shell components

#### **Network First** (Fresh Data)
- API endpoints
- User-generated content
- Real-time data

#### **Stale While Revalidate** (Balanced)
- Course listings
- Navigation data
- Non-critical updates

## Usage Guide

### 🎯 **Getting Started**

1. **Browse Normally**: Use NeuroQuest as usual in your browser
2. **Install Prompt**: Accept the installation prompt when it appears
3. **Download Content**: Use the "Download for Offline" feature on courses
4. **Go Offline**: The app continues working without internet

### 📱 **PWA-Specific Features**

#### **Install Prompt**
- Appears after 5 seconds on supported browsers
- Can be dismissed and will reappear after 7 days
- Manual installation always available in browser menu

#### **Update Notifications**
- Automatic check for updates every 30 seconds
- User prompt when new version is available
- Seamless updates without data loss

#### **Offline Indicator**
- Red banner appears when offline
- Shows available offline features
- Disappears when connection is restored

### 🔧 **Managing PWA**

#### **Storage Management**
```javascript
// Check storage usage
navigator.storage.estimate().then(estimate => {
  console.log('Used:', estimate.usage);
  console.log('Quota:', estimate.quota);
});
```

#### **Clear Cache** (if needed)
1. Go to browser settings
2. Find "Storage" or "Site Data"
3. Select NeuroQuest
4. Clear data (will re-download on next visit)

## Development

### 🛠️ **Technical Details**

#### **Service Worker** (`/public/sw.js`)
- Handles caching strategies
- Manages offline functionality  
- Processes background sync
- Handles push notifications

#### **Web App Manifest** (`/public/manifest.json`)
- Defines app metadata
- Specifies icons and display modes
- Configures shortcuts and categories

#### **PWA Hooks** (`/src/hooks/usePWA.ts`)
- `usePWA()`: Installation and online status
- `useServiceWorker()`: Update management
- `useOfflineStorage()`: Local data storage
- `usePushNotifications()`: Notification handling

### 📦 **Build Configuration**

#### **Next.js PWA Plugin**
```typescript
// next.config.ts
const withPWA = withPWAInit({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
  // ... caching strategies
});
```

#### **Runtime Caching**
- **Google Fonts**: 1 year cache
- **Static Assets**: 24 hour cache with revalidation
- **API Calls**: Network first with 10s timeout
- **Images**: Stale while revalidate

### 🔄 **Development Mode**
PWA features are **disabled in development** to avoid conflicts with hot reloading:
- Service worker registration skipped
- No caching in development
- Install prompts disabled

## Browser Support

### ✅ **Full Support**
- **Chrome** 67+ (Android/Desktop)
- **Safari** 11.1+ (iOS/macOS)
- **Firefox** 60+ (Android/Desktop)
- **Edge** 79+ (Desktop/Mobile)

### ⚠️ **Limited Support**
- **Firefox iOS**: Basic PWA features
- **Internet Explorer**: Not supported
- **Older browsers**: Graceful degradation

## Troubleshooting

### 🔧 **Common Issues**

#### **Install Button Not Showing**
1. Check browser compatibility
2. Ensure HTTPS connection
3. Wait for automatic prompt (5 seconds)
4. Clear browser cache and reload

#### **Offline Features Not Working**
1. Check service worker registration in DevTools
2. Verify IndexedDB permissions
3. Ensure content was downloaded while online
4. Check console for error messages

#### **Updates Not Appearing**
1. Force refresh (Ctrl+F5 or Cmd+Shift+R)
2. Clear service worker cache in DevTools
3. Check "Update on reload" in DevTools > Application > Service Workers

#### **Storage Issues**
1. Check available storage quota
2. Clear unnecessary cached data
3. Download only essential content for offline use

### 🔍 **Debugging**

#### **Chrome DevTools**
1. Open DevTools (F12)
2. Go to **Application** tab
3. Check:
   - **Service Workers**: Registration status
   - **Storage**: Usage and quotas
   - **Cache Storage**: Cached resources
   - **IndexedDB**: Offline data

#### **Lighthouse PWA Audit**
1. Open DevTools
2. Go to **Lighthouse** tab
3. Select **Progressive Web App**
4. Click **Generate report**

## Best Practices

### 📱 **User Experience**
1. **Download Content**: Always download key courses before going offline
2. **Sync Regularly**: Connect to internet periodically to sync progress
3. **Update Promptly**: Accept app updates for best experience
4. **Storage Management**: Monitor storage usage in settings

### 🔒 **Privacy & Security**
- All offline data encrypted locally
- No personal data sent without consent
- Cache cleared on logout
- Secure HTTPS required for all PWA features

### ⚡ **Performance**
- Download only needed content for offline use
- Regular cache cleanup automatically performed
- Background sync minimizes data usage
- Smart caching reduces loading times

## API Reference

### 🎯 **PWA Context**
```typescript
const {
  isInstalled,      // App is installed
  isInstallable,    // Can be installed
  isOnline,         // Network status
  isUpdateAvailable, // Update ready
  install,          // Trigger installation
  updateApp,        // Apply update
} = usePWAContext();
```

### 💾 **Offline Storage**
```typescript
const {
  storeQuizSubmission,  // Save quiz offline
  storeProgressUpdate,  // Save progress offline
  storeContent,         // Cache content
  getStoredContent,     // Retrieve cached content
} = usePWAContext();
```

## Resources

- [PWA Best Practices](https://web.dev/pwa-checklist/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [IndexedDB Guide](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)

---

**Need Help?** If you encounter any issues with PWA functionality, please check the troubleshooting section above or contact our support team.