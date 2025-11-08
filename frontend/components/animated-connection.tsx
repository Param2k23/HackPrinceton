"use client"

import { useEffect, useState } from "react"

export function AnimatedConnection() {
  const [animationState, setAnimationState] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationState((prev) => (prev + 1) % 100)
    }, 30)
    return () => clearInterval(interval)
  }, [])

  // Calculate the animated line position
  const lineProgress = (Math.sin(animationState / 20) + 1) / 2

  return (
    <div className="w-full max-w-sm h-64 flex items-center justify-center">
      <svg viewBox="0 0 300 200" className="w-full h-full" preserveAspectRatio="xMidYMid meet">
        {/* Left spark (Parent - Muted Teal) */}
        <g>
          <circle cx="50" cy="100" r="8" fill="#4a908c" opacity={0.5 + Math.sin(animationState / 10) * 0.3} />
          <circle
            cx="50"
            cy="100"
            r="12"
            fill="none"
            stroke="#4a908c"
            strokeWidth="1"
            opacity={0.3 + Math.sin(animationState / 10) * 0.2}
          />
        </g>

        {/* Right spark (Child - Sky Blue) */}
        <g>
          <circle
            cx="250"
            cy="100"
            r="8"
            fill="#50a6d1"
            opacity={0.5 + Math.sin(animationState / 10 + Math.PI) * 0.3}
          />
          <circle
            cx="250"
            cy="100"
            r="12"
            fill="none"
            stroke="#50a6d1"
            strokeWidth="1"
            opacity={0.3 + Math.sin(animationState / 10 + Math.PI) * 0.2}
          />
        </g>

        {/* Animated connecting line (Sunrise Yellow) */}
        <defs>
          <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset={`${Math.max(0, lineProgress * 100 - 20)}%`} stopColor="#ffc300" stopOpacity="0" />
            <stop offset={`${lineProgress * 100}%`} stopColor="#ffc300" stopOpacity="0.8" />
            <stop offset={`${Math.min(100, lineProgress * 100 + 20)}%`} stopColor="#ffc300" stopOpacity="0" />
          </linearGradient>
        </defs>

        {/* Base connection line */}
        <path
          d={`M 50 100 Q 150 ${80 + Math.sin(animationState / 15) * 15} 250 100`}
          fill="none"
          stroke="#ffc300"
          strokeWidth="2"
          opacity="0.3"
        />

        {/* Animated glowing line */}
        <path
          d={`M 50 100 Q 150 ${80 + Math.sin(animationState / 15) * 15} 250 100`}
          fill="none"
          stroke="url(#connectionGradient)"
          strokeWidth="3"
          strokeLinecap="round"
        />
      </svg>
    </div>
  )
}
