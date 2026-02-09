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
      <div className="w-full space-y-2">
        {label && (
          <label
            htmlFor={selectId}
            className="block text-sm font-semibold text-gray-700"
          >
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <select
          ref={ref}
          id={selectId}
          className={cn(
            "w-full px-4 py-3 bg-gray-50 border rounded-xl text-gray-900 focus:outline-none focus:ring-2 transition-all",
            "disabled:opacity-50 disabled:cursor-not-allowed",
            error
              ? "border-red-400 focus:ring-red-500 focus:border-red-500"
              : "border-gray-300 focus:ring-[#3B82F6] focus:border-[#3B82F6]",
            className
          )}
          {...props}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value} className="bg-white text-gray-900">
              {option.label}
            </option>
          ))}
        </select>
        {error && <p className="mt-1.5 text-sm text-red-400">{error}</p>}
      </div>
    )
  }
)

Select.displayName = "Select"
