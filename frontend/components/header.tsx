import { Settings } from "lucide-react"

interface HeaderProps {
  greeting: string
  userMode: "parent" | "child"
}

export function Header({ greeting, userMode }: HeaderProps) {
  return (
    <header className="bg-white border-b border-border px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-primary/70 flex items-center justify-center">
          <span className="text-sm font-bold text-foreground">K</span>
        </div>
        <span className="font-medium text-foreground hidden sm:inline">Kindred</span>
      </div>

      <button className="p-2 hover:bg-muted rounded-lg transition-colors">
        <Settings className="w-5 h-5 text-muted-foreground" />
      </button>
    </header>
  )
}
