import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
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
class LoaiThuoc(tk.Toplevel):
    def __init__(self,master):
        tk.Toplevel.__init__(self,master)
        self.title("Quản Lý Loại Thuốc")
        center_window(self, 600, 350) 
        tk.Label(self, text="Loại Thuốc", font=("Arial", 16, "bold")).pack(pady=10)
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

        tk.Label(form_frame, text="Mã loại thuốc:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_MaLT = tk.Entry(form_frame)
        self.entry_MaLT.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tên loại thuốc:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_TenLT = tk.Entry(form_frame)
        self.entry_TenLT.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=10)

        self.btnThem = tk.Button(btn_frame, text="Thêm", width=10, command=self.them_lt)
        self.btnThem.grid(row=0, column=0, padx=10, pady=5)

        self.btnSua = tk.Button(btn_frame, text="Sửa", width=10, command=self.sua_lt)
        self.btnSua.grid(row=0, column=1, padx=10, pady=5)

        self.btnXoa = tk.Button(btn_frame, text="Xóa", width=10, command=self.xoa_lt)
        self.btnXoa.grid(row=0, column=2, padx=10, pady=5)

        self.btnLuu = tk.Button(btn_frame, text="Lưu", width=10, command=self.luu_lt)
        self.btnLuu.grid(row=1, column=0, padx=10, pady=10)

        self.btnHuy = tk.Button(btn_frame, text="Hủy", width=10, command=self.huy_input)
        self.btnHuy.grid(row=1, column=1, padx=10, pady=10)

        self.btnThoat = tk.Button(btn_frame, text="Thoát", width=10, command=self.destroy)
        self.btnThoat.grid(row=1, column=2, padx=10, pady=10)

        lbl_ds = tk.Label(right_frame, text="Danh sách loại thuốc", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w")

        columns = ("Mã loại thuốc", "Tên loại thuốc")
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
            self.entry_MaLT.delete(0, tk.END)
            self.entry_MaLT.insert(0, values[0])
            self.entry_TenLT.delete(0, tk.END)
            self.entry_TenLT.insert(0, values[1])
        self.entry_MaLT.config(state="readonly")
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = ("select * from LoaiThuoc")
        cur.execute(sql_query)
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def them_lt(self):
        ma_lt = self.entry_MaLT.get()
        ten_lt = self.entry_TenLT.get()
        tree=self.tree
        if ma_lt == "" or ten_lt == "":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if ma_lt[0]!='L' or ma_lt[1]!='T' or len(ma_lt)!=4:
                messagebox.showinfo("Thông báo","Sai định dạng mã loại thuốc (LT00)")
                return
        for i in range(2, len(ma_lt)):
            if not ma_lt[i].isdigit(): 
                messagebox.showinfo("Thông báo","Sai định dạng mã loại thuốc (LT00)")
                return
        for i in tree.get_children():
            if ma_lt == tree.item(i)["values"][0]:
                messagebox.showwarning("Trùng mã", "Mã đơn vị tính đã tồn tại")
                return
            
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO LoaiThuoc VALUES (?,?)",
            (ma_lt, ten_lt))
            conn.commit()
            self.load_data()
            self.huy_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()      
    def xoa_lt(self):
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn loại thuốc để xóa")
            return
        conn = connect_db()
        cur = conn.cursor()
        ma_lt = tree.item(selected)["values"][0]
        cur.execute("select count(*) from thuoc where malt=?",(ma_lt,))
        lt=cur.fetchone()
        count_lt=lt[0]
        if count_lt>0:
            messagebox.showinfo("Thông báo","Không thể xóa do còn loại thuốc này trong kho!")
            return
        cur.execute("DELETE FROM LoaiThuoc WHERE MaLT=?", (ma_lt,))
        conn.commit() 
        messagebox.showinfo("Xóa thành công", "Xóa loại thuốc")
        conn.close()
        self.load_data()  
    def sua_lt(self):
        tree=self.tree
        selected = tree.focus()
        values = tree.item(selected)["values"]
        ma_lt = self.entry_MaLT.get()
        ten_lt = self.entry_TenLT.get()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn loại thuốc để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        if ma_lt == "" or ten_lt == "":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        tree.item(selected, values=(
        ma_lt, ten_lt))
    def luu_lt(self):
        tree=self.tree
        ma_lt = self.entry_MaLT.get()
        ten_lt = self.entry_TenLT.get()
        conn = connect_db()
        cur = conn.cursor()
        if ma_lt == "" or ten_lt == "":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        cur.execute("UPDATE LoaiThuoc SET tenloaithuoc=? WHERE malt=?",
        (ma_lt, ten_lt))
        conn.commit()
        conn.close()
    def huy_input(self):
        self.entry_MaLT.config(state="normal")
        self.entry_MaLT.delete(0, tk.END)
        self.entry_TenLT.delete(0, tk.END)
        

