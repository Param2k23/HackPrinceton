"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { ParentDashboard } from "@/components/parent-dashboard"
import { ChildDashboard } from "@/components/child-dashboard"
import { ConnectModal } from "@/components/connect-modal"
import { BottomNav } from "@/components/bottom-nav"
import { LandingPage } from "@/components/landing-page"
import type { User } from "@/lib/types"

export default function Page() {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userMode, setUserMode] = useState<"parent" | "child">("parent")
  const [showConnectModal, setShowConnectModal] = useState(false)
  const [activeTab, setActiveTab] = useState<"home" | "timeline" | "guide" | "family">("home")

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/auth/verify', {
          method: 'GET',
          credentials: 'include'
        });
        
        if (response.ok) {
          const data = await response.json();
          setIsAuthenticated(true);
          setUserMode(data.role as "parent" | "child");
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []); // Added dependency array

  if (!isAuthenticated) {
    return <LandingPage
      onLoginSuccess={() => {
        setIsAuthenticated(true);
        setUserMode("parent"); // Default to parent or adjust as needed
      }}
    />;
  }

  return (
    <div className="min-h-screen bg-background flex flex-col pb-24">
      <div className="flex-1 overflow-y-auto">
        {userMode === "parent" ? <ParentDashboard active={activeTab} /> : <ChildDashboard active={activeTab} />}
      </div>

      <BottomNav activeTab={activeTab} onTabChange={setActiveTab} onConnectClick={() => setShowConnectModal(true)} />

      {showConnectModal && <ConnectModal userMode={userMode} onClose={() => setShowConnectModal(false)} />}

      {/* Mode toggle for demo */}
      <div className="fixed top-4 right-4 z-50 flex gap-2">
        <button
          onClick={() => setUserMode("parent")}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            userMode === "parent" ? "bg-secondary text-secondary-foreground" : "bg-muted text-muted-foreground"
          }`}
        >
          Parent
        </button>
        <button
          onClick={() => setUserMode("child")}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            userMode === "child" ? "bg-accent text-accent-foreground" : "bg-muted text-muted-foreground"
          }`}
        >
          Child
        </button>
      </div>
    </div>
  )
}
