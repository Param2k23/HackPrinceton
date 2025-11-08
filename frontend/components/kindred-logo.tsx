export function KindredLogo() {
  return (
    <svg viewBox="0 0 60 60" className="w-12 h-12" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Left branch (Parent) */}
      <path
        d="M 20 50 Q 15 35 18 20 Q 20 10 25 8"
        stroke="#4a908c"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Right branch (Child) */}
      <path
        d="M 40 50 Q 45 35 42 20 Q 40 10 35 8"
        stroke="#50a6d1"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Center trunk */}
      <path d="M 30 60 Q 28 55 28 45 Q 28 35 30 25" stroke="#333333" strokeWidth="2" strokeLinecap="round" />

      {/* Connecting roots */}
      <path d="M 20 50 Q 25 55 30 58" stroke="#ffc300" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
      <path d="M 40 50 Q 35 55 30 58" stroke="#ffc300" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />

      {/* Leaves/flourishes */}
      <circle cx="23" cy="15" r="2.5" fill="#4a908c" opacity="0.7" />
      <circle cx="37" cy="15" r="2.5" fill="#50a6d1" opacity="0.7" />
    </svg>
  )
}
