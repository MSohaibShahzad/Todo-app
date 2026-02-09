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
          className="block text-sm font-semibold text-gray-700"
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
        className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-xl text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-[#3B82F6] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      />

      {/* Suggestions dropdown */}
      {showSuggestions && filteredSuggestions.length > 0 && (
        <div
          ref={dropdownRef}
          className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-48 overflow-y-auto"
        >
          <div className="py-1">
            {filteredSuggestions.map((suggestion, index) => (
              <button
                key={index}
                type="button"
                onClick={() => handleSelectSuggestion(suggestion)}
                className="w-full text-left px-3 py-2 hover:bg-blue-50 hover:text-blue-700 focus:bg-blue-50 focus:outline-none transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
