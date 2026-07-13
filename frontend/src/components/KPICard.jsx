import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function KPICard({ title, value, change, icon: Icon }) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <h3 className="text-2xl font-bold mt-1">{value}</h3>
        </div>
        <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
          <Icon size={20} />
        </div>
      </div>
      <p className={`text-sm mt-4 ${change > 0 ? 'text-green-500' : 'text-red-500'}`}>
        {change > 0 ? '▲' : '▼'} {Math.abs(change)}% so với tuần trước
      </p>
    </div>
  );
}