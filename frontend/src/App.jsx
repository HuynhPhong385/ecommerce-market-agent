import React, { useState } from 'react';

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './views/Dashboard'; // Trang tổng quan
import AnalysisPage from './views/AnalysisPage'; // Trang nhập từ khóa
import ReportPage from './views/ReportPages';   // Trang hiển thị kết quả
import MainLayout from './components/MainLayout';
export default function App() {
    const [isLoading, setIsLoading] = useState(false);

    // Hàm handleSearch này sẽ được dùng chung bởi các trang
    const handleSearch = async (keyword, navigate) => {
        setIsLoading(true);
        try {
            const response = await fetch("http://localhost:8000/api/v1/dashboard/crawl", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ keyword }),
            });
            
            if (response.ok) {
                alert("Cào dữ liệu thành công cho: " + keyword);
                navigate('/report'); // Chuyển hướng sang trang báo cáo sau khi cào xong
            } else {
                alert("Có lỗi xảy ra khi cào dữ liệu.");
            }
        } catch (error) {
            console.error("Lỗi:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainLayout />}>
                    <Route index element={<DashboardLayout />} />
                    <Route path="analysis" element={<AnalysisPage onSearch={handleSearch} isLoading={isLoading} />} />
                    <Route path="report" element={<ReportPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}