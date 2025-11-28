import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime
from tkcalendar import *
import os
import sys
import ReportDoanhThuTheoNgay as r
from datetime import datetime
def connect_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\sqlexpress;'  
            'DATABASE=QLCHMBTND;'      
            'Trusted_Connection=yes;')
    return conn
class DoanhThuTheoNgay(tk.Frame):
    def __init__(self, parent, main_app): 
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.parent=parent
        tk.Label(self, text="DOANH THU THEO NGÀY", font=("Arial", 10, "bold")).pack(pady=10)
        frame_info=tk.Frame(self)
        frame_info.pack(pady=10)
        lbl_ds = tk.Label(frame_info, text="Bảng kê khai chi tiết", font=("Arial", 10, "bold"))
        lbl_ds.grid(row=0,column=0,padx=5,pady=5)
        label_ngaymua=tk.Label(frame_info,text="Chọn ngày").grid(row=0,column=1,padx=5,pady=5,sticky="w")
        self.dtp=DateEntry(frame_info,width=12,background='darkblue',foreground='white',borderwitdh=12,date=datetime.today())
        self.dtp.grid(row=0,column=2,padx=5,pady=5,sticky="w")
        btn=tk.Button(frame_info,text="Load",command=self.load_data).grid(row=0,column=3,padx=5,pady=5,sticky="w")
        btn1=tk.Button(frame_info,text="In báo cáo",command=self.In).grid(row=0,column=4,padx=5,pady=5,sticky="w")

        columns = ("Tên thuốc", "Số lượng","Giá bán","Giá nhập" ,"Giảm giá","Thành tiền", "COS")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Tên thuốc", width=30, anchor="center")
        tree.column("Số lượng", width=50, anchor="center")
        tree.column("Giá bán", width=50, anchor="center")
        tree.column("Giá nhập",width=50, anchor="center")
        tree.column("Giảm giá",width=50, anchor="center")
        tree.column("Thành tiền",width=20,anchor="center")
        tree.column("COS", width=100, anchor="center")
        tree.pack(padx=10, pady=5, fill="both")
        frame=tk.Frame(self)
        frame.pack(pady=10)
        tk.Label(frame,text="Doanh thu thực tế").grid(row=0,column=0,padx=10,pady=10,sticky="w")
        self.entry_doanhthu=tk.Entry(frame,width=10,bg="yellow")
        self.entry_doanhthu.grid(row=0,column=1,padx=10,pady=10,sticky="w")
        tk.Label(frame,text="Thuế").grid(row=0,column=2,padx=10,pady=10,sticky="w")
        self.entry_thue=tk.Entry(frame,width=10,bg="red")
        self.entry_thue.grid(row=0,column=3,padx=10,pady=10,sticky="w")
        tk.Label(frame,text="Lợi nhuận gộp").grid(row=0,column=4,padx=10,pady=10,sticky="w")
        self.entry_loinhuan=tk.Entry(frame,width=10,bg="green")
        self.entry_loinhuan.grid(row=0,column=5,padx=10,pady=10,sticky="w")
        self.load_data()
    def In(self):
        conn = connect_db()
        cur = conn.cursor()
        tree=self.tree
        items = []
        doanhthu=0
        tongcos=0
        for i in tree.get_children():
            tenthuoc=tree.item(i)["values"][0]
            soluong=tree.item(i)["values"][1]
            giaban=tree.item(i)["values"][2]
            gianhap=tree.item(i)["values"][3]
            thanhtien=tree.item(i)["values"][4]
            cos=tree.item(i)["values"][5]
            tongcos=tongcos+tree.item(i)["values"][5]
            doanhthu=doanhthu+tree.item(i)["values"][4]
            items.append((tenthuoc, soluong, f"{float(giaban):,.0f}",f"{float(gianhap):,.0f}",f"{float(thanhtien):,.0f}",f"{float(cos):,.0f}") )
        try:
            loinhuan=doanhthu-tongcos-(doanhthu*0.08)
            thue=doanhthu*0.08
            doanhthu=doanhthu*0.92
            ngay_full=self.dtp.get_date()
            ngay_date=str(ngay_full).split()[0]
            ngay=datetime.strptime(ngay_date,'%Y-%m-%d').date()
            pdf_path = r.export_to_pdf(ngay,doanhthu,thue,loinhuan, items)
            
            if pdf_path and os.path.exists(pdf_path):
                if sys.platform == "win32":
                    os.startfile(pdf_path, 'print') 
                else:
                    os.startfile(pdf_path) 
                
            else:
                messagebox.showwarning("Cảnh báo", "Không thể mở bản xem trước PDF.")
        except Exception as e:
            messagebox.showerror("Lỗi In/PDF", f"Lỗi khi mở bản xem trước: {e}")
    def load_data(self):
        conn = connect_db()
        cur = conn.cursor()
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        sql_query = ("""SELECT t.TenThuoc,SUM(c.SoLuong) AS TongSoLuong,giaban,gianhap,giamgia,SUM(c.ThanhTien) AS TongDoanhThu,
                     SUM(c.SoLuong * t.GiaNhap) AS TongCOS
                    FROM chitietphieumuahang c
                    JOIN
                    phieumuahang p ON c.SoPhieuMuaHang = p.SoPhieuMuaHang
                    JOIN
                    thuoc t ON c.MaThuoc = t.MaThuoc
                    where ngaymuahang=?
                    GROUP BY t.TenThuoc,t.GiaBan,t.GiaNhap,giamgia;""")
        dtp=self.dtp.get_date()
        cur.execute(sql_query,(dtp,))
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        doanhthu=0
        cos=0
        loinhuan=0
        for i in tree.get_children():
            doanhthu=doanhthu+float(tree.item(i)["values"][5])
            cos=cos+int(tree.item(i)["values"][6])
        loinhuan=doanhthu-cos-doanhthu*0.08
        thue=doanhthu*0.08
        doanhthu=doanhthu-thue
        self.entry_doanhthu.delete(0,tk.END)
        self.entry_doanhthu.insert(0,doanhthu)
        self.entry_thue.delete(0,tk.END)
        self.entry_thue.insert(0,thue)
        self.entry_loinhuan.delete(0,tk.END)
        self.entry_loinhuan.insert(0,loinhuan)
        conn.close()


        