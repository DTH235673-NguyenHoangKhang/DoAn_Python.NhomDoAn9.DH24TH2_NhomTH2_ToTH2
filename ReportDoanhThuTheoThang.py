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
def export_to_pdf(thang,nam,doanhthu, thue,loinhuan, items):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    # Tạo đường dẫn file tạm thời
    file_name = f"DoanhThuTheoNgay_InTruoc_{thang}_{nam}.pdf"
    file_path = os.path.join(TEMP_DIR, file_name)

    # 1. KHỞI TẠO CANVAS VÀ CÀI ĐẶT
    c = canvas.Canvas(file_path, pagesize=PAGE_SIZE)
    width, height = PAGE_SIZE 
    y_start = height - 50
    line_height = 18
    margin = 50
    try:
        c.setFont(FONT_BOLD, 16)
        c.drawCentredString(width/2, y_start, "DOANH THU THEO THÁNG")
        
        c.setFont(FONT_NAME, 10)
        c.drawString(margin, y_start - line_height, "Cửa hàng: CỬA HÀNG THUỐC NÔNG DƯỢC")
        c.drawString(width/2, y_start-line_height, f"Tháng: {thang}-{nam}")
        y_start-=2*line_height

        c.line(margin, y_start, width - margin, y_start) 
        y_start -= line_height
        headers = ["Ngày", "Doanh thu", "COS","VAT","Lợi nhuận gộp"]
        col_widths = [100,100,100,100,100, 100]
        x_pos = margin
        c.setFont(FONT_NAME, 10)
        for i, header in enumerate(headers):
            c.drawString(x_pos, y_start, header)
            x_pos += col_widths[i]
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
        
        total_text = f"Tổng doanh thu thực tế: {doanhthu:,.0f} VNĐ"
        # Vẽ chuỗi căn phải
        c.drawString(width - margin - c.stringWidth(total_text, FONT_NAME, 12), y_start, total_text)
        y_start -= line_height
        total_text = f"Thuế: {thue:,.0f} VNĐ"
        c.drawString(width - margin - c.stringWidth(total_text, FONT_NAME, 12), y_start, total_text)
        y_start -= line_height
        total_text = f"Tổng lợi nhuận gộp: {loinhuan:,.0f} VNĐ"
        c.drawString(width - margin - c.stringWidth(total_text, FONT_NAME, 12), y_start, total_text)
        c.save() 
        return file_path
    except Exception as e:
        messagebox.showerror("Lỗi Xuất PDF", f"Không thể tạo file PDF: {e}")
        return None