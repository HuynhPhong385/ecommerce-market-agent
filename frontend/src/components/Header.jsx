import { useState } from 'react';
import SearchForm from './SearchForm';

export default function Header({ onSearch, isLoading }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="flex justify-between items-center bg-gray-50 px-8 pt-8 pb-4">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Xin chào! </h1>
        <h2 className="text-3xl font-bold text-gray-900 mt-1">Phân tích thị trường Tiki với AI Agent</h2>
        <p className="text-gray-500 mt-1"> Cung cấp cái nhìn toàn diện về dữ liệu thị trường và xu hướng sản phẩm </p>
      </div>

      

      {/* Cửa sổ Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-2xl w-full max-w-lg shadow-2xl">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg font-bold">Nhập từ khóa phân tích</h3>
              <button onClick={() => setIsOpen(false)} className="text-gray-400">Đóng</button>
            </div>
            <SearchForm onSearch={(val) => { onSearch(val); setIsOpen(false); }} isLoading={isLoading} />
          </div>
        </div>
      )}
    </header>
  );
}

