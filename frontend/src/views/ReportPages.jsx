// src/components/ReportPages.jsx
import React from 'react';
import { Sparkles, Copy, Check } from 'lucide-react';

export default function ReportPage({ aiContent }) {
  const [copied, setCopied] = React.useState(false);

  if (!aiContent || !aiContent.title) {
    return <div className="text-gray-500 text-center py-6">Đang đợi dữ liệu phân tích từ AI...</div>;
  }

  // Xử lý logic nút bấm Copy nhanh nội dung để mang đi đăng bán sản phẩm
  const handleCopy = () => {
    const fullText = `Tiêu đề: ${aiContent.title}\n\nMô tả:\n${aiContent.description}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000); // 2 giây sau tự trả về trạng thái cũ
  };

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-6 rounded-2xl border border-indigo-100 shadow-sm relative">
      {/* Nút Copy nhanh tích hợp góc trên bên phải */}
      <button 
        onClick={handleCopy}
        className="absolute top-4 right-4 p-2 bg-white hover:bg-gray-100 rounded-lg border border-gray-200 shadow-xs transition-all"
        title="Sao chép toàn bộ nội dung"
      >
        {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4 text-gray-600" />}
      </button>

      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-purple-600 animate-pulse" />
        <h3 className="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-900 to-purple-900">
          Nội Dung Tối Ưu Bởi Gemini AI
        </h3>
      </div>

      {/* Phần 1: Tiêu đề gợi ý chuẩn SEO sàn thương mại điện tử */}
      <div className="mb-5 bg-white p-4 rounded-xl border border-indigo-50">
        <span className="text-xs font-semibold uppercase tracking-wider text-indigo-500 block mb-1">Tiêu đề đề xuất:</span>
        <p className="text-base font-semibold text-gray-800">{aiContent.title}</p>
      </div>

      {/* Phần 2: Nội dung mô tả chi tiết bài viết sản phẩm */}
      <div className="bg-white p-4 rounded-xl border border-indigo-50">
        <span className="text-xs font-semibold uppercase tracking-wider text-purple-500 block mb-1">Mô tả sản phẩm cạnh tranh:</span>
        <div className="text-gray-700 whitespace-pre-line leading-relaxed text-sm">
          {aiContent.description}
        </div>
      </div>
    </div>
  );
}