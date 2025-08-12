import React, { useState, CSSProperties } from 'react';
import { User, LogOut, Edit3, Save, X, Calendar, Mail } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface UserProfileProps {
  isOpen: boolean;
  onClose: () => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ isOpen, onClose }) => {
  const { user, logout, updateProfile, isLoading } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    displayName: user?.displayName || '',
    username: user?.username || ''
  });

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
      displayName: user?.displayName || '',
      username: user?.username || ''
    });
    setIsEditing(false);
  };

  if (!isOpen || !user) return null;

  const styles = {
    overlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.8)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      padding: '20px'
    } as CSSProperties,
    modal: {
      background: 'white',
      borderRadius: '20px',
      padding: '30px',
      maxWidth: '500px',
      width: '100%',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
    } as CSSProperties,
    header: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '30px'
    } as CSSProperties,
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#2a2a2a'
    } as CSSProperties,
    avatarSection: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      marginBottom: '30px'
    } as CSSProperties,
    avatar: {
      width: '80px',
      height: '80px',
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      marginBottom: '15px'
    } as CSSProperties,
    infoSection: {
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
      marginBottom: '30px'
    } as CSSProperties,
    infoRow: {
      display: 'flex',
      alignItems: 'center',
      gap: '15px',
      padding: '15px',
      background: '#f8f8f8',
      borderRadius: '12px'
    } as CSSProperties,
    label: {
      fontSize: '14px',
      fontWeight: '600',
      color: '#666',
      minWidth: '80px'
    } as CSSProperties,
    value: {
      fontSize: '16px',
      color: '#2a2a2a',
      flex: 1
    } as CSSProperties,
    input: {
      flex: 1,
      padding: '8px 12px',
      border: '2px solid #e0e0e0',
      borderRadius: '8px',
      fontSize: '16px',
      color: '#2a2a2a'
    } as CSSProperties,
    buttonGroup: {
      display: 'flex',
      gap: '15px'
    } as CSSProperties,
    button: {
      flex: 1,
      padding: '12px 20px',
      border: 'none',
      borderRadius: '12px',
      fontSize: '14px',
      fontWeight: 'bold',
      cursor: isLoading ? 'not-allowed' : 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px',
      transition: 'all 0.3s ease',
      opacity: isLoading ? 0.7 : 1
    } as CSSProperties,
    primaryButton: {
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      color: 'white'
    } as CSSProperties,
    secondaryButton: {
      background: '#f0f0f0',
      color: '#666'
    } as CSSProperties,
    dangerButton: {
      background: 'linear-gradient(135deg, #ff6b6b, #ff5252)',
      color: 'white'
    } as CSSProperties
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>Profile</h2>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer' }}
          >
            <X size={24} color="#999" />
          </button>
        </div>

        <div style={styles.avatarSection}>
          <div style={styles.avatar}>
            <User size={40} color="white" />
          </div>
        </div>

        <div style={styles.infoSection}>
          <div style={styles.infoRow}>
            <Mail size={20} color="#667eea" />
            <span style={styles.label}>Email</span>
            <span style={styles.value}>{user.email}</span>
          </div>

          <div style={styles.infoRow}>
            <User size={20} color="#667eea" />
            <span style={styles.label}>Username</span>
            {isEditing ? (
              <input
                type="text"
                value={editForm.username}
                onChange={(e) => setEditForm(prev => ({ ...prev, username: e.target.value }))}
                style={styles.input}
              />
            ) : (
              <span style={styles.value}>{user.username}</span>
            )}
          </div>

          <div style={styles.infoRow}>
            <User size={20} color="#667eea" />
            <span style={styles.label}>Display Name</span>
            {isEditing ? (
              <input
                type="text"
                value={editForm.displayName}
                onChange={(e) => setEditForm(prev => ({ ...prev, displayName: e.target.value }))}
                style={styles.input}
              />
            ) : (
              <span style={styles.value}>{user.displayName || 'Not set'}</span>
            )}
          </div>

          <div style={styles.infoRow}>
            <Calendar size={20} color="#667eea" />
            <span style={styles.label}>Joined</span>
            <span style={styles.value}>{user.createdAt.toLocaleDateString()}</span>
          </div>
        </div>

        <div style={styles.buttonGroup}>
          {isEditing ? (
            <>
              <button
                onClick={handleSave}
                style={{ ...styles.button, ...styles.primaryButton }}
                disabled={isLoading}
              >
                <Save size={16} />
                Save Changes
              </button>
              <button
                onClick={handleCancel}
                style={{ ...styles.button, ...styles.secondaryButton }}
                disabled={isLoading}
              >
                <X size={16} />
                Cancel
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setIsEditing(true)}
                style={{ ...styles.button, ...styles.primaryButton }}
                disabled={isLoading}
              >
                <Edit3 size={16} />
                Edit Profile
              </button>
              <button
                onClick={handleLogout}
                style={{ ...styles.button, ...styles.dangerButton }}
                disabled={isLoading}
              >
                <LogOut size={16} />
                Sign Out
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};