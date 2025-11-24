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
class XacNhan(tk.Toplevel):
    def __init__(self,parent):
        tk.Toplevel.__init__(self,parent)
        self.parent=parent
        self.title("Xác Nhận của Admin")
        center_window(self,400,200)
        self.resizable(False, False)
      
        tk.Label(self, text="Tài khoản Admin:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_taikhoan = tk.Entry(self, width=30)
        self.entry_taikhoan.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Mật khẩu Admin:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_matkhau = tk.Entry(self, show="*", width=30)
        self.entry_matkhau.grid(row=1, column=1, padx=10, pady=10)

        btn_xacnhan = tk.Button(self, text="Xác nhận", width=15, command=self.xac_nhan)
        btn_xacnhan.grid(row=2, column=1, pady=20)
    def xac_nhan(self):
        tk_value = self.entry_taikhoan.get()
        mk_value = self.entry_matkhau.get()
        if not tk_value or not mk_value:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            if tk_value=="admin123" and mk_value=="admin123":
                self.result=True
                self.destroy()  
            else:
                self.result=False
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")
                self.entry_taikhoan.delete(0, tk.END)
                self.entry_matkhau.delete(0, tk.END)
                self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
    def show(self):
        self.parent.wait_window(self)
        return self.result

