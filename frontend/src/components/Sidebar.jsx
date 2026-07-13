// src/components/Sidebar.jsx
import { Link } from 'react-router-dom';
export default function Sidebar() {
    return (
        <div className="w-64 bg-slate-900 text-white p-6 h-full">
            <h1 className="text-2xl font-bold mb-8">Tiki Agent</h1>
            <nav className="flex flex-col gap-4">
                <Link to="/" className="p-2 hover:bg-slate-700 rounded">Dashboard</Link>
                <Link to="/analysis" className="p-2 hover:bg-slate-700 rounded">Phân tích</Link>
                <Link to="/report" className="p-2 hover:bg-slate-700 rounded">Báo cáo</Link>
            </nav>
        </div>
    );
}