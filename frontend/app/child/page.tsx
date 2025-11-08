"use client"

import { ChildDashboard } from "@/components/child-dashboard"

export default function ChildPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col pb-24">
      <ChildDashboard active="home" />
    </div>
  )
}
