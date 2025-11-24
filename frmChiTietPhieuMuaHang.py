import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import frmThuoc as t
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

def getdata_loaithuoc():
    loaithuoc=[]
    getloaithuoc=connect_db()
    cursor=getloaithuoc.cursor()
    sql_query = "SELECT tenloaithuoc FROM loaithuoc"
    cursor.execute(sql_query)
    for row in cursor.fetchall():
        loaithuoc.append(row[0])
    cursor.close()
    getloaithuoc.close()
    return loaithuoc
def getdata_tenthuoc():
    tenthuoc=[]
    gettenthuoc=connect_db()
    cursor=gettenthuoc.cursor()
    sql_query = "SELECT tenthuoc FROM thuoc"
    cursor.execute(sql_query)
    for row in cursor.fetchall():
            tenthuoc.append(row[0])
    cursor.close()
    gettenthuoc.close()
    return tenthuoc
class CTPMH(tk.Toplevel):
    def __init__(self,master,maphieu,main):
        tk.Toplevel.__init__(self,master)
        self.thuoc_frame=main
        center_window(self,600,450)
        self.title("Chi tiết phiếu mua hàng")
        self.selected_loaithuoc=tk.StringVar()
        self.selected_tenthuoc=tk.StringVar()
        lbl_title = tk.Label(self, text="CHI TIẾT PHIẾU MUA HÀNG", font=("Arial", 18, "bold"))
        lbl_title.pack(pady=10)
        frame_info=tk.Frame(self)
        frame_info.pack(pady=10)
        tk.Label(frame_info,text="Mã phiếu mua hàng").grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.entry_maphieu=tk.Entry(frame_info,width=25)
        self.entry_maphieu.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        self.entry_maphieu.config(state="normal")
        self.entry_maphieu.delete(0,tk.END)
        self.entry_maphieu.insert(0,str(maphieu))
        self.entry_maphieu.config(state="readonly")

        tk.Label(frame_info,text="Loại thuốc").grid(row=0,column=2,padx=5,pady=5,sticky="w")
        self.cbb_loaithuoc=ttk.Combobox(frame_info,textvariable=self.selected_loaithuoc,values=getdata_loaithuoc(),width=20)
        self.cbb_loaithuoc.grid(row=0,column=3,padx=5,pady=5,sticky="w")
        self.cbb_loaithuoc.bind("<<ComboboxSelected>>",self.update_tenthuoc)

        tk.Label(frame_info,text="Tên thuốc").grid(row=1,column=0,padx=5,pady=5,sticky="w")
        self.cbb_tenthuoc=ttk.Combobox(frame_info,textvariable=self.selected_tenthuoc,width=20)
        self.cbb_tenthuoc.grid(row=1,column=1,padx=5,pady=5,sticky="w")
        self.cbb_tenthuoc.bind("<<ComboboxSelected>>",self.update_giaban)

        tk.Label(frame_info,text="Giá bán").grid(row=1,column=2,padx=5,pady=5,sticky="w")
        self.entry_giaban=tk.Entry(frame_info,width=25)
        self.entry_giaban.grid(row=1,column=3,padx=5,pady=5,sticky="w")

        tk.Label(frame_info,text="Số lượng").grid(row=2,column=0,padx=5,pady=5,sticky="w")
        self.entry_soluong=tk.Entry(frame_info,width=25)
        self.entry_soluong.grid(row=2,column=1,padx=5,pady=5,sticky="w")

        tk.Label(frame_info,text="Đơn vị").grid(row=2,column=2,padx=5,pady=5,sticky="w")
        self.entry_donvi=tk.Entry(frame_info,width=25)
        self.entry_donvi.grid(row=2,column=3,padx=5,pady=5,sticky="w")

        tk.Label(frame_info,text="Giảm giá(%)").grid(row=3,column=0,padx=5,pady=5,sticky="w")
        self.entry_giamgia=tk.Entry(frame_info,width=25)
        self.entry_giamgia.grid(row=3,column=1,padx=5,pady=5,sticky="w")
        self.entry_giamgia.insert(0,'0')

        frame_button=tk.Frame(self)
        frame_button.pack(pady=10)

        self.btnThem=tk.Button(frame_button,text="Thêm",width=8,command=self.Them).grid(row=0,column=0)
        self.btnXoa=tk.Button(frame_button,text="Xóa",width=8,command=self.Xoa).grid(row=0,column=1)
        self.btnSua=tk.Button(frame_button,text="Sửa",width=8,command=self.Sua).grid(row=0,column=2)
        self.btnHuy=tk.Button(frame_button,text="Hủy",width=8,command=self.Huy).grid(row=0,column=3)
        self.btnThoat=tk.Button(frame_button,text="Thoát",width=8,command=self.Thoat).grid(row=0,column=4)
        self.protocol("WM_DELETE_WINDOW", self.Thoat)
        frame_chucnang=tk.Frame(self)
        frame_chucnang.pack(pady=10)

        tk.Label(frame_chucnang,text="Tổng tiền: ",bg="yellow").grid(row=0,column=0,padx=10,pady=5,sticky="w")
        self.entry_tongtien=tk.Entry(frame_chucnang,width=20)
        self.entry_tongtien.grid(row=0,column=1,padx=5,pady=5,sticky="w")
        self.entry_tongtien.insert(0,0)

        btnThanhToan=tk.Button(frame_chucnang,text="Thanh toán",width=20,command=self.ThanhToan).grid(row=0,column=2,padx=10,pady=5)
  
        lbl_ds = tk.Label(self, text="Danh sách thuốc nông dược", font=("Arial", 10, "bold"))
        lbl_ds.pack(pady=5, anchor="w", padx=10)
        columns = ("STT","Mã phiếu", "Mã thuốc", "Tên thuốc", "Số lượng","Đơn vị", "Giá bán","Giảm giá", "Thành tiền")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        tree=self.tree
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.column("STT", width=30, anchor="center")
        tree.column("Mã phiếu", width=30, anchor="center")
        tree.column("Mã thuốc", width=50, anchor="center")
        tree.column("Tên thuốc", width=100, anchor="center")
        tree.column("Số lượng", width=50, anchor="center")
        tree.column("Đơn vị",width=20,anchor="center")
        tree.column("Giá bán", width=100, anchor="center")
        tree.column("Giảm giá", width=50, anchor="center")
        tree.column("Thành tiền", width=80, anchor="center")
        tree.bind("<<TreeviewSelect>>", self.select_record)
        tree.pack(padx=10, pady=5, fill="both")
        self.check_thanhtoan=0
        self.load_data()
    def select_record(self,event):
      conn = connect_db()
      cur = conn.cursor()
      selected = self.tree.selection()
      if not selected:
         return
      values = self.tree.item(selected)["values"]
      self.cbb_tenthuoc.set(values[3])
      sql_loaithuoc = "select l.TenLoaiThuoc from thuoc t,loaithuoc l where t.Malt=l.MaLT and Tenthuoc = ?"
      cur.execute(sql_loaithuoc, (values[3],))
      loaithuoc_result = cur.fetchone()
      loaithuoc = loaithuoc_result[0] if loaithuoc_result else None

      self.cbb_loaithuoc.set(loaithuoc)
      self.entry_giaban.delete(0,tk.END)
      self.entry_giaban.insert(0,values[6])
      self.entry_soluong.delete(0,tk.END)
      self.entry_soluong.insert(0,values[4])
      self.entry_donvi.delete(0,tk.END)
      self.entry_donvi.insert(0,values[5])
      self.entry_giamgia.delete(0,tk.END)
      self.entry_giamgia.insert(0,values[7])

    def Huy(self):
      self.cbb_loaithuoc.set("")
      self.cbb_tenthuoc.set("")
      self.entry_giaban.delete(0,tk.END)
      self.entry_soluong.delete(0,tk.END)
      self.entry_donvi.delete(0,tk.END)
      self.entry_giamgia.delete(0,tk.END)
    def load_data(self):
        tree=self.tree
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        sql_query = ("select c.stt,c.sophieumuahang,t.MaThuoc,t.tenthuoc,c.SoLuong,d.tendonvi,t.GiaBan,c.GiamGia,c.ThanhTien "
                    +"from thuoc t, chitietphieumuahang c,donvitinh d "
                    +"where t.mathuoc=c.mathuoc and t.madvt=d.madvt and sophieumuahang=? order by c.stt ASC")
        maphieu=self.entry_maphieu.get()
        cur.execute(sql_query,(maphieu,))
        for row in cur.fetchall():
         vals = tuple(row)
         tree.insert("", tk.END, values=vals)
        conn.close()
    def Them(self):
        conn = connect_db()
        cur = conn.cursor()
        maphieu=self.entry_maphieu.get()
        loaithuoc=self.cbb_loaithuoc.get()
        tenthuoc=self.cbb_tenthuoc.get()
        sql_thuoc = "SELECT Mathuoc,soluongton FROM thuoc WHERE Tenthuoc = ?"
        cur.execute(sql_thuoc, (tenthuoc))
        thuoc_result = cur.fetchone()
        mathuoc = thuoc_result[0] if thuoc_result else None
        soluongton=thuoc_result[1] if thuoc_result else None
        soluong=self.entry_soluong.get()
        donvi=self.entry_donvi.get()
        giaban=self.entry_giaban.get()
        giamgia=self.entry_giamgia.get()
        tree=self.tree
        stt=len(tree.get_children())+1
        for i in tree.get_children():
            if  mathuoc==str(tree.item(i)["values"][2]):
                messagebox.showwarning("Trùng mã", "Thuôc nông dược đã có trong đơn hàng")
                return
        if int(soluongton)<int(soluong):
                messagebox.showinfo("Thông báo",tenthuoc+" không đủ số lượng")
                return
        if int(giamgia)<0 or int(giamgia)>50:
            messagebox.showinfo("Chỉ có thể giảm từ 0-50%")
            return 
        if int(soluong)<0:
            messagebox.showinfo("Số lượng không được âm")
            return
        if loaithuoc == "" or mathuoc == "" or tenthuoc== "" or giaban=="" or soluong=="" or donvi=="" or giamgia=="":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        if int(giamgia)>0:
            thanhtien=int(giaban)*int(soluong)*((100-int(giamgia))/100)
        else:
            thanhtien=int(giaban)*int(soluong)
        tongtien=0
        tongtien=int(self.entry_tongtien.get())+thanhtien
        self.entry_tongtien.delete(0,tk.END)
        self.entry_tongtien.insert(0,tongtien)
        try:
            cur.execute("INSERT INTO chitietphieumuahang VALUES (?,?,?,?,?,?)",
            (maphieu, mathuoc, soluong,giamgia,thanhtien,stt))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()   
        self.load_data()
        self.Huy()
        self.entry_giamgia.insert(0,0)
    def Xoa(self):
        tree=self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn thuốc để xóa")
            return
        stt=int(tree.item(selected)["values"][0])
        maphieu= tree.item(selected)["values"][1]
        mathuoc=tree.item(selected)["values"][2]
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM chitietphieumuahang WHERE mathuoc=? and sophieumuahang=?", (mathuoc,maphieu,))
        conn.commit() 
        sql_update_stt = "UPDATE chitietphieumuahang SET stt = stt - 1 WHERE sophieumuahang = ? AND stt > ?"
        cur.execute(sql_update_stt, (maphieu, stt))
        conn.commit()
        thanhtien=tree.item(selected)["values"][8]
        tongtien=int(self.entry_tongtien.get())-thanhtien
        self.entry_tongtien.delete(0,tk.END)
        self.entry_tongtien.insert(0,tongtien)
        messagebox.showinfo("Xóa thành công", "Đã xóa thuốc")
        conn.close()
        self.load_data()
    def Sua(self):
        conn = connect_db()
        cur = conn.cursor()
        tree = self.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn thuốc để sửa")
            return
        values = tree.item(selected)["values"]
        stt = values[0]
        maphieu=self.entry_maphieu.get()
        loaithuoc = self.cbb_loaithuoc.get()
        tenthuoc = self.cbb_tenthuoc.get()
        sql_mathuoc = "SELECT Mathuoc FROM thuoc WHERE Tenthuoc = ?"
        cur.execute(sql_mathuoc, (tenthuoc,))
        mathuoc_result = cur.fetchone()
        mathuoc = mathuoc_result[0] if mathuoc_result else None
        soluong = self.entry_soluong.get()
        donvi=self.entry_donvi.get()
        giaban = self.entry_giaban.get()
        giamgia = self.entry_giamgia.get()
        if loaithuoc == ""  or tenthuoc== "" or giaban=="" or soluong=="" or donvi=="" or giamgia=="":
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return
        sql_thuoc = "SELECT soluongton FROM thuoc WHERE Tenthuoc = ?"
        cur.execute(sql_thuoc, (tenthuoc))
        thuoc_result = cur.fetchone()
        soluongton=thuoc_result[0] if thuoc_result else None
        if int(soluongton)<int(soluong):
                messagebox.showinfo("Thông báo",tenthuoc+" không đủ số lượng")
                return
        if int(giamgia)==0:
            thanhtien = int(giaban)*int(soluong)
        elif int(giamgia)<0 or int(giamgia)>50:
            messagebox.showwarning("Cảnh báo","Giảm giá không thể nhỏ hơn 0% và không quá 50%")
            return
        else:
            thanhtien = int(giaban)*int(soluong)*((100-int(giamgia))/100)

        tree=self.tree
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn phiếu mua hàng để sửa")
            return
        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Lỗi", "Không thể lấy dữ liệu từ dòng đã chọn.")
            return
        values = tree.item(selected)["values"]
        tree.item(selected, values=(stt,maphieu, mathuoc, tenthuoc,soluong,donvi, giaban, giamgia, thanhtien))
        tongtien=0
        for i in tree.get_children():
            tongtien=tongtien + float(tree.item(i)["values"][8])
        self.entry_tongtien.delete(0,tk.END)
        self.entry_tongtien.insert(0,tongtien)
    def Luu(self):
        tree = self.tree
        conn = connect_db()
        cur = conn.cursor()
        maphieu = self.entry_maphieu.get()
        for i in tree.get_children():
            stt=tree.item(i)["values"][0]
            mathuoc=tree.item(i)["values"][2]
            soluong=tree.item(i)["values"][4]
            giamgia=tree.item(i)["values"][7]
            thanhtien=float(tree.item(i)["values"][8])
            cur.execute("UPDATE chitietphieumuahang SET soluong=?, giamgia=?, thanhtien=?,stt=?  WHERE sophieumuahang=? and mathuoc=?",
                (soluong,giamgia,thanhtien,stt,maphieu,mathuoc))
        conn.commit()
        tongtien=float(self.entry_tongtien.get())
        cur.execute("update phieumuahang set tongtien=? where sophieumuahang=?",(tongtien,maphieu,))
        conn.commit()
        stt=len(tree.get_children())+1
        conn.close()
    def update_giaban(self, event):
        tenthuoc_chon = self.selected_tenthuoc.get() 
        giaban = None
        if tenthuoc_chon:
            conn = connect_db()
            cur = conn.cursor()
            try:
                sql_giaban = "SELECT giaban FROM thuoc WHERE Tenthuoc = ?"
                cur.execute(sql_giaban, (tenthuoc_chon,))
                giaban_result = cur.fetchone()
                if giaban_result:
                    giaban = giaban_result[0]
                sql_donvi="select tendonvi from thuoc t, donvitinh d where t.madvt=d.madvt and tenthuoc=?"
                cur.execute(sql_donvi,(tenthuoc_chon,))
                donvi_result=cur.fetchone()
                donvi=donvi_result[0] if donvi_result else None
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                messagebox.showerror("Lỗi CSDL", f"Đã xảy ra lỗi khi truy vấn Mã NV: {sqlstate}")
            finally:
                cur.close()
                conn.close()
        self.entry_giaban.delete(0, tk.END)
        self.entry_donvi.delete(0,tk.END)
        if giaban:
            self.entry_giaban.insert(0, giaban)
        else:
            pass 
        if donvi:
            self.entry_donvi.insert(0,donvi)
        else:
            pass
    def update_tenthuoc(self,event):
        loaithuoc_chon=self.selected_loaithuoc.get()
        tenthuoc=[]
        gettenthuoc=connect_db()
        cursor=gettenthuoc.cursor()
        sql_malt = "select malt from loaithuoc where Tenloaithuoc = ?"
        cursor.execute(sql_malt, (loaithuoc_chon,))
        malt_result = cursor.fetchone()
        malt = malt_result[0] if malt_result else None
        sql_query = "SELECT tenthuoc FROM thuoc where malt=?"
        cursor.execute(sql_query,(malt,))
        for row in cursor.fetchall():
            tenthuoc.append(row[0])
        cursor.close()
        gettenthuoc.close()
        self.cbb_tenthuoc.set('') 
        self.cbb_tenthuoc['values']=tenthuoc
        self.entry_giaban.delete(0, tk.END)
    def ThanhToan(self):
        conn = connect_db()
        cur = conn.cursor()
        maphieu=int(self.entry_maphieu.get())
        self.Luu()
        cur.execute("UPDATE thuoc"
                    +" SET SoLuongTon = SoLuongTon - ("
                    +" SELECT ct.SoLuong"
                    +" FROM chitietphieumuahang ct"
                    +" WHERE ct.MaThuoc = thuoc.MaThuoc"
                    +" AND ct.SoPhieuMuaHang = ?)"
                    +" WHERE MaThuoc IN ("
                    +" SELECT DISTINCT MaThuoc"
                    +" FROM chitietphieumuahang"
                    +" WHERE SoPhieuMuaHang = ?);",(maphieu,maphieu,))
        messagebox.showinfo("Thông báo","Thanh toán thành công!")
        self.check_thanhtoan=1
        conn.commit()
        thuoc_instance = self.thuoc_frame
        thuoc_instance.load_data()
        self.destroy()
    def Thoat(self):
        conn = connect_db()
        cur = conn.cursor()
        if self.check_thanhtoan==0:
            r=messagebox.askyesno("Cảnh báo","Bạn cần nhấn thanh toán trước khi thoát! Nếu thoát ngay lúc này đơn hàng sẽ bị hủy! Bạn có thật sự muốn thoát?")
            if r==False:
                return
        maphieu=int(self.entry_maphieu.get())
        sql_delete="delete from chitietphieumuahang where sophieumuahang=?"
        cur.execute(sql_delete,(maphieu,))
        conn.commit()
        conn.close()
        self.destroy()


   
        
        

   





        





