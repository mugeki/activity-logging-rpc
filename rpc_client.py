import xmlrpc.client
import os
import socket

s = xmlrpc.client.ServerProxy("http://127.0.0.1:8000", allow_none=True)
ip_address = socket.gethostbyname(socket.gethostname())

def clearScreen():
    os.system("cls")

def mainMenu():
    clearScreen()
    print("======> Activity Logging\n")
    print("Opsi:")
    print("1. Input Aktivitas")
    print("2. Cek Log")
    print("0. Logout")
    return input("Input nomor menu: ")

def loginMenu():
    clearScreen()
    print("======> Login\n")
    print("Input 0 to exit\n")
    return input("Input username: ")

def inputMenu(user):
    clearScreen()
    print("======> Input Aktivitas\n")
    activity = input("Input nama aktivitas: ")
    s.input_activity(user, {"activity": activity, "ip_address": ip_address})
    print("Data berhasil dimasukkan\n")

def logMenu(user):
    clearScreen()
    menuHeader = "======> Cek Log\n"
    print(menuHeader)
    print("1. Cek Semua Log")
    print("2. Cek Berdasar Waktu")
    menu = input("Input nomor menu: ")

    if menu == "1":
        clearScreen()
        print(menuHeader)
        print(s.get_log(user, ip_address))
        print("\n")

    if menu == "2":
        clearScreen()
        print(menuHeader)
        print("Format tanggal: YYYY-MM-DD, contoh: 2021-1-30")
        print("Format waktu: hh:mm:ss contoh: 3:30:0\n")
        dataDate = input("Input tanggal: ")
        dataTime = input("Input waktu, tekan enter untuk mengosongkan waktu: ")

        clearScreen()
        print(menuHeader)
        print(f"\nMenampilkan log dari {dataDate} {dataTime} hingga saat ini...\n")
        print(s.get_log(user, ip_address, dataDate, dataTime))
        print("\n")

while True:
    user = loginMenu()

    if user == "0": 
        clearScreen()
        break
    
    s.input_activity(user, {"activity": "login", "ip_address": ip_address})

    while True:
        menu = mainMenu()

        if menu == "1":
            inputMenu(user)
            input("Tekan enter untuk kembali ke menu utama")
            continue

        if menu == "2":
            logMenu(user)
            input("Tekan enter untuk kembali ke menu utama")
            continue

        if menu == "0":
            clearScreen()
            s.input_activity(user, {"activity": "logout", "ip_address": ip_address})
            break