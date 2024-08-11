from functions import *

openDataFiles()

cleanseTrades()

app = flask.Flask("__main__")
app.secret_key = str(encrypt(os.urandom(512).hex()))
app.permanent_session_lifetime = 60 * 60 * 24 * 7  # 7 Days

@app.route("/", methods=["GET", "POST"])
def indexPage():
    updateActivity("indexPage", flask.request.remote_addr)
    validateSession()
    validateData()
    output = ""
    if flask.request.method == "POST":
        args = dict(flask.request.form)
        action = args["action"]
        if action == "login":
            id, success = login(args["usernameOrEmail"], args["password"])
            if id == 1:
                args["password"] = ""
            if id == 2:
                args = {}
            if success == 1:
                return flask.render_template("index.html", storedWebData=args, message=output, loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", ""), trades=getTradesForMainPage(flask.session.get("userID", "")), pets=getPets())
            elif success == 0:
                return flask.render_template("index.html", storedWebData=args, message=output, loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", ""), trades=getTradesForMainPage(flask.session.get("userID", "")), pets=getPets())
            else: # -1
                return "ERROR!!!"
        elif action == "readNotifications":
            id, output, success = readNotifications(flask.session.get("userID", ""))
            if success == 1:
                return flask.render_template("index.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), trades=getTradesForMainPage(flask.session.get("userID", "")), pets=getPets())
            elif success == 0:
                return "ERROR"
            else:
                return "ERROR"
        else:
            return flask.render_template("index.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), trades=getTradesForMainPage(flask.session.get("userID", "")), pets=getPets())
    else: # GET
        return flask.render_template("index.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), trades=getTradesForMainPage(flask.session.get("userID", "")), pets=getPets())
    
@app.route("/signup", methods=["GET", "POST"])
def signUpPage():
    updateActivity("signUpPage", flask.request.remote_addr)
    validateSession()
    validateData()
    if flask.request.method == "POST":
        args = dict(flask.request.form)
        action = args["action"]
        if action == "switchToSignIn":
            return flask.redirect(flask.url_for("signInPage"))
        elif action == "createAccount":
            if args["email"] != args["confirmEmail"] or args["password"] != args["confirmPassword"]:
                return flask.render_template("signup.html", storedWebData=args, message="All the fields does not meet the requirement!", loggedIn=False, userID="", userData="", signUp=1)
            else:
                try:
                    if args["robloxUsername"]:
                        pass
                except KeyError:
                    args["robloxUsername"] = ""
                id, output, success = createAccount(args["username"], args["robloxUsername"], args["email"], args["password"])
                if success == 1:
                    return flask.redirect(flask.url_for("indexPage"))
                elif success == 0:
                    return flask.render_template("signup.html", storedWebData=args, message=output, loggedIn=False, userID="", userData="", signUp=1)
                else:
                    return "Error!"
        else:
            return "ERROR"
    else: #GET
        if flask.session.get("loggedIn", False):
            return flask.redirect(flask.url_for("indexPage"))
        else:
            return flask.render_template("signup.html", storedWebData={}, message="", loggedIn=False, userID="", userData="", signUp=1)
    
@app.route("/signin", methods=["GET", "POST"])
def signInPage():
    updateActivity("signInPage", flask.request.remote_addr)
    validateSession()
    validateData()
    if flask.request.method == "POST":
        args = dict(flask.request.form)
        action = args["action"]
        if action == "switchToSignUp":
            return flask.redirect(flask.url_for("signUpPage"))
        elif action == "goBack":
            return flask.redirect(flask.url_for("indexPage"))
        elif action == "signIn":
                id, output, success = login(args["email"], args["password"])
                if success == 1:
                    return flask.redirect(flask.url_for("indexPage"))
                elif success == 0:
                    return flask.render_template("signup.html", storedWebData={}, message=output, loggedIn=False, userID="", userData="", signUp=0)
                else: # -1
                    return "ERROR"
        else:
            return "ERROR"
    else: #GET
        if flask.session.get("loggedIn", False):
            return flask.redirect(flask.url_for("indexPage"))
        else:
            return flask.render_template("signup.html", storedWebData={}, message="", loggedIn=False, userID="", userData="", signUp=0)

@app.route("/reset-password", methods=["GET", "POST"])
def resetPasswordPage():
    updateActivity("resetPasswordPage", flask.request.remote_addr)
    validateSession()
    validateData()
    if flask.request.method == "POST":
        tempID = flask.request.args.get("tempID")
        if tempID:
            try:
                args = dict(flask.request.form)
                action = args["action"]
                if action == "resetPasswordLoggedIn":
                    id, output, success = changePasswordWithTempID(tempID, args["password"])
                    if success == 1:
                        return flask.redirect(flask.url_for("indexPage"))
                    else:
                        return "ERROR"
                else:
                    id, output, success = resetPasswordWithID(tempID)
                    if success == 1:
                        return flask.render_template("resetPassword.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=True, resetPassword=True)
                    elif success == 0:
                        return flask.render_template("resetPassword.html", storedWebData={}, message=output, loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=False, resetPassword=False)
                    else:
                        return "ERROR"
            except KeyError:
                id, output, success = resetPasswordWithID(tempID)
                if success == 1:
                    return flask.render_template("resetPassword.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=True, resetPassword=True)
                elif success == 0:
                    return flask.render_template("resetPassword.html", storedWebData={}, message=output, loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=False, resetPassword=False)
                else:
                    return "ERROR"
        else:
            args = dict(flask.request.form)
            action = args["action"]
            if action == "close":
                return flask.redirect(flask.url_for("indexPage"))
            elif action == "resetPassword":
                email = args["email"]
                id, output, success = resetPassword(email)
                if success == 1:
                    return flask.render_template("resetPassword.html", storedWebData={}, message=output, loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=True, resetPassword=False)
                elif success == 0:
                    return flask.render_template("resetPassword.html", storedWebData={}, message=output, loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=False, resetPassword=False)
                else:
                    return "ERROR"
            else:
                return "ERROR"
    else: #GET
        if flask.session.get("loggedIn", False) == True:
            return flask.render_template("resetPassword.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=True, resetPassword=True)
        else:
            tempID = flask.request.args.get("tempID")
            if tempID:
                id, output, success = resetPasswordWithID(tempID)
                if success == 1:
                    return flask.render_template("resetPassword.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=True, resetPassword=True)
                elif success == 0:
                    return flask.render_template("resetPassword.html", storedWebData={}, message=output, loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=False, resetPassword=False)
                else:
                    return "ERROR"
            else:
                return flask.render_template("resetPassword.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), checkEmail=False, resetPassword=False)
        
@app.route("/login", methods=["GET", "POST"])
def loginPage():
    updateActivity("loginPage", flask.request.remote_addr)
    validateSession()
    validateData()
    return flask.redirect(flask.url_for("signInPage"))

@app.route("/api", methods=["GET", "POST"])
def api():
    updateActivity("api", flask.request.remote_addr)
    validateSession()
    validateData()
    if flask.request.method == "POST":
        args = dict(flask.request.form)
        action = args["action"]
        if action == "readNotifications":
            id, output, success = readNotifications(flask.session.get("userID", ""))
            if success == 1:
                return flask.jsonify("SUCCESS")
            elif success == 0:
                return flask.jsonify("ERROR")
            else:
                return flask.jsonify("ERROR")
        elif action == "modifyPreference":
            if flask.session.get("userID", "") != "":
                id, output, success = modifyPreference(flask.session.get("userID", ""), args["preference"], args["value"])
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "modifyMisc":
            if flask.session.get("userID", "") != "":
                id, output, success = modifyMisc(flask.session.get("userID", ""), args["misc"], args["value"])
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR") 
        elif action == "logout":
            flask.session.clear()
            return flask.jsonify("SUCCESS")
        elif action == "addPetToInventory":
            id, output, success = addPetToInventory(flask.session.get("userID", ""), args["pet"], args["fly"], args["ride"], args["regular"], args["neon"], args["mega"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "removePetFromInventory":
            id, output, success = removePetFromInventory(flask.session.get("userID", ""), args["pet"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "createListing":
            id, output, success = createListing(flask.session.get("userID", ""), json.loads(args["trade1"]), json.loads(args["trade2"]))
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify(output)
        elif action == "removeListing":
            id, output, success = removeListing(flask.session.get("userID", ""), str(args["index"]))
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify(output)
        elif action == "saveListing":
            id, output, success = saveListing(flask.session.get("userID", ""), str(args["index"]), json.loads(args["trade1"]), json.loads(args["trade2"]))
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify(output)
        elif action == "addPetToWishlist":
            id, output, success = addPetToWishlist(flask.session.get("userID", ""), args["pet"], args["fly"], args["ride"], args["regular"], args["neon"], args["mega"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "removePetFromWishlist":
            id, output, success = removePetFromWishlist(flask.session.get("userID", ""), args["pet"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "sendFriendRequest":
            id, output, success = sendFriendRequest(flask.session.get("userID", ""), args["ID"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "removeFriend":
            id, output, success = removeFriend(flask.session.get("userID", ""), args["ID"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "acceptOffer":
            id, output, success = acceptOffer(flask.session.get("userID", ""), args["user"], args["listing"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "sendCustomOffer":
            id, output, success = sendCustomOffer(flask.session.get("userID", ""), args["user"], json.loads(args["trade1"]), json.loads(args["trade2"]))
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "searchPets":
            return flask.jsonify(searchPets(args["input"]))
        elif action == "search":
            id, output, success = search(args["input"])
            if output != "Nothing Found":
                return flask.jsonify({
                    "type":output[0],
                    "name":output[1],
                    "id":output[2]
                })
            else:
                return flask.jsonify("Nothing Found")
        elif action == "getFriendsDetails":
            return flask.jsonify(getFriendsDetails(flask.session.get("userID", "")))
        elif action == "getPendingDetails":
            return flask.jsonify(getPendingDetails(flask.session.get("userID", "")))
        elif action == "getBlockedDetails":
            return flask.jsonify(getBlockedDetails(flask.session.get("userID", "")))
        elif action == "block":
            id, output, success = block(flask.session.get("userID", ""), args["ID"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "unblock":
            id, output, success = unblock(flask.session.get("userID", ""), args["ID"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "rejectFriendRequest":
            id, output, success = rejectFriendRequest(flask.session.get("userID", ""), args["ID"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "getInbox":
            id, output, success = getInbox(flask.session.get("userID", ""))
            if success == 1:
                return flask.jsonify(output)
            else:
                return flask.jsonify("ERROR")
        elif action == "getRobloxUsername":
            id, output, success = getRobloxUsername(args["ID"])
            if success == 1:
                return flask.jsonify(output)
            else:
                return flask.jsonify(0)
        elif action == "acceptTradeWithKey":
            id, output, success = acceptTradeWithKey(flask.session.get("userID", ""), args["key"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "rejectTradeWithKey":
            id, output, success = rejectTradeWithKey(flask.session.get("userID", ""), args["key"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "getPending":
            id, output, success = getPending(flask.session.get("userID", ""))
            if success == 1:
                return flask.jsonify(output)
            else:
                return flask.jsonify("ERROR")
        elif action == "completeTradeWithKey":
            id, output, success = completeTradeWithKey(flask.session.get("userID", ""), args["key"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "getHistory":
            id, output, success = getHistory(flask.session.get("userID", ""))
            if success ==  1:
                return flask.jsonify(output)
            else:
                return flask.jsonify("ERROR")
        elif action == "setAsProfilePicture":
            id, output, success = setAsProfilePicture(flask.session.get("userID", ""), args["image"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "changeUsername":
            id, output, success = changeUsername(flask.session.get("userID", ""), args["username"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "changeRobloxUsername":
            id, output, success = changeRobloxUsername(flask.session.get("userID", ""), args["robloxUsername"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "changePassword":
            id, output, success = changePassword(flask.session.get("userID", ""), args["password"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "updateViewsOnTrade":
            id, output, success = updateViewsOnTrade(flask.session.get("userID", ""), args["user2ID"], args["index"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "updateViewsOnTradeWithKey":
            id, output, success = updateViewsOnTradeWithKey(flask.session.get("userID", ""), args["key"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify("ERROR")
        elif action == "getUnreadNotifications":
            id, output, success = getUnreadNotifications(flask.session.get("userID", ""))
            if success == 1:
                return flask.jsonify(output)
            else:
                return flask.jsonify("ERROR")
        elif action == "get20Notifications":
            id, output, success = get20Notifications(flask.session.get("userID", ""), args["loaded"])
            if success == 1:
                return flask.jsonify(output)
            else:
                return flask.jsonify("ERROR")
        elif action == "acceptOfferWithKey":
            id, output, success = acceptOfferWithKey(flask.session.get("userID", ""), args["key"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify(output)
        elif action == "addCustomOffer":
            id, output, success = addCustomOffer(flask.session.get("userID", ""), args["trade"], args["pets"])
            if success == 1:
                return flask.jsonify("SUCCESS")
            else:
                return flask.jsonify(output)
        elif action == "getUserData":
            id, output, success = getUserData(args["user"])
            if success == 1:
                return flask.jsonify(output)
            else:
                return flask.jsonify("ERROR")


        else:
            return flask.jsonify("ERROR")

    else: #GET
        return "ERROR"   
     
    
@app.route("/notifications", methods=["GET", "POST"])
def notificationsPage():
    updateActivity("notificationsPage", flask.request.remote_addr)
    validateSession()
    validateData()
    if flask.request.method == "POST":
        args = dict(flask.request.form)
        action = args["action"]
        if action == "logout":
            flask.session.clear()
            return flask.render_template("index.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}))
        else:
            return "ERROR"
    else: #GET
        if flask.session.get("loggedIn", False) == True:
            return flask.render_template("notifications.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}))
        else:
            return flask.redirect(flask.url_for("indexPage"))

@app.route('/user/<int:userID>', methods=["GET", "POST"])
def profilePage(userID):
    updateActivity("profilePage", flask.request.remote_addr)
    validateSession()
    validateData()
    id, output, success = searchUpAccount(userID)
    if success == 1:
        profileData = getDataFromIDWithoutDetails(userID)
        listings = getListings(str(userID))
        return flask.render_template("userPage.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), profileID=userID, profileData=profileData, pets=getPets(), profileListings=listings)
    else:
        return flask.render_template('siteUnavailable.html', storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), error=404)
    
@app.errorhandler(404)
def pageNotFound(error):
    validateSession()
    validateData()
    return flask.render_template('siteUnavailable.html', storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), error=error)

@app.route('/pet/<int:petID>', methods=["GET", "POST"])
def petPage(petID):
    updateActivity("petPage" + str(petID), flask.request.remote_addr)
    validateSession()
    validateData()
    return flask.render_template("pet.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), pets = getPets(), pet = str(petID))

@app.route('/user/<int:userID>/edit', methods=["GET", "POST"])
def editPage(userID):
    updateActivity("editPage", flask.request.remote_addr)
    validateSession()
    validateData()
    id, output, success = searchUpAccount(userID)
    if success == 1 and str(userID) == flask.session.get("userID", ""):
        return flask.render_template("edit.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), profilePictures=getProfilePictures())
    else:
        return flask.render_template('siteUnavailable.html', storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}), error=404)

@app.route("/support", methods=["GET", "POST"])
def supportPage():
    updateActivity("support", flask.request.remote_addr)
    validateSession()
    validateData()
    return flask.render_template("support.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}))

@app.route("/tos", methods=["GET"])
def tosPage():
    validateSession()
    return flask.render_template("tos.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}))

@app.route("/apply", methods=["GET"])
def applyPage():
    updateActivity("apply", flask.request.remote_addr)
    validateSession()
    validateData()
    return flask.render_template("apply.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}))

@app.route("/apply/application", methods=["GET"])
def applicationPage():
    updateActivity("application", flask.request.remote_addr)
    validateSession()
    validateData()
    return flask.render_template("application.html", storedWebData={}, message="", loggedIn=flask.session.get("loggedIn", False), userID=flask.session.get("userID", ""), userData=flask.session.get("userData", {}))

@app.cli.command("status")
def status():
    checkStatus()

#if __name__ == "__main__": 
#    from waitress import serve
#    serve(app, host="127.0.0.1", port=80)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
