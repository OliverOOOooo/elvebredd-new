import json, hashlib, flask, time, random
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
import copy
import os
import atexit
from better_profanity import profanity
import click, requests

ValidateDataCheck = time.time()

WebsiteAddress = "https://127.0.0.1:5000"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def getCredentials():
    global SCOPES
    try:
        creds = Credentials.from_authorized_user_file("account/token.json", SCOPES)
    except FileNotFoundError:
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("account/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("account/token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def checkStatus():
    try:
        response = requests.get(WebsiteAddress)
        if response.status_code == 200:
            click.echo("Server is running.")
        else:
            click.echo("Server is not responding as expected.")
    except requests.ConnectionError:
        click.echo("Server is not running.")

def sendEmail(to_mail, subject, body):
    global SCOPES
    credentials = getCredentials()
    service = build("gmail", "v1", credentials=credentials)
    message = MIMEText(body)
    message["to"] = to_mail
    message["subject"] = subject

    try:
        message = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()})
            .execute()
        )
    except HttpError:
        message = None

    return message

def changePasswordWithTempID(tempID = "", password = ""):
    global ResetPassword
    if tempID != "" and password != "":
        try:
            if ResetPassword[tempID]:
                if time.time() - ResetPassword[tempID]["time"] < 300:
                    UserData[ResetPassword[tempID]["userID"]]["password"] = encrypt(password)
                    with open("data/UserData.json", "w") as file:
                        json.dump(UserData, file, indent=4, ensure_ascii=True)
                    return 3, "Successfully changed password!", 1
                else:
                    pass
            else:
                return 1, "TempID does not exist!", 0
        except:
            return 2, "Bad Request 400 # TempID Error", -1
    else:
        return 0, "Bad Request 100 # Missing Arguments", -1

def sendResetPasswordEmail(email = "", tempID = ""):
    global WebsiteAddress
    if email != "" and tempID != "":
        title = "Reset Your Password"
        message = "You can reset your password using this link:" + WebsiteAddress + "/reset-password?tempID=" + tempID
        sendEmail(email, title, message)
        return 0, "Email sent!", 1
    else:
        return 1, "Bad Request 100 # Missing arguments", -1

