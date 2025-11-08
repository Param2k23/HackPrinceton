"use client"

import { ParentDashboard } from "@/components/parent-dashboard"

export default function ParentPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col pb-24">
      <ParentDashboard active="home" />
    </div>
  )
}
