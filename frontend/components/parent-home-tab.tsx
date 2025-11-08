"use client"

import { ArrowRight, CheckCircle2, Clock, Sparkles } from "lucide-react"
import { useState } from "react"

export function ParentHomeTab() {
  const [dismissedNudge, setDismissedNudge] = useState(false)

  return (
    <div className="space-y-6">
      {/* Greeting */}
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-2">Good morning, Sarah</h1>
        <p className="text-muted-foreground">Today looks like a great day to connect</p>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-border shadow-sm hover:shadow-md transition-all hover:border-secondary/50">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-6 h-6 text-secondary" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-foreground mb-1">Today's Connect</h3>
            <p className="text-muted-foreground text-sm mb-4">Tim has his big spelling bee today at 11:00 AM.</p>
            <button className="inline-flex items-center gap-2 bg-secondary hover:bg-secondary/90 text-secondary-foreground px-4 py-2 rounded-lg font-medium transition-all active:scale-95 hover:shadow-md">
              🚀 Send Good Luck!
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-border shadow-sm hover:shadow-md transition-all">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
            <Clock className="w-6 h-6 text-primary" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-foreground mb-1">Guide's Corner</h3>
            <p className="text-muted-foreground text-sm mb-4">
              Your Guide suggests a 15-min chat with Tim tonight. You're both free around 6:30 PM.
            </p>
            <button className="px-4 py-2 rounded-lg font-medium text-primary bg-primary/10 hover:bg-primary/20 transition-all active:scale-95">
              Ask Guide for help
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-border shadow-sm hover:shadow-md transition-shadow">
        <h3 className="font-semibold text-foreground mb-4">Tim's World</h3>
        <div className="space-y-3">
          <div className="flex items-center gap-3 pb-3 border-b border-border last:border-0 last:pb-0 hover:bg-muted/30 p-2 -mx-2 px-3 rounded-lg transition-colors cursor-pointer">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-accent to-accent/70 flex items-center justify-center flex-shrink-0">
              <span className="text-xs font-bold">😊</span>
            </div>
            <div>
              <p className="text-sm text-foreground font-medium">Tim shared a "Happy" mood</p>
              <p className="text-xs text-muted-foreground">3:00 PM today</p>
            </div>
          </div>
          <div className="flex items-center gap-3 pb-3 border-b border-border last:border-0 last:pb-0 hover:bg-muted/30 p-2 -mx-2 px-3 rounded-lg transition-colors cursor-pointer">
            <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
              <CheckCircle2 className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-foreground font-medium">Tim completed "Clean Room" task</p>
              <p className="text-xs text-muted-foreground">1:30 PM today</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
