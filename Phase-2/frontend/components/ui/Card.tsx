/**
 * Card component for container styling
 * T117: Responsive padding and font sizes
 */
import { cn } from "@/lib/utils/cn"
import { HTMLAttributes, forwardRef } from "react"

export interface CardProps extends HTMLAttributes<HTMLDivElement> {}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-lg border border-gray-200 bg-white shadow-sm",
          className
        )}
        {...props}
      />
    )
  }
)

Card.displayName = "Card"

export const CardHeader = forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn("flex flex-col space-y-1.5 p-4 sm:p-6", className)}
        {...props}
      />
    )
  }
)

CardHeader.displayName = "CardHeader"

export const CardTitle = forwardRef<
  HTMLParagraphElement,
  HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => {
  return (
    <h3
      ref={ref}
      className={cn("text-xl sm:text-2xl font-semibold leading-none", className)}
      {...props}
    />
  )
})

CardTitle.displayName = "CardTitle"

export const CardContent = forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => {
    return <div ref={ref} className={cn("p-4 pt-0 sm:p-6", className)} {...props} />
  }
)

CardContent.displayName = "CardContent"
