"use client"

import { MessageSquare, Plus, Clock, Star } from "lucide-react"
import { useState } from "react"

export function FamilyTab({ userMode }: { userMode: "parent" | "child" }) {
  const [selectedMember, setSelectedMember] = useState<string | null>(null)

  const familyMembers = [
    { id: "1", name: "Sarah", role: "Mom", emoji: "👩", status: "online", streakDays: 12 },
    { id: "2", name: "Tim", role: "Son", emoji: "👦", status: "online", streakDays: 8 },
    { id: "3", name: "Mike", role: "Dad", emoji: "👨", status: "offline", streakDays: 10 },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">Family</h2>
        <p className="text-muted-foreground">Your connected family members</p>
      </div>

      {/* Family Members Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {familyMembers.map((member) => (
          <div
            key={member.id}
            onClick={() => setSelectedMember(member.id)}
            className={`rounded-2xl p-6 border transition-all cursor-pointer ${
              selectedMember === member.id
                ? "bg-secondary/5 border-secondary shadow-md"
                : "bg-white border-border hover:shadow-md hover:border-secondary/30"
            }`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="text-4xl">{member.emoji}</div>
              <div
                className={`w-3 h-3 rounded-full ${member.status === "online" ? "bg-green-500 animate-pulse" : "bg-gray-300"}`}
              />
            </div>
            <h3 className="font-semibold text-foreground">{member.name}</h3>
            <p className="text-xs text-muted-foreground mb-3">{member.role}</p>
            <div className="flex items-center gap-2 mb-4 text-xs font-medium text-secondary">
              <Star className="w-3 h-3 fill-current" />
              {member.streakDays} day streak
            </div>
            <div className="flex gap-2">
              <button className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/90 transition-colors font-medium text-sm">
                <MessageSquare className="w-4 h-4" />
                Message
              </button>
            </div>
          </div>
        ))}

        {/* Add Family Member Card */}
        <button className="rounded-2xl p-6 border-2 border-dashed border-border hover:border-secondary hover:bg-secondary/5 transition-all flex flex-col items-center justify-center min-h-48 text-center">
          <Plus className="w-8 h-8 text-muted-foreground mb-2" />
          <p className="font-medium text-foreground">Add Family Member</p>
          <p className="text-xs text-muted-foreground mt-1">Invite others to connect</p>
        </button>
      </div>

      {/* Connect Time Schedule */}
      <div className="bg-white rounded-2xl p-6 border border-border">
        <h3 className="font-semibold text-foreground mb-4">Upcoming Connect Times</h3>
        <div className="space-y-3">
          <div className="flex items-center gap-3 pb-3 border-b border-border last:border-0">
            <Clock className="w-5 h-5 text-secondary flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm font-medium text-foreground">Chat with Mom & Dad</p>
              <p className="text-xs text-muted-foreground">Today at 6:30 PM</p>
            </div>
            <button className="px-3 py-1 text-xs bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/90 transition-colors font-medium">
              Confirm
            </button>
          </div>
          <div className="flex items-center gap-3 pb-3 border-b border-border last:border-0">
            <Clock className="w-5 h-5 text-secondary flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm font-medium text-foreground">Family dinner call</p>
              <p className="text-xs text-muted-foreground">Saturday at 7:00 PM</p>
            </div>
            <button className="px-3 py-1 text-xs bg-secondary/10 text-secondary rounded-lg hover:bg-secondary/20 transition-colors font-medium">
              Maybe
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
