# import SimpleXMLRPCServer
from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler

from datetime import datetime
import os
import re

# Membuat program yang mencatat semua aktivitas yang dilakukan terhadap server
# (alamat IP client, waktu, dan aktivitas yang dilakukan). Informasi dari client-client
# dikirimkan ke server kemudian diolah oleh server. Misalnya, deteksi anomali komputer
# client, monitoring jaringan, dan lain sebagainya. Selain itu, client dapat melihat log
# aktivitas untuk hari, tanggal, dan jam yang diinginkan.

# Membuat database dummy
DATABASE = {
    "elang":{
        "1": {
            "ip_address": "192.168.0.1",
            "activity": "login",
            "time": datetime(2021,12,31,14,45,0,0,None),
            "min_ping": "10ms",
            "max_ping": "326ms",
            "avg_ping": "200ms",
        },
    }
}

# Definisi regex untuk ping
regexAvgPing = re.compile(r" = (\d*ms)")

# Batasi path hanya menjadi /RPC2
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

# Membuat server
with SimpleXMLRPCServer(("127.0.0.1", 8000), requestHandler=RequestHandler, allow_none=True) as server:
    # Membuat fungsi untuk melakukan input aktivitas user
    def inputActivity(user, data):
        pingOutput = os.popen("ping -n 2 google.com").read()
        pings = regexAvgPing.findall(pingOutput)
        
        idx = 1
        if user not in DATABASE:
            DATABASE[user] = {}

        if len(DATABASE[user]) != 0: 
            idx = len(DATABASE[user])+1
            
        DATABASE[user][f"{idx}"] = {
            "ip_address": data["ip_address"],
            "activity": data["activity"],
            "time": datetime.now(),
            "min_ping": "timed out" if not pings else pings[0],
            "max_ping": "timed out" if not pings else pings[1],
            "avg_ping": "timed out" if not pings else pings[2],
        }
        return

    # Membuat fungsi untuk mendapatkan log user
    def getLog(user="", client_ip="127.0.0.1", dataDate=None, dataTime=None, ):
        if len(DATABASE) == 0:
            return "LOG KOSONG..."

        response = ""
        if dataDate is None and dataTime is None:
            for key in reversed(DATABASE[user]):
                response += (
                    "[{}] ".format(DATABASE[user][key]["time"].strftime("%m/%d/%Y, %H:%M:%S")) + 
                    "IP Address: {}, ".format(DATABASE[user][key]["ip_address"]) + 
                    "Aktivitas: {}, " .format(DATABASE[user][key]["activity"]) +
                    "Min Ping: {}, ".format(DATABASE[user][key]["min_ping"]) +
                    "Max Ping: {}, ".format(DATABASE[user][key]["max_ping"]) +
                    "Average Ping: {}\n".format(DATABASE[user][key]["avg_ping"])
                )
        # Handle ketika user tidak mengintputkan waktu
        else:
            targetTime = None
            date = dataDate.split("-")
            
            if dataTime != "":
                time = dataTime.split(":")
                targetTime = datetime(int(date[0]),int(date[1]),int(date[2]),
                                    int(time[0]),int(time[1]),int(time[2]))
            else:
                targetTime = datetime(int(date[0]),int(date[1]),int(date[2]))

            for key in reversed(DATABASE[user]):
                if DATABASE[user][key]["time"] >= targetTime:
                    response += (
                        "[{}] ".format(DATABASE[user][key]["time"].strftime("%m/%d/%Y, %H:%M:%S")) + 
                        "IP Address: {}, ".format(DATABASE[user][key]["ip_address"]) + 
                        "Aktivitas: {}\n" .format(DATABASE[user][key]["activity"])
                    )
                    
        if response == "": response = "LOG KOSONG..."
        return response
    
    # Register fungsi ke server rpc
    server.register_function(inputActivity, "input_activity")
    server.register_function(getLog, "get_log")

    # Run server
    print("Server berjalan...")
    server.serve_forever()