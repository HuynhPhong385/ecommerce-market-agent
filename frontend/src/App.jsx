//File này chịu trách nhiệm gọi Axios xuống cổng port 8000 của FastAPI, 
// quản lý state loading và kết hợp 3 component trên lại với nhau thành một Dashboard thống nhất.

// src/App.jsx
import React, { useState } from 'react';
import axios from 'axios';
import SearchForm from "/src/components/SearchForm.jsx";
import PriceChart from "/src/components/PriceChart.jsx";
import ReportSection from "/src/components/ReportSection.jsx";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resultData, setResultData] = useState(null);

  const handleSearch = async (keyword) => {
    setLoading(true);
    setError('');
    setResultData(null);

    try {
      // Gọi chính xác POST API Endpoint xuống FastAPI Backend
      const response = await axios.post('http://localhost:8000/api/v1/agent/run-analysis', {
        keyword: keyword
      });

      if (response.data && response.data.status === 'success') {
        // Đổ toàn bộ payload JSON dữ liệu nhận được vào state
        setResultData(response.data.data);
      } else {
        setError('Có lỗi xảy ra trong phản hồi từ Server.');
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Không thể kết nối tới server Backend!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Phần Header Tiêu Đề Dự Án */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-black text-gray-900 mb-2 tracking-tight">
            TIKI MARKET <span className="text-blue-600">AGENT</span>
          </h1>
          <p className="text-gray-600 text-base max-w-md mx-auto">
            Hệ thống tự động cào dữ liệu, phân tích xu hướng giá MySQL và tối ưu SEO bằng LangGraph.
          </p>
        </div>

        {/* Thanh tìm kiếm */}
        <SearchForm onSearch={handleSearch} isLoading={loading} />

        {/* Thông báo lỗi nếu có */}
        {error && (
          <div className="max-w-2xl mx-auto mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-center text-sm">
            ⚠️ {error}
          </div>
        )}

        {/* Dashboard kết quả - Tự động hiển thị khi cào & phân tích xong */}
        {resultData && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8 animate-fade-in">
            {/* Cột trái: Biểu đồ phân phối giá */}
            <PriceChart priceTrends={resultData.price_trends} />
            
            {/* Cột phải: Khung nội dung tối ưu của AI */}
            <ReportSection aiContent={resultData.ai_optimized_content} />
          </div>
        )}
      </div>
    </div>
  );
}