# Server Modules
import socket # API's Native Language 
import websockets # API's Translated Language
import ssl # Required for WebSockets BS
import urllib.request # Required for CORS Proxy

# Multi-threading modules
import asyncio # Required for WebSockets
import _thread # Required for multi-client raw socket clients.
import threading # Required for WebSockets

# Miscellaneous Modules
import time # Required for logs
import os # Required for KeyboardInterrupt (DEBUG) and loading config files
import sys # Required for KeyboardInterrupt (DEBUG)
import configparser # Load a  back-end server config file
import traceback # Error handling

# Load sensitive information
import dotenv
dotenv.load_dotenv()

# Own Modules
from SN_PyDepends import *

""" [!] This function makes debugging harder """
def ServerCFG():
    Log(f'[System]: Configuring server...')
    SRV_CFG = LoadCFG(os.path.basename(__file__).replace(".py", ".cfg"))
    
    """ .env Variables """
    SSL_Cert = os.getenv('SSL_Cert')
    SSL_Key = os.getenv('SSL_Key')

    """ .cfg Variables """
    SRV_Name = SRV_CFG["Info"]["Name"]
    SRV_Desc = SRV_CFG["Info"]["Description"]
    SRV_Vers = SRV_CFG["Info"]["Version"]
    
    RoutineTimeout = int(SRV_CFG["API"]["RoutineTimeout"])
    API_RawPort = int(SRV_CFG["API"]["RawPort"])
    API_WebPort = int(SRV_CFG["API"]["WebPort"])
    API_PacketSize = int(SRV_CFG["API"]["PacketSize"])

    """ Processed Variables """
    API_RawSocket = socket.gethostname()
    API_WebSocket = socket.socket()

    SSL_Options = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    SSL_Options.load_cert_chain(SSL_Cert, keyfile=SSL_Key)

    globals().update(locals())

""" Service Functions """
def SirioAPI_Thread():
    Log(f'[System] INFO: Initializing SirioAPI...')

    async def Server_Redirect(Client_Request,Client_Address):
        Client_Request = Client_Request.split("://")
        if doesEntryExists(Client_Request,0) == True and doesEntryExists(Client_Request,1) == True:
            Log(f'[Forwarding] "{Client_Request[0]} API": {Client_Request[1]}')
            return str(Client_Request[1])
        else:
            Log(f'[ERROR] Invalid Request: "{str(Client_Request)}" !')
            return "INVALID_REQUEST"
        
    """ Socket Handlers
    def RawSocket_Server(): # This is broken right now
        Log(f'INFO: Starting RawSockets Server...')
        async def Socket_Handler(Connection_Socket):
            # Make the client connection readable
            Client_Socket, Address = Connection_Socket.accept()
            Client_Address = str(Address[0])+":"+str(Address[1])
            Log(f"CONNECTED (RAW): {Client_Address}")
            try: 
                await Server_Redirect(Client_Address, False)
            except Exception as ErrorInfo:
                Log(f'CONNECTION ERROR: {Client_Address}. \n[TRACEBACK]\n{ErrorInfo}\n',True)

        def Socket_Asyncer(Connection_Socket):
            asyncio.run(Socket_Handler(Connection_Socket))
            try: 
                API_RawSocket.bind((API_RawSocket, API_RawPort))
            except socket.error as ErrorInfo:
                Log(f"ERROR: Failed to bind the server's address! \n[TRACEBACK]\n{ErrorInfo}\n",False)
            Response = await Client.recv()
            Log(f'SYSTEM: Initiated Socket Server.',False)
            API_RawSocket.listen()
            while True: threading.Thread(target=Socket_Asyncer(API_RawSocket)).start()
    """

    def WebSocket_Server():
        Log(f'[System] INFO: Starting WebSockets Server...')

        async def Websocket_Handler(websocket):
            # Make the client connection readable
            Address = websocket.remote_address
            Client_Address = str(Address[0])+":"+str(Address[1])

            Log(f'[Connection] OK: Web://{Client_Address}.')
            
            Client_Request = await websocket.recv()
            Log(f'[Request] Web://{Client_Address}: "{Client_Request}".')
            Server_Result = await Server_Redirect(Client_Request,Client_Address)
            Log(f'[Sending] Web://{Client_Address}: {Server_Result}')
            await websocket.send(str())

        async def Websocket_Listener():
            Log(f'[System] OK: Websockets thread started.')
            async with websockets.serve(Websocket_Handler, "0.0.0.0", API_WebPort, ssl=SSL_Options):
                await asyncio.Future()
        asyncio.run(Websocket_Listener())

    #threading.Thread(target=RawSocket_Server).start()
    threading.Thread(target=WebSocket_Server).start()


""" Server State Functions """

def Shutdown():
    Log(f'[System] SHUTDOWN: Shutting down server...')
    """
    DWeb_Title = f'The "{SRV_Name}" Server is offline!'
    DWeb_Desc = "Trinity is the Front-End Server for the Sirio Network API. All services such as the Flashcord API, Sirio News API and etc are now unreachable! <@311057290562371586> will soon provide more information."
    DWeb_Send(DWeb_Title, DWeb_Desc, "Public")
    """
    try: sys.exit(130)
    except SystemExit: os._exit(130)
    
def Bootstrap():
    os.system("clear")
    Log(f"[System] Starting server...")
    ServerCFG()
    threading.Thread(target=SirioAPI_Thread).start()
    Log(f'[System] Server initialized.')
    """
    DWeb_Title = f'The "{SRV_Name}" Server is now online!'
    DWeb_Desc = "Trinity is the Front-End Server for the Sirio Network API. All services such as the Flashcord API, Sirio News API and etc are now accessible."
    DWeb_Send(DWeb_Title, DWeb_Desc, "Public")
    """
    try:
        while True: 
            Log(f'[System] Awaiting next Routine Loop in {RoutineTimeout} seconds.')
            time.sleep(RoutineTimeout)
            Log(f'[System] Executing Routine.')
    except KeyboardInterrupt:
        Shutdown()

# Spark
if __name__== '__main__': 
    while True:
        try: Bootstrap()
        except Exception: Crash(traceback.format_exc(),False)
