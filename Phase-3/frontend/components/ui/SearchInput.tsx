/**
 * T121: SearchInput component for filtering tasks
 */
"use client"

import { Search, X } from "lucide-react"
import { Input } from "./Input"

export interface SearchInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  className?: string
}

export function SearchInput({
  value,
  onChange,
  placeholder = "Search tasks...",
  className,
}: SearchInputProps) {
  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-white/50 pointer-events-none" />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={`w-full pl-10 pr-10 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder:text-white/50 focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-[#3B82F6]/50 transition-all ${className || ""}`}
      />
      {value && (
        <button
          onClick={() => onChange("")}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-white/50 hover:text-white transition-colors"
          title="Clear search"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  )
}
