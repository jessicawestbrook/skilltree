'use client';

import React, { useState } from 'react';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    siteName: 'NeuroQuest',
    maintenanceMode: false,
    registrationEnabled: true,
    emailNotifications: true,
    autoBackup: true,
    backupFrequency: 'daily',
    maxUploadSize: 10,
    defaultLanguage: 'en',
    theme: 'light'
  });

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // Here you would normally save to database
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Settings</h1>
        <p className="text-gray-600 mt-2">Configure system settings and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* General Settings */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">General Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Site Name
              </label>
              <input
                type="text"
                value={settings.siteName}
                onChange={(e) => setSettings({...settings, siteName: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Default Language
              </label>
              <select
                value={settings.defaultLanguage}
                onChange={(e) => setSettings({...settings, defaultLanguage: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Theme
              </label>
              <select
                value={settings.theme}
                onChange={(e) => setSettings({...settings, theme: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="auto">Auto</option>
              </select>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="maintenance"
                checked={settings.maintenanceMode}
                onChange={(e) => setSettings({...settings, maintenanceMode: e.target.checked})}
                className="w-4 h-4"
              />
              <label htmlFor="maintenance" className="text-sm font-medium text-gray-700">
                Maintenance Mode
              </label>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="registration"
                checked={settings.registrationEnabled}
                onChange={(e) => setSettings({...settings, registrationEnabled: e.target.checked})}
                className="w-4 h-4"
              />
              <label htmlFor="registration" className="text-sm font-medium text-gray-700">
                Enable Registration
              </label>
            </div>
          </div>
        </div>

        {/* System Settings */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">System Settings</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Upload Size (MB)
              </label>
              <input
                type="number"
                value={settings.maxUploadSize}
                onChange={(e) => setSettings({...settings, maxUploadSize: parseInt(e.target.value)})}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                min="1"
                max="100"
              />
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="emailNotif"
                checked={settings.emailNotifications}
                onChange={(e) => setSettings({...settings, emailNotifications: e.target.checked})}
                className="w-4 h-4"
              />
              <label htmlFor="emailNotif" className="text-sm font-medium text-gray-700">
                Email Notifications
              </label>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="autoBackup"
                checked={settings.autoBackup}
                onChange={(e) => setSettings({...settings, autoBackup: e.target.checked})}
                className="w-4 h-4"
              />
              <label htmlFor="autoBackup" className="text-sm font-medium text-gray-700">
                Auto Backup
              </label>
            </div>

            {settings.autoBackup && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Backup Frequency
                </label>
                <select
                  value={settings.backupFrequency}
                  onChange={(e) => setSettings({...settings, backupFrequency: e.target.value})}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="hourly">Hourly</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
            )}
          </div>
        </div>

        {/* Database Info */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Database Information</h2>
          
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-500">Database Type:</span>
              <span className="font-medium">Supabase PostgreSQL</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Status:</span>
              <span className="font-medium text-green-600">Connected</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Last Backup:</span>
              <span className="font-medium">2 hours ago</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Database Size:</span>
              <span className="font-medium">24.5 MB</span>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t">
            <button className="w-full px-4 py-2 bg-blue-50 text-blue-700 rounded hover:bg-blue-100">
              Run Manual Backup
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Quick Actions</h2>
          
          <div className="space-y-3">
            <button className="w-full px-4 py-2 bg-purple-50 text-purple-700 rounded hover:bg-purple-100 text-left">
              🔄 Clear Cache
            </button>
            <button className="w-full px-4 py-2 bg-orange-50 text-orange-700 rounded hover:bg-orange-100 text-left">
              📊 Export Analytics
            </button>
            <button className="w-full px-4 py-2 bg-green-50 text-green-700 rounded hover:bg-green-100 text-left">
              🔍 Run System Check
            </button>
            <button className="w-full px-4 py-2 bg-red-50 text-red-700 rounded hover:bg-red-100 text-left">
              🗑️ Clear Old Logs
            </button>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="mt-8 flex justify-end">
        <button
          onClick={handleSave}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Save Settings
        </button>
      </div>

      {/* Success Message */}
      {saved && (
        <div className="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
          Settings saved successfully!
        </div>
      )}
    </div>
  );
}