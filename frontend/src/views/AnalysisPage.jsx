import React, { useState } from 'react'; // Cần để quản lý ô nhập liệu
import { useNavigate } from 'react-router-dom'; // Cần để điều hướng

const POPULAR_SEARCHES = [
    { title: "Iphone 17 Promax", img: "/icons/iphone_17_pro_max_.png" },
    { title: "Vợt đánh cầu lông", img: "/icons/vot.png" },
    { title: "Quần tây nam", img: "/icons/quan_tay.png" },
    { title: "Tai nghe AirPods", img: "/icons/airpods.png" },
    { title: "Áo Hoodie giá rẻ", img: "/icons/hoodie.png" },
    { title: "Bàn phím gaming", img: "/icons/Ban phim.png" },
];

const CATEGORIES = [
    { name: "Đồ Chơi - Mẹ & Bé", img: "/icons/Do choi.png" },
    { name: "Điện Thoại", img: "/icons/Dien thoai.png" },
    { name: "Đồ điện tử", img: "/icons/Dien tu.png" },
    { name: "Đồ gia dụng", img: "/icons/Do gia dung.png" },
    { name: "Mỹ phẩm ", img: "/icons/My pham.png" },
    { name: "Thoi trang", img: "/icons/Thoi trang.png" },
    { name: "Dụng cụ tập thể thao", img: "/icons/vot.png" },
    { name: "Giày & dép", img: "/icons/bata.png" },
];
export default function AnalysisPage({ onSearch }) {
    const [keyword, setKeyword] = useState("");
    const navigate = useNavigate();

    // Hàm gọi khi nhấn nút
    const handleSuggestionClick = (name) => {
        setKeyword(name); // Cập nhật state keyword
        // Sau khi set, gọi luôn hàm tìm kiếm
        onSearch(name, navigate); 
    };
    return (
        <div className="p-8 max-w-4xl mx-auto bg-white rounded-lg shadow-sm">
            {/* Thanh tìm kiếm */}
            <div className="flex border-b pb-4">
                <input 
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    placeholder="Nhập từ khóa..."
                />
                <button onClick={() => onSearch(keyword, navigate)}>Tìm kiếm</button>
                </div>

            {/* Tìm kiếm phổ biến */}
            <div className="mt-6">
                <h3 className="font-bold">Tìm Kiếm Phổ Biến</h3>
                <div className="grid grid-cols-3 gap-4 mt-4">
                    {POPULAR_SEARCHES.map((item, index) => (
                        <button 
                            key={index} 
                            onClick={() => handleSuggestionClick(item.title)} // <--- CLICK LÀ TỰ ĐIỀN
                            className="flex items-center gap-2 border p-2 hover:bg-gray-100"
                        >
                            <img src={item.img} className="w-8 h-8" alt="" />
                            <span>{item.title}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Danh mục nổi bật */}
            <div className="mt-8">
                <h3 className="font-bold mb-4">Danh Mục Nổi Bật</h3>
                <div className="grid grid-cols-4 gap-6">
                    {CATEGORIES.map((cat, index) => (
                        <button 
                            key={index} onClick={() => handleSuggestionClick(cat.name)}
                            className="flex flex-col items-center"
                        >
                            <div className="w-20 h-20 rounded-full border overflow-hidden">
                                <img src={cat.img} alt={cat.name} className="w-full h-full object-cover" />
                            </div>
                            <p className="mt-2 text-sm text-center">{cat.name}</p>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}