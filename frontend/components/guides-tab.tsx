"use client"

import { Bookmark, Clock, ArrowRight } from "lucide-react"
import { useState } from "react"

export function GuidesTab({ userMode }: { userMode: "parent" | "child" }) {
  const [savedGuides, setSavedGuides] = useState<string[]>([])

  const guides =
    userMode === "parent"
      ? [
          {
            id: "1",
            title: "Building Digital Boundaries",
            description: "Help your child develop a healthy relationship with technology",
            duration: "8 min read",
            category: "Digital Health",
          },
          {
            id: "2",
            title: "Active Listening with Kids",
            description: "Learn techniques to connect deeper during conversations",
            duration: "5 min read",
            category: "Communication",
          },
          {
            id: "3",
            title: "Supporting School Success",
            description: "Evidence-based strategies to help your child thrive academically",
            duration: "10 min read",
            category: "Education",
          },
        ]
      : [
          {
            id: "1",
            title: "Managing Emotions",
            description: "Understand and express your feelings in healthy ways",
            duration: "6 min read",
            category: "Wellbeing",
          },
          {
            id: "2",
            title: "Making Friends",
            description: "Tips for building and keeping meaningful friendships",
            duration: "4 min read",
            category: "Social",
          },
          {
            id: "3",
            title: "Homework Tips",
            description: "Strategies to stay organized and focused on your studies",
            duration: "7 min read",
            category: "Learning",
          },
        ]

  const toggleSave = (id: string) => {
    setSavedGuides((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]))
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-foreground mb-6">Guides</h2>
      <div className="space-y-3">
        {guides.map((guide) => (
          <div
            key={guide.id}
            className="bg-white rounded-2xl p-6 border border-border hover:shadow-md transition-all hover:border-secondary/50 cursor-pointer group"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="inline-flex items-center gap-2 mb-2">
                  <span className="text-xs font-semibold px-2 py-1 rounded-full bg-secondary/10 text-secondary">
                    {guide.category}
                  </span>
                </div>
                <h3 className="font-semibold text-foreground group-hover:text-secondary transition-colors">
                  {guide.title}
                </h3>
                <p className="text-sm text-muted-foreground mt-2">{guide.description}</p>
                <div className="flex items-center gap-2 mt-4 text-xs text-muted-foreground">
                  <Clock className="w-4 h-4" />
                  {guide.duration}
                </div>
              </div>
              <button
                onClick={() => toggleSave(guide.id)}
                className={`flex-shrink-0 p-2 rounded-lg transition-colors ${
                  savedGuides.includes(guide.id)
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <Bookmark className={`w-5 h-5 ${savedGuides.includes(guide.id) ? "fill-current" : ""}`} />
              </button>
            </div>
            <button className="mt-4 flex items-center gap-2 font-medium text-secondary hover:text-secondary/80 transition-colors text-sm">
              Read Guide
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
