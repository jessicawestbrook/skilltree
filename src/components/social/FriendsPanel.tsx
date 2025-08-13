'use client';

import React, { useState, useEffect } from 'react';
import { Users, UserPlus, Check, X, Send, Search } from 'lucide-react';

interface Friend {
  id: string;
  friend_id: string;
  friendship_date: string;
  friend: {
    id: string;
    email: string;
    user_profiles: {
      username: string;
      avatar_url: string;
      bio: string;
      neural_level: number;
      total_points: number;
    };
  };
}

interface FriendRequest {
  id: string;
  sender_id: string;
  receiver_id: string;
  status: string;
  message?: string;
  created_at: string;
  sender?: any;
  receiver?: any;
}

export default function FriendsPanel() {
  const [activeTab, setActiveTab] = useState<'friends' | 'requests' | 'find'>('friends');
  const [friends, setFriends] = useState<Friend[]>([]);
  const [friendRequests, setFriendRequests] = useState<FriendRequest[]>([]);
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchFriends();
    fetchFriendRequests();
  }, []);

  const fetchFriends = async () => {
    try {
      const response = await fetch('/api/friends/list');
      const data = await response.json();
      if (response.ok) {
        setFriends(data.friends || []);
        setSuggestions(data.suggestions || []);
      }
    } catch (error) {
      console.error('Error fetching friends:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFriendRequests = async () => {
    try {
      const response = await fetch('/api/friends/request?type=received');
      const data = await response.json();
      if (response.ok) {
        setFriendRequests(data.data?.filter((r: FriendRequest) => r.status === 'pending') || []);
      }
    } catch (error) {
      console.error('Error fetching friend requests:', error);
    }
  };

  const sendFriendRequest = async (receiverId: string) => {
    try {
      const response = await fetch('/api/friends/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receiverId })
      });
      
      if (response.ok) {
        // Remove from suggestions
        setSuggestions(prev => prev.filter(s => s.suggested_user_id !== receiverId));
      }
    } catch (error) {
      console.error('Error sending friend request:', error);
    }
  };

  const respondToRequest = async (requestId: string, action: 'accepted' | 'declined') => {
    try {
      const response = await fetch('/api/friends/respond', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requestId, action })
      });
      
      if (response.ok) {
        setFriendRequests(prev => prev.filter(r => r.id !== requestId));
        if (action === 'accepted') {
          fetchFriends();
        }
      }
    } catch (error) {
      console.error('Error responding to friend request:', error);
    }
  };

  const removeFriend = async (friendId: string) => {
    if (!confirm('Are you sure you want to remove this friend?')) return;
    
    try {
      const response = await fetch('/api/friends/list', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ friendId })
      });
      
      if (response.ok) {
        setFriends(prev => prev.filter(f => f.friend_id !== friendId));
      }
    } catch (error) {
      console.error('Error removing friend:', error);
    }
  };

  const filteredFriends = friends.filter(f => 
    !searchQuery || 
    f.friend.user_profiles?.username?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    f.friend.email.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Users className="w-6 h-6" />
          Friends
        </h2>
        {friendRequests.length > 0 && (
          <span className="bg-red-500 text-white px-2 py-1 rounded-full text-sm">
            {friendRequests.length} new
          </span>
        )}
      </div>

      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('friends')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            activeTab === 'friends'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Friends ({friends.length})
        </button>
        <button
          onClick={() => setActiveTab('requests')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors relative ${
            activeTab === 'requests'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Requests
          {friendRequests.length > 0 && (
            <span className="absolute -top-1 -right-1 bg-red-500 text-white w-5 h-5 rounded-full text-xs flex items-center justify-center">
              {friendRequests.length}
            </span>
          )}
        </button>
        <button
          onClick={() => setActiveTab('find')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            activeTab === 'find'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Find Friends
        </button>
      </div>

      {activeTab === 'friends' && (
        <div>
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search friends..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              />
            </div>
          </div>

          <div className="space-y-3">
            {filteredFriends.length === 0 ? (
              <p className="text-center text-gray-500 py-8">
                {searchQuery ? 'No friends found' : 'No friends yet. Start connecting!'}
              </p>
            ) : (
              filteredFriends.map((friend) => (
                <div key={friend.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-bold">
                      {friend.friend.user_profiles?.username?.[0]?.toUpperCase() || '?'}
                    </div>
                    <div>
                      <p className="font-semibold">
                        {friend.friend.user_profiles?.username || friend.friend.email}
                      </p>
                      <p className="text-sm text-gray-500">
                        Level {friend.friend.user_profiles?.neural_level || 1} • {friend.friend.user_profiles?.total_points || 0} points
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeFriend(friend.friend_id)}
                    className="text-red-500 hover:text-red-600 p-2"
                    title="Remove friend"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {activeTab === 'requests' && (
        <div className="space-y-3">
          {friendRequests.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No pending friend requests</p>
          ) : (
            friendRequests.map((request) => (
              <div key={request.id} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold">{request.sender?.email}</p>
                    {request.message && (
                      <p className="text-sm text-gray-500 mt-1">{request.message}</p>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => respondToRequest(request.id, 'accepted')}
                      className="p-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
                      title="Accept"
                    >
                      <Check className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => respondToRequest(request.id, 'declined')}
                      className="p-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                      title="Decline"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'find' && (
        <div className="space-y-3">
          <h3 className="font-semibold mb-3">Suggested Friends</h3>
          {suggestions.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No suggestions available</p>
          ) : (
            suggestions.map((suggestion) => (
              <div key={suggestion.suggested_user_id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div>
                  <p className="font-semibold">User {suggestion.suggested_user_id.slice(0, 8)}</p>
                  <p className="text-sm text-gray-500">
                    {suggestion.common_groups > 0 && `${suggestion.common_groups} common groups • `}
                    {suggestion.common_nodes} topics in common
                  </p>
                </div>
                <button
                  onClick={() => sendFriendRequest(suggestion.suggested_user_id)}
                  className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                  title="Send friend request"
                >
                  <UserPlus className="w-5 h-5" />
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}