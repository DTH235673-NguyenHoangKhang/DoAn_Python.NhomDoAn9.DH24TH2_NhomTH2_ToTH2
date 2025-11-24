import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime, timedelta
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
class NhaCungCap(tk.Toplevel):
    def __init__(self,master):
        tk.Toplevel.__init__(self,master)
        self.title("Quản Lý Nhà Cung Cấp")
        center_window(self, 700, 450)
        tk.Label(self, text="Nhà Cung Cấp", font=("Arial", 16, "bold")).pack(pady=10)
        self.create_widgets()
    def create_widgets(self):
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Mã Nhà Cung Cấp:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_MaNCC = tk.Entry(form_frame)
        self.entry_MaNCC.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tên Nhà Cung Cấp:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_TenNCC = tk.Entry(form_frame)
        self.entry_TenNCC.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Địa Chỉ:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_DiaChi = tk.Entry(form_frame)
        self.entry_DiaChi.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Số điện thoại:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_SDT = tk.Entry(form_frame)
        self.entry_SDT.grid(row=0, column=3, padx=5, pady=5)
        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btnThem = tk.Button(btn_frame, text="Thêm", width=10, command=self.them_ncc)
        self.btnThem.grid(row=0, column=0, padx=20)

        self.btnSua = tk.Button(btn_frame, text="Sửa", width=10, command=self.sua_ncc)
        self.btnSua.grid(row=0, column=1, padx=20)

        self.btnXoa = tk.Button(btn_frame, text="Xóa", width=10, command=self.xoa_ncc)
        self.btnXoa.grid(row=0, column=2, padx=20)

        self.btnLuu = tk.Button(btn_frame, text="Lưu", width=10, command=self.luu_ncc)
        self.btnLuu.grid(row=0, column=3, padx=20)

        self.btnHuy = tk.Button(btn_frame, text="Hủy", width=10, command=self.huy_input)
        self.btnHuy.grid(row=0, column=4, padx=20)

        self.btnThoat = tk.Button(btn_frame, text="Thoát", width=10, command=self.destroy)
        self.btnThoat.grid(row=0, column=5, padx=20)
        frame_timkiem=tk.Frame(self)
        frame_timkiem.pack(pady=5)
        tk.Label(frame_timkiem,text="Nhập SDT nhà cung cấp cần tìm: ").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_SDTtimkiem=tk.Entry(frame_timkiem,width=15)
        self.entry_SDTtimkiem.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        btnTimKiem=tk.Button(frame_timkiem,text="Tìm nhà cung cấp",width=15,command=self.Tim).grid(row=0,column=2,padx=5,pady=5)
        # ====== Bảng danh sách nhà cung cấp ======
        lbl_ds = tk.Label(self, text="Danh sách nhà cung cấp", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w", padx=10)
        columns = ("Mã nhà cung cấp", "Nhà cung cấp", "Số điện thoại", "Địa chỉ")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Mã nhà cung cấp", width=60, anchor="center")
        tree.column("Nhà cung cấp", width=100, anchor="center")
        tree.column("Số điện thoại", width=70, anchor="center")
        tree.column("Địa chỉ", width=100, anchor="center")
        tree.bind("<<TreeviewSelect>>", self.select_record)
        tree.pack(padx=10, pady=5, fill="both") 
        self.load_data()
    def Tim(self):
        matim=self.entry_SDTtimkiem.get()
        if matim=="":
            messagebox.showinfo("Thông báo","Vui lòng nhập số điện thoại nhà cung cấp cần tìm")
            self.entry_SDTtimkiem.focus()
            return
        tree=self.tree
        check=0
        for i in tree.get_children():
            if int(matim)==tree.item(i)["values"][2]:
                check=1
                id=i
                value=tree.item(i)["values"]
        if check==0:
            messagebox.showinfo("Thông báo","Không tìm thấy số điện thoại trên")
            return
        tree.delete(id)
        new_id = tree.insert("", 0, values=value)
        tree.selection_remove(tree.selection()) 
        tree.selection_add(new_id)             
        tree.see(new_id)                             
        self.select_record(None)
    def select_record(self, event):
        self.entry_MaNCC.config(state="normal")
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.entry_MaNCC.delete(0, tk.END)
            self.entry_MaNCC.insert(0, values[0])
            self.entry_TenNCC.delete(0, tk.END)
            self.entry_TenNCC.insert(0, values[1])
            self.entry_SDT.delete(0, tk.END)
            self.entry_SDT.insert(0, values[2])
            self.entry_DiaChi.delete(0, tk.END)
            self.entry_DiaChi.insert(0, values[3])
        self.entry_MaNCC.config(state="readonly")
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = ("select * from NhaCungCap where tinhtrang=1")
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def them_ncc(self):
        conn = connect_db()
        cur = conn.cursor()
        ma_ncc = self.entry_MaNCC.get()
        ten_ncc = self.entry_TenNCC.get()
        diachi_ncc = self.entry_DiaChi.get()
        sdt = self.entry_SDT.get()
        tree=self.tree
        if ma_ncc == "" or ten_ncc == "" or diachi_ncc == "" or sdt =="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if ma_ncc[0]!='N' or ma_ncc[1]!='C' or ma_ncc[2]!='C' or len(ma_ncc)!=5:
                messagebox.showinfo("Thông báo","Sai định dạng mã nhà cung cấp (NCC00)")
                return
        for i in range(3, len(ma_ncc)):
            if not ma_ncc[i].isdigit(): 
                messagebox.showinfo("Thông báo","Sai định dạng mã nhà cung cấp (NCC00)")
                return
        cur.execute("select tinhtrang from nhacungcap where manhacungcap=?",(ma_ncc,))
        result=cur.fetchone()
        if result:
            t=result[0]
            if t==1:
                messagebox.showwarning("Trùng mã", "Mã nhà cung cấp đã tồn tại")
                return
            elif t==0:
                cur.execute("update nhacungcap set tenncc=?,diachincc=?,sodienthoaincc=?, tinhtrang=1 where manhacungcap=?",(ten_ncc,diachi_ncc,sdt,ma_ncc,))
                conn.commit()
                self.load_data()
                return
        try:
            cur.execute("INSERT INTO NhaCungCap VALUES (?,?,?,?,?)",
            (ma_ncc, ten_ncc, sdt, diachi_ncc,1))
            conn.commit()
            self.load_data()
            self.huy_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()
    def xoa_ncc(self):
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn nhà cung cấp để xóa")
            return
        ma_ncc = tree.item(selected)["values"][0]
        conn = connect_db()
        cur = conn.cursor()
        sql_ngaynhap_gannhat = """SELECT MAX(P.NgaylapphieuNhap) FROM PhieuNhapHang P WHERE p.manhacungcap= ?"""
        cur.execute(sql_ngaynhap_gannhat,(ma_ncc,))
        ngaynhap=cur.fetchone()
        ngay_giao_dich_gannhat=ngaynhap[0]
        ngay_hien_tai = datetime.now().date() 
        ngay_gioi_han = ngay_hien_tai - timedelta(days=180)
        if ngay_giao_dich_gannhat:
            if isinstance(ngay_giao_dich_gannhat, datetime):
                ngay_giao_dich_gannhat = ngay_giao_dich_gannhat.date() 
            if ngay_giao_dich_gannhat > ngay_gioi_han:
                messagebox.showwarning("Không thể xóa", f"Nhà cung cấp có giao dịch gần nhất vào ngày: {ngay_giao_dich_gannhat}. Phải hơn 6 tháng (180 ngày) không phát sinh giao dịch mới có thể xóa.")
                return
        cur.execute("Update NhaCungCap set tinhtrang=0 WHERE MaNhaCungCap=?", (ma_ncc,))
        conn.commit() 
        messagebox.showinfo("Xóa thành công", "Xóa nhà cung cấp")
        conn.close()
        self.load_data()  
    def sua_ncc(self):
        tree=self.tree
        selected = tree.focus()
        ma_ncc = self.entry_MaNCC.get()
        ten_ncc = self.entry_TenNCC.get()
        diachi_ncc = self.entry_DiaChi.get()
        sdt = self.entry_SDT.get()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn nhà cung cấp để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        if ma_ncc == "" or ten_ncc == "" or diachi_ncc == "" or sdt =="" :
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        for i in sdt:
            if ord(i)<48 or ord(i)>57:
                messagebox.showinfo("Thông báo","Sai định dạng số điện thoại!")
                return 
        values = tree.item(selected)["values"]
        tree.item(selected, values=(
        ma_ncc, ten_ncc, sdt, diachi_ncc))
    def luu_ncc(self):
        tree=self.tree
        for i in tree.get_children():
            ma_ncc = tree.item(i)["values"][0]
            ten_ncc = tree.item(i)["values"][1]
            diachi_ncc = tree.item(i)["values"][3]
            sdt = "0"+str(tree.item(i)["values"][2])
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE NhaCungCap SET tenncc=?, sodienthoaincc=?, diachincc=? WHERE manhacungcap=?",
        ( ten_ncc, sdt, diachi_ncc,ma_ncc))
            conn.commit()
            conn.close()
        messagebox.showinfo("Thông báo","Lưu thành công")
    def huy_input(self):
        self.entry_MaNCC.config(state="normal")
        self.entry_MaNCC.delete(0, tk.END)
        self.entry_TenNCC.delete(0, tk.END)
        self.entry_SDT.delete(0, tk.END)
        self.entry_DiaChi.delete(0, tk.END)
        self.entry_SDTtimkiem.delete(0,tk.END)
        self.load_data()
         