def generateRandomString(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    output = ""
    for x in range(length):
        output += characters[random.randint(0, len(characters) - 1)]
    return output


def encrypt(string):
    stringBytes = string.encode("utf-8")
    sha512Hasher = hashlib.sha512()
    sha512Hasher.update(stringBytes)
    return sha512Hasher.hexdigest()

def homePage():
    pass

def updateStreak(userID):
    global UserData
    if time.time() - UserData[userID]["dailyStreakActivated"] > 3600 * 24:
        UserData[userID]["dailyStreak"] = 0
        UserData[userID]["dailyStreakActivated"] = time.time()
    elif time.time() - UserData[userID]["dailyStreakActivated"] > 3600 * 18:
        UserData[userID]["dailyStreak"] += 1
        UserData[userID]["dailyStreakActivated"] = time.time()

def updateActivity(activity = "", ipaddress = ""):
    global UserData
    userID = str(flask.session.get("userID", ""))
    if userID != "":
        updateStreak(userID)
        current_time = time.localtime()
        formatted_time = "{:02}/{:02}:{:02}:{:02}:{:02}".format(current_time.tm_hour, current_time.tm_min, current_time.tm_mday, current_time.tm_mon, current_time.tm_year % 100)
        UserData[userID]["lastActivity"] = [formatted_time, [activity, ipaddress]]
        UserData[userID]["allActivity"][formatted_time] = [activity, ipaddress]
        dumpUserData()

def createAccount(username = "", robloxUsername = "", email = "", password = ""):
    if password != "":
        if len(username) < 21 or 2 < len(username) and "@" in email and "." in email and len(password) > 6 and len(password) < 100:
            emails = []
            usernames = []
            for user, userdata in UserData.items():
                emails.append(userdata["email"])
                usernames.append(userdata["username"])
            if email not in emails and username not in usernames:
                id = str(len(UserData))
                UserData[id] = {
                    "username": profanity.censor(username),
                    "robloxUsername": profanity.censor(robloxUsername),
                    "email": email,
                    "password": encrypt(password),
                    "emailVerified": 0,
                    "sessionToken": generateRandomString(16),
                    "trades": [],
                    "completedTrades": [],
                    "inventory": [],
                    "moderator": 0,
                    "banned": 0,
                    "frozen": 0,
                    "reports": {},
                    "notifications": [{
                                "head":"1st Notification!",
                                "body":"Wow, I can't believe you read this!",
                                "read":False,
                                "important":False,
                                "image":"/static/images/notifications/default.png",
                                "created":time.time(),
                            },{
                                "head":"2nd Notification!",
                                "body":"Wow, I can't believe you read this!",
                                "read":False,
                                "important":False,
                                "image":"/static/images/notifications/default.png",
                                "created":time.time(),
                            },
                    ],
                    "preferences": {
                        "highTiers": 0,
                        "megaLegendaryPets": 0,
                        "neonLegendaryPets": 0,
                        "defaultLegendaryPets": 0,
                        "preppyPets": 0,
                        "randoms": 0,
                        "items": 0
                    },
                    "settings": {
                        "receiveNotifications": 1,
                        "allowUnderpays": 1,
                        "receiveEmailNotifications": 0,
                        "receiveFriendRequestNotification": 0
                    },
                    "friends": [],
                    "friendRequests": {
                        "sent": [],
                        "received": []
                    },
                    "misc": {},
                    "tags": {},
                    "messages": {},
                    "currency": 0,
                    "tokens":0,
                    "achievements": {},
                    "collection": ["default.png", "dino.png"],
                    "badges": {},
                    "verified": 0,
                    "dailyStreak": 1,
                    "dailyStreakActivated": time.time(),
                    "wishlist": [],
                    "lastActivity": time.localtime(),
                    "allActivity": {
                        str(time.localtime()):"accountCreated"
                    },
                    "rewiews": {},
                    "newsRead": {},
                    "profilePicture": "default.png",
                    "blocked": [],
                    "inbox": [],
                    "pending":[],
                    "accountCreatedRawTime":time.time(),
                    "accountCreated":"{:02}/{:02}:{:02}:{:02}:{:02}".format(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year % 100)
                }
                with open("data/UserData.json", "w") as file:
                    json.dump(UserData, file, indent=4, ensure_ascii=True)
                flask.session.permanent = True
                flask.session['loggedIn'] = True
                flask.session['userID'] = id
                flask.session['userData'] = cookifyUserData(UserData[id])
                return 0, "Account Created!", 1
            else:
                if username in usernames:
                    return 1, "Username Occupied!", 0
                else:
                    return 2, "Email taken!", 0
        else:
            return 3, "Bad Request 101 # Create account arguments failed verification", -1
    else:
        return 4, "Bad Request 100 # Missing account arguments", -1

def getProfilePictures():
    output = {}
    files = [file for file in os.listdir("static/images/profile")]
    return files

def validateSession():
    global UserData
    if flask.session.get("userID", "") != "":
        try:
            if flask.session.get("userData", "")["sessionToken"] != UserData[flask.session.get("userID", "")]["sessionToken"]:
                flask.session.clear()
                return 3, "Session expired!", 0
            else:
                return 2, "Session validated!", 1
        except Exception:
            return 1, "Flask session modified!", -1
    else:
        return 0, "Error", 0
    
def changePassword(userID, password):
    global UserData
    if userID != "":
        UserData[userID]["password"] = encrypt(password)
        UserData[userID]["sessionToken"] = generateRandomString(16)
        flask.session['userData'] = cookifyUserData(UserData[userID])
        dumpUserData()
        return 1, "Password Changed!", 1
    else:
        return 0, "Error", -1
    
def getUserData(userID):
    global UserData
    if userID in UserData:
        return 1, cookifyUserData(UserData[userID]), 1
    else:
        return 0, "Invalid User ID", -1

def changeUsername(userID, username):
    global UserData
    if userID != "" and len(username) > 2 and len(username) < 21:
        UserData[userID]["username"] = profanity.censor(username)
        UserData[userID]["sessionToken"] = generateRandomString(16)
        flask.session['userData'] = cookifyUserData(UserData[userID])
        updateTradesWithUsernameChange(userID)
        dumpUserData()
        return 1, "Username Changed!", 1
    else:
        return 0, "Error", -1
    
def changeRobloxUsername(userID, username):
    global UserData
    if userID != "" and len(username) > 2 and len(username) < 21:
        UserData[userID]["robloxUsername"] = profanity.censor(username)
        UserData[userID]["sessionToken"] = generateRandomString(16)
        flask.session['userData'] = cookifyUserData(UserData[userID])
        updateTradesWithUsernameChange(userID)
        dumpUserData()
        return 1, "Roblox Username Changed!", 1
    else:
        return 0, "User not logged in!", -1

def getTrade(key):
    global Trades
    try:
        return {key:Trades[key]}
    except KeyError:
       return {}
    
def setAsProfilePicture(userID, image):
    global UserData
    if userID != "":
        if image in UserData[userID]["collection"]:
            UserData[userID]["profilePicture"] = image
            dumpUserData()
            flask.session['userData'] = cookifyUserData(UserData[userID])
            return 1, "Image changed!", 1
        else:
            return 2, "Image not unlocked!", -1
    else:
        return 0, "User not logged in!", -1

def updateTradesWithUsernameChange(userID):
    global UserData, Trades
    for trade in UserData[userID]["trades"]:
        Trades[trade]["ownerUsername"] = UserData[userID]["username"]
        Trades[trade]["ownerRobloxUsername"] = UserData[userID]["robloxUsername"]
    for trade in UserData[userID]["pending"]:
        if Trades[trade]["owner"] == userID:
            Trades[trade]["ownerUsername"] = UserData[userID]["username"]
            Trades[trade]["ownerRobloxUsername"] = UserData[userID]["robloxUsername"]
        else:
            Trades[trade]["acceptedByUsername"] = UserData[userID]["username"]
            Trades[trade]["acceptedByRobloxUsername"] = UserData[userID]["robloxUsername"]
    for trade in UserData[userID]["completedTrades"]:
        if Trades[trade]["owner"] == userID:
            Trades[trade]["ownerUsername"] = UserData[userID]["username"]
            Trades[trade]["ownerRobloxUsername"] = UserData[userID]["robloxUsername"]
        else:
            Trades[trade]["acceptedByUsername"] = UserData[userID]["username"]
            Trades[trade]["acceptedByRobloxUsername"] = UserData[userID]["robloxUsername"]

def searchUpAccount(searchKey = "username/email"):
    global UserData
    if searchKey != "username/email":
        if type(searchKey) == str:
            emails = []
            usernames = []
            for user, userdata in UserData.items():
                emails.append([userdata["email"], user])
                usernames.append([userdata["username"], user])
            for email, id in emails:
                if searchKey == email:
                    return 0, id, 1
            for username, id in usernames:
                if searchKey == username:
                    return 1, id, 1
            return 2, "Could not find an account!", 0
        elif type(searchKey) == int:
            if str(searchKey) in UserData.keys():
                return 5, "Account Exists!", 1
            return 6, "Account does not exist!", 0
        else:
            return 4, "Unidentified format!", -1
    else:
        return 3, "BadRequest 110 # Missing arguments", -1


def addCustomOffer(userID = "", trade = "", pets = []):
    global UserData, Trades
    if userID != "" and trade != "" and pets != []:
        extraSharkValue = calculateValue(pets)
        if extraSharkValue >= Trades[trade]["extraSharkValueRequested"]:
            Trades[trade]["customOffers"].append({
                "pets":pets,
                "value":calculateValue(pets),
                "owner":userID,
                "ownerProfilePicture":UserData[userID]["profilePicture"],
                "ownerUsername":UserData[userID]["username"],
                "ownerRobloxUsername":UserData[userID]["robloxUsername"],
                "createdAt":time.time(),
                "status":"Pending"
            })
            return 1, "Offer created", 1
        else:
            return 2, "Offer invalid", -1
    else:
        return 0, "Bad Request 110 # Missing arguments", -1




def getDataFromIDWithoutDetails(userID = "") -> dict:
    if userID != "":
        try:
            userID = str(userID)
            safeUserData = copy.deepcopy(UserData[userID])
            safeUserData["email"] = None
            safeUserData["password"] = None
            safeUserData["moderator"] = None
            safeUserData["frozen"] = None
            safeUserData["notifications"] = None
            safeUserData["reports"] = None
            safeUserData["messages"] = None
            safeUserData["lastActivity"] = None
            safeUserData["allActivity"] = None
            safeUserData["currency"] = None
            safeUserData["newsRead"] = None
            safeUserData["preferences"] = None
            safeUserData["settings"] = None
            safeUserData["misc"] = None 
            return safeUserData
        except KeyError:
            return "ERROR"
    else:
        return "ERROR"
    
def cookifyUserData(userData = {}) -> dict:
    if userData != {}:
        try:
            safeUserData = copy.deepcopy(userData)
            safeUserData["email"] = None
            safeUserData["password"] = None
            safeUserData["reports"] = None
            safeUserData["lastActivity"] = None
            safeUserData["allActivity"] = None
            safeUserData["notifications"] = None
            return safeUserData
        except KeyError:
            return "ERROR"
    else:
        return "ERROR"
    
def get20Notifications(userID, loaded):
    global UserData
    loaded = int(loaded)
    if userID != "":
        reversedList = UserData[userID]["notifications"][::-1]
        output = []
        for i in range(loaded, loaded + 20):
            if i < len(reversedList):
                output.append(reversedList[i])
            else:
                break
        return 1, output, 1
    else:
        return 0, "User not logged in!", -1

def dumpUserData():
    global UserData
    with open("data/UserData.json", "w") as file:
        json.dump(UserData, file, indent=4, ensure_ascii=True)  

def dumpTrades():
    global Trades
    with open("data/Trades.json", "w") as file:
        json.dump(Trades, file, indent=4, ensure_ascii=True)  

def readNotifications(userID = ""):
    global UserData
    if userID != "":
        try:
            for x in range(len(UserData[userID]["notifications"])):
                UserData[userID]["notifications"][x]["read"] = True
            dumpUserData()
            flask.session['userData'] = cookifyUserData(UserData[userID])
            return 2, "Notifications read!", 1
        except KeyError:
            return 1, "User not found!", 0
    else:
        return 0, "Bad Request 100 # Missing arguments", -1
    
def login(usernameOrEmail = "", password = ""):
    global UserData
    if usernameOrEmail != "" and password != "":
        Password = encrypt(password)
        for id, data in UserData.items():
            if (data["email"] == usernameOrEmail or data["username"] == usernameOrEmail) and data["password"] == Password:
                flask.session.permanent = True
                flask.session['loggedIn'] = True
                flask.session['userID'] = str(id)
                flask.session['userData'] = cookifyUserData(data)
                return 0, "Login Sucessfully!", 1
        return 1, "Your information is incorrect!", 0
    else:
        return 3, "Bad Request 100 # Missing arguments", -1
    
def loginUnsafe(userID = ""):
    global UserData
    if userID != "":
        if userID in UserData:
            flask.session.permanent = True
            flask.session['loggedIn'] = True
            flask.session['userID'] = userID
            flask.session['userData'] = cookifyUserData(UserData[userID])
        else:
            return 1, "UserID not found!", 0
    else:
        return 0, "Bad Request 100 # Missing arguments", -1
    

def search(input):
    global UserData, Pets
    
    for userID, userData in UserData.items():
        if userData["username"] == input:
            return 0, ["user", userData["username"], userID], 1
        elif userData["robloxUsername"] == input:
            return 1, ["user", userData["robloxUsername"], userID], 1
    for petID, petData in Pets.items():
        if petData["name"] == input:
            return 2, ["pet", petData["name"], petID], 1
    
    return 3, "Nothing Found", -1


def searchPets(input):
    output = []
    output2 = []
    global Pets
    if input != "":
        for petID, pet in Pets.items():
            if len(output) < 5:
                if input in pet["name"]:
                    output.append(pet)
                    output2.append(petID)
            else:
                break
    return [output, output2]

def getFriendsDetails(userID):
    output = {}
    try:
        for friendID in UserData[userID]["friends"]:
            output[friendID] = {"username":UserData[friendID]["username"], 
                                "robloxUsername":UserData[friendID]["robloxUsername"],
                                "profilePicture":UserData[friendID]["profilePicture"]
                                }
    except KeyError:
        return {}
    return output

def getPendingDetails(userID):
    output = {}
    try:
        for friendID in UserData[userID]["friendRequests"]["received"]:
            output[friendID] = {"username":UserData[friendID]["username"], 
                                "robloxUsername":UserData[friendID]["robloxUsername"],
                                "profilePicture":UserData[friendID]["profilePicture"]
                                }
    except KeyError:
        return {}
    return output

def getBlockedDetails(userID):
    output = {}
    try:
        for user2ID in UserData[userID]["blocked"]:
            output[user2ID] = {"username":UserData[user2ID]["username"], 
                                "robloxUsername":UserData[user2ID]["robloxUsername"],
                                "profilePicture":UserData[user2ID]["profilePicture"]
                                }
    except KeyError:
        return {}
    return output

def getIDFromEmail(email = ""):
    if email != "":
        for user, userdata in UserData.items():
            if email == userdata["email"]:
                return 1, user, 1
            return 2, "No user found!", 0
    else:
        return 0, "Bad Request 100 # Missing arguments"
    
def acceptOffer(userID, user2ID, listing):
    global Trades, UserData
    if userID != "" and user2ID != "" and userID not in UserData[user2ID]["blocked"] and user2ID not in UserData[userID]["blocked"] and Trades[str(UserData[user2ID]["trades"][int(listing)])]["acceptedBy"] == None:
        key = str(UserData[user2ID]["trades"][int(listing)])
        Trades[key]["acceptedBy"] = str(userID)
        Trades[key]["acceptedByUsername"] = UserData[userID]["username"]
        Trades[key]["public"] = False
        Trades[key]["visibleTo"] = [userID, user2ID]
        if key in UserData[userID]["inbox"]:
            UserData[userID]["inbox"].remove(key)
        if key not in UserData[userID]["pending"]:
            UserData[userID]["pending"].append(key)
        sendNotification(Trades[key]["owner"], "Trade", "One of your listings has been accepted by " + UserData[userID]["username"] + ". Make sure to contact '" + UserData[userID]["robloxUsername"] + "' through roblox!", False, "/static/images/profile/" + UserData[Trades[key]["owner"]]["profilePicture"])
        dumpUserData()
        dumpTrades()
        return 0, "Success", 1
    else:
        return 1, "User not allowed to make trade", -1
    
def acceptOfferWithKey(userID, key):
    global Trades, UserData
    user2ID = Trades[key]["owner"]
    if userID != "" and userID not in UserData[user2ID]["blocked"] and user2ID not in UserData[userID]["blocked"]:
        if Trades[key]["acceptedBy"] == None:
            Trades[key]["acceptedBy"] = str(userID)
            Trades[key]["acceptedByUsername"] = UserData[userID]["username"]
            Trades[key]["public"] = False
            Trades[key]["visibleTo"] = [userID, user2ID]
            if key in UserData[userID]["inbox"]:
                UserData[userID]["inbox"].remove(key)
            if key not in UserData[userID]["pending"]:
                UserData[userID]["pending"].append(key)
            dumpUserData()
            dumpTrades()
            return 0, "Success", 1
        else:
            return 2, "Trade already Accepted!", -1

    else:
        return 1, "User not allowed to make trade", -1

def sendCustomOffer(userID, user2ID, trade1, trade2):
    global Trades, UserData
    if userID != "" and user2ID != "" and userID not in UserData[user2ID]["blocked"] and user2ID not in UserData[userID]["blocked"]:
        UserData[user2ID]["inbox"].append(str(len(Trades)))
        dumpUserData()
        dumpTrades()
        createListing(userID, trade1, trade2, False, [userID, user2ID])
        sendNotification(user2ID, "Trade", "You have received a custom offer from " + UserData[userID]["username"] + ". Check it out!", False, "/static/images/profile/" + UserData[userID]["profilePicture"])
        return 0, "Success", 1
    else:
        return 1, "Failed", -1
    
def sendCustomOfferWithKey(userID, key, trade1, trade2):
    global Trades, UserData
    try:
        user2ID = Trades[key]["owner"]
        if userID != "" and user2ID != "" and userID not in UserData[user2ID]["blocked"] and user2ID not in UserData[userID]["blocked"]:
            UserData[user2ID]["inbox"].append(str(len(Trades)))
            dumpUserData()
            dumpTrades()
            createListing(userID, trade1, trade2, False, [userID, user2ID])
            return 0, "Success", 1
        else:
            return 1, "Failed", -1
    except Exception:
        return 2, "Critical error", -1

def getInbox(userID):
    global UserData, Trades
    output = {}
    if userID != "":
        for tradeID in UserData[userID]["inbox"]:
            try:
                output[tradeID] = Trades[tradeID]
            except KeyError:
                continue
    return 0, output, 1

def getPending(userID):
    global UserData, Trades
    output = {}
    if userID != "":
        for tradeID in UserData[userID]["pending"]:
            try:
                output[tradeID] = Trades[tradeID]
            except KeyError:
                continue
    return 0, output, 1

def getHistory(userID):
    global UserData, Trades
    output = {}
    if userID != "":
        for tradeID in UserData[userID]["completedTrades"]:
            try:
                output[tradeID] = Trades[tradeID]
            except KeyError:
                continue
    return 0, output, 1

def getRobloxUsername(ID):
    global UserData
    ouput = ""
    try:
        output = UserData[ID]["robloxUsername"]
    except KeyError:
        pass

    if output != "":
        return 0, output, 1
    else:
        return 1, "NULL", 0

def completeTradeWithKey(userID, key):
    global UserData, Trades
    if userID != "" and key in UserData[userID]["pending"]:
        if userID not in Trades[key]["markedAsCompletedBy"]:
            Trades[key]["markedAsCompletedBy"].append(userID)
        if len(Trades[key]["markedAsCompletedBy"]) == 2:
            Trades[key]["completed"] = True
            for user in Trades[key]["markedAsCompletedBy"]:
                try:
                    UserData[user]["completedTrades"].append(key)
                    UserData[user]["pending"].remove(key)
                    UserData[user]["tokens"] += 1
                except ValueError:
                    continue
            sendNotification(Trades[key]["acceptedBy"], "Trade", "You completed the trade with " + Trades[key]["ownerUsername"] + "! Congratulations!", False, "/static/images/profile/" + UserData[Trades[key]["owner"]]["profilePicture"])
            sendNotification(Trades[key]["owner"], "Trade", "You completed the trade with " + Trades[key]["acceptedByUsername"] + "! Congratulations!", False, "/static/images/profile/" + UserData[Trades[key]["acceptedBy"]]["profilePicture"])
        else:
            if Trades[key]["owner"] == userID:
                sendNotification(Trades[key]["acceptedBy"], "Trade", Trades[key]["ownerUsername"] +  " has marked the trade as completed.", False, "/static/images/profile/" + UserData[userID]["profilePicture"])
            else:
                sendNotification(Trades[key]["owner"], "Trade", Trades[key]["acceptedByUsername"] +  " has marked the trade as completed.", False, "/static/images/profile/" + UserData[Trades[key]["acceptedBy"]]["profilePicture"])

        dumpUserData()
        dumpTrades()
        return 0, "Trade completed!", 1
    else:
        return 1, "Error", -1
    
def validateData():
    global ValidateDataCheck
    if time.time() - ValidateDataCheck > 1:
        write = 0
        with open("updateData.txt", "r+") as file:
            data = str(file.read())
            if data == "0":
                write = 0
            else:
                write = 1
                openDataFiles()
        if write == 1:
            with open("updateData.txt", "w") as file:
                file.write("0")

        ValidateDataCheck = time.time()
    
def getListings(userID):
    global Trades, UserData
    if userID in UserData.keys():
        list = []
        for tradeID in UserData[userID]["trades"]:
            try:
                list.append(Trades[str(tradeID)])
            except KeyError:
                continue
        return list
    else:
        return "UserID does not exist!"
    
def rejectFriendRequest(userID, user2ID):
    global UserData
    if userID != "" and user2ID != "":
        try:
            UserData[userID]["friendRequests"]["received"].remove(user2ID)
        except ValueError:
            pass
        dumpUserData()
    return 0, "User rejected", 1

def calculateValue(trade):
    global Pets, UserData
    value = 0
    for pet in trade:
        keyValue = ""
        if pet["regular"] == 1:
            keyValue += "rvalue"
        elif pet["neon"] == 1:
            keyValue += "nvalue"
        elif pet["mega"] == 1:
            keyValue += "mvalue"
        else:
            keyValue += "rvalue"
        if pet["fly"] == 1 and pet["ride"] == 1:
            keyValue += " - fly&ride"
        elif pet["fly"] == 1:
            keyValue += " - fly"
        elif pet["ride"] == 1:
            keyValue += " - ride"
        try:
            value += Pets[str(pet["id"])][keyValue]
        except KeyError:
            value += Pets[str(pet["id"])]["value"]
    return value


def createListing(userID, trade1, trade2, public = True, visibleTo = "all", extra = 0):
    global Trades, UserData
    if userID != "" and len(trade1) > 0 and len(trade2) > 0:
        UserData[userID]["trades"].append(str(len(Trades)))
        giveValue, takeValue = calculateValue(trade1), calculateValue(trade2)
        trade = {
            "owner":userID,
            "ownerUsername":UserData[userID]["username"],
            "ownerRobloxUsername":UserData[userID]["robloxUsername"],
            "offer":{"give":trade1, "take":trade2, "giveValue":giveValue, "takeValue":takeValue},
            "extraSharkValueRequested":extra,
            "completed":False,
            "acceptedBy":None,
            "acceptedByUsername":None,
            "acceptedByRobloxUsername":None,
            "public":public,
            "visibleTo":visibleTo,
            "customOffers":[],
            "createdAt":time.time(),
            "views":[],
            "markedAsCompletedBy":[],
            "status":"Pending",

        }
        tradeID = str(len(Trades))
        Trades[tradeID] = trade
        dumpUserData()
        dumpTrades()
        return 0, tradeID, 1
    else:
        if len(trade1) > 0 and len(trade2) > 0:
            return 1, "User not logged in!", -1
        else:
            return 3, "Invalid trade!", -1
        
def updateViewsOnTrade(userID, user2ID, index):
    global UserData, Trades
    if userID != "":
        if userID not in Trades[UserData[user2ID]["trades"][index]]["views"]:
            Trades[UserData[user2ID]["trades"][index]]["views"].append(userID)
            dumpTrades()

def updateViewsOnTradeWithKey(userID, key):
    global UserData, Trades
    if userID != "" and key in Trades.keys():
        if userID not in Trades[key]["views"]:
            Trades[key]["views"].append(userID)
            dumpTrades()
            return 0, "View added", 1
        else:
            return 1, "You have already viewed this", 1
    else:
        return 2, "User not logged in!", -1

def getUnreadNotifications(userID):
    global UserData
    output = []
    if userID != "":
        try:
            extra = 0
            for notification in reversed(UserData[userID]["notifications"]):
                if notification["read"] == False:
                    if len(output) < 5:
                        output.append(notification)
                    else:
                        extra += 1
                else:
                    break
            if extra > 0:
                output.append({
                    "head":"",
                    "body":f"+{extra} more",
                    "read":False,
                    "important":False,
                    "image":"blank",
                    "created":time.time(),
                })
        except Exception:
            return 0, "Critical Error", -1
        if output == []:
            return 2, "Nothing found", 1
        return 3, output, 1
    else:
        return 1, "User not logged n!", -1



def removeListing(userID, index):
    global UserData, Trades
    if userID != "":
        if len(UserData[userID]["trades"]) > int(index):
            Trades[str(UserData[userID]["trades"][int(index)])]["completed"] = True
            if Trades[str(UserData[userID]["trades"][int(index)])]["visibleTo"] != "all":
                for user in Trades[str(UserData[userID]["trades"][int(index)])]["visibleTo"]:
                    UserData[user]["trades"].append(str(UserData[userID]["trades"][int(index)]))
                dumpUserData()
                dumpTrades()
            return 2, "Trade removed!", 1
        else:
            return 1, "Can't delete this trade!", 0
    else:
        return 0, "Not logged in!", -1
    
def saveListing(userID, index, trade1, trade2):
    global UserData, Trades
    if userID in UserData.keys():
        if len(UserData[userID]["trades"]) > int(index):
            Trades[str(UserData[userID]["trades"][int(index)])]["offer"]["give"] = trade1
            Trades[str(UserData[userID]["trades"][int(index)])]["offer"]["take"] = trade2
            dumpUserData()
            dumpTrades()
            return 2, "Trade updated!", 1
        else:
            return 1, "Can't modify this trade!", 0
    else:
        return 0, "Not logged in!", -1

def resetPassword(email = ""):
    if email == "":
        return 0, "Bad Request 100 # Missing arguments", -1
    else:
        randomString = generateRandomString(40)
        while randomString in ResetPassword:
            randomString = generateRandomString(40)
        userID = ""
        for user, userdata in UserData.items():
            if email == userdata["email"]:
                userID = user
        if userID == "":
            return 2, "Email not found!", 0
        ResetPassword[randomString] = {
            "time":time.time(),
            "userID":userID
        }
        with open("data/ResetPassword.json", "w") as file:
            json.dump(ResetPassword, file, indent=4, ensure_ascii=True)
        sendResetPasswordEmail(email, randomString)
        return 1, "Email sent!", 1
    
def resetPasswordWithID(tempID = ""):
    if tempID == "":
        return 0, "Bad Request 100 # Missing arguments"
    else:
        if tempID in ResetPassword:
            if time.time() - ResetPassword[tempID]["time"] > 900:
                return 2, "Time expired!", 0
            else:
                loginUnsafe(ResetPassword[tempID]["userID"])
                return 3, ResetPassword[tempID]["userID"], 1
        else:
            return 1, "ID invalid!", 0

def modifyPreference(userID, preference, value):
        try:
            UserData[userID]["preferences"][preference] = int(value)
            flask.session['userData'] = cookifyUserData(UserData[flask.session.get("userID", "")])
            with open("data/UserData.json", "w") as file:
                json.dump(UserData, file, indent=4, ensure_ascii=True)
            return 0, "success", 1
        except KeyError:
            return 1, "error", -1

def modifyMisc(userID, misc, value):
        try:
            UserData[userID]["settings"][misc] = int(value)
            flask.session['userData'] = cookifyUserData(UserData[flask.session.get("userID", "")])
            with open("data/UserData.json", "w") as file:
                json.dump(UserData, file, indent=4, ensure_ascii=True)
            return 0, "success", 1
        except KeyError:
            return 1, "error", -1

def sendNotification(userID, head, body, important, image):
    global UserData
    if userID == "all":
        for user in UserData.keys():
            UserData[user]["notifications"].append({
                "head":head,
                "body":body,
                "read":False,
                "important":important,
                "image":image,
                "created":time.time()
            })
        with open("data/UserData.json", "w") as file:
            json.dump(UserData, file, indent=4, ensure_ascii=True)
        return 3, "Success", 1
    else:
        try:
            UserData[str(userID)]["notifications"].append(
                {
                    "head":head,
                    "body":body,
                    "read":False,
                    "important":important,
                    "image":image,
                    "created":time.time()
            })
            dumpUserData()
            return 2, "Success", 1
        except KeyError:
            id, output, success = searchUpAccount(userID)
            if success == 1:
                userID = str(output)
                UserData[userID]["notifications"].append({
                        "head":head,
                        "body":body,
                        "read":False,
                        "important":important,
                        "image":image,
                        "created":time.time()
                })
                dumpUserData()
                return 1, "Success", 1
            else:
                return 0, "Failed", -1

def changeUserData(path, value):
    exec("UserData" + path + " = " + str(value))

def modifyATrade():
    pass

def placeCustomOffer():
    pass

def sendFriendRequest(userID = -1, friendID = -1):
    global UserData
    if userID != -1 and userID != "":
        if friendID != -1 and friendID != "":
            sentRequest = 0
            if userID != friendID:
                    if userID in UserData[friendID]["blocked"]:
                        return 6, "This user has blocked you!", -1
                    else:
                        if not userID in UserData[friendID]["friendRequests"]["received"] and not friendID in UserData[userID]["friendRequests"]["sent"]:
                            UserData[friendID]["friendRequests"]["received"].append(userID)
                            UserData[userID]["friendRequests"]["sent"].append(friendID)
                            sentRequest = 1
                            if friendID in UserData[userID]["friendRequests"]["sent"] and friendID in UserData[userID]["friendRequests"]["received"]:
                                sentRequest = 0
                                UserData[userID]["friends"].append(friendID)
                                UserData[userID]["friendRequests"]["received"].pop(UserData[userID]["friendRequests"]["received"].index(friendID))
                                UserData[userID]["friendRequests"]["sent"].pop(UserData[userID]["friendRequests"]["sent"].index(friendID))
                            if userID in UserData[friendID]["friendRequests"]["sent"] and userID in UserData[friendID]["friendRequests"]["received"]:
                                sentRequest = 0
                                UserData[friendID]["friends"].append(userID)
                                UserData[friendID]["friendRequests"]["received"].pop(UserData[friendID]["friendRequests"]["received"].index(userID))
                                UserData[friendID]["friendRequests"]["sent"].pop(UserData[friendID]["friendRequests"]["sent"].index(userID))
                            if sentRequest == 0:
                                sendNotification(friendID, "Friends", "You are now friends with " + str(UserData[userID]["username"]) + "!", False, "/static/images/profile/" + UserData[userID]["profilePicture"])
                                flask.session['userData'] = cookifyUserData(UserData[userID])
                                return 6, "You are now friends!", 1
                        else:
                            sentRequest = -1
                            return 0, "You have already sent a friend request to that person!", 0
                        if sentRequest == 1:
                            with open("data/UserData.json", "w") as file:
                                json.dump(UserData, file, indent=4, ensure_ascii=True)
                            sendNotification(friendID, "Friends", "You just got a friend request from " + str(UserData[userID]["username"]) + "!", False, "/static/images/profile/" + UserData[userID]["profilePicture"])
                            flask.session['userData'] = cookifyUserData(UserData[userID])
                            return 1, "Friend request sent!", 1
                        elif sentRequest == 0:
                            return 2, "User not found!", 0
            else:
                return 3, "Bad Request 401 # You can't send a friend request to yourself!", -1
        else:
            return 4, "Bad Request 100 # Missing arguments", -1
    else:
        return 5, "Bad Request 300 # You are not logged in!", -1
    
def getPets():
    global Pets
    return Pets

def addPetToInventory(user, pet, fly, ride, regular, neon, mega):
    global UserData
    if user != "":
        if (int(regular) + int(neon) + int(mega)) > 1 or 1 in (1 for x in [int(fly), int(ride), int(regular), int(neon), int(mega)] if x != 0 and x != 1):
            return 2, "Manipulated information", -1
        UserData[user]["inventory"].append({
            "id":pet,
            "fly":int(fly),
            "ride":int(ride),
            "regular":int(regular),
            "neon":int(neon),
            "mega":int(mega)
        })
        dumpUserData()
        if user == flask.session.get('userID', ""):
            flask.session['userData'] = cookifyUserData(UserData[user])
        return 1, "Success", 1
    else:
        return 0, "Not logged in", -1
    
def removeFriend(userID, friendID):
    global UserData
    if userID != "" and friendID != "":
        try:
            if friendID in UserData[userID]["friends"] and userID in UserData[friendID]["friends"]:
                UserData[userID]["friends"].remove(friendID)
                UserData[friendID]["friends"].remove(userID)
                dumpUserData()
                flask.session['userData'] = cookifyUserData(UserData[userID])
                return 1, "Removed friend!", 1
            else:
                return 2, "You are not even friends!", 0
        except KeyError:
            return 0, "FriendID doesn't exist", -1
        
def block(userID, user2ID):
    global UserData
    if userID != "" and user2ID != "":
        if user2ID not in UserData[userID]["blocked"]:
            UserData[userID]["blocked"].append(user2ID)
        if user2ID in UserData[userID]["friends"]:
            try:
                UserData[userID]["friends"].remove(user2ID)
                UserData[user2ID]["friends"].remove(userID)
            except ValueError:
                pass
        if user2ID in UserData[userID]["friendRequests"]["sent"]:
            try:
                UserData[userID]["friendRequests"]["sent"].remove(user2ID)
                UserData[user2ID]["friendRequests"]["received"].remove(userID)
            except ValueError:
                pass
        if user2ID in UserData[userID]["friendRequests"]["received"]:
            try:
                UserData[userID]["friendRequests"]["received"].remove(user2ID)
                UserData[user2ID]["friendRequests"]["sent"].remove(userID)
            except ValueError:
                pass
    flask.session['userData'] = cookifyUserData(UserData[userID])
    dumpUserData()
    return 0, "User blocked", 1

def unblock(userID, user2ID):
    global UserData
    if userID != "" and user2ID != "":
        if user2ID in UserData[userID]["blocked"]:
            UserData[userID]["blocked"].remove(user2ID)
    flask.session['userData'] = cookifyUserData(UserData[userID])
    dumpUserData()
    return 0, "User unblocked", 1

def getTradesWithCategory(category):
    pass

def acceptTradeWithKey(userID, key):
    global UserData, Trades
    key = str(key)
    if userID != "" and key in Trades.keys():
        if str(Trades[key]["acceptedBy"]) == "None" and Trades[key]["completed"] == False and ((Trades[key]["public"] == False and userID in Trades[key]["visibleTo"]) or Trades[key]["public"] == True):
            Trades[key]["acceptedBy"] = userID
            Trades[key]["acceptedByUsername"] = UserData[userID]["username"]
            Trades[key]["acceptedByRobloxUsername"] = UserData[userID]["robloxUsername"]
            Trades[key]["public"] = False
            Trades[key]["visibleTo"] = [userID, Trades[key]["owner"]]
            if key in UserData[userID]["inbox"]:
                UserData[userID]["inbox"].remove(key)
            if key not in UserData[userID]["pending"]:
                UserData[userID]["pending"].append(key)
            if key in UserData[Trades[key]["owner"]]["inbox"]:
                UserData[Trades[key]["owner"]]["inbox"].remove(key)
            if key not in UserData[Trades[key]["owner"]]["pending"]:
                UserData[Trades[key]["owner"]]["pending"].append(key)
            sendNotification(Trades[key]["owner"], "Trade", "One of your listings has been accepted by " + UserData[userID]["username"] + ". Make sure to contact '" + UserData[userID]["robloxUsername"] + "' through roblox!", False, "/static/images/profile/" + UserData[Trades[key]["owner"]]["profilePicture"])
        dumpUserData()
        dumpTrades()
        return 1, "Success", 1
    else:
        return 0, "Error", -1
    
def rejectTradeWithKey(userID, key):
    global UserData, Trades
    if userID != "" and key in UserData[userID]["inbox"]:
        if key in UserData[userID]["inbox"]:
            Trades[key]["completed"] = True
            UserData[userID]["inbox"].remove(key)
        dumpUserData()
        return 1, "Success", 1
    else:
        return 0, "Error", -1

    
def removePetFromInventory(user, pet):
    global UserData
    if user != "":
        UserData[user]["inventory"].pop(int(pet))
        dumpUserData()
        if user == flask.session.get('userID', ""):
            flask.session['userData'] = cookifyUserData(UserData[user])
        return 1, "Success", 1
    else:
        return 0, "Not logged in", -1
    
def addPetToWishlist(user, pet, fly, ride, regular, neon, mega):
    global UserData
    if user != "":
        if (int(regular) + int(neon) + int(mega)) > 1 or 1 in (1 for x in [int(fly), int(ride), int(regular), int(neon), int(mega)] if x != 0 and x != 1):
            return 2, "Manipulated information", -1
        UserData[user]["wishlist"].append({
            "id":pet,
            "fly":int(fly),
            "ride":int(ride),
            "regular":int(regular),
            "neon":int(neon),
            "mega":int(mega)
        })
        dumpUserData()
        if user == flask.session.get('userID', ""):
            flask.session['userData'] = cookifyUserData(UserData[user])
        return 1, "Success", 1
    else:
        return 0, "Not logged in", -1
    
def removePetFromWishlist(user, pet):
    global UserData
    if user != "":
        UserData[user]["wishlist"].pop(int(pet))
        dumpUserData()
        if user == flask.session.get('userID', ""):
            flask.session['userData'] = cookifyUserData(UserData[user])
        return 1, "Success", 1
    else:
        return 0, "Not logged in", -1
    
def dumpAllData():
    global UserData, Trades, ResetPassword, Pets
    with open("data/UserData.json", "w") as file:
        json.dump(UserData, file, indent=4, ensure_ascii=True)
    with open("data/Trades.json", "w") as file:
        json.dump(Trades, file, indent=4, ensure_ascii=True)
    with open("data/ResetPassword.json", "w") as file:
        json.dump(ResetPassword, file, indent=4, ensure_ascii=True)
    with open("data/Pets.json", "w") as file:
        json.dump(Pets, file, indent=4, ensure_ascii=True)

            
def openDataFiles():
    global UserData, Trades, ResetPassword, Pets
    try:
        with open("data/UserData.json", "r+") as file:
            try:
                UserData = dict(json.load(file))
            except json.decoder.JSONDecodeError:
                UserData = {}
                with open("data/UserData.json", "w") as file:
                    print("Couldn't read the UserData file. Creating a new empty one!")
                    file.write("{}")
    except FileNotFoundError:
        with open("data/UserData.json", "w") as file:
            print("No file found, creating new UserData json file.")
            file.write("{}")
        UserData = {}

    try:
        with open("data/Trades.json", "r+") as file:
            try:
                Trades = dict(json.load(file))
            except json.decoder.JSONDecodeError:
                Trades = {}
                with open("data/Trades.json", "w") as file:
                    file.write("{}")
    except FileNotFoundError:
        with open("data/Trades.json", "w") as file:
            file.write("{}")
        Trades = {}

    try:
        with open("data/ResetPassword.json", "r+") as file:
            try:
                ResetPassword = dict(json.load(file))
            except json.decoder.JSONDecodeError:
                ResetPassword = {}
                with open("data/ResetPassword.json", "w") as file:
                    file.write("{}")
    except FileNotFoundError:
        with open("data/ResetPassword.json", "w") as file:
            file.write("{}")

    try:
        with open("data/Pets.json", "r+") as file:
            try:
                Pets = dict(json.load(file))
            except json.decoder.JSONDecodeError:
                Pets = {}
                with open("data/Pets.json", "w") as file:
                    file.write("{}")
    except FileNotFoundError:
        with open("data/Pets.json", "w") as file:
            file.write("{}")
        Pets = {}

def cleanseTrades():
    global Trades, UserData
    for userID, userData in UserData.items():
        list = []
        for trade in userData["trades"]:
            if trade in Trades.keys():
                list.append(trade)
        UserData[userID]["trades"] = list

        list = []
        for trade in userData["inbox"]:
            if trade in Trades.keys():
                list.append(trade)
        UserData[userID]["inbox"] = list

        list = []
        for trade in userData["pending"]:
            if trade in Trades.keys():
                list.append(trade)
        UserData[userID]["pending"] = list

        list = []
        for trade in userData["completedTrades"]:
            if trade in Trades.keys():
                list.append(trade)
        UserData[userID]["completedTrades"] = list


def getTradesForMainPage(userID):
    global Trades, UserData
    suggested = {}
    recent = {}
    overpay = {}
    inventory = {}
    smallTrade = {}
    mediumTrade = {}
    bigTrade = {}
    megaTrade = {}
    randomTrade = {}
    if len(Trades.keys()) > 0:  
        output_trades = []
        suggested_trades = []
        recent_trades = []
        overpay_trades = []
        for x in range(200):
            counter = 0
            random_trade = random.randint(0, len(Trades) - 1)
            while counter < 10 and random_trade in output_trades:
                random_trade = random.randint(0, len(Trades) - 1)
                counter += 1
            if counter < 10:
                output_trades.append(random_trade)
                key = str(random_trade)

                recentPoints = 1000000 / (time.time() + 1 - Trades[key]["createdAt"])
                inventoryPoints = 1
                
                giveValue = Trades[key]["offer"]["giveValue"]
                for pet in Trades[key]["offer"]["give"]:
                    if userID != "":
                        if str(pet["id"]) in UserData[userID]["inventory"]:
                            inventoryPoints *= 2

                takeValue = Trades[key]["offer"]["takeValue"]
                for pet in Trades[key]["offer"]["take"]:
                    if userID != "":
                        if str(pet["id"]) in UserData[userID]["wishlist"]:
                            inventoryPoints *= 2

                overpayPoints = int(takeValue - giveValue) / 10

                activeUserPoints = len(UserData[Trades[key]["owner"]]["completedTrades"]) / 2

                viewsPoints = len(Trades[key]["views"]) / 50

                suggestedPoints = int((inventoryPoints * viewsPoints) + activeUserPoints + 3 * overpayPoints + viewsPoints ** 2 + recentPoints * 0.001 + random.randint(5, 45))

                suggested_trades.append([suggestedPoints, key])
                recent_trades.append([recentPoints, key])
                overpay_trades.append([overpayPoints, key])
        
        suggested_trades.sort(key=lambda x: x[0],  reverse=True)
        suggested_trades = suggested_trades[:20]
        recent_trades.sort(key=lambda x: x[0],  reverse=True)
        recent_trades = recent_trades[:20]
        overpay_trades.sort(key=lambda x: x[0],  reverse=True)
        overpay_trades = overpay_trades[:20]

        for trade in suggested_trades:
            suggested[trade[1]] = Trades[trade[1]]

        for trade in recent_trades:
            recent[trade[1]] = Trades[trade[1]]

        for trade in overpay_trades:
            overpay[trade[1]] = Trades[trade[1]]

        return {"Suggested":suggested,"Recent":recent,"Overpay":overpay}
        





def generateListings(amount, user):
    global Pets    
    for x in range(amount):
        trade1 = []
        trade2 = []
        for y in range(0, random.randint(1, 10)):
            trade1.append({
                "id":random.randint(0, len(Pets.keys()) - 1),
                "fly":random.randint(0, 1),
                "ride":random.randint(0,1),
                "regular":1,
                "neon":0,
                "mega":0,
            })
        for y in range(0, random.randint(1, 10)):
            trade2.append({
                "id":random.randint(0, len(Pets.keys()) - 1),
                "fly":random.randint(0, 1),
                "ride":random.randint(0,1),
                "regular":1,
                "neon":0,
                "mega":0,
            })
        id, output, success = createListing(user, trade1, trade2, True, "all", random.randint(0,2))
        if success == 1:
            for y in range(0, random.randint(0, 10)):
                pets = []
                for z in range(0, random.randint(1, 16)):
                    pets.append({
                        "id":random.randint(0, len(Pets.keys()) - 1),
                        "fly":random.randint(0, 1),
                        "ride":random.randint(0,1),
                        "regular":1,
                        "neon":0,
                        "mega":0,
                    })
                addCustomOffer(user, output, pets)


openDataFiles()