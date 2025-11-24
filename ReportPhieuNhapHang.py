from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from tkinter import messagebox
import os
TEMP_DIR = os.path.join(os.environ.get('TEMP', '/tmp'), 'PhieuMuaHang_Temp')
try:
    registerFont(TTFont('Arial-Regular', 'C:\\Windows\\Fonts\\Arial.ttf'))
    registerFont(TTFont('Arial-Bold', 'C:\\Windows\\Fonts\\Arialbd.ttf')) 
    FONT_NAME = 'Arial-Regular'
    FONT_BOLD = 'Arial-Bold'
except:
    FONT_NAME = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold' 
PAGE_SIZE = A4
def export_to_pdf(sophieu, ngaylap,trangthai,tennv, tenncc, diachi, sdt, tongtien, items):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    # Tạo đường dẫn file tạm thời
    file_name = f"PhieuNhapHang_InTruoc_{sophieu}.pdf"
    file_path = os.path.join(TEMP_DIR, file_name)
    # 1. KHỞI TẠO CANVAS VÀ CÀI ĐẶT
    c = canvas.Canvas(file_path, pagesize=PAGE_SIZE)
    width, height = PAGE_SIZE 
    y_start = height - 50
    line_height = 18
    margin = 50
    try:
        c.setFont(FONT_BOLD, 16)
        c.drawCentredString(width/2, y_start, "PHIẾU NHẬP HÀNG")
        c.setFont(FONT_NAME, 10)
        c.drawString(margin, y_start - line_height, "Cửa hàng: CỬA HÀNG THUỐC NÔNG DƯỢC")
        y_start -=  2*line_height
        c.drawString(margin, y_start, f"Mã Phiếu: {sophieu}")
        c.drawString(width/2, y_start, f"Ngày lập: {ngaylap}")
        c.drawString(width - margin - c.stringWidth(f"Trạng thái: {trangthai}", FONT_NAME, 12), y_start, f"Trạng thái: {trangthai}")
        y_start-=line_height
        c.line(margin, y_start, width - margin, y_start) 
        y_start -= line_height
        c.drawString(margin, y_start, f"Nhà cung cấp: {tenncc}")
        y_start -= line_height
        c.drawString(margin, y_start, f"Địa chỉ: {diachi}")
        y_start -= line_height
        c.drawString(margin, y_start, f"SĐT: {sdt}")
        y_start -= line_height
        # === 3. CHI TIẾT SẢN PHẨM (Bảng) ===
        c.line(margin, y_start, width - margin, y_start) 
        y_start -= line_height
        # Header bảng
        headers = ["Tên Thuốc", "Số lượng", "Giá bán","Đơn vị", "Thành tiền"]
        col_widths = [200,60, 60,60, 100]
        x_pos = margin
        c.setFont(FONT_NAME, 10)
        for i, header in enumerate(headers):
            c.drawString(x_pos, y_start, header)
            x_pos += col_widths[i]
        # Đường kẻ dưới tiêu đề bảng
        y_start -= 3 
        c.line(margin, y_start, width - margin, y_start)
        y_start -= line_height
        # Dữ liệu bảng
        for item in items:
            x_pos = margin
            for i, data in enumerate(item):
                c.drawString(x_pos, y_start, str(data))
                x_pos += col_widths[i]
            y_start -= line_height
        c.line(margin, y_start, width - margin, y_start) 
        y_start -= line_height
        c.setFont(FONT_BOLD, 12)
        total_text = f"TỔNG THANH TOÁN: {tongtien:,.0f} VNĐ"
        c.drawString(width - margin - c.stringWidth(total_text, FONT_NAME, 12), y_start, total_text)
        y_start -= line_height
        c.setFont(FONT_NAME, 12)
        total_text = f"Nhân viên lập phiếu"
        c.drawString(width - margin - c.stringWidth(total_text, FONT_NAME, 12), y_start, total_text)
        y_start -= 5*line_height
        total_text = f"{tennv}       "
        c.drawString(width - margin - c.stringWidth(total_text, FONT_NAME, 12), y_start, total_text)

        c.save()
        return file_path 
    except Exception as e:
        messagebox.showerror("Lỗi Xuất PDF", f"Không thể tạo file PDF: {e}")
        return None