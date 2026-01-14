/**
 * T108: StatsCard component displaying count with label and icon
 */
"use client";

import { Card, CardContent } from "@/components/ui/Card";
import { LucideIcon } from "lucide-react";

export interface StatsCardProps {
  label: string;
  count: number;
  icon: LucideIcon;
  color?: "blue" | "green" | "yellow" | "red" | "purple";
}

const colorClasses = {
  blue: "bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400",
  green: "bg-green-100 text-green-600 dark:bg-green-900/20 dark:text-green-400",
  yellow: "bg-yellow-100 text-yellow-600 dark:bg-yellow-900/20 dark:text-yellow-400",
  red: "bg-red-100 text-red-600 dark:bg-red-900/20 dark:text-red-400",
  purple: "bg-purple-100 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400",
};

export function StatsCard({
  label,
  count,
  icon: Icon,
  color = "blue",
}: StatsCardProps) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center gap-4">
          <div className={`rounded-full p-3 ${colorClasses[color]}`}>
            <Icon className="h-6 w-6" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {label}
            </p>
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {count}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
