import React from 'react'

interface TreeLogoProps {
  className?: string
  size?: number
}

const TreeLogo: React.FC<TreeLogoProps> = ({ className = '', size = 32 }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Tree trunk */}
      <rect
        x="42"
        y="60"
        width="16"
        height="35"
        fill="url(#trunk-gradient)"
        rx="2"
      />
      
      {/* Tree roots */}
      <path
        d="M50 90 L40 100 M50 90 L50 100 M50 90 L60 100"
        stroke="url(#trunk-gradient)"
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />
      
      {/* Tree crown - layered circles for foliage */}
      <circle cx="50" cy="25" r="20" fill="url(#leaves-gradient-1)" opacity="0.9" />
      <circle cx="40" cy="35" r="18" fill="url(#leaves-gradient-2)" opacity="0.85" />
      <circle cx="60" cy="35" r="18" fill="url(#leaves-gradient-2)" opacity="0.85" />
      <circle cx="35" cy="45" r="15" fill="url(#leaves-gradient-3)" opacity="0.8" />
      <circle cx="65" cy="45" r="15" fill="url(#leaves-gradient-3)" opacity="0.8" />
      <circle cx="50" cy="48" r="16" fill="url(#leaves-gradient-1)" opacity="0.75" />
      
      {/* Small decorative leaves/fruits */}
      <circle cx="45" cy="30" r="2" fill="#FFD700" opacity="0.9" />
      <circle cx="55" cy="28" r="2" fill="#FFD700" opacity="0.9" />
      <circle cx="38" cy="40" r="2" fill="#FFD700" opacity="0.9" />
      <circle cx="62" cy="42" r="2" fill="#FFD700" opacity="0.9" />
      <circle cx="50" cy="45" r="2" fill="#FFD700" opacity="0.9" />
      
      {/* Gradient definitions */}
      <defs>
        {/* Trunk gradient - brown tones */}
        <linearGradient id="trunk-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#8B4513" />
          <stop offset="50%" stopColor="#A0522D" />
          <stop offset="100%" stopColor="#654321" />
        </linearGradient>
        
        {/* Leaves gradients - green tones */}
        <radialGradient id="leaves-gradient-1">
          <stop offset="0%" stopColor="#22C55E" />
          <stop offset="100%" stopColor="#16A34A" />
        </radialGradient>
        
        <radialGradient id="leaves-gradient-2">
          <stop offset="0%" stopColor="#16A34A" />
          <stop offset="100%" stopColor="#15803D" />
        </radialGradient>
        
        <radialGradient id="leaves-gradient-3">
          <stop offset="0%" stopColor="#15803D" />
          <stop offset="100%" stopColor="#166534" />
        </radialGradient>
      </defs>
    </svg>
  )
}

export default TreeLogo