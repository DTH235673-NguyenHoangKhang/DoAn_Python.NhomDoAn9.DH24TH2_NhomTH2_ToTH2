import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
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
class DangNhap(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        center_window(self, 400, 300)
        self.title("Đăng Nhập")
        lb=tk.Label(self, text="ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 20))
        lb.pack(pady=20)
        label_tendangnhap=tk.Label(self, text="Tên Đăng Nhập:")
        label_tendangnhap.pack(pady=10)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)
        label_matkhau=tk.Label(self, text="Mật Khẩu:")
        label_matkhau.pack(pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)
        btn_dangnhap = tk.Button(self, text="Đăng Nhập",command=self.dang_nhap)
        btn_dangnhap.pack(pady=20)
    def dang_nhap(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "SELECT * FROM Users WHERE TaiKhoan=? AND MatKhau=?"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result:
                self.destroy()  
                import frmMain
                main=frmMain.Main(username)
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
        finally:
            cursor.close()
            conn.close()
    def show(self):
       self.mainloop()
login=DangNhap()
login.mainloop()