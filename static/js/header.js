window.addEventListener("DOMContentLoaded", (event) => {
    var nav = document.querySelector("nav");
    var menuImage = document.getElementById("menuImage");
    var signUpImage = document.getElementById("signUpImage");
    var headerText = document.querySelectorAll(".headerText");
    var signInButtonHeader = document.getElementById("signInButtonHeader");
    var headerLogo = document.getElementById("headerLogo");
    var profilePicture = document.getElementById("profilePicture");
    var notificationIcon = document.getElementById("notificationIcon");
    var username = document.getElementById("username");
    var profileMenu = document.getElementById("profileMenu");
    var profileNotifications = document.getElementById("profileNotifications");
    var notificationCircle = document.getElementById("notificationCircle");
    var menuTextButton = document.getElementById("menuTextButton");
    var profileClick = 0
    var scrollY = 0

    var main = document.querySelector("main")

    var headerSearchBar = document.getElementById("headerSearchBar")
    var headerSearchBarMain = document.getElementById("headerSearchBarMain")
    var searchIcon = document.getElementById("searchIcon")
    var searchInput = document.getElementById("searchInput")

    var resultsPets = document.getElementById("resultsPets")

    var notificationsMenu = document.getElementById("notificationsMenu")

    var rem = Math.min(Math.max(Math.max(0.069444444 * window.innerWidth, 0.12345679012 * window.innerHeight), (2/3)), (8/3))

    function updateHeader() {

        if (window.innerWidth < 500*rem)  {
            headerSearchBar.style.display = "none"
            menuTextButton.style.display = "none"
        } else {
            headerSearchBar.style.display = "flex"
            menuTextButton.style.display = "flex"
        }

        if (window.innerWidth < 200*rem)  {
            headerLogo.style.display = "none"
        } else {
            headerLogo.style.display = "flex"
        }

        if (loggedIn == "True") {
            if (window.innerWidth < 400*rem) {
                notificationIcon.style.display = "none";
                username.style.display = "none";
                profileNotifications.style.display = "flex";
                profileNotifications.style.padding = "10px";
                notificationCountID.style.display = "none";
                notificationCircle.style.display = "none";
                username.style.paddingRight = "0px"
                notificationsMenu.style.marginRight = "max(14vw, 28vh)";
            } else {
                notificationIcon.style.display = "flex";
                username.style.display = "flex";
                profileNotifications.style.display = "none";
                profileNotifications.style.padding = "0px";
                notificationCountID.style.display = "flex";
                notificationCircle.style.display = "flex";
                username.style.paddingRight = "3vw"
                notificationsMenu.style.marginRight = "max(23vw, 46vh)";
            };
        }
        

    }
    if (loggedIn == "True") {
        profilePicture.addEventListener("click", (event) => {
            if (profileMenu.style.display == "flex") {
                profileMenu.style.display = "none";
            } else {
                profileMenu.style.display = "flex";
                profileClick = 1
            }
        });
        profileMenu.addEventListener("click", (event) => {
            profileClick = 1
        })
    };

    if (document.title == "Index") {
        window.addEventListener("scroll", (event) => {
            if (loggedIn == "True") {
                profileMenu.style.display = "none";
            };
            scrollY = window.scrollY;
            startY = window.innerHeight * 0.25
            endY = window.innerHeight * 0.6
            if (scrollY < startY) {
                headerLogo.style.filter = "invert(100%) contrast(200%)";
                menuImage.style.filter = "invert(100%) contrast(200%)";
                nav.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 0) 0%, rgb(235, 229, 220, 0) 50%, rgb(253, 249, 234, 0) 100%)";
                headerText.forEach(text => {
                    text.style.color = "rgb(255, 255, 255)"
                });
                if (loggedIn == "True") {
                    profileMenu.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 0.25) 0%, rgb(235, 229, 220, 0.25) 50%, rgb(253, 249, 234, 0.25) 100%)";
                    notificationIcon.style.filter = "invert(1) contrast(2)";
                };
            } else if (scrollY < endY) {
                headerLogo.style.filter = "invert(" + (100 - ((scrollY - startY) / 2)).toString() + "%) contrast(" + (200 - ((scrollY - startY) / 2)).toString() + "%)";
                menuImage.style.filter = "invert(" + (100 - ((scrollY - startY) / 2)).toString() + "%) contrast(" + (200 - ((scrollY - startY) / 2)).toString() + "%)";
                nav.style.background = "linear-gradient(135deg, rgb(243, 231, 214, " + (((scrollY - startY) / 2.5) / 100).toString() + ") 0%, rgb(235, 229, 220, " + (((scrollY - startY) / 2.5) / 100).toString() + ") 50%, rgb(253, 249, 234, " + (((scrollY - startY) / 2.5) / 100).toString() + ") 100%)";
                headerText.forEach(text => {
                    text.style.color = "rgb(" + (255 - (scrollY - startY) / 2 * 2.55) + ", " + (255 - (scrollY - startY) / 2 * 2.55) + ", " + (255 - (scrollY - startY) / 2 * 2.55) + ")";
                });
                if (loggedIn == "True") {
                    notificationIcon.style.filter = "invert(" + (100 - ((scrollY - startY) / 2)).toString() + "%) contrast(" + (200 - ((scrollY - startY) / 2)).toString() + "%)";
                    profileMenu.style.background = "linear-gradient(135deg, rgb(243, 231, 214, " + (0.25 + ((scrollY - startY) / 2) / 100).toString() + ") 0%, rgb(235, 229, 220, " + (0.25 + ((scrollY - startY) / 2) / 100).toString() + ") 50%, rgb(253, 249, 234, " + (0.25 + ((scrollY - startY) / 2) / 100).toString() + ") 100%)";
                };
            } else {
                headerLogo.style.filter = "invert(0%) contrast(100%)"
                menuImage.style.filter = "invert(0%) contrast(100%)"
                nav.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 1) 0%, rgb(235, 229, 220, 1) 50%, rgb(253, 249, 234, 1) 100%)";
                headerText.forEach(text => {
                    text.style.color = "rgb(0, 0, 0)"
                });
                if (loggedIn == "True") {
                    profileMenu.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 1) 0%, rgb(235, 229, 220, 1) 50%, rgb(253, 249, 234, 1) 100%)";
                    notificationIcon.style.filter = "invert(0) contrast(1)";
                };
            };
        });
    } else {
        headerLogo.style.filter = "invert(0%) contrast(100%)"
        menuImage.style.filter = "invert(0%) contrast(100%)"
        nav.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 1) 0%, rgb(235, 229, 220, 1) 50%, rgb(253, 249, 234, 1) 100%)";
        if ( loggedIn == "True") {
            profileMenu.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 1) 0%, rgb(235, 229, 220, 1) 50%, rgb(253, 249, 234, 1) 100%);"
        };
        headerText.forEach(text => {
            text.style.color = "rgb(0, 0, 0)"
        });
        if (loggedIn == "True") {
            notificationIcon.style.filter = "invert(0%) contrast(100%)";
        };        
    };

    if (document.title == "Index") {
        if (loggedIn == "True") {
            profileMenu.style.display = "none";
        };
        scrollY = window.scrollY;
        startY = window.innerWidth * 0.45
        endY = window.innerWidth * 0.5625
        if (scrollY < startY) {
            headerLogo.style.filter = "invert(100%) contrast(200%)";
            menuImage.style.filter = "invert(100%) contrast(200%)";
            nav.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 0) 0%, rgb(235, 229, 220, 0) 50%, rgb(253, 249, 234, 0) 100%)";
            headerText.forEach(text => {
                text.style.color = "rgb(255, 255, 255)"
            });
            if (loggedIn == "True") {
                profileMenu.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 0.25) 0%, rgb(235, 229, 220, 0.25) 50%, rgb(253, 249, 234, 0.25) 100%)";
            };
        } else if (scrollY < endY) {
            headerLogo.style.filter = "invert(" + (100 - ((scrollY - startY) / 2)).toString() + "%) contrast(" + (200 - ((scrollY - startY) / 2)).toString() + "%)";
            menuImage.style.filter = "invert(" + (100 - ((scrollY - startY) / 2)).toString() + "%) contrast(" + (200 - ((scrollY - startY) / 2)).toString() + "%)";
            nav.style.background = "linear-gradient(135deg, rgb(243, 231, 214, " + (((scrollY - startY) / 2.5) / 100).toString() + ") 0%, rgb(235, 229, 220, " + (((scrollY - startY) / 2.5) / 100).toString() + ") 50%, rgb(253, 249, 234, " + (((scrollY - startY) / 2.5) / 100).toString() + ") 100%)";
            headerText.forEach(text => {
                text.style.color = "rgb(" + (255 - (scrollY - startY) / 2 * 2.55) + ", " + (255 - (scrollY - startY) / 2 * 2.55) + ", " + (255 - (scrollY - startY) / 2 * 2.55) + ")";
            });
            if (loggedIn == "True") {
                profileMenu.style.background = "linear-gradient(135deg, rgb(243, 231, 214, " + (0.25 + ((scrollY - startY) / 2) / 100).toString() + ") 0%, rgb(235, 229, 220, " + (0.25 + ((scrollY - startY) / 2) / 100).toString() + ") 50%, rgb(253, 249, 234, " + (0.25 + ((scrollY - startY) / 2) / 100).toString() + ") 100%)";
            };
        } else {
            headerLogo.style.filter = "invert(0%) contrast(100%)"
            menuImage.style.filter = "invert(0%) contrast(100%)"
            nav.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 1) 0%, rgb(235, 229, 220, 1) 50%, rgb(253, 249, 234, 1) 100%)";
            headerText.forEach(text => {
                text.style.color = "rgb(0, 0, 0)"
            });
            if (loggedIn == "True") {
                profileMenu.style.background = "linear-gradient(135deg, rgb(243, 231, 214, 1) 0%, rgb(235, 229, 220, 1) 50%, rgb(253, 249, 234, 1) 100%)";
            };
        };
    };

    window.addEventListener("resize", (event) => {
        updateHeader();
    });

    window.addEventListener("click", (event) => {
        if (loggedIn == "True") {
            if (profileMenu.style.display == "flex") {
                if (profileClick == 1) {
                    profileClick = 0
                } else {
                    profileMenu.style.display = "none";
                };
            };
        };
    })

    updateHeader();

    searchInput.addEventListener("input", (event) => {
        formData = new FormData();
        formData.append('input', searchInput.value)
        formData.append('action', "searchPets");

        fetch('/api', {
        method: 'POST',
        body: formData
        })
        .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
        })
        .then(data => {
            resultsPets.innerHTML = ""
            for (const i in data[0]) {
                const a = document.createElement("a")
                a.className = "resultPet"
                if (window.innerHeight < 600) {
                    a.style.height = "22.2px"
                } else if (window.innerHeight < 1080) {
                    a.style.height = "3.7vh"
                } else {
                    a.style.height = "40px"
                }
                const p = document.createElement("p")
                p.innerText = data[0][i]["name"]
                if (window.innerHeight < 600) {
                    p.style.fontSize = "10px"
                } else if (window.innerHeight < 1080) {
                    p.style.fontSize = "1.66vh"
                } else {
                    p.style.fontSize = "18px"
                }


                const img = document.createElement("img")
                img.src = data[0][i]["image"].slice(2)
                if (window.innerHeight < 600) {
                    img.style.height = "22.2px"
                } else if (window.innerHeight < 1080) {
                    img.style.height = "3.7vh"
                } else {
                    img.style.height = "40px"
                }
                img.style.aspectRatio = "1/1"
                a.appendChild(p)
                a.appendChild(img)
                a.href = "/pet/" + data[1][i]
                if (parseInt(i) + 1 == data[0].length) {
                    a.style.borderBottom = "0.5px solid lightgray"
                }
                resultsPets.appendChild(a)
            }
            headerSearchBar.style.marginTop = "0px"
            if (data[0].length > 0) {
                headerSearchBar.style.paddingBottom = "8%"
            } else {
                headerSearchBar.style.paddingBottom = "0%"
            }

            headerSearchBar.style.marginTop = (headerSearchBar.getBoundingClientRect().height - (headerSearchBarMain.getBoundingClientRect().height + 2)).toString() + "px"
            
            updateHeader()
        })
        .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        });
    })

    searchInput.addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
            search()
        }
    })

    searchIcon.addEventListener("click", (event) => {
        search()
    })

    function search() {
        formData = new FormData();
        formData.append('input', searchInput.value)
        formData.append('action', "search");

        fetch('/api', {
        method: 'POST',
        body: formData
        })
        .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
        })
        .then(data => {
            if (data == "Nothing Found") {
                window.location.href = "/search/" + searchInput.value
            } else {
                if (data["type"] == "user") {
                    window.location.href = "/user/" + data["id"].toString()
                } else {
                    window.location.href = "/pet/" + data["id"].toString()
                }
            }
        })
        .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        });
    }


    //<p class="headerText">Notifications</p>
    //<div class="smallLine blackBackground notificationFlex"> &nbsp; </div>
    //{% for user, data in userData["notifications"].items() %}
    //    <div class="center" style="align-items:center;text-align:center;">
    //        {% if "/" in data['image'] %}
    //        <img style="width:15px;height:15px;margin-left:5px;" src="{{ url_for('static', filename=(data['image']))}}">
    //        {% else %}
    //            <img style="width:15px;height:15px;margin-left:5px;" src="{{ url_for('static', filename=('images/notifications/' + data['image']))}}">
    //        {% endif %}
    //        <div class="center smallPadding" style="flex-direction:column;">
    //            <h1 style="font-size:10px;margin:0px;">{{data["head"]}}</h1>
    //            <p style="font-size:8px;margin:0px;">{{data["body"]}}</p>
    //        </div>
    //</img></img>    </div>
    //{% endfor %}
    //<div class="smallLine blackBackground"> &nbsp; </div>
    //</img><p class="headerText lightHover" style="font-size:6px;color:white;"><a href="/notifications" class="bland headerText" style="color:white;">Read All Notifications</a></p>


});

