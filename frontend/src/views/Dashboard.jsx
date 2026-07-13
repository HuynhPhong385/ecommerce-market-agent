import React, { useState } from 'react';
import KPICard from '../components/KPICard';
import OverviewChart from '../components/OverviewChart';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import SearchForm from '../components/SearchForm';
import { DollarSign, Package, Store, Star } from 'lucide-react';
// Tạm thời import các icon cơ bản từ lucide-react để test
import { LayoutDashboard, Search, Bell, User } from 'lucide-react';

export default function DashboardLayout() {
  const [isLoading, setIsLoading] = useState(false); 
  const handleSearch = async (keyword) => {
    setIsLoading(true);
    try {
        const response = await fetch("http://localhost:8000/api/v1/dashboard/crawl", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ keyword }),
        });
        const data = await response.json();
        console.log("Kết quả:", data);
        alert("Đã bắt đầu cào dữ liệu cho: " + keyword);
    } catch (error) {
        console.error("Lỗi:", error);
    } finally {
        setIsLoading(false);
    }
};
  return (
    // Container bao phủ toàn màn hình, nền xám nhạt
    <div className="flex h-screen bg-gray-50 font-sans overflow-hidden">   
      
      {/* 2. KHU VỰC CHÍNH (Bên phải) */}
      <main className="flex-1 flex flex-col overflow-hidden">   
        <Header/>
        {/* Nội dung Dashboard (Có thể cuộn) */}
        <div className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Các Grid chứa KPI, Biểu đồ sẽ nằm ở đây */}
            {/* LƯỢC ĐỒ 4 THẺ KPI TIKI */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <KPICard 
                title="Doanh số Tiki" 
                value="1.85T VNĐ" 
                change={14.2} 
                isPositive={true} 
                icon={DollarSign} 
                colorClass="bg-blue-50 text-blue-600" 
              />
              <KPICard 
                title="Sản phẩm đang bán" 
                value="8,420" 
                change={5.8}
                isPositive={true} 
                icon={Package} 
                colorClass="bg-cyan-50 text-cyan-600" 
              />
              <KPICard 
                title="Shop Official & Trading" 
                value="1,250" 
                change={12.0}
                isPositive={true} 
                icon={Store} 
                colorClass="bg-indigo-50 text-indigo-600" 
              />
              <KPICard 
                title="Đánh giá & Review TB" 
                value="4.8 / 5.0" 
                change={-0.2}
                isPositive={false} 
                icon={Star} 
                colorClass="bg-amber-50 text-amber-500" 
              />
            </div>

            {/* BIỂU ĐỒ XU HƯỚNG TIKI */}
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <OverviewChart />
              <p className="mt-4 text-sm text-gray-500">
              </p>
            </div>

          </div>
        </div>
      </main>

    </div>
  );
}