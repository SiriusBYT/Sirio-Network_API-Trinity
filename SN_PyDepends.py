# Modules
import time # Required for sleep functions and time related shenanigans
import discord_webhook # I'm not fucking logging into SSH every nano second but I'm a chronically online Flashcord user so.. Discord for emergency notifications!!!

# Load sensitive information
import dotenv, os
dotenv.load_dotenv()

SRV_Name = os.getenv('SRV_Name')
SRV_Desc = os.getenv('SRV_Desc')
SRV_Vers = os.getenv('SRV_Vers')

""" Sensitive Variables """
DWeb_LogURL = os.getenv("DWeb_LogURL") # Private
DWeb_PubURL = os.getenv("DWeb_PubURL") # Public


""" Variables for Webhooks Logging """
# Colors for Webhook Color
Color_Red = "FF3737"
Color_Orange = "FFE137"
Color_Green = "37FF64"
Color_Blue = "3764FF"
Color_Purple = "9B32FF"
Color_Pink = "FF9BFF"

# Keywords for getting Webhook Color
""" [!] This should be replaced by an external JSON file. """
Words_Error = [
    "ERROR",
    "SHUTDOWN",
    "CRASH",
    "FUCK",
    "OFFLINE"
]
Words_Warning = [
    "WARNING",
    "TIMED OUT"
]

Words_Success = [
    "SUCCESS",
    "OK",
    "ONLINE"
]
Words_Info = [
    "INFO",
    "REQUEST",
    "CONNECTION",
    "FORWARDING"
]
Words_Special = [
    "SYSTEM"
]



""" int() Functions """
# Checks if a specified array number exist
def doesEntryExists(Array,Number):
    try:
        Dummy = Array[Number]
        return True
    except:
        return False

# Get current time string in the example format "22:10:10" - "31-07-2024"
def GetTime():
    CTime = time.localtime()
    Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
    Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
    return Time,Date

def Log(Log):
    Time,Date = GetTime()
    Log = f"[{Time}] {Log}"
    with open(f"logs/{Date}.log", "a", encoding="utf=8") as LogFile:
        LogFile.write(f"{Log}\n")
        print(Log)

    DWeb = discord_webhook.DiscordWebhook(url=DWeb_LogURL, rate_limit_retry=True)
    DWeb_Embed = discord_webhook.DiscordEmbed(title="", description=Log, color=DWeb_Color(Log))
    DWeb_Embed.set_footer(text=f"Log Time: {Time} - {Date}")
    DWeb.add_embed(DWeb_Embed)
    DWeb.execute()


""" void() Functions """
# Logs the server's information
def ServerInfo():
    Log(f"Server Name: {SRV_Name}")
    Log(f"Server Description: {SRV_Desc}")
    Log(f"Server Version: {SRV_Vers}")

def DoNothing(): return

# Quickly send a Discord Webhook Embed Message
def DWeb_Send(Title, Description, Visibility):
    match Visibility:
        case "Private":
            URL = DWeb_LogURL
        case "Public":
            URL = DWeb_PubURL

    Time,Date = GetTime()
    DWeb = discord_webhook.DiscordWebhook(url=URL, rate_limit_retry=True)
    DWeb_Embed = discord_webhook.DiscordEmbed(title=Title, description=Description, color=DWeb_Color(f"{Title} {Description}"))
    DWeb_Embed.set_footer(text=f"Log Time: {Time} - {Date}")
    DWeb.add_embed(DWeb_Embed)
    DWeb.execute()

""" Private Functions """
# Used for Webhook Embeds 
def DWeb_Color(String):
    for cycle in Words_Error:
        if cycle in String:
            return Color_Red
    for cycle in Words_Warning:
        if cycle in String:
            return Color_Orange
    for cycle in Words_Success:
        if cycle in String:
            return Color_Green
    for cycle in Words_Info:
        if cycle in String:
            return Color_Blue
    for cycle in Words_Special:
        if cycle in String:
            return Color_Purple
        
    """ [!] This is kinda ugly, there has to be a better way to do this. """
    return Color_Pink
