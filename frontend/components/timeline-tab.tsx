"use client"

import { Heart, MessageCircle, Share2 } from "lucide-react"
import { useState } from "react"

export function TimelineTab({ userMode }: { userMode: "parent" | "child" }) {
  const [likedItems, setLikedItems] = useState<string[]>([])

  const events = [
    {
      id: "1",
      name: "Tim",
      action: "completed",
      activity: "Spelling Bee Practice",
      time: "2 hours ago",
      emoji: "🏆",
    },
    {
      id: "2",
      name: "Tim",
      action: "shared",
      activity: "A photo from Science Class",
      time: "4 hours ago",
      emoji: "📸",
    },
    {
      id: "3",
      name: "Sarah",
      action: "sent",
      activity: "A good luck message",
      time: "Today",
      emoji: "💌",
    },
    {
      id: "4",
      name: "Tim",
      action: "connected",
      activity: "Chat about the day",
      time: "Yesterday",
      emoji: "💬",
    },
  ]

  const toggleLike = (id: string) => {
    setLikedItems((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]))
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-foreground mb-6">Timeline</h2>
      <div className="space-y-3">
        {events.map((event) => (
          <div
            key={event.id}
            className="bg-white rounded-2xl p-6 border border-border hover:shadow-md transition-shadow"
          >
            <div className="flex items-start gap-4">
              <div className="text-3xl flex-shrink-0">{event.emoji}</div>
              <div className="flex-1">
                <p className="text-sm text-muted-foreground">{event.time}</p>
                <p className="text-foreground font-medium mt-1">
                  <span className="font-semibold text-foreground">{event.name}</span> {event.action} {event.activity}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4 mt-4 pt-4 border-t border-border">
              <button
                onClick={() => toggleLike(event.id)}
                className={`flex items-center gap-1 px-3 py-2 rounded-lg transition-colors ${
                  likedItems.includes(event.id)
                    ? "bg-red-100 text-red-600"
                    : "hover:bg-muted text-muted-foreground hover:text-foreground"
                }`}
              >
                <Heart className={`w-4 h-4 ${likedItems.includes(event.id) ? "fill-current" : ""}`} />
                <span className="text-xs font-medium">{likedItems.includes(event.id) ? "Liked" : "Like"}</span>
              </button>
              <button className="flex items-center gap-1 px-3 py-2 rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground transition-colors">
                <MessageCircle className="w-4 h-4" />
                <span className="text-xs font-medium">Comment</span>
              </button>
              <button className="flex items-center gap-1 px-3 py-2 rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground transition-colors">
                <Share2 className="w-4 h-4" />
                <span className="text-xs font-medium">Share</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
