import xmlrpc.client
import os

s = xmlrpc.client.ServerProxy('http://127.0.0.1:8000', allow_none=True)

def clearScreen():
    os.system("cls")

def mainMenu():
    clearScreen()
    print("======> Activity Logging\n")
    print("Opsi:")
    print("1. Input Aktivitas")
    print("2. Cek Log")
    print("0. Exit")
    return input("Input nomor menu: ")

def inputMenu():
    clearScreen()
    print("======> Input Aktivitas\n")
    data = input("Input nama aktivitas: ")
    s.input_activity(data)
    print("Data berhasil dimasukkan")

def logMenu():
    clearScreen()
    menuHeader = "======> Cek Log\n"
    print(menuHeader)
    print("1. Cek Semua Log")
    print("2. Cek Berdasar Waktu")
    menu = input("Input nomor menu: ")

    if menu == "1":
        clearScreen()
        print(menuHeader)
        print(s.get_log())

    if menu == "2":
        clearScreen()
        print(menuHeader)
        print("Format tanggal: YYYY-MM-DD, contoh: 2021-1-30")
        print("Format waktu: hh:mm:ss contoh: 3:30:0\n")
        dataDate = input("Input tanggal: ")
        dataTime = input("Input waktu, tekan enter untuk mengosongkan waktu: ")

        clearScreen()
        print(menuHeader)
        print("\nMenampilkan log dari tanggal & waktu inputan hingga saat ini...\n")
        print(s.get_log(dataDate,dataTime))

while True:
    menu = mainMenu()

    if menu == "1":
        inputMenu()
        input("Tekan enter untuk kembali ke menu utama")
        continue

    if menu == "2":
        logMenu()
        input("Tekan enter untuk kembali ke menu utama")
        continue

    if menu == "0":
        clearScreen()
        break