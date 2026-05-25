"use client";

import { HTMLAttributes, TdHTMLAttributes, ThHTMLAttributes, forwardRef } from "react";

export const Table = forwardRef<HTMLTableElement, HTMLAttributes<HTMLTableElement>>(
  ({ className = "", ...props }, ref) => (
    <table ref={ref} className={`min-w-full divide-y divide-gray-200 ${className}`} {...props} />
  )
);
Table.displayName = "Table";

export const TableHeader = forwardRef<HTMLTableSectionElement, HTMLAttributes<HTMLTableSectionElement>>(
  ({ className = "", ...props }, ref) => (
    <thead ref={ref} className={`bg-gray-50 ${className}`} {...props} />
  )
);
TableHeader.displayName = "TableHeader";

export const TableBody = forwardRef<HTMLTableSectionElement, HTMLAttributes<HTMLTableSectionElement>>(
  ({ ...props }, ref) => <tbody ref={ref} className="divide-y divide-gray-200 bg-white" {...props} />
);
TableBody.displayName = "TableBody";

export const TableRow = forwardRef<HTMLTableRowElement, HTMLAttributes<HTMLTableRowElement>>(
  ({ className = "", ...props }, ref) => (
    <tr ref={ref} className={`hover:bg-gray-50 ${className}`} {...props} />
  )
);
TableRow.displayName = "TableRow";

export const TableHead = forwardRef<HTMLTableCellElement, ThHTMLAttributes<HTMLTableCellElement>>(
  ({ className = "", ...props }, ref) => (
    <th ref={ref} className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 ${className}`} {...props} />
  )
);
TableHead.displayName = "TableHead";

export const TableCell = forwardRef<HTMLTableCellElement, TdHTMLAttributes<HTMLTableCellElement>>(
  ({ className = "", ...props }, ref) => (
    <td ref={ref} className={`whitespace-nowrap px-6 py-4 text-sm text-gray-900 ${className}`} {...props} />
  )
);
TableCell.displayName = "TableCell";
