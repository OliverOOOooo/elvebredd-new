window.addEventListener("DOMContentLoaded", (event) => {
    var verifyForm = 0
    var emailID = document.getElementById("emailInput")
    var confirmEmailID = document.getElementById("confirmEmailInput")
    var passwordID = document.getElementById("passwordInput")
    var confirmPasswordID = document.getElementById("confirmPasswordInput")
    var emailMatchText = document.getElementById("emailMatchText")
    var passwordMatchText = document.getElementById("passwordMatchText")
    var minPasswordLengthText = document.getElementById("minPasswordLengthText")
    var createAccountButton = document.getElementById("createAccountButton")
    var changePasswordButton = document.getElementById("changePasswordButton")
    var minUsernameLengthText = document.getElementById("minUsernameLengthText")
    var usernameID = document.getElementById("usernameInput")
    var signInButton = document.getElementById("signInButton")

    var email = ""
    var confirmEmail = ""
    var password = ""
    var confirmPassword = ""
    var username = ""

    function updateSignUp() {
        if (emailID != null) {
            email = emailID.value
        } else {
            email = ""
        }
        if (confirmEmailID != null) {
            confirmEmail = confirmEmailID.value
        } else {
            confirmEmail = ""
        }
        if (passwordID != null) {
            password = passwordID.value
        } else {
            password = ""
        }
        if (confirmPasswordID != null) {
            confirmPassword = confirmPasswordID.value
        } else {
            confirmPassword = ""
        }
        if (usernameID != null) {
            username = usernameID.value
        } else {
            username = ""
        }
        verifyForm = 0
        if (email != "") {
            if (email === confirmEmail || confirmEmail === "") {
                if (emailMatchText != null) {
                    emailMatchText.style.display = "none";
                };
                if (confirmEmail != "") {
                    verifyForm += 1
                };
            } else if (emailMatchText != null) {
                emailMatchText.style.display = "block";
            };
        };
        if (password === confirmPassword || confirmPassword === "") {
            if (passwordMatchText != null) {
                passwordMatchText.style.display = "none";
            };
            if (confirmPassword != "") {
                verifyForm += 1
            };
        } else if (passwordMatchText != null) {
            passwordMatchText.style.display = "block";
        };
        if (password.length > 6 || password.length === 0) {
            if (minPasswordLengthText != null) {
                minPasswordLengthText.style.display = "none"
            };
            if (password.length != 0) {
                verifyForm += 1
            };
        } else if (minPasswordLengthText != null) {
            minPasswordLengthText.style.display = "block"
        };
        if (username.length > 2 || username.length === 0) {
            if (minUsernameLengthText != null) {
                minUsernameLengthText.style.display = "none"
            };
            if (username.length > 2 && username.length < 21) {
                verifyForm += 1
            };
        } else if (minUsernameLengthText != null) {
            minUsernameLengthText.style.display = "block"
        };
        if (createAccountButton != null) {
            if (verifyForm > 3) {
                createAccountButton.disabled = false
                createAccountButton.style.border = "1px solid rgb(0, 0, 0)"
            } else {
                createAccountButton.disabled = true
                createAccountButton.style.border = "1px solid rgb(180, 180, 180)"
            };
        } else if (changePasswordButton != null) {
            if (verifyForm > 1) {
                changePasswordButton.disabled = false
                changePasswordButton.style.border = "1px solid rgb(0, 0, 0)"
            } else {
                changePasswordButton.disabled = true
                changePasswordButton.style.border = "1px solid rgb(180, 180, 180)"
            };
        } else if (signInButton != null) {
            if (verifyForm > 0) {
                signInButton.disabled = false
                signInButton.style.border = "1px solid rgb(0, 0, 0)"
            } else {
                signInButton.disabled = true
                signInButton.style.border = "1px solid rgb(180, 180, 180)"
            };
        };
    };

    window.addEventListener("input", (event) => {
        updateSignUp();
    });

    updateSignUp();

});