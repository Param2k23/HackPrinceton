"use client"

import { Home, Calendar, Plus, Sparkles, Users } from "lucide-react"

interface BottomNavProps {
  activeTab: "home" | "timeline" | "guide" | "family"
  onTabChange: (tab: "home" | "timeline" | "guide" | "family") => void
  onConnectClick: () => void
}

export function BottomNav({ activeTab, onTabChange, onConnectClick }: BottomNavProps) {
  const tabs = [
    { id: "home", label: "Home", icon: Home },
    { id: "guide", label: "Guide", icon: Sparkles },
    { id: "timeline", label: "Timeline", icon: Calendar },
    { id: "family", label: "Family", icon: Users },
  ] as const

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-border flex items-center justify-around px-4 py-3">
      {tabs.slice(0, 1).map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
            activeTab === tab.id
              ? "text-secondary scale-110"
              : "text-muted-foreground hover:text-foreground hover:scale-105"
          }`}
        >
          <tab.icon className="w-6 h-6" />
          <span className="text-xs font-medium">{tab.label}</span>
        </button>
      ))}

      {tabs.slice(1, 2).map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
            activeTab === tab.id
              ? "text-secondary scale-110"
              : "text-muted-foreground hover:text-foreground hover:scale-105"
          }`}
        >
          <tab.icon className="w-6 h-6" />
          <span className="text-xs font-medium">{tab.label}</span>
        </button>
      ))}

      <button
        onClick={onConnectClick}
        className="w-16 h-16 -mt-8 rounded-full bg-gradient-to-br from-primary to-primary/80 text-foreground flex items-center justify-center font-bold shadow-lg hover:shadow-xl hover:scale-110 transition-all active:scale-95"
      >
        <Plus className="w-8 h-8" />
      </button>

      {tabs.slice(2).map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-all ${
            activeTab === tab.id
              ? "text-secondary scale-110"
              : "text-muted-foreground hover:text-foreground hover:scale-105"
          }`}
        >
          <tab.icon className="w-6 h-6" />
          <span className="text-xs font-medium">{tab.label}</span>
        </button>
      ))}
    </div>
  )
}