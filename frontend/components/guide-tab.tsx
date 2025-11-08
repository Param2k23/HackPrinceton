"use client"

import { Mic, Send } from "lucide-react"
import { useState } from "react"

interface GuideTabProps {
  userMode: "parent" | "child"
}

export function GuideTab({ userMode }: GuideTabProps) {
  const [messages, setMessages] = useState<Array<{ id: string; type: "bot" | "user"; content: string }>>([
    {
      id: "1",
      type: "bot",
      content:
        userMode === "parent"
          ? "Hi Sarah! I'm here to help you stay connected with Tim. What can I assist you with today?"
          : "Hi Tim! Your guide here to help. How are you feeling today?",
    },
  ])
  const [inputValue, setInputValue] = useState("")

  const quickReplies =
    userMode === "parent"
      ? [
          "Help me schedule time",
          "What's Tim interested in?",
          "Give me a conversation starter",
          "Tips for homework help",
        ]
      : ["I'm bored", "Tell me a joke", "I want to tell Mom something", "I feel sad"]

  const handleSend = () => {
    if (!inputValue.trim()) return

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      type: "user" as const,
      content: inputValue,
    }
    setMessages([...messages, userMessage])
    setInputValue("")

    // Simulate bot response
    setTimeout(() => {
      const botResponses = [
        "That's a great question! Let me help you with that.",
        "I understand. Here are some suggestions for you...",
        "That sounds important. Let's explore this together.",
      ]
      const randomResponse = botResponses[Math.floor(Math.random() * botResponses.length)]
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          type: "bot",
          content: randomResponse,
        },
      ])
    }, 500)
  }

  const handleQuickReply = (reply: string) => {
    setInputValue(reply)
    setTimeout(() => handleSend(), 0)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-200px)] bg-background rounded-2xl">
      {/* Header */}
      <div className="px-6 py-4 border-b border-border">
        <h2 className="text-2xl font-bold text-foreground">Your Guide</h2>
      </div>

      {/* Chat Stream */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-xs px-4 py-3 rounded-2xl ${
                message.type === "bot"
                  ? "bg-muted text-foreground"
                  : userMode === "parent"
                    ? "bg-secondary text-secondary-foreground"
                    : "bg-accent text-accent-foreground"
              }`}
            >
              <p className="text-sm">{message.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Reply Chips */}
      {messages.length > 0 && (
        <div className="px-6 py-3 border-t border-border overflow-x-auto">
          <div className="flex gap-2 flex-nowrap">
            {quickReplies.map((reply) => (
              <button
                key={reply}
                onClick={() => handleQuickReply(reply)}
                className="flex-shrink-0 px-3 py-2 bg-muted hover:bg-muted/80 text-foreground rounded-full text-xs font-medium transition-colors whitespace-nowrap"
              >
                {reply}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Bar */}
      <div className="border-t border-border p-4 flex items-center gap-3">
        <button className="p-2 hover:bg-muted rounded-lg transition-colors text-muted-foreground hover:text-foreground">
          <Mic className="w-5 h-5" />
        </button>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
          placeholder={userMode === "parent" ? "Ask your Guide for help..." : "Tell your Guide how you feel..."}
          className="flex-1 px-4 py-2 bg-muted rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <button
          onClick={handleSend}
          disabled={!inputValue.trim()}
          className="p-2 bg-primary hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors text-foreground"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  )
}
