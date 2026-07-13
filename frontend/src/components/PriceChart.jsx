// src/components/PriceChart.jsx
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function PriceChart({ priceTrends }) {
  if (!priceTrends || priceTrends.error) {
    return <div className="text-gray-500 text-center py-6">Không có dữ liệu giá hợp lệ.</div>;
  }

  // Định dạng lại cấu trúc dữ liệu thô từ FastAPI để nạp vào biểu đồ Recharts
  const data = [
    { name: 'Thấp Nhất', price: priceTrends.lowest_price, color: '#10B981' }, // Xanh lá
    { name: 'Trung Bình', price: priceTrends.average_price, color: '#3B82F6' }, // Xanh dương
    { name: 'AI Gợi Ý', price: priceTrends.suggested_price, color: '#8B5CF6' }, // Tím độc quyền
    { name: 'Cao Nhất', price: priceTrends.highest_price, color: '#EF4444' }, // Đỏ
  ];

  const formatVND = (value) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">📊 Xu Hướng Định Giá Thị Trường</h3>
      <p className="text-sm text-gray-500 mb-6">Dựa trên phân tích mẫu của {priceTrends.total_analyzed} sản phẩm từ MySQL</p>
      
      {/* Khung chứa biểu đồ co giãn tự động */}
      <div className="w-full h-72">
        <ResponsiveContainer width="100%" h="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F3F4F6" />
            <XAxis dataKey="name" tick={{ fill: '#6B7280', fontSize: 13 }} axisLine={false} tickLine={false} />
            <YAxis tickFormatter={formatVND} tick={{ fill: '#6B7280', fontSize: 11 }} axisLine={false} tickLine={false} />
            <Tooltip formatter={(value) => [formatVND(value), 'Mức giá']} contentStyle={{ borderRadius: '8px', border: '1px solid #E5E7EB' }} />
            
            <Bar dataKey="price" radius={[8, 8, 0, 0]} barSize={50}>
              {/* Đổ màu động riêng biệt cho từng cột dữ liệu */}
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}