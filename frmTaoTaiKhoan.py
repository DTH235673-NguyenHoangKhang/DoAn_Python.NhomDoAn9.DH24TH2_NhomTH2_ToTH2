import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import frmMain
def connect_db():
 conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\sqlexpress;'  
            'DATABASE=QLCHMBTND;'       
            'Trusted_Connection=yes;')
 return conn
def center_window(win, w=700, h=500):
 ws = win.winfo_screenwidth()
 hs = win.winfo_screenheight()
 x = (ws // 2) - (w // 2)
 y = (hs // 2) - (h // 2)
 win.geometry(f'{w}x{h}+{x}+{y}')
class TaoTaiKhoan(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        center_window(self, 400, 400)
        self.title("Tạo tài khoản")
        lb=tk.Label(self, text="TẠO TÀI KHOẢN", font=("Arial", 20))
        lb.pack(pady=20)
        label_tendangnhap=tk.Label(self, text="Tên Đăng Nhập:")
        label_tendangnhap.pack(pady=10)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)
        label_matkhau=tk.Label(self, text="Mật Khẩu:")
        label_matkhau.pack(pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)
        label_matkhau_check=tk.Label(self, text="Nhập lại mật Khẩu:")
        label_matkhau_check.pack(pady=10)
        self.entry_password_check = tk.Entry(self, show="*")
        self.entry_password_check.pack(pady=5)
        btn_dangnhap = tk.Button(self, text="Tạo tài khoản",command=self.SingUp)
        btn_dangnhap.pack(pady=20)
    def SingUp(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        password_check=self.entry_password_check
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query_check_user = "SELECT TaiKhoan FROM Users WHERE TaiKhoan=?"
            cursor.execute(query_check_user, (username,))
            if cursor.fetchone():
                messagebox.showinfo("Thông báo","Tài khoản đã tồn tại.")
                return
            query_check_nhanvien = "SELECT COUNT(*) FROM NhanVien WHERE MaNV = ? AND tinhtrang = 1"
            cursor.execute(query_check_nhanvien, (username,))
            nhanvien_count = cursor.fetchone()[0]
            if nhanvien_count == 0:
                messagebox.showinfo("Thông báo","Mã nhân viên này chưa được thêm vào hệ thống hoặc không hoạt động.")
                return
            if password != self.entry_password_check.get():
                messagebox.showwarning("Cảnh báo", "Mật khẩu không khớp.")
                return
            query = "insert into users values(?,?,?)"
            cursor.execute(query, (username, password,0))
            conn.commit()
            messagebox.showinfo("Thông báo","Tạo tài khoản thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
        finally:
            cursor.close()
            conn.close()
            