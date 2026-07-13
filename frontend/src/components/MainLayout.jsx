// src/components/MainLayout.jsx
import Sidebar from './Sidebar';
import { Outlet } from 'react-router-dom';

export default function MainLayout() {
    return (
        <div className="flex h-screen">
            <Sidebar /> {/* Sidebar luôn cố định ở đây */}
            <div className="flex-1 overflow-y-auto bg-gray-50">
                <Outlet /> {/* Các trang con (Analysis, Report) sẽ hiển thị ở đây */}
            </div>
        </div>
    );
}