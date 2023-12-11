from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def veri_silme_ekrani():
    class VeriSilmeAramaEkrani:
        def __init__(self, master):
            self.master = master
            self.master.title('Katalog: Eserleri Listele ve Sil')
            self.master.geometry('800x600')
            self.master.resizable = True
            self.master['bg'] = 'white'  # Arka plan rengi beyaz

            # Veritabanı bağlantısı ve sorgusu
            self.baglanti = sqlite3.connect("2200396003.db")
            self.sorgu = self.baglanti.cursor()

            # Eser tablosu çerçevesi
            self.eserTabloCercevesi = ttk.Frame(self.master, padding=25)
            self.eserTabloCercevesi.pack()

            self.eserTablosu = ttk.Treeview(self.eserTabloCercevesi,
                                            columns=('eserID', 'eserAdi', 'eserBasim', 'eserURL', 'sil'),
                                            show='headings', selectmode='browse')

            self.eserTablosu.column("eserID", anchor=CENTER, width=50)
            self.eserTablosu.column("eserAdi", anchor=CENTER, width=250)
            self.eserTablosu.column("eserBasim", anchor=CENTER, width=75)
            self.eserTablosu.column("eserURL", anchor=CENTER, width=250)
            self.eserTablosu.column("sil", anchor=CENTER, width=50)

            self.eserTablosu.heading("eserID", text="Eser ID", anchor=CENTER)
            self.eserTablosu.heading("eserAdi", text="Eser Adı", anchor=CENTER)
            self.eserTablosu.heading("eserBasim", text="Eser Basım", anchor=CENTER)
            self.eserTablosu.heading("eserURL", text="Eser URL", anchor=CENTER)
            self.eserTablosu.heading("sil", text="Sil", anchor=CENTER)

            self.eserTablosu.pack()

            self.verileri_guncelle()

            # Eser tablosundan seçilen satırın silinmesi için çöp kutusu simgesine tıklama olayı
            self.eserTablosu.bind("<ButtonRelease-1>", self.satir_sil)

        def verileri_guncelle(self):
            self.eserTablosu.delete(*self.eserTablosu.get_children())

            # İlk sorgunun sonuçlarını ekleyelim
            sonuc = self.sorgu.execute("SELECT * FROM eser")
            for index, eser in enumerate(sonuc.fetchall()):
                self.eserTablosu.insert(parent='', index='end', iid=index, text='',
                                        values=(eser[0], eser[1], eser[2], eser[3], 'Çöp'))

        def satir_sil(self, event):
            item = self.eserTablosu.selection()[0]
            eser_id = self.eserTablosu.item(item, 'values')[0]

            # Eser tablosundan seçilen satırı sil
            self.sorgu.execute("DELETE FROM eser WHERE eserID=?", (eser_id,))
            self.baglanti.commit()

            # Verileri güncelle
            self.verileri_guncelle()

    if __name__ == "__main__":
        root = Tk()
        uygulama = VeriSilmeAramaEkrani(root)
        root.mainloop()


def veri_listeleme_arama_ekrani():
    def arama_yap():
        anahtar = arama_input.get()

        # İkinci sorguyu burada yeniden çalıştırabilirsiniz
        sonuc2 = sorgu2.execute(
            "SELECT * FROM eser WHERE eserAdi LIKE('%{}%') ORDER BY eser DESC".format(anahtar,
                                                                                                              anahtar)
        )
        veriler2 = sonuc2.fetchall()

        # Eski verileri temizle
        for item in eserTablosu.get_children():
            eserTablosu.delete(item)

        # Yeni verileri ekleyin
        for index, eser in enumerate(veriler2):
            eserTablosu.insert(parent='', index='end', iid=index, text='',
                               values=(eser[0], eser[1], eser[2], eser[3]))

    # İlk sorgu
    baglanti1 = sqlite3.connect("2200396003.db")
    sorgu1 = baglanti1.cursor()
    sonuc1 = sorgu1.execute("SELECT * FROM eser")

    # İkinci sorgu
    baglanti2 = sqlite3.connect("data.sqlite3")
    sorgu2 = baglanti2.cursor()

    # Tkinter arayüzü
    pencere = Tk()
    pencere.title('Katalog: Eserleri Listele')
    pencere.geometry('800x600')
    pencere.resizable = True
    pencere['bg'] = '#FBE54E'

    # Eser tablosu çerçevesi
    eserTabloCercevesi = ttk.Frame(pencere, padding=25)
    eserTabloCercevesi.pack()

    eserTablosu = ttk.Treeview(eserTabloCercevesi)

    eserTablosu['columns'] = ('eserID', 'eserAdi', 'eserBasim', 'eserURL')

    eserTablosu.column("#0", width=0, stretch=NO)
    eserTablosu.column("eserID", anchor=CENTER, width=50)
    eserTablosu.column("eserAdi", anchor=CENTER, width=250)
    eserTablosu.column("eserBasim", anchor=CENTER, width=75)
    eserTablosu.column("eserURL", anchor=CENTER, width=250)

    eserTablosu.heading("#0", text="", anchor=CENTER)
    eserTablosu.heading("eserID", text="Eser ID", anchor=CENTER)
    eserTablosu.heading("eserAdi", text="Eser Adı", anchor=CENTER)
    eserTablosu.heading("eserBasim", text="Eser Basım", anchor=CENTER)
    eserTablosu.heading("eserURL", text="Eser URL", anchor=CENTER)

    # İlk sorgunun sonuçlarını ekleyelim
    for index, eser in enumerate(sonuc1.fetchall()):
        eserTablosu.insert(parent='', index='end', iid=index, text='',
                           values=(eser[0], eser[1], eser[2], eser[3]))

    eserTablosu.pack()

    # Arama için giriş kutusu ve buton
    arama_cercevesi = Frame(pencere, pady=10, bg='#FBE54E')
    arama_cercevesi.pack(side=TOP, fill=X)

    arama_input = Entry(arama_cercevesi, width=50)
    arama_input.grid(row=0, column=0, padx=(10, 5))

    arama_buton = Button(arama_cercevesi, text='Ara', command=arama_yap)
    arama_buton.grid(row=0, column=1, padx=(5, 10))

    pencere.mainloop()
