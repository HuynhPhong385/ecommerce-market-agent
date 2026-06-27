// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Cấu hình lõi giúp Vite định vị chính xác file chạy và fix lỗi 404 đường dẫn
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true, // Không tự động đổi port nếu port 5173 bị chiếm
    // Cấu hình dự phòng giúp xử lý các request route không khớp về lại index.html
    historyApiFallback: true, 
  },
  root: '.', // Chỉ định thư mục hiện tại làm thư mục gốc chứa index.html
})