/**
 * T109: TaskSummary component calculating and displaying stats from tasks
 */
"use client";

import { StatsCard } from "@/components/features/dashboard/StatsCard";
import type { Task } from "@/types/task";
import { useMemo } from "react";
import {
  AlertCircle,
  Calendar,
  CheckCircle2,
  Clock,
  ListTodo,
} from "lucide-react";

interface TaskSummaryProps {
  tasks: Task[];
}

export function TaskSummary({ tasks }: TaskSummaryProps) {
  const summary = useMemo(() => {
    const total = tasks.length;
    const pending = tasks.filter((t) => !t.completed).length;
    const completed = tasks.filter((t) => t.completed).length;
    const overdue = tasks.filter((t) => t.is_overdue && !t.completed).length;
    const due_today = tasks.filter((t) => t.is_due_today && !t.completed).length;

    // Calculate due_tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowDate = tomorrow.toDateString();

    const due_tomorrow = tasks.filter((t) => {
      if (!t.due_date || t.completed) return false;
      const taskDate = new Date(t.due_date);
      return taskDate.toDateString() === tomorrowDate;
    }).length;

    return {
      total,
      pending,
      completed,
      overdue,
      due_today,
      due_tomorrow,
    };
  }, [tasks]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-8">
      <StatsCard
        label="Total Tasks"
        count={summary.total}
        icon={ListTodo}
        color="blue"
      />
      <StatsCard
        label="Pending"
        count={summary.pending}
        icon={Clock}
        color="purple"
      />
      <StatsCard
        label="Completed"
        count={summary.completed}
        icon={CheckCircle2}
        color="green"
      />
      <StatsCard
        label="Overdue"
        count={summary.overdue}
        icon={AlertCircle}
        color="red"
      />
      <StatsCard
        label="Due Today"
        count={summary.due_today}
        icon={Calendar}
        color="yellow"
      />
      <StatsCard
        label="Due Tomorrow"
        count={summary.due_tomorrow}
        icon={Calendar}
        color="blue"
      />
    </div>
  );
}
