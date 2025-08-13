import React, { CSSProperties } from 'react';
import { Brain, Flame, LogIn, User as UserIcon } from 'lucide-react';
import { UserStats } from '../types';
import { useAuth } from '../contexts/AuthContext';

interface HeaderProps {
  userStats: UserStats;
  isMobile: boolean;
  calculateProgress: () => number;
  onAuthClick: () => void;
  onProfileClick: () => void;
  onLogout?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ userStats, isMobile, calculateProgress, onAuthClick, onProfileClick }) => {
  const { user, isAuthenticated } = useAuth();
  const styles = {
    header: {
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderRadius: isMobile ? '0 0 20px 20px' : '20px',
      padding: isMobile ? '15px' : '20px',
      margin: isMobile ? '0 0 15px 0' : '20px 20px 20px 20px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
    } as CSSProperties
  };

  return (
    <div style={styles.header}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Brain size={36} color="#667eea" />
          <div>
            <h1 style={{ margin: 0, fontSize: isMobile ? '24px' : '28px', color: '#1a1a1a', fontWeight: 'bold' }}>NeuroQuest</h1>
            <p style={{ margin: 0, fontSize: '12px', color: '#4a4a4a', fontWeight: '500' }}>Master All Human Knowledge</p>
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
          {isAuthenticated && (
            <>
              <div style={{ 
                background: 'linear-gradient(135deg, #ff6b6b, #ffd93d)', 
                padding: '8px 15px', 
                borderRadius: '20px',
                color: 'white',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}>
                <Flame size={18} />
                {userStats.synapticStreak} Day Streak!
              </div>
              
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#667eea' }}>
                  {userStats.pathfinderPoints.toLocaleString()}
                </div>
                <div style={{ fontSize: '10px', color: '#5a5a5a', fontWeight: '600' }}>POINTS</div>
              </div>
              
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#764ba2' }}>
                  {userStats.neuralLevel}
                </div>
                <div style={{ fontSize: '10px', color: '#5a5a5a', fontWeight: '600' }}>LEVEL</div>
              </div>
            </>
          )}

          {/* Authentication Button */}
          <button
            onClick={isAuthenticated ? onProfileClick : onAuthClick}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '10px 16px',
              background: isAuthenticated ? 'linear-gradient(135deg, #667eea, #764ba2)' : 'rgba(255, 255, 255, 0.9)',
              color: isAuthenticated ? 'white' : '#667eea',
              border: isAuthenticated ? 'none' : '2px solid #667eea',
              borderRadius: '12px',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            {isAuthenticated ? (
              <>
                <UserIcon size={18} />
                {isMobile ? user?.username?.slice(0, 8) : user?.username}
              </>
            ) : (
              <>
                <LogIn size={18} />
                {isMobile ? 'Login' : 'Sign In'}
              </>
            )}
          </button>
        </div>
      </div>
      
      {/* Progress Bar */}
      <div style={{ marginTop: '15px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '5px', color: '#4a4a4a', fontWeight: '500' }}>
          <span>Overall Progress</span>
          <span>{calculateProgress()}%</span>
        </div>
        <div style={{ height: '8px', background: '#e0e0e0', borderRadius: '10px', overflow: 'hidden' }}>
          <div style={{
            width: `${calculateProgress()}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #667eea, #764ba2)',
            transition: 'width 0.5s ease'
          }} />
        </div>
      </div>
    </div>
  );
};