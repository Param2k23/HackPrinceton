"use client"

import { Header } from "./header"
import { ParentHomeTab } from "./parent-home-tab"
import { TimelineTab } from "./timeline-tab"
import { GuideTab } from "./guide-tab"
import { FamilyTab } from "./family-tab"

interface ParentDashboardProps {
  active: "home" | "timeline" | "guide" | "family"
}

export function ParentDashboard({ active }: ParentDashboardProps) {
  return (
    <div className="min-h-screen bg-background">
      <Header greeting="Good morning, Sarah" userMode="parent" />

      <div className="max-w-4xl mx-auto px-6 py-8">
        {active === "home" && <ParentHomeTab />}
        {active === "timeline" && <TimelineTab userMode="parent" />}
        {active === "guide" && <GuideTab userMode="parent" />}
        {active === "family" && <FamilyTab userMode="parent" />}
      </div>
    </div>
  )
}
