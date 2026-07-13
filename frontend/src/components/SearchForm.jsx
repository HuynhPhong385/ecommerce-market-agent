// src/components/SearchForm.jsx
import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react'; // Import icon đẹp mắt

export default function SearchForm({ onSearch, isLoading }) {
  const [keyword, setKeyword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Đang nhấn nút Phân Tích với keyword:", keyword);
    onSearch(keyword); // Truyền giá trị này lên App.jsx
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto mb-8">
      <div className="relative flex items-center">
        {/* Ô nhập từ khóa tìm kiếm */}
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Nhập sản phẩm cần phân tích"
          disabled={isLoading}
          className="w-full px-5 py-4 pl-12 text-gray-900 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
        />
        {/* Kính lúp Icon */}
        <Search className="absolute left-4 text-gray-400 w-5 h-5" />
        
        {/* Nút bấm Kích hoạt luồng Agent */}
        <button
          type="submit"
          disabled={isLoading || !keyword.trim()}
          className="absolute right-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 disabled:bg-blue-400"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" /> {/* Xoay xoay khi loading */}
              Analyzing...
            </>
          ) : (
            'Phân Tích'
          )}
        </button>
      </div>
    </form>
  );
}