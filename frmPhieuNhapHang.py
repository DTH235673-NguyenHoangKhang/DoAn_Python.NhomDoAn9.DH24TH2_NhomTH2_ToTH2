import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import os
import sys
from datetime import datetime,timedelta
from tkcalendar import *
import frmChiTietPhieuNhapHang as c
import ReportPhieuNhapHang as r
import frmThuoc as t
import frmNhaCungCap as ncc
import frmNhanVien as n
import frmXacNhan as x
def connect_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\sqlexpress;'  
            'DATABASE=QLCHMBTND;'      
            'Trusted_Connection=yes;'
            'CHARSET=UTF8')
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
def getdata_manhacungcap():
    nhacungcap=[]
    getnhacungcap=connect_db()
    cursor=getnhacungcap.cursor()
    sql_query = "SELECT manhacungcap FROM nhacungcap where tinhtrang=1"
    cursor.execute(sql_query)
    for row in cursor.fetchall():
        nhacungcap.append(row[0])
    cursor.close()
    getnhacungcap.close()
    return nhacungcap
class PhieuNhapHang(tk.Frame):
    def __init__(self, parent, main_app): 
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.parent=parent
        self.selected_manv = tk.StringVar() 
        self.selected_mancc= tk.StringVar()
        lbl_title = tk.Label(self, text="PHIẾU NHẬP HÀNG", font=("Arial", 18, "bold"))
        lbl_title.pack(pady=10)

        frame_phieu=tk.Frame(self)
        frame_phieu.pack(pady=10)
        # Hàng 0
        label_maphieu=tk.Label(frame_phieu,text="Mã phiếu nhập hàng").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_maphieu=tk.Entry(frame_phieu,width=20)
        self.entry_maphieu.grid(row=0,column=1,padx=5,pady=5,sticky="w")

        label_ngaynhap=tk.Label(frame_phieu,text="Ngày nhập hàng").grid(row=0,column=2,padx=5,pady=5,sticky="w")
        self.dtp=DateEntry(frame_phieu,width=12,background='darkblue',foreground='white',borderwitdh=12)
        self.dtp.grid(row=0,column=3,padx=5,pady=5,sticky="w")

        # Hàng 1
        label_nhanvien=tk.Label(frame_phieu,text="Nhân viên").grid(row=1,column=0,padx=5,pady=5,sticky="w")
        
        self.cbb_manhanvien=ttk.Combobox(frame_phieu,textvariable=self.selected_manv, value=getdata_manhanvien(), width=20)
        self.cbb_manhanvien.grid(row=1,column=1,padx=5,pady=5,sticky="w")

        label_nhanvien=tk.Label(frame_phieu,text="Nhân viên").grid(row=1,column=2,padx=5,pady=5,sticky="w")
        self.entry_nhanvien=tk.Entry(frame_phieu,width=30)
        self.entry_nhanvien.grid(row=1,column=3,padx=5,pady=5,sticky="w")
        btnAlterNV=tk.Button(frame_phieu,text="...",width=5,command=self.AlterNV).grid(row=1,column=4,pady=5)

        #hang2
        label_nhacungcap=tk.Label(frame_phieu,text="Mã nhà cung cấp").grid(row=2,column=0,padx=5,pady=5,sticky="w")
        self.cbb_manhacungcap=ttk.Combobox(frame_phieu,textvariable=self.selected_mancc, value=getdata_manhacungcap(),width=20)
        self.cbb_manhacungcap.grid(row=2,column=1,padx=5,pady=5,sticky="w")

        label_nhacungcap=tk.Label(frame_phieu,text="Nhà cung cấp").grid(row=2,column=2,padx=5,pady=5,sticky="w")
        self.entry_nhacungcap=tk.Entry(frame_phieu,width=30)
        self.entry_nhacungcap.grid(row=2,column=3,padx=5,pady=5,sticky="w")
        btnAlterNCC=tk.Button(frame_phieu,text="...",width=5,command=self.AlterNCC).grid(row=2,column=4,pady=5)

        label_sodienthoaincc=tk.Label(frame_phieu,text="Số điện thoại").grid(row=3,column=0,padx=5,pady=5,sticky="w")
        self.entry_sodienthoaincc=tk.Entry(frame_phieu,width=20)
        self.entry_sodienthoaincc.grid(row=3,column=1,padx=5,pady=5,sticky="w")

        label_diachincc=tk.Label(frame_phieu,text="Địa chỉ").grid(row=3,column=2,padx=5,pady=5,sticky="w")
        self.entry_diachincc=tk.Entry(frame_phieu,width=30)
        self.entry_diachincc.grid(row=3,column=3,padx=5,pady=5,sticky="w")

        self.cbb_manhanvien.bind("<<ComboboxSelected>>", self.update_manhanvien)
        self.cbb_manhacungcap.bind("<<ComboboxSelected>>",self.update_manhacungcap)
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Thêm", width=8,command=self.Them).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Xóa", width=8,command=self.Xoa).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Sửa", width=8,command=self.Sua).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Hủy", width=8,command=self.Huy).grid(row=0, column=3, padx=5)
        tk.Button(frame_btn,text="Duyệt phiếu",width=11,command=self.DuyetPhieu).grid(row=0,column=4,padx=5)
        tk.Button(frame_btn,text="In phiếu",width=11,command=self.In).grid(row=0,column=5,padx=5)
        frame_timkiem=tk.Frame(self)
        frame_timkiem.pack(pady=5)
        tk.Label(frame_timkiem,text="Nhập mã phiếu nhập cần tìm: ").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_matimkiem=tk.Entry(frame_timkiem,width=15)
        self.entry_matimkiem.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        btnTimKiem=tk.Button(frame_timkiem,text="Tìm phiếu",width=10,command=self.Tim).grid(row=0,column=2,padx=5,pady=5)
  
        lbl_ds = tk.Label(self, text="Danh sách phiếu nhập hàng", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w", padx=10)
        columns = ("Trạng thái","Mã phiếu bán hàng", "Mã nhân viên", "Nhân viên", "Mã nhà cung cấp", "Nhà cung cấp","Số điện thoại", "Địa chỉ","Ngày nhập","Tổng tiền")
        self.tree = ttk.Treeview(self    , columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Trạng thái",width=50,anchor="center")
        tree.column("Mã phiếu bán hàng", width=40, anchor="center")
        tree.column("Mã nhân viên", width=50,anchor="center")
        tree.column("Nhân viên", width=100,anchor="center")
        tree.column("Mã nhà cung cấp", width=50, anchor="center")
        tree.column("Nhà cung cấp", width=100, anchor="center")
        tree.column("Số điện thoại", width=50,anchor="center")
        tree.column("Địa chỉ", width=80,anchor="center")
        tree.column("Ngày nhập",width=60,anchor="center")
        tree.column("Tổng tiền", width=60,anchor="center")
        tree.bind("<<TreeviewSelect>>", self.select_record)
        tree.pack(padx=10, pady=5, fill="both")
        self.load_data()
    def Tim(self):
        matim=self.entry_matimkiem.get()
        if matim=="":
            messagebox.showinfo("Thông báo","Vui lòng nhập mã phiếu nhập hàng cần tìm")
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
            messagebox.showinfo("Thông báo","Không tìm thấy mã phiếu nhập hàng trên")
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
        self.load_data()
    def AlterNCC(self):
        chi_tiet_window = ncc.NhaCungCap(self.parent)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        self.cbb_manhacungcap.config(values=None)
        self.cbb_manhacungcap.config(values=getdata_manhacungcap())
        thuoc=self.main_app.frames.get(t.Thuoc)
        thuoc.reload_manhacungcap()
        self.load_data()
    def select_record(self,event):
      self.entry_maphieu.config(state="normal")
      selected = self.tree.selection()
      if not selected:
         return
      values = self.tree.item(selected)["values"]
      self.entry_maphieu.delete(0, tk.END)
      self.entry_maphieu.insert(0, values[1])
      self.entry_nhanvien.delete(0,tk.END)
      self.entry_nhanvien.insert(0,values[3])
      self.cbb_manhanvien.set(values[2])
      self.entry_nhacungcap.delete(0,tk.END)
      self.entry_nhacungcap.insert(0,values[5])
      self.cbb_manhacungcap.set(values[4])
      self.entry_sodienthoaincc.delete(0,tk.END)
      self.entry_sodienthoaincc.insert(0,"0"+str(values[6]))
      self.entry_diachincc.delete(0,tk.END)
      self.entry_diachincc.insert(0,values[7])
      date_only_string = values[8].split()[0]
      date_object = datetime.strptime(date_only_string, '%Y-%m-%d').date()
      self.dtp.set_date(date_object)
      self.entry_maphieu.config(state="readonly")
    def reload_manhacungcap(self):
        self.cbb_manhacungcap.config(values=None)
        self.cbb_manhacungcap.config(values=getdata_manhacungcap())
    def Huy(self):
      self.entry_maphieu.config(state="normal")
      self.entry_maphieu.delete(0, tk.END)
      self.entry_maphieu.delete(0, tk.END)
      self.entry_nhanvien.delete(0,tk.END)
      self.entry_nhacungcap.delete(0,tk.END)
      self.entry_sodienthoaincc.delete(0,tk.END)
      self.entry_diachincc.delete(0,tk.END)
      self.cbb_manhanvien.set("")
      self.cbb_manhacungcap.set("")
      self.entry_matimkiem.delete(0,tk.END)
      self.load_data()
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = (
        "select distinct p.TrangThai,p.SoPhieuNhapHang,  p.MaNV, n.TenNV,p.MaNhacungCap,ncc.TenNCC,ncc.SoDienThoaiNCC,ncc.DiaChincc, p.NgaylapphieuNhap, p.TongTien "
        +" from nhacungcap ncc,phieunhaphang p,nhanvien n "
        +" where ncc.manhacungcap=p.manhacungcap and p.MaNV=n.MaNV")
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def Them(self):
        tree=self.tree
        maphieu = self.entry_maphieu.get()
        nhanvien = self.entry_nhanvien.get()
        nhacungcap = self.entry_nhacungcap.get()
        sdtncc = self.entry_sodienthoaincc.get()
        diachincc = self.entry_diachincc.get()
        manhanvien = self.cbb_manhanvien.get()
        manhacungcap = self.cbb_manhacungcap.get()
        if maphieu == "" or manhanvien == "" or manhacungcap== "" or sdtncc=="" or diachincc=="" or nhanvien=="" or nhacungcap=="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if not maphieu.isdigit(): 
                messagebox.showinfo("Thông báo","Mã phiếu nhập hàng phải là 1 chuỗi 8 số bắt đầu là 2(20000000)")
                return
        elif int(maphieu[0])!=2 or len(maphieu)!=8:
                messagebox.showinfo("Thông báo","Mã phiếu nhập hàng phải là 1 chuỗi 8 số bắt đầu là 2(20000000)")
                return
        for i in tree.get_children():
            ma_tren_tree = str(tree.item(i)["values"][1])
            if maphieu == ma_tren_tree:
                messagebox.showwarning("Trùng mã", "Phiếu nhập hàng đã tồn tại")
                return
        today=datetime.now().date()
        ngaynhap_full=self.dtp.get_date()
        ngaynhap_date=str(ngaynhap_full).split()[0]
        ngaynhap=datetime.strptime(ngaynhap_date,'%Y-%m-%d').date()
        if today != ngaynhap:
            messagebox.showinfo("Thông báo","Phiếu nhập hàng chỉ có thể tạo trong ngày!")
            return  
        if maphieu == "" or manhanvien == "" or manhacungcap== "" or sdtncc=="" or diachincc=="" or nhanvien=="" or nhacungcap=="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO phieunhaphang VALUES (?,?,?,?,?,?)",
            (maphieu, manhanvien, manhacungcap,ngaynhap,0,"Chưa duyệt"))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        self.Luu()
        maphieu_moi = self.entry_maphieu.get()
        chi_tiet_window = c.CTPNH(self.parent, maphieu_moi)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        sql_check="delete from phieunhaphang where tongtien=0"
        cur.execute(sql_check)
        conn.commit()      
        conn.close()   
        self.load_data()
        self.Huy()
    def Xoa(self):
        conn = connect_db()
        cur = conn.cursor()
        tree=self.tree
        selected=tree.focus()
        sql_trangthai="select trangthai from phieunhaphang where sophieunhaphang=?"
        maphieu=self.entry_maphieu.get()
        cur.execute(sql_trangthai,(maphieu,))
        trangthai_result=cur.fetchone()
        trangthai=trangthai_result[0] if trangthai_result else None
        if trangthai=="Đã duyệt":
            today=datetime.now().date()
            ngaynhap_full=tree.item(selected)["values"][8]
            ngaynhap_date=ngaynhap_full.split()[0]
            ngaynhap=datetime.strptime(ngaynhap_date,'%Y-%m-%d').date()
            if today != ngaynhap:
                messagebox.showinfo("Thông báo","Chỉ có thể xóa phiếu nhập đã duyệt trong ngày!")
                return
            r=messagebox.askyesno("Thông báo","Thao tác xóa đồng nghĩa với việc phiếu nhập hàng này sẽ bị hủy. Bạn có thật sự muốn xóa?")
            if r==False:
                return
        xacnhan=x.XacNhan(self.parent)
        result=xacnhan.show()
        if not xacnhan:
            return
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn phiếu nhập hàng để xóa")
            return
        maphieu= tree.item(selected)["values"][1]
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("UPDATE thuoc"
                    +" SET SoLuongTon = SoLuongTon - ("
                    +" SELECT ct.SoLuong"
                    +" FROM chitietphieunhaphang ct"
                    +" WHERE ct.MaThuoc = thuoc.MaThuoc"
                    +" AND ct.SoPhieuNhapHang = ?)"
                    +" WHERE MaThuoc IN ("
                    +" SELECT DISTINCT MaThuoc"
                    +" FROM chitietphieunhaphang"
                    +" WHERE SoPhieunhapHang = ?);",(maphieu,maphieu,))
        cur.execute("DELETE FROM chitietphieunhaphang WHERE SoPhieunhaphang=?", (maphieu,))
        cur.execute("DELETE FROM phieunhaphang WHERE SoPhieunhaphang=?", (maphieu,))
        conn.commit() 
        messagebox.showinfo("Thông báo", "Xóa thành công!")
        thuoc_instance = self.main_app.frames.get(t.Thuoc)
        thuoc_instance.load_data()
        conn.close()
        self.load_data()
        self.Luu()
    def Sua(self):
        conn = connect_db()
        cur = conn.cursor()
        tree=self.tree
        selected = tree.focus()
        maphieu = self.entry_maphieu.get()
        manhanvien = self.entry_nhanvien.get()
        nhanvien = self.cbb_manhanvien.get()
        nhacungcap = self.cbb_manhacungcap.get()
        manhacungcap = self.entry_nhacungcap.get()
        sdtncc = self.entry_sodienthoaincc.get()
        diachincc = self.entry_diachincc.get()
        ngaynhap=self.dtp.get_date()
        sql_trangthai="select trangthai from phieunhaphang where sophieunhaphang=?"
        maphieu=self.entry_maphieu.get()
        cur.execute(sql_trangthai,(maphieu,))
        trangthai_result=cur.fetchone()
        trangthai=trangthai_result[0] if trangthai_result else None
        if trangthai=="Đã duyệt":
            messagebox.showinfo("Thông báo","Phiếu đã được duyệt không thể sửa!")
            return        
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn thuoc để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        values = tree.item(selected)["values"]
        if maphieu == "" or manhanvien == "" or manhacungcap== "" or sdtncc=="" or diachincc=="" or nhanvien=="" or nhacungcap=="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        sql_pnh="select trangthai,tongtien from phieunhaphang where sophieunhaphang=?"
        cur.execute(sql_pnh,(maphieu,))
        pnh_result=cur.fetchone()
        trangthai=pnh_result[0] if pnh_result else None
        tongtien=pnh_result[1] if pnh_result else None
        tree.item(selected, values=(trangthai,maphieu, manhanvien, nhanvien, manhacungcap, nhacungcap, sdtncc, diachincc, ngaynhap,tongtien))
        self.Luu()
    def Luu(self):
        tree=self.tree
        maphieu = self.entry_maphieu.get()
        nhanvien = self.entry_nhanvien.get()
        manhanvien = self.cbb_manhanvien.get()
        manhacungcap = self.cbb_manhacungcap.get()
        nhacungcap = self.entry_nhacungcap.get()
        sdtncc = self.entry_sodienthoaincc.get()
        diachincc = self.entry_diachincc.get()
        ngaynhap=self.dtp.get_date()
        if maphieu == "" or manhanvien == "" or manhacungcap== "" or sdtncc=="" or diachincc=="" or nhanvien=="" or nhacungcap=="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        conn = connect_db()
        cur = conn.cursor()
        sql_pnh="select trangthai,tongtien from phieunhaphang where sophieunhaphang=?"
        cur.execute(sql_pnh,(maphieu,))
        pnh_result=cur.fetchone()
        trangthai=pnh_result[0] if pnh_result else None
        tongtien=pnh_result[1] if pnh_result else None
        cur.execute("UPDATE phieunhaphang SET manv=?, manhacungcap=?, ngaylapphieunhap=?,tongtien=?,trangthai=?  WHERE sophieunhaphang=?",
        (manhanvien,manhacungcap,ngaynhap,tongtien,trangthai,maphieu))
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
    def update_manhacungcap(self,event):
        ma_ncc_chon = self.selected_mancc.get() 
        ten_ncc = None
        sdt_ncc= None
        diachi_ncc=None
        if ma_ncc_chon:
            conn = connect_db()
            cur = conn.cursor()
            try:
                sql_tenncc = "SELECT tenncc,sodienthoaincc,diachincc FROM nhacungcap WHERE manhacungcap = ?"
                cur.execute(sql_tenncc, (ma_ncc_chon,))
                tenncc_result = cur.fetchone()
                if tenncc_result:
                    ten_ncc = tenncc_result[0]
                    sdt_ncc=tenncc_result[1]
                    diachi_ncc=tenncc_result[2]
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi khi truy vấn Mã NV: {sqlstate}")
            finally:
                cur.close()
                conn.close()
        self.entry_nhacungcap.delete(0, tk.END)
        self.entry_sodienthoaincc.delete(0,tk.END)
        self.entry_diachincc.delete(0,tk.END)
        if ten_ncc: self.entry_nhacungcap.insert(0, ten_ncc)
        else: pass 
        if sdt_ncc: self.entry_sodienthoaincc.insert(0,sdt_ncc)
        else: pass
        if diachi_ncc: self.entry_diachincc.insert(0,diachi_ncc)
        else: pass
    def DuyetPhieu(self):
        conn = connect_db()
        cur = conn.cursor()
        tree=self.tree
        selected=tree.focus()
        trangthai=tree.item(selected)["values"][0]
        if trangthai=="Đã duyệt":
            messagebox.showinfo("Thông báo","Phiếu đã được duyệt!")
            return
        maphieu=self.entry_maphieu.get()
        ngaynhap=datetime.now().date()
        trangthai="Đã duyệt"
        sql="update phieunhaphang set trangthai=?,ngaylapphieunhap=? where sophieunhaphang=?"
        cur.execute(sql,(trangthai,ngaynhap,maphieu,))
        cur.execute("UPDATE thuoc"
                    +" SET SoLuongTon = SoLuongTon + ("
                    +" SELECT ct.SoLuong"
                    +" FROM chitietphieunhaphang ct"
                    +" WHERE ct.MaThuoc = thuoc.MaThuoc"
                    +" AND ct.SoPhieunhapHang = ?)"
                    +" WHERE MaThuoc IN ("
                    +" SELECT DISTINCT MaThuoc"
                    +" FROM chitietphieunhaphang"
                    +" WHERE SoPhieunhapHang = ?);",(maphieu,maphieu,))
        conn.commit()
        conn.close()
        self.load_data()
        try:
            thuoc_instance = self.main_app.frames.get(t.Thuoc)
            if thuoc_instance:
                thuoc_instance.load_data() 
                messagebox.showinfo("Thông báo", "Phiếu đã được duyệt và tồn kho đã được cập nhật!")
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy form Thuốc để cập nhật tồn kho tự động.")
        except AttributeError as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật tồn kho: {e}. Kiểm tra lại kiến trúc Main App và form Thuoc.")
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
        ngaylap = datetime.strptime(date_only_string, '%m/%d/%y').date()
        tennv=self.entry_nhanvien.get()
        tenncc=self.entry_nhacungcap.get()
        sdt=self.entry_sodienthoaincc.get()
        diachi=self.entry_diachincc.get()
        cur.execute("select count(*) from chitietphieunhaphang where sophieunhaphang=?",(sophieu,))
        result=cur.fetchone()
        n=result[0]
        items = []
        sql_detail = """
            SELECT t.TenThuoc, c.SoLuong, t.GiaBan, c.ThanhTien ,tendonvi
            FROM Thuoc t, DonViTinh d, ChiTietPhieunhapHang c
            WHERE t.MaThuoc = c.MaThuoc AND d.MaDVT = t.MaDVT AND c.SoPhieuNhapHang = ?"""
        cur.execute(sql_detail, (sophieu,))
        items = []
        for result in cur.fetchall():
            ten_thuoc = result[0]
            sl = result[1]
            gia = result[2]
            thanhtien = result[3]
            dvt=result[4]
            items.append((ten_thuoc, sl, f"{float(gia):,.0f}",dvt, f"{float(thanhtien):,.0f}")) 
        tongtien=tree.item(selected)["values"][9]
        trangthai=tree.item(selected)["values"][0]
        try:
            pdf_path = r.export_to_pdf(sophieu, ngaylap,trangthai,tennv, tenncc, diachi, sdt, tongtien, items)
            if pdf_path and os.path.exists(pdf_path):
                if sys.platform == "win32":
                    os.startfile(pdf_path, 'print') 
                else:
                    os.startfile(pdf_path) 
            else:
                messagebox.showwarning("Cảnh báo", "Không thể mở bản xem trước PDF.")
        except Exception as e:
            messagebox.showerror("Lỗi In/PDF", f"Lỗi khi mở bản xem trước: {e}")

       


       
