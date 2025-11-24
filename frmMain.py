import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import ctypes
from PIL import Image, ImageTk
import frmThuoc as t
import frmPhieuMuaHang as pmh
import frmPhieuNhapHang as pnh
import frmDoanhThuTheoNgay as dttn
import frmDoanhThuTheoThang as dttt
import frmThongKe as thk
import frmTaoTaiKhoan as taikhoan
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
class AnhNen(tk.Frame):
   def __init__(self, parent, main_app): 
      tk.Frame.__init__(self, parent)
      self.main_app = main_app
      self.parent=parent
      try:
            pil_image = Image.open("c:\\Users\\KHANG\\Downloads\\QUẢN LÝ CỬA HÀNG MUA BÁN THUỐC NÔNG DƯỢC.png") 
            pil_image = pil_image.resize((800, 600 ), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(pil_image)
            lbl_bg = tk.Label(self, image=self.bg_image)
            lbl_bg.pack(fill="both", expand=True)
      except Exception as e:
             messagebox.showwarning("Cảnh báo", f"Lỗi tải ảnh nền: {e}")
class Main(tk.Tk):
    def __init__(self,username):
        super().__init__()
        center_window(self, 800, 550)
        self.username=username    
        self.withdraw()
        self.title("Quản lý cửa hàng mua bán thuốc nông dược")
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frames = {} 
        for F in (thk.ThongKe,dttt.DoanhThuTheoThang,dttn.DoanhThuTheoNgay,pnh.PhieuNhapHang,t.Thuoc):
            frame=F(container,self)
            frame.grid(row=0,column=0,sticky="nsew")
            self.frames[F]=frame
        frame_pmh = pmh.PhieuMuaHang(container, self, self.username)
        frame_pmh.grid(row=0, column=0, sticky="nsew")
        self.frames[pmh.PhieuMuaHang] = frame_pmh
        frame_nen = AnhNen(container,self)
        frame_nen.grid(row=0, column=0, sticky="nsew")
        self.frames[AnhNen] = frame_nen
        self.showPage(AnhNen)
        my_menu=tk.Menu(self)
        self.config(menu=my_menu)
        file_menu=tk.Menu(my_menu, tearoff=0)
        my_menu.add_command(label="Trang chủ",command=lambda: self.showPage(AnhNen))
        my_menu.add_command(label="Quản lý thuốc",command=lambda: self.showPage(t.Thuoc))
        my_menu.add_command(label="Phiếu nhập hàng",command=lambda: self.showPage(pnh.PhieuNhapHang))
        my_menu.add_command(label="Phiếu mua hàng",command=lambda: self.showPage(pmh.PhieuMuaHang))
        dt_menu=tk.Menu(my_menu,tearoff=0)
        dt_menu.add_command(label="Doanh thu theo ngày",command=lambda: self.showPage(dttn.DoanhThuTheoNgay))
        dt_menu.add_command(label="Doanh thu theo tháng",command=lambda: self.showPage(dttt.DoanhThuTheoThang))
        my_menu.add_cascade(label="Báo cáo doanh thu",menu=dt_menu)
        my_menu.add_command(label="Thống kê",command=lambda: self.showPage(thk.ThongKe))
        my_menu.add_command(label="Tạo tài khoản", command=lambda: self.TaoTaiKhoan())
        my_menu.add_command(label="Đăng xuất", command=lambda: self.DangXuat())
        my_menu.add_command(label="Thoát", command=self.Thoat)
        self.protocol("WM_DELETE_WINDOW", self.Thoat)
        if self.username!="admin123":
            my_menu.entryconfig(2, state="disabled")
            my_menu.entryconfig(3, state="disabled")
            my_menu.entryconfig(5, state="disabled")
            my_menu.entryconfig(6, state="disabled")
            my_menu.entryconfig(7, state="disabled")
        self.after(0,self.deiconify)
        self.mainloop()
    def showPage(self,page):
        if page == pmh.PhieuMuaHang:
            self.frames[pmh.PhieuMuaHang].tkraise()
        else:
            self.frames[page].tkraise()
    def Thoat(self):
        r=messagebox.askyesno("Thoát","Bạn có thật sự muốn thoát?")
        if r==False:
            return
        self.destroy()
    def DangXuat(self):
        self.destroy()
        import DangNhap as dn
        dangnhap=dn.DangNhap()
        dangnhap.show()
    def TaoTaiKhoan(self):
        chi_tiet_window = taikhoan.TaoTaiKhoan()
        chi_tiet_window.grab_set()
        self.wait_window(chi_tiet_window)
        
        


    

