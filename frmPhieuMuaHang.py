import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime
from tkcalendar import *
import frmChiTietPhieuMuaHang as c
import os
import sys
import ReportPhieuMuaHang as r
import frmThuoc as t
import frmKhachHang as k
import frmNhanVien as n
import frmXacNhan as x
def connect_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\sqlexpress;' 
            'DATABASE=QLCHMBTND;'      
            'Trusted_Connection=yes;')
    return conn
def getdata_manhanvien():
    nhanvien=[]
    getnhanvien=connect_db()
    cursor=getnhanvien.cursor()
    sql_query = "SELECT manv FROM nhanvien where tinhtrang=1"
    cursor.execute(sql_query)
    for row in cursor.fetchall():
        nhanvien.append(row[0])
    cursor.close()
    getnhanvien.close()
    return nhanvien
def getdata_makhachhang():
    khachhang=[]
    getkhachhang=connect_db()
    cursor=getkhachhang.cursor()
    sql_query = "SELECT makh FROM khachhang where tinhtrang=1"
    cursor.execute(sql_query)
    for row in cursor.fetchall():
        khachhang.append(row[0])
    cursor.close()
    getkhachhang.close()
    return khachhang
class PhieuMuaHang(tk.Frame):
    def __init__(self, parent, main_app,username): 
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.parent=parent
        self.username=username
        self.selected_manv = tk.StringVar() 
        self.selected_makh= tk.StringVar()
        lbl_title = tk.Label(self, text="PHIẾU MUA HÀNG", font=("Arial", 18, "bold"))
        lbl_title.pack(pady=10)
        frame_phieu=tk.Frame(self)
        frame_phieu.pack(pady=10)
      
        label_maphieu=tk.Label(frame_phieu,text="Mã phiếu mua hàng").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_maphieu=tk.Entry(frame_phieu,width=20)
        self.entry_maphieu.grid(row=0,column=1,padx=5,pady=5,sticky="w")

        label_ngaymua=tk.Label(frame_phieu,text="Ngày mua hàng").grid(row=0,column=2,padx=5,pady=5,sticky="w")
        self.dtp=DateEntry(frame_phieu,width=12,background='darkblue',foreground='white',borderwitdh=12)
        self.dtp.grid(row=0,column=3,padx=5,pady=5,sticky="w")

        label_nhanvien=tk.Label(frame_phieu,text="Mã nhân viên").grid(row=1,column=0,padx=5,pady=5,sticky="w")
        self.cbb_manhanvien=ttk.Combobox(frame_phieu,textvariable=self.selected_manv,value=getdata_manhanvien(),width=20)
        self.cbb_manhanvien.grid(row=1,column=1,padx=5,pady=5,sticky="w")

        label_nhanvien=tk.Label(frame_phieu,text="Nhân viên").grid(row=1,column=2,padx=5,pady=5,sticky="w")
        self.entry_nhanvien=tk.Entry(frame_phieu,width=30)
        self.entry_nhanvien.grid(row=1,column=3,padx=5,pady=5,sticky="w")
        self.btnAlterNV=tk.Button(frame_phieu,text="...",width=5,command=self.AlterNV)
        self.btnAlterNV.grid(row=1,column=4,padx=5,pady=5)
        if self.username!="admin123":
            conn = connect_db()
            cur = conn.cursor()
            self.selected_manv.set(self.username)
            sql_tennv = "SELECT tenNV FROM nhanvien WHERE maNV = ?"
            cur.execute(sql_tennv, (self.selected_manv.get(),))
            tennhanvien_result = cur.fetchone() 
            if tennhanvien_result:
                ten_nv = tennhanvien_result[0]
            self.entry_nhanvien.delete(0,tk.END)
            self.entry_nhanvien.insert(0,ten_nv)
            self.cbb_manhanvien.config(state="disabled")
            self.entry_nhanvien.config(state="readonly")
            self.btnAlterNV.config(state="disabled")
        label_khachhang=tk.Label(frame_phieu,text="Mã khách hàng").grid(row=2,column=0,padx=5,pady=5,sticky="w")
        self.cbb_makhachhang=ttk.Combobox(frame_phieu,textvariable=self.selected_makh, value=getdata_makhachhang(),width=20)
        self.cbb_makhachhang.grid(row=2,column=1,padx=5,pady=5,sticky="w")

        label_nhanvien=tk.Label(frame_phieu,text="Khách hàng").grid(row=2,column=2,padx=5,pady=5,sticky="w")
        self.entry_khachhang=tk.Entry(frame_phieu,width=30)
        self.entry_khachhang.grid(row=2,column=3,padx=5,pady=5,sticky="w")
        btnAlterKH=tk.Button(frame_phieu,text="...",width=5,command=self.AlterKH).grid(row=2,column=4,padx=5,pady=5)

        label_sodienthoaikh=tk.Label(frame_phieu,text="Số điện thoại").grid(row=3,column=0,padx=5,pady=5,sticky="w")
        self.entry_sodienthoaikh=tk.Entry(frame_phieu,width=20)
        self.entry_sodienthoaikh.grid(row=3,column=1,padx=5,pady=5,sticky="w")

        label_diachikh=tk.Label(frame_phieu,text="Địa chỉ").grid(row=3,column=2,padx=5,pady=5,sticky="w")
        self.entry_diachikh=tk.Entry(frame_phieu,width=30)
        self.entry_diachikh.grid(row=3,column=3,padx=5,pady=5,sticky="w")

        self.cbb_manhanvien.bind("<<ComboboxSelected>>", self.update_manhanvien)
        self.cbb_makhachhang.bind("<<ComboboxSelected>>",self.update_khachhang)
        
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Thêm", width=8,command=self.Them).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Xóa", width=8,command=self.Xoa).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Sửa", width=8,command=self.Sua).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Hủy", width=8,command=self.Huy).grid(row=0, column=3, padx=5)
        tk.Button(frame_btn, text="In phiếu",width=10,command=self.In).grid(row=0,column=4,padx=5)
        frame_timkiem=tk.Frame(self)
        frame_timkiem.pack(pady=5)
        tk.Label(frame_timkiem,text="Nhập mã phiếu mua hàng cần tìm: ").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_matimkiem=tk.Entry(frame_timkiem,width=15)
        self.entry_matimkiem.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        btnTimKiem=tk.Button(frame_timkiem,text="Tìm phiếu",width=10,command=self.Tim).grid(row=0,column=2,padx=5,pady=5)
  
        lbl_ds = tk.Label(self, text="Danh sách phiếu mua hàng", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w", padx=10)
        columns = ("Mã phiếu mua hàng", "Mã nhân viên", "Nhân viên", "Mã khách hàng", "Khách hàng","Số điện thoại", "Địa chỉ","Ngày mua","Tổng tiền")
        self.tree = ttk.Treeview(self    , columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Mã phiếu mua hàng", width=40, anchor="center")
        tree.column("Mã nhân viên", width=50)
        tree.column("Nhân viên", width=100)
        tree.column("Mã khách hàng", width=50, anchor="center")
        tree.column("Khách hàng", width=100, anchor="center")
        tree.column("Số điện thoại", width=50)
        tree.column("Địa chỉ", width=80)
        tree.column("Ngày mua",width=60)
        tree.column("Tổng tiền", width=60)
        tree.bind("<<TreeviewSelect>>", self.select_record)
        tree.pack(padx=10, pady=5, fill="both")
        self.load_data()
    def Tim(self):
        matim=self.entry_matimkiem.get()
        if matim=="":
            messagebox.showinfo("Thông báo","Vui lòng nhập mã phiếu mua hàng cần tìm")
            self.entry_matimkiem.focus()
            return
        tree=self.tree
        check=0
        for i in tree.get_children():
            if int(matim)==tree.item(i)["values"][0]:
                check=1
                id=i
                value=tree.item(i)["values"]
        if check==0:
            messagebox.showinfo("Thông báo","Không tìm thấy mã phiếu mua hàng trên")
            return
        tree.delete(id)
        new_id = tree.insert("", 0, values=value)
            
        tree.selection_remove(tree.selection()) 
        tree.selection_add(new_id)             
        tree.see(new_id)                                
        self.select_record(None)
    def AlterNV(self):
        chi_tiet_window = n.NhanVien(self.parent)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        self.cbb_manhanvien.config(values=None)
        self.cbb_manhanvien.config(values=getdata_manhanvien())
        self.load_data
    def AlterKH(self):
        chi_tiet_window = k.KhachHang(self.parent)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        self.cbb_makhachhang.config(values=None)
        self.cbb_makhachhang.config(values=getdata_makhachhang())
        self.load_data()
    def select_record(self,event):
      self.entry_maphieu.config(state="normal")
      selected = self.tree.selection()
      if not selected:
         return
      values = self.tree.item(selected)["values"]
      self.entry_maphieu.delete(0, tk.END)
      self.entry_maphieu.insert(0, values[0])
      self.entry_nhanvien.delete(0,tk.END)
      self.entry_nhanvien.insert(0,values[2])
      self.cbb_manhanvien.set(values[1])
      self.entry_khachhang.delete(0,tk.END)
      self.entry_khachhang.insert(0,values[4])
      self.cbb_makhachhang.set(values[3])
      self.entry_sodienthoaikh.delete(0,tk.END)
      self.entry_sodienthoaikh.insert(0,"0"+str(values[5]))
      self.entry_diachikh.delete(0,tk.END)
      self.entry_diachikh.insert(0,values[6])
      date_only_string = values[7].split()[0]
      date_object = datetime.strptime(date_only_string, '%Y-%m-%d').date()
      self.dtp.set_date(date_object)
      self.entry_maphieu.config(state="readonly")
    def Huy(self):
      self.entry_maphieu.config(state="normal")
      self.entry_maphieu.delete(0, tk.END)
      self.entry_maphieu.delete(0, tk.END)
      self.entry_khachhang.delete(0,tk.END)
      self.entry_sodienthoaikh.delete(0,tk.END)
      self.entry_diachikh.delete(0,tk.END)
      if self.username=="admin123":
        self.cbb_manhanvien.set("")
        self.entry_nhanvien.delete(0,tk.END)
      self.cbb_makhachhang.set("")
      self.entry_matimkiem.delete(0,tk.END)
      self.load_data()
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = (
        "select distinct p.SoPhieuMuaHang,  p.MaNV, n.TenNV,p.MaKH,k.TenKH,k.SoDienThoaiKH,k.DiaChiKH, p.NgayMuaHang, p.TongTien "
        +" from Khachhang k,phieumuahang p,nhanvien n "
        +" where k.MaKH=p.MaKH and p.MaNV=n.MaNV")
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def Them(self):
        maphieu = self.entry_maphieu.get()
        nhanvien = self.entry_nhanvien.get()
        khachhang = self.entry_khachhang.get()
        sdtkh = self.entry_sodienthoaikh.get()
        diachikh = self.entry_diachikh.get()
        manhanvien = self.cbb_manhanvien.get()
        makhachhang = self.cbb_makhachhang.get()
        ngaymua_full=self.dtp.get_date()
        ngaymua_date=str(ngaymua_full).split()[0]
        ngaymua=datetime.strptime(ngaymua_date,'%Y-%m-%d').date()
        today=datetime.now().date()
        if today != ngaymua:
            messagebox.showinfo("Thông báo","Chỉ có thể thêm phiếu mua hàng trong ngày!")
            return
        if maphieu == "" or manhanvien == "" or makhachhang== "" or sdtkh=="" or diachikh=="" or nhanvien=="" or khachhang=="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if not maphieu.isdigit(): 
                messagebox.showinfo("Thông báo","Mã phiếu mua hàng phải là 1 chuỗi 8 số bắt đầu là 1(10000000)")
                return
        elif int(maphieu[0])!=1 or len(maphieu)!=8:
                messagebox.showinfo("Thông báo","Mã phiếu mua hàng phải là 1 chuỗi 8 số bắt đầu là 1(1000000)")
                return
        tree=self.tree  
        for i in tree.get_children():
            ma_tren_tree = str(tree.item(i)["values"][0])
            if maphieu == ma_tren_tree:
                messagebox.showwarning("Trùng mã", "Phiếu mua hàng đã tồn tại")
                return
        
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO phieumuahang VALUES (?,?,?,?,?)",
            (maphieu, manhanvien, makhachhang,ngaymua,0))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        self.Luu()
        maphieu_moi = self.entry_maphieu.get()
        thuoc=self.main_app.frames.get(t.Thuoc)
        chi_tiet_window = c.CTPMH(self.parent, maphieu_moi,thuoc)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        sql_check="delete from phieumuahang where tongtien=0"
        cur.execute(sql_check)
        conn.commit()      
        conn.close()   
        self.load_data()
        self.Huy()
    def Xoa(self):
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn thuốc để xóa")
            return
        today=datetime.now().date()
        ngaymua_full=tree.item(selected)["values"][7]
        ngaymua_date=ngaymua_full.split()[0]
        ngaymua=datetime.strptime(ngaymua_date,'%Y-%m-%d').date()
        if today != ngaymua:
            messagebox.showinfo("Thông báo","Chỉ có thể xóa phiếu mua hàng trong ngày!")
            return
        r=messagebox.askyesno("Thông báo","Thao tác xóa đồng nghĩa với việc giao dịch này sẽ bị hủy. Bạn có thật sự muốn xóa?")
        if r==False:
            return
        xacnhan=x.XacNhan(self.parent)
        result=xacnhan.show()
        if not xacnhan:
            return
        maphieu= tree.item(selected)["values"][0]
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("UPDATE thuoc"
                    +" SET SoLuongTon = SoLuongTon + ("
                    +" SELECT ct.SoLuong"
                    +" FROM chitietphieumuahang ct"
                    +" WHERE ct.MaThuoc = thuoc.MaThuoc"
                    +" AND ct.SoPhieuMuaHang = ?)"
                    +" WHERE MaThuoc IN ("
                    +" SELECT DISTINCT MaThuoc"
                    +" FROM chitietphieumuahang"
                    +" WHERE SoPhieuMuaHang = ?);",(maphieu,maphieu,))
        cur.execute("DELETE FROM chitietphieumuahang WHERE SoPhieuMuahang=?", (maphieu,))
        cur.execute("DELETE FROM phieumuahang WHERE SoPhieuMuahang=?", (maphieu,))
        conn.commit() 
        messagebox.showinfo("Thông báo", "Xóa thành công!")
        conn.close()
        self.load_data()
        self.Luu()
        thuoc_instance = self.main_app.frames.get(t.Thuoc)
        thuoc_instance.load_data()
    def Sua(self):
        conn = connect_db()
        cur = conn.cursor()
        tree=self.tree
        selected = tree.focus()
        maphieu = self.entry_maphieu.get()
        nhanvien = self.entry_nhanvien.get()
        manhanvien = self.cbb_manhanvien.get()
        makhachhang = self.cbb_makhachhang.get()
        khachhang = self.entry_khachhang.get()
        sdtkh = self.entry_sodienthoaikh.get()
        diachi = self.entry_diachikh.get()
        today=datetime.now().date()
        ngaymua_full=tree.item(selected)["values"][7]
        ngaymua_date=ngaymua_full.split()[0]
        ngaymua=datetime.strptime(ngaymua_date,'%Y-%m-%d').date()
        if today != ngaymua:
            messagebox.showinfo("Thông báo","Chỉ có thể sửa phiếu mua hàng trong ngày!")
            return        
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn thuoc để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        if maphieu == "" or manhanvien == "" or makhachhang== "" or sdtkh=="" or diachi=="" or nhanvien=="" or khachhang=="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        sql_tongtien="select tongtien from phieumuahang where sophieumuahang=?"
        cur.execute(sql_tongtien,(maphieu,))
        tongtien_result=cur.fetchone()
        tongtien=tongtien_result[0] if tongtien_result else None
        tree.item(selected, values=(maphieu, manhanvien, nhanvien, makhachhang, khachhang, sdtkh, diachi, ngaymua,tongtien))
        self.Luu()
    def Luu(self):
        tree=self.tree
        maphieu = self.entry_maphieu.get()
        nhanvien = self.entry_nhanvien.get()
        manhanvien = self.cbb_manhanvien.get()
        makhachhang = self.cbb_makhachhang.get()
        khachhang = self.entry_khachhang.get()
        sdtkh = self.entry_sodienthoaikh.get()
        diachi = self.entry_diachikh.get()
        ngaymua=self.dtp.get_date()
        if maphieu == "" or manhanvien == "" or makhachhang== "" or sdtkh=="" or diachi=="" or nhanvien=="" or khachhang=="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        
        conn = connect_db()
        cur = conn.cursor()
        sql_tt = "SELECT tongtien FROM phieumuahang WHERE sophieumuahang = ?"
        cur.execute(sql_tt, (maphieu))
        tongtien_result = cur.fetchone()
        tongtien = tongtien_result[0] if tongtien_result else None
        cur.execute("UPDATE phieumuahang SET manv=?, makh=?, ngaymuahang=?,tongtien=?  WHERE sophieumuahang=?",
        (manhanvien,makhachhang,ngaymua,tongtien,maphieu))
        conn.commit()
        conn.close()  
    def update_manhanvien(self, event):
        ma_nv_chon = self.selected_manv.get() 
        ten_nv = None
        if ma_nv_chon:
            conn = connect_db()
            cur = conn.cursor()
            try:
                sql_tennv = "SELECT tenNV FROM nhanvien WHERE maNV = ?"
                cur.execute(sql_tennv, (ma_nv_chon,))
                tennhanvien_result = cur.fetchone() 
                if tennhanvien_result:
                    ten_nv = tennhanvien_result[0]  
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi khi truy vấn Mã NV: {sqlstate}")
            finally:
                cur.close()
                conn.close()   
        self.entry_nhanvien.delete(0, tk.END)
        if ten_nv:
            self.entry_nhanvien.insert(0, ten_nv)
        else:
            pass 
    def update_khachhang(self,event):
        ma_kh_chon = self.selected_makh.get() 
        ten_kh = None
        sdt_kh= None
        diachi_kh=None
        if ma_kh_chon:
            conn = connect_db()
            cur = conn.cursor()
            try:
                sql_tenkh = "SELECT tenkh FROM khachhang WHERE makh = ?"
                cur.execute(sql_tenkh, (ma_kh_chon,))
                tenkhachhang_result = cur.fetchone()
                if tenkhachhang_result:
                    ten_kh = tenkhachhang_result[0]
                sql_sodienthoaikh = "SELECT sodienthoaikh FROM khachhang WHERE makh = ?"
                cur.execute(sql_sodienthoaikh, (ma_kh_chon,))
                sodienthoaikh_result = cur.fetchone()
                if sodienthoaikh_result:
                    sdt_kh = sodienthoaikh_result[0]
                sql_diachikh = "SELECT diachikh FROM khachhang WHERE makh = ?"
                cur.execute(sql_diachikh, (ma_kh_chon,))
                diachikh_result = cur.fetchone()
                if diachikh_result:
                    diachi_kh = diachikh_result[0]
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi khi truy vấn Mã NV: {sqlstate}")
            finally:
                cur.close()
                conn.close()
        self.entry_khachhang.delete(0, tk.END)
        self.entry_sodienthoaikh.delete(0,tk.END)
        self.entry_diachikh.delete(0,tk.END)
        if ten_kh: self.entry_khachhang.insert(0, ten_kh)
        else: pass 
        if sdt_kh: self.entry_sodienthoaikh.insert(0,sdt_kh)
        else: pass
        if diachi_kh: self.entry_diachikh.insert(0,diachi_kh)
        else: pass
    def In(self):
        conn = connect_db()
        cur = conn.cursor()
        tree=self.tree
        selected=tree.focus()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn phiếu để in")
            return
        sophieu = self.entry_maphieu.get()
        date_only_string = self.dtp.get().split()[0]
        ngaymua = datetime.strptime(date_only_string, '%m/%d/%y').date()
        tennv=self.entry_nhanvien.get()
        tenkh=self.entry_khachhang.get()
        sdt=self.entry_sodienthoaikh.get()
        diachi=self.entry_diachikh.get()
        cur.execute("select count(*) from chitietphieumuahang where sophieumuahang=?",(sophieu,))
        result=cur.fetchone()
        n=result[0]
        items = []
        sql_detail = """SELECT t.TenThuoc, c.SoLuong, t.GiaBan, c.GiamGia, c.ThanhTien ,tendonvi
            FROM Thuoc t, DonViTinh d, ChiTietPhieuMuaHang c
            WHERE t.MaThuoc = c.MaThuoc AND d.MaDVT = t.MaDVT AND c.SoPhieuMuaHang = ?"""
        cur.execute(sql_detail, (sophieu,))
        items = []
        for result in cur.fetchall():
            ten_thuoc = result[0]
            sl = result[1]
            gia = result[2]
            giamgia = result[3] 
            thanhtien = result[4]
            dvt=result[5]
            items.append((ten_thuoc, sl, f"{float(gia):,.0f}",dvt,giamgia, f"{float(thanhtien):,.0f}")) 
        tongtien=tree.item(selected)["values"][8]
        try:
            pdf_path = r.export_to_pdf(sophieu, ngaymua, tennv,tenkh, diachi, sdt, tongtien, items)
            if pdf_path and os.path.exists(pdf_path):
                if sys.platform == "win32":
                    os.startfile(pdf_path, 'print') 
                else:
                    os.startfile(pdf_path) 
            else:
                messagebox.showwarning("Cảnh báo", "Không thể mở bản xem trước PDF.")
        except Exception as e:
            messagebox.showerror("Lỗi In/PDF", f"Lỗi khi mở bản xem trước: {e}")

       
