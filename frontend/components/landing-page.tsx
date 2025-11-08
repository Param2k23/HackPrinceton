"use client"

import type React from "react"

import { useState } from "react"
import { KindredLogo } from "./kindred-logo"
import { AnimatedConnection } from "./animated-connection"

interface LandingPageProps {
  onLoginSuccess: () => void
}

export function LandingPage({ onLoginSuccess }: LandingPageProps) {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [username, setUsername] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Mock authentication
    if (email && password) {
      onLoginSuccess()
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-between p-4 pt-8 pb-8">
      {/* Top: Logo */}
      <div className="flex justify-center pt-4">
        <KindredLogo />
      </div>

      {/* Middle: Animated Connection */}
      <div className="flex-1 flex items-center justify-center w-full">
        <AnimatedConnection />
      </div>

      {/* Tagline */}
      <div className="text-center mb-12 w-full max-w-md">
        <h1 className="text-4xl font-bold text-foreground mb-3 text-balance">Nurture your connection.</h1>
        <p className="text-lg text-muted-foreground text-balance">Your gentle, helping hand for a closer family.</p>
      </div>

      {/* Action Card */}
      <div className="w-full max-w-md">
        <div className="bg-card rounded-3xl p-8 shadow-sm border border-border">
          <h2 className="text-2xl font-bold text-card-foreground mb-8 text-center">
            {isLogin ? "Welcome" : "Create Your Account"}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            {!isLogin && (
              <div>
                <label htmlFor="username" className="sr-only">
                  Username
                </label>
                <input
                  id="username"
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-0 py-3 bg-transparent border-b-2 border-muted text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
                />
              </div>
            )}

            <div>
              <label htmlFor="email" className="sr-only">
                Email or Username
              </label>
              <div className="flex items-center gap-3 border-b-2 border-muted focus-within:border-primary transition-colors">
                <span className="text-muted-foreground text-lg">@</span>
                <input
                  id="email"
                  type="email"
                  placeholder="Email or Username"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex-1 py-3 bg-transparent text-foreground placeholder-muted-foreground focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <div className="flex items-center gap-3 border-b-2 border-muted focus-within:border-primary transition-colors">
                <span className="text-muted-foreground text-lg">🔒</span>
                <input
                  id="password"
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="flex-1 py-3 bg-transparent text-foreground placeholder-muted-foreground focus:outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-primary text-primary-foreground font-bold py-4 px-6 rounded-full hover:opacity-90 transition-opacity mt-8"
            >
              {isLogin ? "Log In" : "Create Account"}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-muted-foreground">
              {isLogin ? "First time here? " : "Already have an account? "}
              <button
                onClick={() => {
                  setIsLogin(!isLogin)
                  setEmail("")
                  setPassword("")
                  setUsername("")
                }}
                className="font-bold text-secondary hover:opacity-80 transition-opacity"
              >
                {isLogin ? "Create an account" : "Log in"}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
