import { Heart, Zap, MessageSquare, HelpCircle, Star } from "lucide-react"

export function ChildHomeTab() {
  return (
    <div className="space-y-6">
      {/* Greeting */}
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-2">Hi Tim! 👋</h1>
        <p className="text-muted-foreground">Your tree is looking happy!</p>
      </div>

      {/* Kindred Tree Visual */}
      <div className="bg-white rounded-2xl p-8 border border-border shadow-sm flex flex-col items-center justify-center min-h-64">
        <div className="text-6xl mb-4">🌱</div>
        <h2 className="text-xl font-semibold text-foreground text-center mb-2">Your Kindred Tree</h2>
        <p className="text-muted-foreground text-center text-sm">
          Complete tasks and connect with Mom & Dad to watch it grow
        </p>
        <div className="mt-6 flex gap-2 flex-wrap justify-center">
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-medium">
            <Star className="w-3 h-3" />3 leaves today
          </span>
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-accent/10 text-accent text-xs font-medium">
            <Heart className="w-3 h-3" />
            Connected
          </span>
        </div>
      </div>

      {/* Today's Quest */}
      <div className="bg-white rounded-2xl p-6 border border-border shadow-sm hover:shadow-md transition-shadow">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center flex-shrink-0">
            <Zap className="w-6 h-6 text-accent" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-foreground mb-1">Today's Quest</h3>
            <p className="text-muted-foreground text-sm mb-3">Spelling Bee day! Remember, you're awesome! 🌟</p>
            <div className="bg-accent/5 rounded-lg p-3 mb-3">
              <p className="text-sm text-foreground">
                <span className="font-medium">Mom sent you a good luck charm!</span>
                <span className="block text-accent font-semibold mt-2">"You've got this, Tim! We believe in you!"</span>
              </p>
            </div>
            <button className="px-4 py-2 bg-accent hover:bg-accent/90 text-accent-foreground rounded-lg font-medium transition-colors text-sm">
              Reply to Mom
            </button>
          </div>
        </div>
      </div>

      {/* Connect Time Card */}
      <div className="bg-white rounded-2xl p-6 border border-border shadow-sm">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
            <MessageSquare className="w-6 h-6 text-primary" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-foreground mb-1">Connect Time!</h3>
            <p className="text-muted-foreground text-sm mb-4">
              Mom & Dad would love to chat at 6:30 PM! Want to tell them about your day?
            </p>
            <div className="flex gap-2">
              <button className="px-6 py-2 bg-accent hover:bg-accent/90 text-accent-foreground rounded-lg font-medium transition-colors">
                Yes!
              </button>
              <button className="px-6 py-2 bg-muted hover:bg-muted/80 text-muted-foreground rounded-lg font-medium transition-colors">
                Maybe later
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Ask Your Guide */}
      <div className="bg-white rounded-2xl p-6 border border-border shadow-sm">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center flex-shrink-0">
            <HelpCircle className="w-6 h-6 text-secondary" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-foreground mb-3">Ask Your Guide</h3>
            <div className="grid grid-cols-2 gap-2">
              <button className="px-3 py-2 bg-secondary/10 hover:bg-secondary/20 text-secondary rounded-lg font-medium transition-colors text-sm">
                I'm bored
              </button>
              <button className="px-3 py-2 bg-secondary/10 hover:bg-secondary/20 text-secondary rounded-lg font-medium transition-colors text-sm">
                Help with homework
              </button>
              <button className="px-3 py-2 bg-secondary/10 hover:bg-secondary/20 text-secondary rounded-lg font-medium transition-colors text-sm">
                I feel lonely
              </button>
              <button className="px-3 py-2 bg-secondary/10 hover:bg-secondary/20 text-secondary rounded-lg font-medium transition-colors text-sm">
                Tell Mom/Dad
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
