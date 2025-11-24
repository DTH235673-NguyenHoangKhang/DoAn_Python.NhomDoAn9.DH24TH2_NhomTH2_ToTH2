import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime, timedelta
def connect_db():
 conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
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
class NhanVien(tk.Toplevel):
    def __init__(self,master):
        tk.Toplevel.__init__(self,master)
        self.title("Quản Lí Nhân Viên")
        center_window(self, 700, 450) 
        tk.Label(self, text="Nhân Viên", font=("Arial", 16, "bold")).pack(pady=10)
        self.create_widgets()
    def create_widgets(self):
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Mã Nhân Viên:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_MaNV = tk.Entry(form_frame)
        self.entry_MaNV.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tên Nhân Viên:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_TenNV = tk.Entry(form_frame)
        self.entry_TenNV.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Địa Chỉ:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_DiaChi = tk.Entry(form_frame)
        self.entry_DiaChi.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Số điện thoại:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_SDT = tk.Entry(form_frame)
        self.entry_SDT.grid(row=0, column=3, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btnThem = tk.Button(btn_frame, text="Thêm", width=10, command=self.them_nv)
        self.btnThem.grid(row=0, column=0, padx=20)

        self.btnSua = tk.Button(btn_frame, text="Sửa", width=10, command=self.sua_nv)
        self.btnSua.grid(row=0, column=1, padx=20)

        self.btnXoa = tk.Button(btn_frame, text="Xóa", width=10, command=self.xoa_nv)
        self.btnXoa.grid(row=0, column=2, padx=20)

        self.btnLuu = tk.Button(btn_frame, text="Lưu", width=10, command=self.luu_nv)
        self.btnLuu.grid(row=0, column=3, padx=20)

        self.btnHuy = tk.Button(btn_frame, text="Hủy", width=10, command=self.huy_input)
        self.btnHuy.grid(row=0, column=4, padx=20)

        self.btnThoat = tk.Button(btn_frame, text="Thoát", width=10, command=self.destroy)
        self.btnThoat.grid(row=0, column=5, padx=20)
        frame_timkiem=tk.Frame(self)
        frame_timkiem.pack(pady=5)
        tk.Label(frame_timkiem,text="Nhập mã nhân viên cần tìm: ").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_matimkiem=tk.Entry(frame_timkiem,width=15)
        self.entry_matimkiem.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        btnTimKiem=tk.Button(frame_timkiem,text="Tìm nhân viên",width=10,command=self.Tim).grid(row=0,column=2,padx=5,pady=5)
           
        lbl_ds = tk.Label(self, text="Danh sách nhân viên", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w", padx=10)
        columns = ("Mã NV", "Tên NV", "Địa chỉ", "Số điện thoại")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Mã NV", width=60, anchor="center")
        tree.column("Tên NV", width=100, anchor="center")
        tree.column("Địa chỉ", width=70, anchor="center")
        tree.column("Số điện thoại", width=100, anchor="center")
        tree.bind("<<TreeviewSelect>>", self.select_record)
        tree.pack(padx=10, pady=5, fill="both")   
        self.load_data()
    def Tim(self):
        matim=self.entry_matimkiem.get().strip()
        if matim=="":
            messagebox.showinfo("Thông báo","Vui lòng nhập mã nhân viên cần tìm")
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
            messagebox.showinfo("Thông báo","Không tìm thấy mã nhân viên trên")
            return
        tree.delete(id)
        new_id = tree.insert("", 0, values=value)
            
        tree.selection_remove(tree.selection()) 
        tree.selection_add(new_id)             
        tree.see(new_id)                                
        self.select_record(None)
    def select_record(self, event):
        self.entry_MaNV.config(state="normal")
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.entry_MaNV.delete(0, tk.END)
            self.entry_MaNV.insert(0, values[0])
            self.entry_TenNV.delete(0, tk.END)
            self.entry_TenNV.insert(0, values[1])
            self.entry_DiaChi.delete(0, tk.END)
            self.entry_DiaChi.insert(0, values[2])
            self.entry_SDT.delete(0, tk.END)
            self.entry_SDT.insert(0, values[3])
        self.entry_MaNV.config(state="readonly")  
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = ("select * from NhanVien where tinhtrang=1")
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def them_nv(self):
        conn = connect_db()
        cur = conn.cursor()
        ma_nv = self.entry_MaNV.get()
        ten_nv = self.entry_TenNV.get()
        diachi_nv = self.entry_DiaChi.get()
        sdt_nv = self.entry_SDT.get()  
        tree=self.tree
        if ma_nv == "" or ten_nv == "" or diachi_nv == "" or sdt_nv =="" :
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
            return
        if ma_nv[0]!='N' or ma_nv[1]!='V' or  len(ma_nv)!=4:
                messagebox.showinfo("Thông báo","Sai định dạng mã nhân viên (NV00)")
                return
        for i in range(2, len(ma_nv)):
            if not ma_nv[i].isdigit(): 
                messagebox.showinfo("Thông báo","Sai định dạng mã nhân viên (NV00)")
                return
        for i in sdt_nv:
            if ord(i)<48 or ord(i)>57:
                messagebox.showinfo("Thông báo","Sai định dạng số điện thoại!")
                return 
        cur.execute("select tinhtrang from nhanvien where manv=?",(ma_nv,))
        result=cur.fetchone()
        if result:
            t=result[0]
            if t==1:
                messagebox.showwarning("Trùng mã", "Mã nhân viên đã tồn tại")
                return
            elif t==0:
                cur.execute("update nhanvien set tinhtrang=1,tenv=?,diachinv=?,sodienthoai=? where manv=?",
                            (ten_nv,diachi_nv,sdt_nv,ma_nv,))
                conn.commit()
                self.load_data()                
                return
        try:
            cur.execute("INSERT INTO NhanVien VALUES (?,?,?,?,?)",
            (ma_nv, ten_nv, diachi_nv, sdt_nv,1))
            conn.commit()
            self.load_data()
            self.huy_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()
    def xoa_nv(self):
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để xóa")
            return
        ma_nv = tree.item(selected)["values"][0]
        conn = connect_db()
        cur = conn.cursor()
        sql_ngayban_gannhat = """SELECT MAX(p.Ngaymuahang) FROM phieumuahang p JOIN nhanvien n on p.manv=n.manv 
            WHERE n.manv = ?"""
        cur.execute(sql_ngayban_gannhat, (ma_nv,))
        ngay_ban_gannhat = cur.fetchone()[0]
        sql_ngaynhap_gannhat = """SELECT MAX(P.NgaylapphieuNhap) FROM PhieuNhapHang P JOIN nhanvien n on p.manv=n.manv
            WHERE n.manv= ?"""
        cur.execute(sql_ngaynhap_gannhat, (ma_nv,))
        ngay_nhap_gannhat = cur.fetchone()[0]  
        ngay_giao_dich_gannhat = None
        if ngay_ban_gannhat and ngay_nhap_gannhat:
            ngay_giao_dich_gannhat = max(ngay_ban_gannhat, ngay_nhap_gannhat)
        elif ngay_ban_gannhat:
            ngay_giao_dich_gannhat = ngay_ban_gannhat
        elif ngay_nhap_gannhat:
            ngay_giao_dich_gannhat = ngay_nhap_gannhat
        ngay_hien_tai = datetime.now().date() 
        ngay_gioi_han = ngay_hien_tai - timedelta(days=30)
        if ngay_giao_dich_gannhat:
            if isinstance(ngay_giao_dich_gannhat, datetime):
                ngay_giao_dich_gannhat = ngay_giao_dich_gannhat.date() 
            if ngay_giao_dich_gannhat > ngay_gioi_han:
                messagebox.showwarning("Không thể xóa", f"Nhân viên có giao dịch gần nhất vào ngày: {ngay_giao_dich_gannhat}. Phải hơn 1 tháng (30 ngày) kể từ ngày thôi việc mới có thể xóa.")
                return
        cur.execute("Update nhanvien set tinhtrang=0 WHERE MaNV=?", (ma_nv,))
        conn.commit() 
        messagebox.showinfo("Xóa thành công", "Xóa nhân viên?")
        conn.close()
        self.load_data()  
    def sua_nv(self):
        tree=self.tree
        selected = tree.focus()
        ma_nv = self.entry_MaNV.get()
        ten_nv = self.entry_TenNV.get()
        diachi_nv = self.entry_DiaChi.get()
        sdt_nv = self.entry_SDT.get()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        if ma_nv == "" or ten_nv == "" or diachi_nv == "" or sdt_nv =="" :
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
            return
        values = tree.item(selected)["values"]
        tree.item(selected, values=(
        ma_nv, ten_nv, diachi_nv, sdt_nv))
    def luu_nv(self):
        tree=self.tree
        for i in tree.get_children():
            ma_nv = tree.item(i)["values"][0]
            ten_nv = tree.item(i)["values"][1]
            diachi_nv = tree.item(i)["values"][2]
            sdt_nv = "0"+str(tree.item(i)["values"][3])
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE NhanVien SET tennv=?, diachinv=?, sodienthoai=? WHERE manv=?",
        (ten_nv, diachi_nv, sdt_nv,ma_nv))
            conn.commit()
            conn.close()
        messagebox.showinfo("Thông báo","Lưu thành công")
    def huy_input(self):
        self.entry_MaNV.config(state="normal")
        self.entry_MaNV.delete(0, tk.END)
        self.entry_TenNV.delete(0, tk.END)
        self.entry_SDT.delete(0, tk.END)
        self.entry_DiaChi.delete(0, tk.END)
        self.entry_matimkiem.delete(0,tk.END)
        self.load_data()


