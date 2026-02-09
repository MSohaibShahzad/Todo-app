/**
 * Category input with autocomplete suggestions
 */
"use client"

import { useState, useRef, useEffect } from "react"

interface CategoryInputProps {
  label?: string
  value: string
  onChange: (value: string) => void
  suggestions: string[]
  disabled?: boolean
  placeholder?: string
}

export function CategoryInput({
  label,
  value,
  onChange,
  suggestions,
  disabled,
  placeholder,
}: CategoryInputProps) {
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([])
  const inputRef = useRef<HTMLInputElement>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Filter suggestions based on input value
  useEffect(() => {
    if (value) {
      const filtered = suggestions.filter(
        (suggestion) =>
          suggestion.toLowerCase().includes(value.toLowerCase()) &&
          suggestion.toLowerCase() !== value.toLowerCase()
      )
      setFilteredSuggestions(filtered)
    } else {
      setFilteredSuggestions(suggestions)
    }
  }, [value, suggestions])

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        !inputRef.current?.contains(event.target as Node)
      ) {
        setShowSuggestions(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleSelectSuggestion = (suggestion: string) => {
    onChange(suggestion)
    setShowSuggestions(false)
    inputRef.current?.blur()
  }

  return (
    <div className="relative space-y-2">
      {label && (
        <label
          htmlFor="category-input"
          className="block text-sm font-semibold text-white/90"
        >
          {label}
        </label>
      )}
      <input
        ref={inputRef}
        id="category-input"
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setShowSuggestions(true)}
        disabled={disabled}
        placeholder={placeholder}
        className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-[#3B82F6]/50 backdrop-blur-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      />

      {/* Suggestions dropdown */}
      {showSuggestions && filteredSuggestions.length > 0 && (
        <div
          ref={dropdownRef}
          className="absolute z-20 w-full mt-2 bg-gradient-to-br from-[#1A1F2E] to-[#232936] border border-white/20 rounded-xl shadow-2xl max-h-48 overflow-y-auto backdrop-blur-lg"
        >
          <div className="py-2">
            {filteredSuggestions.map((suggestion, index) => (
              <button
                key={index}
                type="button"
                onClick={() => handleSelectSuggestion(suggestion)}
                className="w-full text-left px-4 py-2.5 text-white/90 hover:bg-[#3B82F6]/20 hover:text-white focus:bg-[#3B82F6]/30 focus:outline-none transition-all border-b border-white/5 last:border-b-0"
              >
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-gradient-to-r from-[#3B82F6] to-[#06B6D4]" />
                  {suggestion}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
