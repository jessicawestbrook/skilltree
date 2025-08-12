import React, { CSSProperties } from 'react';
import { domainIcons } from '../data/domainIcons';
import { learningPaths } from '../data/learningPaths';

interface SidebarProps {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  currentView: string;
  setCurrentView: (view: string) => void;
  activeFilters: string[];
  toggleFilter: (domain: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  searchTerm,
  setSearchTerm,
  currentView,
  setCurrentView,
  activeFilters,
  toggleFilter
}) => {
  const styles = {
    panel: {
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderRadius: '15px',
      padding: '20px',
      marginBottom: '15px',
      boxShadow: '0 5px 20px rgba(0,0,0,0.1)'
    } as CSSProperties
  };

  return (
    <div>
      {/* Search */}
      <div style={styles.panel}>
        <input
          type="text"
          placeholder="Search knowledge..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '10px',
            border: '2px solid #e0e0e0',
            borderRadius: '10px',
            fontSize: '14px',
            color: '#2a2a2a',
            backgroundColor: '#ffffff'
          }}
        />
      </div>

      {/* Category Filter */}
      <div style={styles.panel}>
        <h3 style={{ fontSize: '16px', marginBottom: '15px', color: '#2a2a2a', fontWeight: 'bold' }}>Knowledge Level</h3>
        {['all', 'foundation', 'fundamentals', 'domains', 'mastery'].map(view => (
          <button
            key={view}
            onClick={() => setCurrentView(view)}
            style={{
              width: '100%',
              padding: '10px',
              marginBottom: '8px',
              border: 'none',
              borderRadius: '8px',
              background: currentView === view ? 'linear-gradient(135deg, #667eea, #764ba2)' : '#f0f0f0',
              color: currentView === view ? 'white' : '#3a3a3a',
              cursor: 'pointer',
              fontWeight: currentView === view ? 'bold' : 'normal',
              transition: 'all 0.3s'
            }}
          >
            {view.charAt(0).toUpperCase() + view.slice(1)}
          </button>
        ))}
      </div>

      {/* Domain Filter */}
      <div style={styles.panel}>
        <h3 style={{ fontSize: '16px', marginBottom: '15px', color: '#2a2a2a', fontWeight: 'bold' }}>Domains</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {Object.keys(domainIcons).map(domain => {
            const Icon = domainIcons[domain];
            const isActive = activeFilters.includes(domain);
            return (
              <button
                key={domain}
                onClick={() => toggleFilter(domain)}
                style={{
                  padding: '8px 12px',
                  border: 'none',
                  borderRadius: '20px',
                  background: isActive ? 'linear-gradient(135deg, #667eea, #764ba2)' : '#f0f0f0',
                  color: isActive ? 'white' : '#3a3a3a',
                  cursor: 'pointer',
                  fontSize: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <Icon size={14} />
                {domain.replace('_', ' ')}
              </button>
            );
          })}
        </div>
      </div>

      {/* Learning Paths */}
      <div style={styles.panel}>
        <h3 style={{ fontSize: '16px', marginBottom: '15px', color: '#2a2a2a', fontWeight: 'bold' }}>Learning Paths</h3>
        {Object.entries(learningPaths).slice(0, 3).map(([key, path]) => {
          const Icon = path.icon;
          return (
            <div key={key} style={{
              padding: '10px',
              background: '#f8f8f8',
              borderRadius: '8px',
              marginBottom: '8px',
              cursor: 'pointer'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Icon size={20} color="#667eea" />
                <div>
                  <div style={{ fontWeight: 'bold', fontSize: '13px', color: '#2a2a2a' }}>{path.name}</div>
                  <div style={{ fontSize: '11px', color: '#4a4a4a' }}>{path.description}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};