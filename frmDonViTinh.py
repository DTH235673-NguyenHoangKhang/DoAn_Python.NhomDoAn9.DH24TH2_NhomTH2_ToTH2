import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
# ====== Kết nối MySQL ======
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
class DonViTinh(tk.Toplevel):
    def __init__(self,master):
        tk.Toplevel.__init__(self,master)
        center_window(self,600,450)
        self.title("Quản Lý Đơn Vị Tính")
        center_window(self, 600, 350) 
        tk.Label(self, text="Đơn Vị Tính", font=("Arial", 16, "bold")).pack(pady=10)
        self.create_widgets()
    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)

        form_frame = tk.Frame(left_frame)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Mã đơn vị tính:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_MaDVT = tk.Entry(form_frame)
        self.entry_MaDVT.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tên đơn vị tính:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_TenDVT = tk.Entry(form_frame)
        self.entry_TenDVT.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=10)

        self.btnThem = tk.Button(btn_frame, text="Thêm", width=10, command=self.them_dvt)
        self.btnThem.grid(row=0, column=0, padx=10, pady=5)

        self.btnSua = tk.Button(btn_frame, text="Sửa", width=10, command=self.sua_dvt)
        self.btnSua.grid(row=0, column=1, padx=10, pady=5)

        self.btnXoa = tk.Button(btn_frame, text="Xóa", width=10, command=self.xoa_dvt)
        self.btnXoa.grid(row=0, column=2, padx=10, pady=5)

        self.btnLuu = tk.Button(btn_frame, text="Lưu", width=10, command=self.luu_dvt)
        self.btnLuu.grid(row=1, column=0, padx=10, pady=10)

        self.btnHuy = tk.Button(btn_frame, text="Hủy", width=10, command=self.huy_input)
        self.btnHuy.grid(row=1, column=1, padx=10, pady=10)

        self.btnThoat = tk.Button(btn_frame, text="Thoát", width=10, command=self.destroy)
        self.btnThoat.grid(row=1, column=2, padx=10, pady=10)

        lbl_ds = tk.Label(right_frame, text="Danh sách đơn vị tính", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w")

        columns = ("Mã đơn vị tính", "Tên đơn vị tính")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.bind("<<TreeviewSelect>>", self.select_record)
        self.tree.pack(fill="both", expand=True)
        self.load_data()
    def select_record(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.entry_MaDVT.delete(0, tk.END)
            self.entry_MaDVT.insert(0, values[0])
            self.entry_TenDVT.delete(0, tk.END)
            self.entry_TenDVT.insert(0, values[1])
        self.entry_MaDVT.config(state="readonly")
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = ("select * from DonViTinh")
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def them_dvt(self):
        ma_dvt = self.entry_MaDVT.get()
        ten_dvt = self.entry_TenDVT.get()
        tree=self.tree
        if ma_dvt == "" or ten_dvt == "":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if ma_dvt[0]!='D' or ma_dvt[1]!='V' or ma_dvt[2]!='T' or len(ma_dvt)!=5:
                messagebox.showinfo("Thông báo","Sai định dạng mã đơn vị tính (DVT00)")
                return
        for i in range(3, len(ma_dvt)):
            if not ma_dvt[i].isdigit(): 
                messagebox.showinfo("Thông báo","Sai định dạng mã đơn vị tính (DVT00)")
                return
        for i in tree.get_children():
            if ma_dvt == tree.item(i)["values"][0]:
                messagebox.showwarning("Trùng mã", "Mã đơn vị tính đã tồn tại")
                return
        
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO DonViTinh VALUES (?,?)",
            (ma_dvt, ten_dvt))
            conn.commit()
            self.load_data()
            self.huy_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()      
    def xoa_dvt(self):
        tree=self.tree
        selected = tree.selection()
        conn = connect_db()
        cur = conn.cursor()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn đơn vị tính để xóa")
            return
        ma_dvt = tree.item(selected)["values"][0]
        cur.execute("select count(*) from thuoc where madvt=?",(ma_dvt,))
        dvt=cur.fetchone()
        count_dvt=dvt[0]
        if count_dvt>0:
            messagebox.showinfo("Thông báo","Không thể xóa do còn thuốc sử dụng đơn vị tính này!")
            return
        cur.execute("DELETE FROM DonViTinh WHERE MaDVT=?", (ma_dvt,))
        conn.commit() 
        messagebox.showinfo("Xóa thành công", "Đã xóa đơn vị tính")
        conn.close()
        self.load_data()  
    def sua_dvt(self):
        tree=self.tree
        selected = tree.focus()
        values = tree.item(selected)["values"]
        ma_dvt = self.entry_MaDVT.get()
        ten_dvt = self.entry_TenDVT.get()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn đơn vị tính để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        if ma_dvt == "" or ten_dvt == "":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        tree.item(selected, values=( ma_dvt, ten_dvt))
    def luu_dvt(self):
        tree=self.tree
        ma_dvt = self.entry_MaDVT.get()
        ten_dvt = self.entry_TenDVT.get()
        conn = connect_db()
        cur = conn.cursor()
        if ma_dvt == "" or ten_dvt == "":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        cur.execute("UPDATE DonViTinh SET tendonvi=? WHERE madvt=?",
        (ten_dvt, ma_dvt))
        conn.commit()
        conn.close()
    def huy_input(self):
        self.entry_MaDVT.config(state="normal")
        self.entry_MaDVT.delete(0, tk.END)
        self.entry_TenDVT.delete(0, tk.END)
        

