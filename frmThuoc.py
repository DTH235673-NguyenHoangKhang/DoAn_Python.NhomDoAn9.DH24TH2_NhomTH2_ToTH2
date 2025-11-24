import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime, timedelta
import frmDonViTinh as d
import frmLoaiThuoc as l
import frmNhaCungCap as ncc
import frmPhieuNhapHang as p
import frmXacNhan as x
def connect_db():
 conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\sqlexpress;'  
            'DATABASE=QLCHMBTND;'       
            'Trusted_Connection=yes;')
 return conn
def getdata_nhacungcap():
 nhacungcap=[]
 getnhacungcap=connect_db()
 cursor=getnhacungcap.cursor()
 sql_query = "SELECT TenNCC FROM nhacungcap where tinhtrang=1"
 cursor.execute(sql_query)
 for row in cursor.fetchall():
        nhacungcap.append(row[0])
 cursor.close()
 getnhacungcap.close()
 return nhacungcap
def getdata_loaithuoc():
 loaithuoc=[]
 getloaithuoc=connect_db()
 cursor=getloaithuoc.cursor()
 sql_query = "SELECT Tenloaithuoc FROM loaithuoc"
 cursor.execute(sql_query)
 for row in cursor.fetchall():
        loaithuoc.append(row[0])
 cursor.close()
 getloaithuoc.close()
 return loaithuoc
def getdata_donvitinh():
 donvitinh=[]
 getdonvitinh=connect_db()
 cursor=getdonvitinh.cursor()
 sql_query = "SELECT Tendonvi FROM donvitinh"
 cursor.execute(sql_query)
 for row in cursor.fetchall():
        donvitinh.append(row[0])
 cursor.close()
 getdonvitinh.close()
 return donvitinh
