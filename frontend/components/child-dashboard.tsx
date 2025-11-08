"use client"

import { Header } from "./header"
import { ChildHomeTab } from "./child-home-tab"
import { TimelineTab } from "./timeline-tab"
import { GuideTab } from "./guide-tab"
import { FamilyTab } from "./family-tab"

interface ChildDashboardProps {
  active: "home" | "timeline" | "guide" | "family"
}

export function ChildDashboard({ active }: ChildDashboardProps) {
  return (
    <div className="min-h-screen bg-background">
      <Header greeting="Hi Tim!" userMode="child" />

      <div className="max-w-4xl mx-auto px-6 py-8">
        {active === "home" && <ChildHomeTab />}
        {active === "timeline" && <TimelineTab userMode="child" />}
        {active === "guide" && <GuideTab userMode="child" />}
        {active === "family" && <FamilyTab userMode="child" />}
      </div>
    </div>
  )
}
