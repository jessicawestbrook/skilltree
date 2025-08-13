'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Users, Plus, Lock, Globe } from 'lucide-react';

interface StudyGroup {
  id: string;
  name: string;
  description: string;
  avatar_url?: string;
  owner_id: string;
  max_members: number;
  is_public: boolean;
  join_code: string;
  created_at: string;
  member_count: number;
  user_role?: string;
}

export default function StudyGroupsPanel() {
  const [groups, setGroups] = useState<StudyGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'my-groups' | 'public'>('my-groups');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newGroup, setNewGroup] = useState({
    name: '',
    description: '',
    is_public: true,
    max_members: 20
  });

  const fetchGroups = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/study-groups?filter=${filter}`);
      const data = await response.json();
      if (response.ok) {
        setGroups(data.data || []);
      }
    } catch (error) {
      console.error('Error fetching study groups:', error);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    fetchGroups();
  }, [filter, fetchGroups]);

  const createGroup = async () => {
    if (!newGroup.name.trim()) return;

    try {
      const response = await fetch('/api/study-groups', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newGroup.name,
          description: newGroup.description,
          isPublic: newGroup.is_public,
          maxMembers: newGroup.max_members
        })
      });

      if (response.ok) {
        setShowCreateModal(false);
        setNewGroup({ name: '', description: '', is_public: true, max_members: 20 });
        fetchGroups();
      }
    } catch (error) {
      console.error('Error creating study group:', error);
    }
  };

  const joinGroup = async (groupId: string, joinCode?: string) => {
    try {
      const response = await fetch(`/api/study-groups/${groupId}/join`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ joinCode })
      });

      if (response.ok) {
        fetchGroups();
      }
    } catch (error) {
      console.error('Error joining study group:', error);
    }
  };

  const leaveGroup = async (groupId: string) => {
    if (!confirm('Are you sure you want to leave this group?')) return;

    try {
      const response = await fetch(`/api/study-groups/${groupId}/leave`, {
        method: 'POST'
      });

      if (response.ok) {
        fetchGroups();
      }
    } catch (error) {
      console.error('Error leaving study group:', error);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Users className="w-6 h-6" />
          Study Groups
        </h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          <Plus className="w-5 h-5" />
          Create Group
        </button>
      </div>

      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setFilter('my-groups')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            filter === 'my-groups'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          My Groups
        </button>
        <button
          onClick={() => setFilter('public')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            filter === 'public'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Discover
        </button>
        <button
          onClick={() => setFilter('all')}
          className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
            filter === 'all'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          All Groups
        </button>
      </div>

      {loading ? (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {groups.length === 0 ? (
            <div className="col-span-2 text-center text-gray-500 py-8">
              {filter === 'my-groups' 
                ? 'You haven\'t joined any groups yet' 
                : 'No groups found'}
            </div>
          ) : (
            groups.map((group) => (
              <div key={group.id} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg flex items-center gap-2">
                      {group.name}
                      {group.is_public ? (
                        <Globe className="w-4 h-4 text-green-500" />
                      ) : (
                        <Lock className="w-4 h-4 text-yellow-500" />
                      )}
                    </h3>
                    {group.user_role && (
                      <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 px-2 py-1 rounded">
                        {group.user_role}
                      </span>
                    )}
                  </div>
                </div>

                {group.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
                    {group.description}
                  </p>
                )}

                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span className="flex items-center gap-1">
                    <Users className="w-4 h-4" />
                    {group.member_count}/{group.max_members} members
                  </span>
                  {group.join_code && (
                    <span className="font-mono bg-gray-200 dark:bg-gray-600 px-2 py-1 rounded">
                      {group.join_code}
                    </span>
                  )}
                </div>

                <div className="mt-4 flex gap-2">
                  {group.user_role ? (
                    <>
                      <button className="flex-1 py-2 px-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm">
                        View Group
                      </button>
                      {group.user_role !== 'owner' && (
                        <button
                          onClick={() => leaveGroup(group.id)}
                          className="py-2 px-3 bg-red-500 text-white rounded-lg hover:bg-red-600 text-sm"
                        >
                          Leave
                        </button>
                      )}
                    </>
                  ) : (
                    <button
                      onClick={() => joinGroup(group.id)}
                      className="flex-1 py-2 px-3 bg-green-500 text-white rounded-lg hover:bg-green-600 text-sm"
                    >
                      Join Group
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h3 className="text-xl font-bold mb-4">Create Study Group</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Group Name</label>
                <input
                  type="text"
                  value={newGroup.name}
                  onChange={(e) => setNewGroup({ ...newGroup, name: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
                  placeholder="Enter group name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  value={newGroup.description}
                  onChange={(e) => setNewGroup({ ...newGroup, description: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
                  rows={3}
                  placeholder="What's this group about?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Max Members</label>
                <input
                  type="number"
                  value={newGroup.max_members}
                  onChange={(e) => setNewGroup({ ...newGroup, max_members: parseInt(e.target.value) || 20 })}
                  className="w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
                  min="2"
                  max="100"
                />
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="is_public"
                  checked={newGroup.is_public}
                  onChange={(e) => setNewGroup({ ...newGroup, is_public: e.target.checked })}
                  className="rounded"
                />
                <label htmlFor="is_public" className="text-sm">
                  Make this group public (anyone can join)
                </label>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 py-2 px-4 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600"
              >
                Cancel
              </button>
              <button
                onClick={createGroup}
                className="flex-1 py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                Create Group
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}