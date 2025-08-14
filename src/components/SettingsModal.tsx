'use client';

import React, { useState } from 'react';
import { X, Sun, Moon, Monitor, Bell, Palette, User, Mail, LogOut, Edit3, Save, Calendar, Cake } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useAuth } from '../contexts/AuthContext';
import { NotificationSettings } from './NotificationSettings';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type SettingsTab = 'profile' | 'appearance' | 'notifications';

export const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose }) => {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const { user, logout, updateProfile, isLoading } = useAuth();
  const [activeTab, setActiveTab] = useState<SettingsTab>('profile');
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    username: user?.username || '',
    birthYear: user?.birthYear || new Date().getFullYear() - 18
  });

  if (!isOpen) return null;

  const handleLogout = async () => {
    await logout();
    onClose();
  };

  const handleSave = async () => {
    const result = await updateProfile(editForm);
    if (result.success) {
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setEditForm({
      username: user?.username || '',
      birthYear: user?.birthYear || new Date().getFullYear() - 18
    });
    setIsEditing(false);
  };

  const calculateAge = (birthYear?: number) => {
    if (!birthYear) return null;
    const currentYear = new Date().getFullYear();
    return currentYear - birthYear;
  };

  const age = calculateAge(user?.birthYear);

  const tabs = [
    { id: 'profile' as SettingsTab, label: 'Profile', icon: User },
    { id: 'appearance' as SettingsTab, label: 'Appearance', icon: Palette },
    { id: 'notifications' as SettingsTab, label: 'Notifications', icon: Bell },
  ];

  const themeOptions = [
    { value: 'light' as const, label: 'Light', icon: Sun },
    { value: 'dark' as const, label: 'Dark', icon: Moon },
    { value: 'system' as const, label: 'System', icon: Monitor },
  ];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[9999] p-4">
      <div className="bg-white dark:bg-gray-900 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Settings</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
        </div>

        <div className="flex h-[calc(90vh-80px)]">
          {/* Sidebar */}
          <div className="w-64 border-r border-gray-200 dark:border-gray-700 p-4">
            <nav className="space-y-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-forest-100 dark:bg-forest-900/30 text-forest-700 dark:text-forest-400'
                        : 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {activeTab === 'profile' && user && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-6">
                  Profile Settings
                </h3>
                
                <div className="space-y-6">
                  {/* Avatar */}
                  <div className="flex justify-center mb-6">
                    <div className="w-24 h-24 rounded-full bg-gradient-to-r from-forest-600 to-sky-600 flex items-center justify-center">
                      <User className="w-12 h-12 text-white" />
                    </div>
                  </div>

                  {/* Profile Information */}
                  <div className="space-y-4">
                    {/* Email */}
                    <div className="flex items-center gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <Mail className="w-5 h-5 text-forest-600 dark:text-forest-400" />
                      <div className="flex-1">
                        <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Email</label>
                        <div className="text-gray-900 dark:text-gray-100">{user.email}</div>
                      </div>
                    </div>

                    {/* Username */}
                    <div className="flex items-center gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <User className="w-5 h-5 text-forest-600 dark:text-forest-400" />
                      <div className="flex-1">
                        <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Username</label>
                        {isEditing ? (
                          <input
                            type="text"
                            value={editForm.username}
                            onChange={(e) => setEditForm(prev => ({ ...prev, username: e.target.value }))}
                            className="w-full mt-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100"
                          />
                        ) : (
                          <div className="text-gray-900 dark:text-gray-100">{user.username}</div>
                        )}
                      </div>
                    </div>

                    {/* Age */}
                    <div className="flex items-center gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <Cake className="w-5 h-5 text-forest-600 dark:text-forest-400" />
                      <div className="flex-1">
                        <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Age</label>
                        {isEditing ? (
                          <input
                            type="number"
                            value={editForm.birthYear}
                            onChange={(e) => setEditForm(prev => ({ ...prev, birthYear: parseInt(e.target.value) }))}
                            min={1900}
                            max={new Date().getFullYear()}
                            className="w-full mt-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100"
                          />
                        ) : (
                          <div className="text-gray-900 dark:text-gray-100">
                            {age ? `${age} years old` : 'Not set'}
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Member Since */}
                    <div className="flex items-center gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <Calendar className="w-5 h-5 text-forest-600 dark:text-forest-400" />
                      <div className="flex-1">
                        <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Member Since</label>
                        <div className="text-gray-900 dark:text-gray-100">
                          {new Date(user.createdAt).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-4 pt-4">
                    {isEditing ? (
                      <>
                        <button
                          onClick={handleSave}
                          disabled={isLoading}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-forest-600 to-sky-600 text-white rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
                        >
                          <Save className="w-4 h-4" />
                          Save Changes
                        </button>
                        <button
                          onClick={handleCancel}
                          disabled={isLoading}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors disabled:opacity-50"
                        >
                          <X className="w-4 h-4" />
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => setIsEditing(true)}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-forest-600 to-sky-600 text-white rounded-lg hover:shadow-lg transition-all"
                        >
                          <Edit3 className="w-4 h-4" />
                          Edit Profile
                        </button>
                        <button
                          onClick={handleLogout}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                        >
                          <LogOut className="w-4 h-4" />
                          Sign Out
                        </button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'appearance' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-6">
                  Appearance Settings
                </h3>
                
                <div className="space-y-6">
                  {/* Theme Selection */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                      Theme
                    </label>
                    <div className="grid grid-cols-3 gap-4">
                      {themeOptions.map((option) => {
                        const Icon = option.icon;
                        const isSelected = theme === option.value;
                        return (
                          <button
                            key={option.value}
                            onClick={() => setTheme(option.value)}
                            className={`p-4 rounded-lg border-2 transition-all ${
                              isSelected
                                ? 'border-forest-600 bg-forest-50 dark:bg-forest-900/20'
                                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                            }`}
                          >
                            <Icon className={`w-6 h-6 mx-auto mb-2 ${
                              isSelected 
                                ? 'text-forest-600 dark:text-forest-400' 
                                : 'text-gray-600 dark:text-gray-400'
                            }`} />
                            <div className={`text-sm font-medium ${
                              isSelected
                                ? 'text-forest-700 dark:text-forest-300'
                                : 'text-gray-700 dark:text-gray-300'
                            }`}>
                              {option.label}
                            </div>
                            {option.value === 'system' && (
                              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                Currently: {resolvedTheme}
                              </div>
                            )}
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Preview */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                      Preview
                    </label>
                    <div className="p-6 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                      <div className="space-y-4">
                        <div className="flex items-center gap-3">
                          <div className="w-12 h-12 rounded-full bg-gradient-to-r from-forest-600 to-sky-600"></div>
                          <div>
                            <div className="h-4 bg-gray-900 dark:bg-gray-100 rounded w-32 mb-2"></div>
                            <div className="h-3 bg-gray-400 dark:bg-gray-500 rounded w-48"></div>
                          </div>
                        </div>
                        <div className="grid grid-cols-3 gap-2">
                          <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
                          <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
                          <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'notifications' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-6">
                  Notification Settings
                </h3>
                <NotificationSettings />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};