def veri_ekleme_ekrani():

    baglanti = sqlite3.connect("2200396003.db")
    sorgu = baglanti.cursor()

    def eserEkle():
        formVeri = (e1.get(), e2.get(), e3.get())
        sorgu.execute("INSERT INTO eser VALUES(NULL,?,?,?)", formVeri)
        baglanti.commit()
        messagebox.showinfo(title="Katalog Bilgi", message="Eser başarıyla eklendi..!")

    def formTemizle():
        e1.delete(0, 'end')
        e2.delete(0, 'end')
        e3.delete(0, 'end')

    pencere = Tk()
    pencere.title('Katalog: Eser Ekle')
    pencere.geometry('300x200')
    pencere.resizable = True
    pencere['bg'] = '#FBE54E'

    eserCercevesi = ttk.Frame(pencere, padding=10)
    eserCercevesi.pack()

    l1 = Label(eserCercevesi, text="Eser Adı")
    l2 = Label(eserCercevesi, text="Eser Basım")
    l3 = Label(eserCercevesi, text="Eser URL")
    l4 = Label(eserCercevesi, text=":")
    l5 = Label(eserCercevesi, text=":")
    l6 = Label(eserCercevesi, text=":")
    e1 = Entry(eserCercevesi, width=25)
    e2 = Entry(eserCercevesi, width=25)
    e3 = Entry(eserCercevesi, width=25)
    b1 = Button(eserCercevesi, text="Yeni Eser Ekle", command=eserEkle)
    b2 = Button(eserCercevesi, text="Temizle", command=formTemizle)

    l1.grid(row=0, column=0, sticky=W, pady=2)
    l4.grid(row=0, column=1, sticky=W, pady=2)
    e1.grid(row=0, column=2, pady=2)
    l2.grid(row=1, column=0, sticky=W, pady=2)
    l5.grid(row=1, column=1, sticky=W, pady=2)
    e2.grid(row=1, column=2, pady=2)
    l3.grid(row=2, column=0, sticky=W, pady=2)
    l6.grid(row=2, column=1, sticky=W, pady=2)
    e3.grid(row=2, column=2, pady=2)
    b1.grid(row=3, column=2, pady=2)
    b2.grid(row=3, columnspan=2, pady=2)

    pencere.mainloop()

def menu_ekrani():
    pencere = Tk()
    pencere.title("Menü")
    pencere.geometry("400x300")
    pencere['bg'] = '#D2B48C'  # Bej rengi arka plan

    hoşgeldiniz_label = Label(pencere, text="Hoşgeldiniz", font=('Arial', 16), bg='#D2B48C')
    hoşgeldiniz_label.pack(pady=20)

    # Veri Silme Butonu
    silme_buton = Button(pencere, text="Veri Silme", bg='white', command=veri_silme_ekrani, font=('Arial', 12))
    silme_buton.pack(pady=10)

    # Veri Listeleme ve Arama Butonu
    listeleme_buton = Button(pencere, text="Veri Listeleme ve Arama", bg='white', command=veri_listeleme_arama_ekrani, font=('Arial', 12))
    listeleme_buton.pack(pady=10)

    # Veri Ekleme Butonu
    ekleme_buton = Button(pencere, text="Veri Ekle", bg='white', command=veri_ekleme_ekrani, font=('Arial', 12))
    ekleme_buton.pack(pady=10)

    pencere.mainloop()

# Menü ekranını çalıştır
menu_ekrani()