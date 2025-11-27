import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime
from tkcalendar import *
import os
import sys
import pandas as pd
from tkinter import filedialog
import ReportDoanhThuTheoThang as r
from datetime import datetime
def connect_db():
    conn = pyodbc.connect( 'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\sqlexpress;'  
            'DATABASE=QLCHMBTND;'      
            'Trusted_Connection=yes;')
    return conn
class DoanhThuTheoThang(tk.Frame):
    def __init__(self, parent, main_app): 
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.parent=parent
        tk.Label(self, text="DOANH THU THEO THÁNG", font=("Arial", 10, "bold")).pack(pady=10)
        frame_info=tk.Frame(self)
        frame_info.pack(pady=10)
        lbl_ds = tk.Label(frame_info, text="Bảng kê khai chi tiết", font=("Arial", 10, "bold"))
        lbl_ds.grid(row=0,column=0,padx=5,pady=5)
        tk.Label(frame_info, text="Tháng:").grid(row=0,column=1,padx=5,pady=5)
        self.months = [f"{i:02d}" for i in range(1, 13)] 
        self.month_cb = ttk.Combobox(frame_info, values=self.months, width=5, state="readonly")
        self.month_cb.grid(row=0,column=2,padx=5,pady=5,sticky="w")
        current_month = datetime.now().strftime("%m")
        self.month_cb.set(current_month)
        tk.Label(frame_info, text="Năm:").grid(row=0,column=3,padx=5,pady=5)
        current_year = datetime.now().year
        self.years = [str(y) for y in range(current_year - 10, current_year + 5)]
        self.year_cb = ttk.Combobox(frame_info, values=self.years, width=8, state="readonly")
        self.year_cb.grid(row=0,column=4,padx=5,pady=5)
        
        self.year_cb.set(str(current_year))
        btn=tk.Button(frame_info,text="Load",command=self.load_data).grid(row=0,column=5,padx=5,pady=5,sticky="w")
        btn1=tk.Button(frame_info,text="In báo cáo",command=self.In).grid(row=0,column=6,padx=5,pady=5,sticky="w")
        columns = ("Ngày", "Doanh thu", "Tổng vốn(COS)","VAT" ,"Lợi nhuận gộp")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Ngày", width=30, anchor="center")
        tree.column("Doanh thu", width=50, anchor="center")
        tree.column("Tổng vốn(COS)",width=20,anchor="center")
        tree.column("VAT", width=50, anchor="center")
        tree.column("Lợi nhuận gộp", width=100, anchor="center")
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
        tongdoanhthu=0
        tongloinhuan=0
        thue=0
        for i in tree.get_children():
            ngay=tree.item(i)["values"][0]
            doanhthu=tree.item(i)["values"][1]
            cos=tree.item(i)["values"][2]
            vat=tree.item(i)["values"][3]
            loinhuan=tree.item(i)["values"][4]
            tongloinhuan=tongloinhuan+float(tree.item(i)["values"][4])
            tongdoanhthu=doanhthu+float(tree.item(i)["values"][2])
            thue=thue+float(tree.item(i)["values"][3])
            items.append((ngay, f"{float(doanhthu):,.0f}", f"{float(cos):,.0f}",f"{float(vat):,.0f}",f"{float(loinhuan):,.0f}") )
        try:
            pdf_path = r.export_to_pdf(self.month_cb.get(),self.year_cb.get(),tongdoanhthu,thue,tongloinhuan, items)
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
        month = self.month_cb.get()
        year = self.year_cb.get()
        if not month and not year:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cả Tháng và Năm.")
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        sql_query = ("""SELECT
    CONVERT(DATE, p.ngaymuahang) AS NgayMuaHang,
    SUM(c.ThanhTien) AS TongDoanhThu,
    SUM(c.SoLuong * t.GiaNhap) AS TongCOS,
    SUM(thanhtien*0.08) AS VAT,
    SUM(c.ThanhTien) - SUM(c.SoLuong * t.GiaNhap+thanhtien*0.08) AS LoiNhuanGop
FROM chitietphieumuahang c
JOIN
    phieumuahang p ON c.SoPhieuMuaHang = p.SoPhieuMuaHang
JOIN
    thuoc t ON c.MaThuoc = t.MaThuoc
where month(ngaymuahang)=? and year(ngaymuahang)=?
GROUP BY p.ngaymuahang
ORDER BY p.ngaymuahang ;""")
        cur.execute(sql_query,(month,year,))
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        doanhthu=0
        cos=0
        loinhuan=0
        for i in tree.get_children():
            doanhthu=doanhthu+float(tree.item(i)["values"][1])
            cos=cos+int(tree.item(i)["values"][2])

        loinhuan=doanhthu*0.92-cos
        thue=doanhthu*0.08
        doanhthu=doanhthu*0.92
        self.entry_doanhthu.delete(0,tk.END)
        self.entry_doanhthu.insert(0,doanhthu)
        self.entry_thue.delete(0,tk.END)
        self.entry_thue.insert(0,thue)
        self.entry_loinhuan.delete(0,tk.END)
        self.entry_loinhuan.insert(0,loinhuan)
        conn.close()
  