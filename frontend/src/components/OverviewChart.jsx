import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function OverviewChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
  fetch('http://localhost:8000/api/v1/dashboard/chart-data')
    .then(res => res.json())
    .then(json => {
      // Sắp xếp lại dữ liệu theo ngày tăng dần để tránh nhảy lộn
      const sortedData = json.sort((a, b) => new Date(a.date) - new Date(b.date));
      setData(sortedData);
    });
}, []);

  return (
    <div className="bg-white p-6 rounded-2xl border shadow-sm" style={{ height: 450 }}>
      <h3 className="text-lg font-bold mb-4">Xu hướng doanh thu theo Ngành hàng</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" />
          <YAxis  tickFormatter={(val) => `${(val / 1000000).toFixed(0)}tr`} />
          <Tooltip 
            formatter={(val) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val)}
          />
          <Legend 
            verticalAlign="bottom" 
            height={36} 
            wrapperStyle={{ 
              paddingTop: '30px', // Tạo khoảng cách giữa biểu đồ và chú thích
              paddingBottom: '10px' 
            }} 
          />
          <Line type="monotone" dataKey="Dien tu" stroke="#8884d8" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Do gia dung" stroke="#82ca9d" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Do choi" stroke="#ff7300" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Thoi trang" stroke="#ff0000" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="My pham" stroke="#a4de6c" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}