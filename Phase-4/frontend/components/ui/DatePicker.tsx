/**
 * T103: DatePicker component with calendar selection
 */
"use client";

import { Input } from "@/components/ui/Input";
import { formatDateForInput } from "@/lib/utils/date-formatting";

export interface DatePickerProps {
  label?: string;
  value: string | null;
  onChange: (value: string) => void;
  disabled?: boolean;
  placeholder?: string;
  minDate?: string;
}

export function DatePicker({
  label,
  value,
  onChange,
  disabled,
  placeholder = "Select date",
  minDate,
}: DatePickerProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return (
    <Input
      label={label}
      type="date"
      value={value ? formatDateForInput(value) : ""}
      onChange={handleChange}
      disabled={disabled}
      placeholder={placeholder}
      min={minDate}
    />
  );
}
