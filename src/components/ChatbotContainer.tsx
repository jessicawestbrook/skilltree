'use client';

import React, { useState, useEffect } from 'react';
import { Chatbot } from './Chatbot';

interface ChatbotContainerProps {
  nodeId?: string;
  nodeTitle?: string;
  currentContent?: string;
  isLearningMode?: boolean;
  className?: string;
}

export const ChatbotContainer: React.FC<ChatbotContainerProps> = ({
  nodeId,
  nodeTitle,
  currentContent,
  isLearningMode = false,
  className = ''
}) => {
  const [isMinimized, setIsMinimized] = useState(!isLearningMode);
  const [hasNewMessages, setHasNewMessages] = useState(false);

  // Auto-minimize when not in learning mode
  useEffect(() => {
    if (!isLearningMode) {
      setIsMinimized(true);
    }
  }, [isLearningMode]);

  const handleMinimize = () => {
    setIsMinimized(true);
  };

  const handleMaximize = () => {
    setIsMinimized(false);
    setHasNewMessages(false);
  };

  if (isLearningMode && !isMinimized) {
    // Full chatbot in learning mode
    return (
      <div className={`${className}`}>
        <Chatbot
          nodeId={nodeId}
          nodeTitle={nodeTitle}
          currentContent={currentContent}
          isMinimized={false}
          onMinimize={handleMinimize}
        />
      </div>
    );
  }

  // Minimized floating chatbot
  return (
    <Chatbot
      nodeId={nodeId}
      nodeTitle={nodeTitle}
      currentContent={currentContent}
      isMinimized={true}
      onMaximize={handleMaximize}
      className={className}
    />
  );
};