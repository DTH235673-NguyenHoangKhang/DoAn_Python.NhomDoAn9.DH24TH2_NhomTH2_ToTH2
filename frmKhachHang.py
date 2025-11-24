import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import frmXacNhan as x
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
class KhachHang(tk.Toplevel):
    def __init__(self,master):
        tk.Toplevel.__init__(self,master)
        self.title("Quản Lí Khách Hàng")
        center_window(self, 700, 450) 
        tk.Label(self, text="Danh Sách Khách Hàng", font=("Arial", 16, "bold")).pack(pady=10)
        self.create_widgets()
    def create_widgets(self):
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Mã Khách Hàng:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_MaKH = tk.Entry(form_frame)
        self.entry_MaKH.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tên Khách Hàng:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_TenKH = tk.Entry(form_frame)
        self.entry_TenKH.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Số điện thoại").grid(row=1, column=2, padx=5, pady=5)
        self.entry_SDT = tk.Entry(form_frame)
        self.entry_SDT.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Địa Chỉ:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_DiaChi = tk.Entry(form_frame)
        self.entry_DiaChi.grid(row=0, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btnThem = tk.Button(btn_frame, text="Thêm", width=10, command=self.them_kh)
        self.btnThem.grid(row=0, column=0, padx=10)

        self.btnSua = tk.Button(btn_frame, text="Sửa", width=10, command=self.sua_kh)
        self.btnSua.grid(row=0, column=1, padx=10)

        self.btnXoa = tk.Button(btn_frame, text="Xóa", width=10, command=self.xoa_kh)
        self.btnXoa.grid(row=0, column=2, padx=10)

        self.btnLuu = tk.Button(btn_frame, text="Lưu", width=10, command=self.luu_kh)
        self.btnLuu.grid(row=0, column=3, padx=10)

        self.btnHuy = tk.Button(btn_frame, text="Hủy", width=10, command=self.huy_input)
        self.btnHuy.grid(row=0, column=4, padx=10)

        self.btnThoat = tk.Button(btn_frame, text="Thoát", width=10, command=self.destroy)
        self.btnThoat.grid(row=0, column=5, padx=10)

        frame_timkiem=tk.Frame(self)
        frame_timkiem.pack(pady=5)
        tk.Label(frame_timkiem,text="Nhập SDT khách hàng cần tìm: ").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_SDTtimkiem=tk.Entry(frame_timkiem,width=15)
        self.entry_SDTtimkiem.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        btnTimKiem=tk.Button(frame_timkiem,text="Tìm khách hàng",width=15,command=self.Tim).grid(row=0,column=2,padx=5,pady=5)
    
        lbl_ds = tk.Label(self, text="Danh sách khách hàng", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w", padx=10)
        columns = ("Mã khách hàng", "Tên khách hàng", "Số Điện Thoại KH", "Địa chỉ KH" )
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("Mã khách hàng", width=60, anchor="center")
        tree.column("Tên khách hàng", width=80, anchor="center")
        tree.column("Số Điện Thoại KH", width=70, anchor="center")
        tree.column("Địa chỉ KH", width=100, anchor="center")
        tree.bind("<<TreeviewSelect>>", self.select_record)
        tree.pack(padx=10, pady=5, fill="both")
        self.load_data()
    def Tim(self):
        matim=self.entry_SDTtimkiem.get()
        if matim=="":
            messagebox.showinfo("Thông báo","Vui lòng nhập số điện thoại khách hàng cần tìm")
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
        self.entry_MaKH.config(state="normal")
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.entry_MaKH.delete(0, tk.END)
            self.entry_MaKH.insert(0, values[0])
            self.entry_TenKH.delete(0, tk.END)
            self.entry_TenKH.insert(0, values[1])
            self.entry_SDT.delete(0, tk.END)
            self.entry_SDT.insert(0, values[2])
            self.entry_DiaChi.delete(0, tk.END)
            self.entry_DiaChi.insert(0, values[3])
        self.entry_MaKH.config(state="readonly")
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = ("select * from KhachHang where tinhtrang=1")        
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def them_kh(self):
        conn = connect_db()
        cur = conn.cursor()
        ma_kh = self.entry_MaKH.get()
        ten_kh = self.entry_TenKH.get()
        diachi_kh = self.entry_DiaChi.get()
        sdt_kh = self.entry_SDT.get()
        tree=self.tree
        if ma_kh == "" or ten_kh == "" or sdt_kh =="" or diachi_kh =="":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
            return
        if ma_kh[0]!='K' or ma_kh[1]!='H'  or len(ma_kh)!=4:
                messagebox.showinfo("Thông báo","Sai định dạng mã khách háng (KH00)")
                return
        for i in range(2, len(ma_kh)):
            if not ma_kh[i].isdigit(): 
                messagebox.showinfo("Thông báo","Sai định dạng mã khách hàng (KH00)")
                return
        for i in sdt_kh:
            if ord(i)<48 or ord(i)>57:
                messagebox.showinfo("Thông báo","Sai định dạng số điện thoại!")
                return         
        cur.execute("select tinhtrang from khachhang where makh=?",(ma_kh,))
        result=cur.fetchone()
        if result:
            t=result[0]
            if t==1:
                messagebox.showwarning("Trùng mã", "Mã khách hàng đã tồn tại")
                return
            elif t==0:
                cur.execute("update khachhang set tinhtrang=1,tenkh=?,diachikh=?,sodienthoaikh=? where makh=?",
                            (ten_kh,diachi_kh,sdt_kh,ma_kh,))
                conn.commit()
                self.load_data()               
                return
        try:
            cur.execute("INSERT INTO KhachHang VALUES (?,?,?,?,?)",
            (ma_kh, ten_kh, sdt_kh, diachi_kh,1))
            conn.commit()
            self.load_data()
            self.huy_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()
    def xoa_kh(self):
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn khách hàng để xóa")
            return
        ma_kh = tree.item(selected)["values"][0]
        conn = connect_db()
        cur = conn.cursor()
        sql_ngaynhap_gannhat = """SELECT MAX(P.Ngaymuahang) FROM PhieuMuaHang P WHERE p.makh= ?"""
        cur.execute(sql_ngaynhap_gannhat,(ma_kh,))
        ngaynhap=cur.fetchone()
        ngay_giao_dich_gannhat=ngaynhap[0]
        ngay_hien_tai = datetime.now().date() 
        ngay_gioi_han = ngay_hien_tai - timedelta(days=180)
        if ngay_giao_dich_gannhat:
            if isinstance(ngay_giao_dich_gannhat, datetime):
                ngay_giao_dich_gannhat = ngay_giao_dich_gannhat.date() 
            if ngay_giao_dich_gannhat > ngay_gioi_han:
                messagebox.showwarning("""Không thể xóa", f"Khách hàng có giao dịch gần nhất vào ngày: 
                {ngay_giao_dich_gannhat}. Phải hơn 6 tháng (180 ngày) không phát sinh giao dịch mới có thể xóa.""")
                return
        cur.execute("update KhachHang set tinhtrang=0 WHERE MaKH=?", (ma_kh,))
        conn.commit() 
        messagebox.showinfo("Xóa thành công", "Xóa khách hàng?")
        conn.close()
        self.load_data()  
    def sua_kh(self):
        tree=self.tree
        selected = tree.focus()
        ma_kh = self.entry_MaKH.get()
        ten_kh = self.entry_TenKH.get()
        diachi_kh = self.entry_DiaChi.get()
        sdt_kh = self.entry_SDT.get()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn khách hàng để sửa")
            return
        for i in sdt_kh:
            if ord(i)<48 or ord(i)>57:
                messagebox.showinfo("Thông báo","Sai định dạng số điện thoại!")
                return   
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        if ma_kh == "" or ten_kh == "" or sdt_kh =="" or diachi_kh =="":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
            return
        tree.item(selected, values=(ma_kh, ten_kh, sdt_kh, diachi_kh))
    def luu_kh(self):
        tree=self.tree
        for i in tree.get_children():
            ma_kh = tree.item(i)["values"][0]
            ten_kh = tree.item(i)["values"][1]
            diachi_kh = tree.item(i)["values"][3]
            sdt_kh = "0"+str(tree.item(i)["values"][2])
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE KhachHang SET tenkh=?, diachikh=?, sodienthoaikh=? WHERE makh=?",
        (ten_kh, diachi_kh,sdt_kh, ma_kh))
            conn.commit()
            conn.close()
        messagebox.showinfo("Thông báo","Lưu thành công")
    def huy_input(self):
        self.entry_MaKH.config(state="normal")
        self.entry_MaKH.delete(0, tk.END)
        self.entry_TenKH.delete(0, tk.END)
        self.entry_SDT.delete(0, tk.END)
        self.entry_DiaChi.delete(0, tk.END)
        self.entry_SDTtimkiem.delete(0,tk.END)
        self.load_data()

    


