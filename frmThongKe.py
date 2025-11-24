import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import math
from datetime import datetime
from tkcalendar import *
import os
import sys
from datetime import datetime
def connect_db():
    conn = pyodbc.connect( 'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\sqlexpress;'  
            'DATABASE=QLCHMBTND;'      
            'Trusted_Connection=yes;')
    return conn
class ThongKe(tk.Frame):
    def __init__(self, parent, main_app): 
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.parent=parent
        tk.Label(self, text="THỐNG KÊ THUỐC NÔNG DƯỢC", font=("Arial", 10, "bold")).pack(pady=10)
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
        columns = ("Tên thuốc", "% Doanh thu", "Số lượng bán","Số lượng tồn")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Tên thuốc", width=150, anchor="center")
        tree.column("% Doanh thu", width=50, anchor="center")
        tree.column("Số lượng bán",width=50,anchor="center")
        tree.column("Số lượng tồn", width=50, anchor="center")
        tree.pack(padx=10, pady=5, fill="both")
        frame=tk.Frame(self)
        frame.pack(pady=10)
        tk.Label(frame,text="Doanh thu cao nhất").grid(row=0,column=0,padx=10,pady=10,sticky="w")
        self.entry_max=tk.Entry(frame,width=30)
        self.entry_max.grid(row=0,column=1,padx=10,pady=10,sticky="w")
        tk.Label(frame,text="Doanh thu thấp nhất").grid(row=0,column=2,padx=10,pady=10,sticky="w")
        self.entry_min=tk.Entry(frame,width=30)
        self.entry_min.grid(row=0,column=3,padx=10,pady=10,sticky="w")
        
        self.load_data()
        
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
        sql_query = ("""WITH TongDoanhThu AS (
    SELECT SUM(c.ThanhTien) AS TongThanhTien
    FROM chitietphieumuahang c)
    SELECT t.TenThuoc,
    (SUM(c.ThanhTien) * 100.0 / (SELECT TongThanhTien FROM TongDoanhThu)) AS PhanTramDoanhThu,
    SUM(c.SoLuong) AS SoLuongBan,t.SoLuongTon
    FROM chitietphieumuahang c
    JOIN
    thuoc t ON c.MaThuoc = t.MaThuoc, phieumuahang p
    where p.SoPhieuMuaHang=c.SoPhieuMuaHang and month(ngaymuahang)=? and year(ngaymuahang)=?
    GROUP BY t.TenThuoc, t.SoLuongTon
    ORDER BY PhanTramDoanhThu DESC;""")
        cur.execute(sql_query,(month,year,))
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        max=0
        min=100
        for i in tree.get_children():
            if max<float(tree.item(i)["values"][1]):
                max=float(tree.item(i)["values"][1])
                max_ten=tree.item(i)["values"][0]
            if min>=float(tree.item(i)["values"][1]):
                min=float(tree.item(i)["values"][1])
                min_ten=tree.item(i)["values"][0]
        if max==0 or min==100:
            return
        self.entry_max.delete(0,tk.END)
        self.entry_min.delete(0,tk.END)
        self.entry_max.insert(0,max_ten)
        self.entry_min.insert(0,min_ten)
        conn.close()