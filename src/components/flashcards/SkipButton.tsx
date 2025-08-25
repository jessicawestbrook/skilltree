import React from 'react'
import { ForwardIcon } from '@heroicons/react/24/outline'

interface SkipButtonProps {
  onSkip: () => void
  disabled?: boolean
  className?: string
}

const SkipButton: React.FC<SkipButtonProps> = ({ 
  onSkip, 
  disabled = false,
  className = '' 
}) => {
  return (
    <button
      onClick={onSkip}
      disabled={disabled}
      className={`text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200 text-xs flex items-center gap-1 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
    >
      Skip <ForwardIcon className="h-3 w-3" />
    </button>
  )
}

export default SkipButton