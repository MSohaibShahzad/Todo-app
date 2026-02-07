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
  blue: "bg-[#3B82F6] text-white",
  green: "bg-[#10B981] text-white",
  yellow: "bg-[#F59E0B] text-white",
  red: "bg-[#EF4444] text-white",
  purple: "bg-[#8B5CF6] text-white",
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
          <div className={`rounded-xl p-3 ${colorClasses[color]} shadow-lg`}>
            <Icon className="h-6 w-6" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-white/70">
              {label}
            </p>
            <p className="text-2xl font-bold text-white">
              {count}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
