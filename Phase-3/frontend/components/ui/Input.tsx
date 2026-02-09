/**
 * Input component with label and error state
 */
import { cn } from "@/lib/utils/cn"
import { InputHTMLAttributes, forwardRef } from "react"

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, "-")

    return (
      <div className="w-full space-y-2">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-semibold text-gray-700"
          >
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            "w-full px-4 py-3 bg-gray-50 border rounded-xl text-gray-900 placeholder:text-gray-400",
            "focus:outline-none focus:ring-2 transition-all",
            "disabled:opacity-50 disabled:cursor-not-allowed",
            error
              ? "border-red-400 focus:ring-red-500 focus:border-red-500"
              : "border-gray-300 focus:ring-[#3B82F6] focus:border-[#3B82F6]",
            className
          )}
          {...props}
        />
        {error && <p className="mt-1.5 text-sm text-red-400">{error}</p>}
      </div>
    )
  }
)

Input.displayName = "Input"