class Thuoc(tk.Frame):
    def __init__(self, parent, main_app): 
        super().__init__(parent)
        self.main_app = main_app
        self.parent=parent
        lbl_title = tk.Label(self, text="QUẢN LÝ THUỐC NÔNG DƯỢC", font=("Arial", 18, "bold"))
        lbl_title.pack(pady=10)
        frame_info = tk.Frame(self)
        frame_info.pack(pady=5, padx=10, fill="x")
        tk.Label(frame_info, text="Mã thuốc").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_mathuoc = tk.Entry(frame_info, width=10)
        self.entry_mathuoc.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_info, text="Tên thuốc").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_tenthuoc = tk.Entry(frame_info, width=20)
        self.entry_tenthuoc.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(frame_info, text="Nhà cung cấp").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.cbb_nhacungcap = ttk.Combobox(frame_info, values=getdata_nhacungcap(), width=15)
        self.cbb_nhacungcap.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        btnAlterNCC=tk.Button(frame_info,text="...",width=5,command=self.AlterNCC).grid(row=0,column=6,padx=5,pady=5)

        tk.Label(frame_info,text="Giá bán").grid(row=1,column=0,padx=5,pady=5,sticky="w")
        self.entry_giaban=tk.Entry(frame_info,width=10)
        self.entry_giaban.grid(row=1,column=1,padx=5,pady=5,sticky="w")

        tk.Label(frame_info,text="Giá nhập").grid(row=1,column=2,padx=5,pady=5,sticky="w")
        self.entry_gianhap=tk.Entry(frame_info,width=10)
        self.entry_gianhap.grid(row=1,column=3,padx=5,pady=5,sticky="w")
        tk.Label(frame_info, text="Loại thuốc").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.cbb_loaithuoc = ttk.Combobox(frame_info, values=getdata_loaithuoc(), width=20)
        self.cbb_loaithuoc.grid(row=1, column=5, padx=5, pady=5, sticky="w")
        btnAlterLT=tk.Button(frame_info,text="...",width=5,command=self.AlterLT).grid(row=1,column=6,padx=5,pady=5)

        tk.Label(frame_info,text="Số lượng tổn").grid(row=2,column=0,pady=5,padx=5,sticky="w")
        self.entry_soluongton=tk.Entry(frame_info,width=10)
        self.entry_soluongton.grid(row=2,column=1,padx=5,pady=5,sticky="w")

        tk.Label(frame_info, text="Đơn vị").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.cbb_donvitinh = ttk.Combobox(frame_info, values=getdata_donvitinh(), width=20)
        self.cbb_donvitinh.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        btnAlterDVT=tk.Button(frame_info,text="...",width=5,command=self.AlterDVT).grid(row=2,column=4,padx=5,pady=5,sticky="w")
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Thêm", width=8, command=self.them_thuoc).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Lưu", width=8, command=self.luu_thuoc).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Sửa", width=8, command=self.sua_thuoc).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Hủy", width=8, command=self.clear_input).grid(row=0, column=3, padx=5)
        tk.Button(frame_btn, text="Xóa", width=8, command=self.xoa_thuoc).grid(row=0, column=4, padx=5)
        lbl_ds = tk.Label(self, text="Danh sách thuốc nông dược", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w", padx=10)
        columns = ("Mã thuốc", "Tên thuốc", "Nhà cung cấp", "Loại thuốc", "Đơn vị tính","Số lượng tồn", "Giá bán","Giá nhập")
        self.tree = ttk.Treeview(self    , columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Mã thuốc", width=60, anchor="center")
        tree.column("Tên thuốc", width=150)
        tree.column("Nhà cung cấp", width=100)
        tree.column("Loại thuốc", width=70, anchor="center")
        tree.column("Đơn vị tính", width=50, anchor="center")
        tree.column("Số lượng tồn", width=50)
        tree.column("Giá bán", width=50)
        tree.column("Giá nhập", width=50)
        tree.bind("<<TreeviewSelect>>", self.select_record)
        tree.pack(padx=10, pady=5, fill="both")
        frame_timkiem=tk.Frame(self)
        frame_timkiem.pack(pady=5)
        tk.Label(frame_timkiem,text="Nhập mã thuốc cần tìm: ").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_matimkiem=tk.Entry(frame_timkiem,width=15)
        self.entry_matimkiem.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        btnTimKiem=tk.Button(frame_timkiem,text="Tìm thuốc",width=10,command=self.Tim).grid(row=0,column=2,padx=5,pady=5)
        self.load_data()
    def Tim(self):
        matim=self.entry_matimkiem.get().strip()
        if matim=="":
            messagebox.showinfo("Thông báo","Vui lòng nhập mã thuốc cần tìm")
            self.entry_matimkiem.focus()
            return
        tree=self.tree
        check=0
        for i in tree.get_children():
            if matim==tree.item(i)["values"][0].strip():
                check=1
                id=i
                value=tree.item(i)["values"]
        if check==0:
            messagebox.showinfo("Thông báo","Không tìm thấy mã thuốc trên")
            return
        tree.delete(id)
        new_id = tree.insert("", 0, values=value)
        tree.selection_remove(tree.selection()) 
        tree.selection_add(new_id)             
        tree.see(new_id)                       
        self.select_record(None)
    def AlterDVT(self):
        chi_tiet_window = d.DonViTinh(self.parent)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        self.cbb_donvitinh.config(values=None)
        self.cbb_donvitinh.config(values=getdata_donvitinh())
        self.load_data()
    def AlterLT(self):
        chi_tiet_window = l.LoaiThuoc(self.parent)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        self.cbb_loaithuoc.config(values=None)
        self.cbb_loaithuoc.config(values=getdata_loaithuoc())
        self.load_data()
    def AlterNCC(self):
        chi_tiet_window = ncc.NhaCungCap(self.parent)
        chi_tiet_window.grab_set()
        self.parent.wait_window(chi_tiet_window)
        self.cbb_nhacungcap.config(values=None)
        self.cbb_nhacungcap.config(values=getdata_nhacungcap())
        pnh=self.main_app.frames.get(p.PhieuNhapHang)
        pnh.reload_manhacungcap()
        self.load_data()
    def reload_manhacungcap(self):
        self.cbb_nhacungcap.config(values=None)
        self.cbb_nhacungcap.config(values=getdata_nhacungcap())
    def select_record(self,event):
      self.entry_mathuoc.config(state="normal")
      selected = self.tree.selection()
      if not selected:
         return
      values = self.tree.item(selected)["values"]
      self.entry_mathuoc.delete(0, tk.END)
      self.entry_mathuoc.insert(0, values[0])
      self.entry_tenthuoc.delete(0, tk.END)
      self.entry_tenthuoc.insert(0, values[1])
      self.cbb_nhacungcap.set(values[2])
      self.cbb_loaithuoc.set(values[3])
      self.cbb_donvitinh.set(values[4])
      self.entry_soluongton.delete(0, tk.END)
      self.entry_soluongton.insert(0, values[5])
      self.entry_giaban.delete(0, tk.END)
      self.entry_giaban.insert(0, values[6])
      self.entry_gianhap.delete(0, tk.END)
      self.entry_gianhap.insert(0, values[7])
      self.entry_mathuoc.config(state="readonly")
    def clear_input(self):
      self.entry_mathuoc.config(state="normal")
      self.entry_mathuoc.delete(0, tk.END)
      self.entry_tenthuoc.delete(0, tk.END)
      self.entry_soluongton.delete(0, tk.END)
      self.entry_giaban.delete(0, tk.END)
      self.entry_gianhap.delete(0, tk.END)
      self.cbb_nhacungcap.set("")
      self.cbb_loaithuoc.set("")
      self.cbb_donvitinh.set("")
      self.entry_matimkiem.delete(0,tk.END)
      self.load_data()
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = (
        "SELECT "
        +"t.mathuoc, t.tenthuoc, n.TenNCC as nhacungcap, l.Tenloaithuoc as loaithuoc, d.Tendonvi as donvitinh, "
        +"t.soluongton, t.giaban, t.gianhap "
        +"FROM thuoc t, loaithuoc l, donvitinh d, nhacungcap n "
        +"WHERE t.MaLT = l.MaLT AND t.MaDVT = d.MaDVT AND t.MaNhaCungCap = n.MaNhaCungCap")
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def them_thuoc(self):
        mathuoc = self.entry_mathuoc.get()
        tenthuoc = self.entry_tenthuoc.get()
        soluongton = self.entry_soluongton.get()
        giaban = self.entry_giaban.get()
        gianhap = self.entry_gianhap.get()
        nhacungcap = self.cbb_nhacungcap.get()
        loaithuoc = self.cbb_loaithuoc.get()
        donvitinh = self.cbb_donvitinh.get()
        tree=self.tree
        if mathuoc == "" or tenthuoc == "" or soluongton == "" or giaban=="" or gianhap=="" or nhacungcap=="" or loaithuoc=="" or donvitinh=="":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if mathuoc[0]!='T' or mathuoc[1]!='N' or mathuoc[2]!='D' or len(mathuoc)!=5:
                messagebox.showinfo("Thông báo","Sai định dạng mã thuốc (TND00)")
                return
        for i in range(3, len(mathuoc)):
            if not mathuoc[i].isdigit(): 
                messagebox.showinfo("Thông báo","Sai định dạng mã thuốc (TND00)")
                return
        for i in tree.get_children():
            if mathuoc == tree.item(i)["values"][0]:
                messagebox.showwarning("Trùng mã", "Mã thuốc đã tồn tại")
                return
        if not giaban.isdigit(): 
                messagebox.showinfo("Thông báo","Giá bán phải là 1 số và lớn hơn 0")
                return
        elif int(giaban)<=0:
                messagebox.showinfo("Thông báo","Giá bán phải là 1 số và lớn hơn 0")
                return
        if not gianhap.isdigit(): 
                messagebox.showinfo("Thông báo","Giá nhập phải là 1 số và lớn hơn 0")
                return
        elif int(gianhap)<=0:
                messagebox.showinfo("Thông báo","Giá nhập phải là 1 số và lớn hơn 0")
                return
        if not soluongton.isdigit(): 
                messagebox.showinfo("Thông báo","Số lượng tồn phải là 1 số và lớn hơn 0")
                return
        elif int(soluongton)<=0:
                messagebox.showinfo("Thông báo","Số lượng tồn phải là 1 số và lớn hơn 0")
                return
        if int(giaban)<int(gianhap):
            messagebox.showinfo("Thông báo","Giá bán phải lớn hơn giá nhập!")
            return  
        conn = connect_db()
        cur = conn.cursor()
        try:
            sql_ncc = "SELECT MaNhaCungCap FROM nhacungcap WHERE TenNCC = ?"
            cur.execute(sql_ncc, (nhacungcap))
            manhacungcap_result = cur.fetchone()
            manhacungcap = manhacungcap_result[0] if manhacungcap_result else None
            sql_lt = "SELECT MaLT FROM loaithuoc WHERE Tenloaithuoc = ?"
            cur.execute(sql_lt, (loaithuoc))
            malt_result = cur.fetchone()
            malt = malt_result[0] if malt_result else None
            sql_dvt = "SELECT MaDVT FROM donvitinh WHERE Tendonvi = ?"
            cur.execute(sql_dvt, (donvitinh))
            madvt_result = cur.fetchone()
            madvt = madvt_result[0] if madvt_result else None
            if manhacungcap is None or malt is None or madvt is None:
                messagebox.showerror("Lỗi tra cứu", "Không tìm thấy Mã tương ứng cho Nhà cung cấp, Loại thuốc, hoặc Đơn vị tính.")
                return
            cur.execute("INSERT INTO thuoc VALUES (?,?,?,?,?,?,?,?)",
            (mathuoc, tenthuoc, manhacungcap,giaban,gianhap, soluongton,malt, madvt))
            conn.commit()
            self.load_data()
            self.clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()   
    def xoa_thuoc(self):
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn thuốc để xóa")
            return
        mathuoc=self.tree.item(selected)["values"][0]
        conn = connect_db()
        cur = conn.cursor()
        sql_tonkho = "SELECT soluongton FROM thuoc WHERE mathuoc=?"
        cur.execute(sql_tonkho, (mathuoc,))
        tonkho_result = cur.fetchone()
        if tonkho_result and tonkho_result[0] != 0:
            messagebox.showwarning("Không thể xóa", "Thuốc còn tồn kho (Số lượng: {}). Không thể xóa.".format(tonkho_result[0]))
            return
        sql_ngayban_gannhat = """
            SELECT MAX(p.Ngaymuahang) 
            FROM phieumuahang p JOIN ChiTietphieumuahang CT ON p.sophieumuahang = CT.sophieumuahang 
            WHERE CT.MaThuoc = ?
            """
        cur.execute(sql_ngayban_gannhat, (mathuoc,))
        ngay_ban_gannhat = cur.fetchone()[0]
        sql_ngaynhap_gannhat = """
            SELECT MAX(P.NgaylapphieuNhap) 
            FROM PhieuNhapHang P JOIN ChiTietPhieuNhaphang CT ON P.sophieunhaphang = CT.sophieunhaphang 
            WHERE CT.MaThuoc = ? """
        cur.execute(sql_ngaynhap_gannhat, (mathuoc,))
        ngay_nhap_gannhat = cur.fetchone()[0]
        ngay_giao_dich_gannhat = None
        if ngay_ban_gannhat and ngay_nhap_gannhat:
            ngay_giao_dich_gannhat = max(ngay_ban_gannhat, ngay_nhap_gannhat)
        elif ngay_ban_gannhat:
            ngay_giao_dich_gannhat = ngay_ban_gannhat
        elif ngay_nhap_gannhat:
            ngay_giao_dich_gannhat = ngay_nhap_gannhat
        ngay_hien_tai = datetime.now().date() 
        ngay_gioi_han = ngay_hien_tai - timedelta(days=90)
        if ngay_giao_dich_gannhat:
            if isinstance(ngay_giao_dich_gannhat, datetime):
                ngay_giao_dich_gannhat = ngay_giao_dich_gannhat.date() 
            if ngay_giao_dich_gannhat > ngay_gioi_han:
                messagebox.showwarning("Không thể xóa", f"Thuốc có giao dịch gần nhất vào ngày: {ngay_giao_dich_gannhat}. Phải hơn 3 tháng (90 ngày) mới có thể xóa.")
                return
        mathuoc = tree.item(selected)["values"][0]
        cur.execute("DELETE FROM thuoc WHERE mathuoc=?", (mathuoc,))
        conn.commit() 
        messagebox.showinfo("Xóa thành công", "Đã xóa thuốc")
        conn.close()
        self.load_data()
    def sua_thuoc(self):

        tree=self.tree
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn thuoc để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        values = tree.item(selected)["values"]
        mathuoc = self.entry_mathuoc.get()
        tenthuoc = self.entry_tenthuoc.get()
        nhacungcap = self.cbb_nhacungcap.get()
        loaithuoc = self.cbb_loaithuoc.get()
        donvitinh = self.cbb_donvitinh.get()
        soluongton = self.entry_soluongton.get()
        giaban = self.entry_giaban.get()
        gianhap = self.entry_gianhap.get()
        if mathuoc == "" or tenthuoc == "" or soluongton == "" or giaban=="" or gianhap=="" or nhacungcap=="" or loaithuoc=="" or donvitinh=="":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if not giaban.isdigit(): 
                messagebox.showinfo("Thông báo","Giá bán phải là 1 số và lớn hơn 0")
                return
        elif int(giaban)<=0:
                messagebox.showinfo("Thông báo","Giá bán phải là 1 số và lớn hơn 0")
                return
        if not gianhap.isdigit(): 
                messagebox.showinfo("Thông báo","Giá nhập phải là 1 số và lớn hơn 0")
                return
        elif int(gianhap)<=0:
                messagebox.showinfo("Thông báo","Giá nhập phải là 1 số và lớn hơn 0")
                return
        if not soluongton.isdigit(): 
                messagebox.showinfo("Thông báo","Số lượng tồn phải là 1 số và lớn hơn 0")
                return
        elif int(soluongton)<0:
                messagebox.showinfo("Thông báo","Số lượng tồn phải là 1 số và lớn hơn 0")
                return
        if int(giaban)<int(gianhap):
            messagebox.showinfo("Thông báo","Giá bán phải lớn hơn giá nhập!")
            return
        tree.item(selected, values=(
        mathuoc, tenthuoc, nhacungcap, loaithuoc, donvitinh, soluongton, giaban, gianhap))
    def luu_thuoc(self):
        tree=self.tree
        for i in tree.get_children():
            mathuoc = tree.item(i)["values"][0]
            tenthuoc = tree.item(i)["values"][1]
            nhacungcap = tree.item(i)["values"][2]
            loaithuoc = tree.item(i)["values"][3]
            donvitinh = tree.item(i)["values"][4]
            soluongton = tree.item(i)["values"][5]
            giaban = tree.item(i)["values"][6]
            gianhap = tree.item(i)["values"][7]
            conn = connect_db()
            cur = conn.cursor()
            sql_ncc = "SELECT MaNhaCungCap FROM nhacungcap WHERE TenNCC = ?"
            cur.execute(sql_ncc, (nhacungcap))
            manhacungcap_result = cur.fetchone()
            manhacungcap = manhacungcap_result[0] if manhacungcap_result else None
            sql_lt = "SELECT MaLT FROM loaithuoc WHERE Tenloaithuoc = ?"
            cur.execute(sql_lt, (loaithuoc))
            malt_result = cur.fetchone()
            malt = malt_result[0] if malt_result else None
            sql_dvt = "SELECT MaDVT FROM donvitinh WHERE Tendonvi = ?"
            cur.execute(sql_dvt, (donvitinh))
            madvt_result = cur.fetchone()
            madvt = madvt_result[0] if madvt_result else None
            cur.execute("UPDATE thuoc SET tenthuoc=?, manhacungcap=?, giaban=?,gianhap=?,soluongton=?,malt=?,madvt=?  WHERE mathuoc=?",
        (tenthuoc, manhacungcap ,giaban,gianhap,soluongton,malt,madvt,mathuoc))
            conn.commit()
            conn.close()
        messagebox.showinfo("Thông báo","Lưu thành công")
    def Thoat(self):
        self.quit()