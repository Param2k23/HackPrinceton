"use client"

import { X, Send, Trophy, Clock, AlertCircle, PenTool } from "lucide-react"
import { useState } from "react"

interface ConnectModalProps {
  userMode: "parent" | "child"
  onClose: () => void
}

export function ConnectModal({ userMode, onClose }: ConnectModalProps) {
  const [selectedAction, setSelectedAction] = useState<"nudge" | "win" | "request" | "help" | "custom" | null>(null)
  const [customMessage, setCustomMessage] = useState("")

  return (
    <div className="fixed inset-0 bg-black/40 flex items-end z-40">
      <div className="w-full bg-white rounded-t-3xl p-6 animate-in slide-in-from-bottom-3 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-foreground">Share a Spark</h2>
          <button onClick={onClose} className="p-1 hover:bg-muted rounded-lg transition-colors">
            <X className="w-6 h-6 text-muted-foreground" />
          </button>
        </div>

        {!selectedAction ? (
          <div className="space-y-3">
            <button
              onClick={() => setSelectedAction("nudge")}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border border-border hover:bg-muted/50 transition-colors text-left`}
            >
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                <Send className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="font-semibold text-foreground">Send a Nudge</p>
                <p className="text-sm text-muted-foreground">Send "Thinking of you!"</p>
              </div>
            </button>

            <button
              onClick={() => setSelectedAction("win")}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border border-border hover:bg-muted/50 transition-colors text-left`}
            >
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                <Trophy className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="font-semibold text-foreground">Share a Win</p>
                <p className="text-sm text-muted-foreground">Type a 1-sentence win for the day</p>
              </div>
            </button>

            <button
              onClick={() => setSelectedAction("request")}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border border-border hover:bg-muted/50 transition-colors text-left`}
            >
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                <Clock className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="font-semibold text-foreground">Request Time</p>
                <p className="text-sm text-muted-foreground">Schedule a chat</p>
              </div>
            </button>

            <button
              onClick={() => setSelectedAction("custom")}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border border-border hover:bg-muted/50 transition-colors text-left`}
            >
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                <PenTool className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="font-semibold text-foreground">Send Custom Note</p>
                <p className="text-sm text-muted-foreground">Write a short message</p>
              </div>
            </button>

            {userMode === "child" && (
              <button
                onClick={() => setSelectedAction("help")}
                className={`w-full flex items-center gap-4 p-4 rounded-xl border border-destructive/20 hover:bg-destructive/5 transition-colors text-left`}
              >
                <div className="w-12 h-12 rounded-lg bg-destructive/10 flex items-center justify-center flex-shrink-0">
                  <AlertCircle className="w-6 h-6 text-destructive" />
                </div>
                <div>
                  <p className="font-semibold text-destructive">I Need Help</p>
                  <p className="text-sm text-muted-foreground">Alert Mom/Dad immediately</p>
                </div>
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            <button
              onClick={() => setSelectedAction(null)}
              className="text-sm text-muted-foreground hover:text-foreground font-medium mb-4"
            >
              ← Back
            </button>

            {selectedAction === "nudge" && (
              <div className="space-y-4">
                <div className="bg-muted/50 p-4 rounded-xl">
                  <p className="text-sm font-medium text-foreground mb-2">Preview:</p>
                  <p className="text-foreground font-medium italic">"Thinking of you!"</p>
                </div>
                <button className="w-full bg-secondary text-secondary-foreground py-3 rounded-lg font-semibold hover:bg-secondary/90 transition-colors">
                  Send Nudge
                </button>
              </div>
            )}

            {selectedAction === "win" && (
              <div className="space-y-4">
                <input
                  type="text"
                  placeholder="I aced my test!"
                  className="w-full px-4 py-3 rounded-lg border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                />
                <button className="w-full bg-secondary text-secondary-foreground py-3 rounded-lg font-semibold hover:bg-secondary/90 transition-colors">
                  Share Win
                </button>
              </div>
            )}

            {selectedAction === "request" && (
              <div className="space-y-4">
                <input
                  type="time"
                  className="w-full px-4 py-3 rounded-lg border border-border bg-background text-foreground"
                />
                <button className="w-full bg-secondary text-secondary-foreground py-3 rounded-lg font-semibold hover:bg-secondary/90 transition-colors">
                  Request Time
                </button>
              </div>
            )}

            {selectedAction === "custom" && (
              <div className="space-y-4">
                <textarea
                  value={customMessage}
                  onChange={(e) => setCustomMessage(e.target.value)}
                  placeholder="Write your message..."
                  className="w-full px-4 py-3 rounded-lg border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary min-h-24"
                />
                <button className="w-full bg-secondary text-secondary-foreground py-3 rounded-lg font-semibold hover:bg-secondary/90 transition-colors">
                  Send Message
                </button>
              </div>
            )}

            {selectedAction === "help" && (
              <div className="space-y-4">
                <div className="bg-destructive/5 p-4 rounded-xl border border-destructive/20">
                  <p className="text-sm text-foreground">
                    <span className="font-semibold">High Priority Alert</span>
                    <span className="block text-muted-foreground mt-1">Your parents will be notified immediately</span>
                  </p>
                </div>
                <button className="w-full bg-destructive text-white py-3 rounded-lg font-semibold hover:bg-destructive/90 transition-colors">
                  Send Help Alert
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
