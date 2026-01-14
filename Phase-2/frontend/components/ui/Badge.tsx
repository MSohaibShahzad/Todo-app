/**
 * T091: Badge component for displaying labels with color variants
 */

import { cn } from "@/lib/utils/cn";

export interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger" | "info";
  className?: string;
  size?: "sm" | "md" | "lg";
}

const variantClasses = {
  default: "bg-gray-100 text-gray-800 border-gray-300 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700",
  success: "bg-green-100 text-green-800 border-green-300 dark:bg-green-900/20 dark:text-green-300 dark:border-green-700",
  warning: "bg-yellow-100 text-yellow-800 border-yellow-300 dark:bg-yellow-900/20 dark:text-yellow-300 dark:border-yellow-700",
  danger: "bg-red-100 text-red-800 border-red-300 dark:bg-red-900/20 dark:text-red-300 dark:border-red-700",
  info: "bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-700",
};

const sizeClasses = {
  sm: "text-xs px-2 py-0.5",
  md: "text-sm px-2.5 py-1",
  lg: "text-base px-3 py-1.5",
};

export function Badge({
  children,
  variant = "default",
  className,
  size = "sm",
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border font-medium",
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
    >
      {children}
    </span>
  );
}

/**
 * Priority Badge with custom colors
 */
export interface PriorityBadgeProps {
  priority: "low" | "medium" | "high";
  className?: string;
  size?: "sm" | "md" | "lg";
  showIcon?: boolean;
}

export function PriorityBadge({
  priority,
  className,
  size = "sm",
  showIcon = true,
}: PriorityBadgeProps) {
  const { bg, text, border } = getPriorityColorClasses(priority);
  const icon = getPriorityIcon(priority);
  const label = priority.charAt(0).toUpperCase() + priority.slice(1);

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border font-medium",
        bg,
        text,
        border,
        sizeClasses[size],
        className
      )}
    >
      {showIcon && <span>{icon}</span>}
      <span>{label}</span>
    </span>
  );
}

function getPriorityColorClasses(priority: "low" | "medium" | "high") {
  switch (priority) {
    case "high":
      return {
        bg: "bg-red-100 dark:bg-red-900/20",
        text: "text-red-800 dark:text-red-300",
        border: "border-red-300 dark:border-red-700",
      };
    case "medium":
      return {
        bg: "bg-yellow-100 dark:bg-yellow-900/20",
        text: "text-yellow-800 dark:text-yellow-300",
        border: "border-yellow-300 dark:border-yellow-700",
      };
    case "low":
      return {
        bg: "bg-blue-100 dark:bg-blue-900/20",
        text: "text-blue-800 dark:text-blue-300",
        border: "border-blue-300 dark:border-blue-700",
      };
  }
}

function getPriorityIcon(priority: "low" | "medium" | "high"): string {
  switch (priority) {
    case "high":
      return "🔴";
    case "medium":
      return "🟡";
    case "low":
      return "🔵";
  }
}
