/**
 * T090: Priority color utilities for Tailwind CSS
 */

export type Priority = "low" | "medium" | "high";

/**
 * Get Tailwind CSS color classes for a priority level
 */
export function getPriorityColor(priority: Priority): {
  bg: string;
  text: string;
  border: string;
} {
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
    default:
      return {
        bg: "bg-gray-100 dark:bg-gray-800",
        text: "text-gray-800 dark:text-gray-300",
        border: "border-gray-300 dark:border-gray-700",
      };
  }
}

/**
 * Get display label for priority
 */
export function getPriorityLabel(priority: Priority): string {
  return priority.charAt(0).toUpperCase() + priority.slice(1);
}

/**
 * Get priority icon (emoji)
 */
export function getPriorityIcon(priority: Priority): string {
  switch (priority) {
    case "high":
      return "🔴";
    case "medium":
      return "🟡";
    case "low":
      return "🔵";
    default:
      return "⚪";
  }
}
