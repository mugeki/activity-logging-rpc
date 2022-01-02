# import SimpleXMLRPCServer
from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer

from datetime import datetime
import os
import re

# Membuat program yang mencatat semua aktivitas yang dilakukan terhadap server
# (alamat IP client, waktu, dan aktivitas yang dilakukan). Informasi dari client-client
# dikirimkan ke server kemudian diolah oleh server. Misalnya, deteksi anomali komputer
# client, monitoring jaringan, dan lain sebagainya. Selain itu, client dapat melihat log
# aktivitas untuk hari, tanggal, dan jam yang diinginkan.

DATABASE = {
    "1": {
        "ip_address": "192.168.0.1",
        "activity": "login",
        "time": datetime(2021,12,31,14,45,0,0,None),
        "min_ping": "",
        "max_ping": "",
        "avg_ping": "326ms",
    },
}

regexAvgPing = re.compile(r" = (\d*ms)")

with SimpleXMLRPCServer(("26.95.204.95", 8000), allow_none=True) as server:
    def inputActivity(data):
        pingOutput = os.popen("ping -n 2 www.google.com").read()
        pings = regexAvgPing.findall(pingOutput)
        idx = 0
        if len(DATABASE) != 0: idx = len(DATABASE)+1
        DATABASE[idx] = {
            "ip_address": client_ip,
            "activity": data,
            "time": datetime.now(),
            "min_ping": pings[0],
            "max_ping": pings[1],
            "avg_ping": pings[2],
        }
        return

    def getLog(dataDate=None, dataTime=None):
        if len(DATABASE) == 0:
            return "LOG KOSONG..."
        response = ""
        if dataDate is None and dataTime is None:
            for key in reversed(DATABASE):
                if DATABASE[key]["ip_address"] == client_ip:
                    response += (
                        "[{}] ".format(DATABASE[key]["time"].strftime("%m/%d/%Y, %H:%M:%S")) + 
                        "IP Address: {}, ".format(DATABASE[key]["ip_address"]) + 
                        "Aktivitas: {}, " .format(DATABASE[key]["activity"]) +
                        "Min Ping: {}, ".format(DATABASE[key]["min_ping"]) +
                        "Max Ping: {}, ".format(DATABASE[key]["max_ping"]) +
                        "Average Ping: {}\n".format(DATABASE[key]["avg_ping"])
                    )
        else:
            targetTime = None
            date = dataDate.split("-")
            
            if dataTime != "":
                time = dataTime.split(":")
                targetTime = datetime(int(date[0]),int(date[1]),int(date[2]),
                                    int(time[0]),int(time[1]),int(time[2]))
            else:
                targetTime = datetime(int(date[0]),int(date[1]),int(date[2]))

            for key in reversed(DATABASE):
                if DATABASE[key]["ip_address"] == client_ip and DATABASE[key]["time"] >= targetTime:
                    response += (
                        "[{}] ".format(DATABASE[key]["time"].strftime("%m/%d/%Y, %H:%M:%S")) + 
                        "IP Address: {}, ".format(DATABASE[key]["ip_address"]) + 
                        "Aktivitas: {}\n" .format(DATABASE[key]["activity"])
                    )
                    
        if response == "": response = "LOG KOSONG..."
        return response

    server.register_function(inputActivity, "input_activity")
    server.register_function(getLog, "get_log")

    print("Server berjalan...")
    client_ip = server.get_request()[1][0]
    
    server.serve_forever()