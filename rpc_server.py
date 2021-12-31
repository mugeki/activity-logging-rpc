# import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime

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
    },
    "2": {
        "ip_address": "192.168.0.1",
        "activity": "logout",
        "time": datetime(2022,1,1,10,00,0,0,None),
    },
    "3": {
        "ip_address": "192.168.0.1",
        "activity": "logout",
        "time": datetime(2022,1,1,12,30,0,0,None),
    },
}


class RequestHandler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
        SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)

with SimpleXMLRPCServer(("127.0.0.1", 8000), requestHandler=RequestHandler, allow_none=True) as server:
    def inputActivity(data):
        DATABASE[f"{len(DATABASE)+1}"] = {
            "ip_address": "baru",
            "activity": data,
            "time": datetime.now(),
        }

    def getLog(dataDate=None, dataTime=None):
        response = ""
        if dataDate is None and dataTime is None:
            for key in reversed(DATABASE):
                response += (
                    "[{}] ".format(DATABASE[key]["time"].strftime("%m/%d/%Y, %H:%M:%S")) + 
                    "IP Address: {}, ".format(DATABASE[key]["ip_address"]) + 
                    "Aktivitas: {}\n" .format(DATABASE[key]["activity"])
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
                if DATABASE[key]["time"] >= targetTime:
                    response += (
                        "[{}] ".format(DATABASE[key]["time"].strftime("%m/%d/%Y, %H:%M:%S")) + 
                        "IP Address: {}, ".format(DATABASE[key]["ip_address"]) + 
                        "Aktivitas: {}\n" .format(DATABASE[key]["activity"])
                    )
        
        return response

    server.register_function(inputActivity, "input_activity")
    server.register_function(getLog, "get_log")

    print("Server berjalan...")
    server.serve_forever()