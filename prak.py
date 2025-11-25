import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk
import sqlite3


def koneksi():
    con = sqlite3.connect("database.db")
    return con

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            bahasa INTEGER,
            prediksi TEXT
        )
    """)
    con.commit()
    con.close()

def prediksi_jurusan(biologi, fisika, bahasa):
    if biologi >= fisika and biologi >= bahasa:
        return "Kedokteran"
    elif fisika >= biologi and fisika >= bahasa:
        return "Teknik"
    else:
        return "Bahasa"

def insertsiswa(name: str, biologi: int, fisika: int, bahasa: int) -> int:
    jurusan = prediksi_jurusan(biologi, fisika, bahasa)
    con = koneksi()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO students (name, biologi, fisika, bahasa, prediksi) VALUES (?, ?, ?, ?, ?)",
        (name, biologi, fisika, bahasa, jurusan)
    )
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid

def readsiswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, name, biologi, fisika, bahasa, prediksi FROM students ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

def updatedata(id: int, name: str, biologi: int, fisika: int, bahasa: int):
    con = koneksi()
    cur = con.cursor()
    hasil = prediksi_jurusan(biologi, fisika, bahasa)
    cur.execute("""
        UPDATE students
        SET name = ?, biologi = ?, fisika = ?, bahasa = ?, prediksi = ?
        WHERE id = ?
    """, (name, biologi, fisika, bahasa, hasil, id))
    con.commit()
    con.close()

def deletenilai(id: int):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (id,))
    con.commit()
    con.close()


create_table()

class Nilai(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Nilai Siswa")
        self.geometry("600x420")
        self.configure(bg="white")

        self.selected_id = None

        frm = tk.Frame(self, bg="lightblue", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        tk.Label(frm, text="Nama:", bg="lightblue").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(frm, width=30)
        self.ent_name.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Biologi:", bg="lightblue").grid(row=1, column=0, sticky="w")
        self.ent_biologi = tk.Entry(frm, width=30)
        self.ent_biologi.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Fisika:", bg="lightblue").grid(row=2, column=0, sticky="w")
        self.ent_fisika = tk.Entry(frm, width=30)
        self.ent_fisika.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Bahasa:", bg="lightblue").grid(row=3, column=0, sticky="w")
        self.ent_bahasa = tk.Entry(frm, width=30)
        self.ent_bahasa.grid(row=3, column=1, sticky="w", padx=6, pady=6)

        btn_frame = tk.Frame(frm, bg="lightblue")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(6, 0))

        # tombol-tombol
        self.btn_add = tk.Button(btn_frame, text="Submit", width=10, command=self.insertdata)
        self.btn_add.pack(side="right", padx=6)

        self.btn_update = tk.Button(btn_frame, text="Update", width=10, command=self.updatedata_gui)
        self.btn_update.pack(side="right", padx=6)

        self.btn_delete = tk.Button(btn_frame, text="Delete", width=10, command=self.deletedata_gui)
        self.btn_delete.pack(side="right", padx=6)

        self.btn_refresh = tk.Button(btn_frame, text="Refresh", width=10, command=self.read_data)
        self.btn_refresh.pack(side="right", padx=6)

        cols = ("id", "name", "biologi", "fisika", "bahasa", "prediksi")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        self.tree.heading("name", text="Nama")
        self.tree.column("name", width=350)
        self.tree.heading("biologi", text="Biologi")
        self.tree.column("biologi", width=40, anchor="center")
        self.tree.heading("fisika", text="Fisika")
        self.tree.column("fisika", width=40, anchor="center")
        self.tree.heading("bahasa", text="Bahasa")
        self.tree.column("bahasa", width=40, anchor="center")
        self.tree.heading("prediksi", text="Prediksi Fakultas")
        self.tree.column("prediksi", width=120, anchor="center")
        self.tree.pack(padx=16, pady=(0, 12), fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.read_data()

    def clear_inputs(self):
        self.ent_name.delete(0, tk.END)
        self.ent_biologi.delete(0, tk.END)
        self.ent_fisika.delete(0, tk.END)
        self.ent_bahasa.delete(0, tk.END)

    def validate_inputs(self):
        name = self.ent_name.get().strip()
        biologi_str = self.ent_biologi.get().strip()
        fisika_str = self.ent_fisika.get().strip()
        bahasa_str = self.ent_bahasa.get().strip()
        if not name or not biologi_str or not fisika_str or not bahasa_str:
            msg.showwarning("Peringatan", "Nama dan nilai-nilai tidak boleh kosong.")
            return None
        try:
            biologi = int(biologi_str)
            fisika = int(fisika_str)
            bahasa = int(bahasa_str)
            if biologi < 0 or fisika < 0 or bahasa < 0:
                raise ValueError
        except ValueError:
            msg.showerror("Salah", "Nilai harus bilangan bulat >= 0.")
            return None
        return name, biologi, fisika, bahasa

    def insertdata(self):
        val = self.validate_inputs()
        if not val:
            return
        name, biologi, fisika, bahasa = val
        try:
            new_id = insertsiswa(name, biologi, fisika, bahasa)
            msg.showinfo("Sukses", f"Data disimpan (id={new_id}).")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))

    def on_tree_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        id_val, name, biologi, fisika, bahasa, _ = item["values"]
        self.selected_id = id_val

        self.clear_inputs()

        self.ent_name.insert(0, name)
        self.ent_biologi.insert(0, str(biologi))
        self.ent_fisika.insert(0, str(fisika))
        self.ent_bahasa.insert(0, str(bahasa))

    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = readsiswa()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))


    def updatedata_gui(self):
        if self.selected_id is None:
            msg.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu.")
            return

        val = self.validate_inputs()
        if not val:
            return

        name, biologi, fisika, bahasa = val
        try:
            updatedata(self.selected_id, name, biologi, fisika, bahasa)
            msg.showinfo("Sukses", "Data berhasil diupdate.")
            self.read_data()
            self.clear_inputs()
            self.selected_id = None
        except Exception as e:
            msg.showerror("DB Error", str(e))

    def deletedata_gui(self):
        if self.selected_id is None:
            msg.showwarning("Peringatan", "Pilih data yang ingin dihapus.")
            return

        jawab = msg.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?")
        if not jawab:
            return

        try:
            deletenilai(self.selected_id)
            msg.showinfo("Sukses", "Data berhasil dihapus.")
            self.read_data()
            self.clear_inputs()
            self.selected_id = None
        except Exception as e:
            msg.showerror("DB Error", str(e))


if __name__ == "__main__":
    app = Nilai()
    app.mainloop()
