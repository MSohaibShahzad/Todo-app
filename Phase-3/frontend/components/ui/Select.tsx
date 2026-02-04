/**
 * Select dropdown component
 */
import { cn } from "@/lib/utils/cn"
import { SelectHTMLAttributes, forwardRef } from "react"

export interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: Array<{ value: string; label: string }>
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, options, id, ...props }, ref) => {
    const selectId = id || label?.toLowerCase().replace(/\s+/g, "-")

    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={selectId}
            className="block text-sm font-medium text-white/90 mb-2"
          >
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={selectId}
          className={cn(
            "w-full px-3 py-3 border rounded-xl shadow-sm focus:outline-none focus:ring-2 bg-white/10 backdrop-blur-sm text-white transition-all",
            error
              ? "border-red-400/50 focus:ring-red-500 focus:border-red-500"
              : "border-white/20 focus:ring-[#3B82F6] focus:border-[#3B82F6]/50",
            className
          )}
          {...props}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value} className="bg-[#1A1F2E] text-white">
              {option.label}
            </option>
          ))}
        </select>
        {error && <p className="mt-1 text-sm text-red-300">{error}</p>}
      </div>
    )
  }
)

Select.displayName = "Select"
