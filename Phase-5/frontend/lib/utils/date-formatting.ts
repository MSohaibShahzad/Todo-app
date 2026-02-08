/**
 * T102: Date formatting utilities for due dates
 */

/**
 * Format a date string for display
 */
export function formatDueDate(date: string | null): string {
  if (!date) return "";

  const dueDate = new Date(date);
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  const dueDay = new Date(
    dueDate.getFullYear(),
    dueDate.getMonth(),
    dueDate.getDate()
  );

  // Check if today
  if (dueDay.getTime() === today.getTime()) {
    return "Today";
  }

  // Check if tomorrow
  if (dueDay.getTime() === tomorrow.getTime()) {
    return "Tomorrow";
  }

  // Check if this week
  const diffDays = Math.ceil((dueDay.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
  if (diffDays > 0 && diffDays <= 7) {
    return dueDate.toLocaleDateString("en-US", { weekday: "long" });
  }

  // Format as date
  return dueDate.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: dueDate.getFullYear() !== now.getFullYear() ? "numeric" : undefined,
  });
}

/**
 * Check if a date is overdue
 */
export function isOverdue(date: string | null, completed: boolean): boolean {
  if (!date || completed) return false;

  const dueDate = new Date(date);
  const now = new Date();

  return dueDate < now;
}

/**
 * Check if a date is due today
 */
export function isDueToday(date: string | null): boolean {
  if (!date) return false;

  const dueDate = new Date(date);
  const now = new Date();

  return (
    dueDate.getDate() === now.getDate() &&
    dueDate.getMonth() === now.getMonth() &&
    dueDate.getFullYear() === now.getFullYear()
  );
}

/**
 * Get relative time string (e.g., "in 2 days", "3 days ago")
 */
export function getRelativeTime(date: string | null): string {
  if (!date) return "";

  const dueDate = new Date(date);
  const now = new Date();
  const diffMs = dueDate.getTime() - now.getTime();
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "Tomorrow";
  if (diffDays === -1) return "Yesterday";
  if (diffDays > 1) return `in ${diffDays} days`;
  if (diffDays < -1) return `${Math.abs(diffDays)} days ago`;

  return "";
}

/**
 * Format date for input field (YYYY-MM-DD)
 */
export function formatDateForInput(date: string | Date | null): string {
  if (!date) return "";

  const d = typeof date === "string" ? new Date(date) : date;
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}
