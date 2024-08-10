window.addEventListener("DOMContentLoaded", (event) => {
    var footerQuickLinks1 = document.getElementById("footerQuickLinks1")
    var footerQuickLinks2 = document.getElementById("footerQuickLinks2")
    var helpCenter1 = document.getElementById("helpCenter1")
    var helpCenter2 = document.getElementById("helpCenter2")
    var footerMenu = document.getElementById("footerMenu")
    var footerAvailableOptions = document.getElementById("footerAvailableOptions")
    var footerLine = document.getElementById("footerLine")
    var footerSection = document.getElementById("footerSection")

    function updateFooter() {
        if (window.innerWidth > 1080) {
            footerQuickLinks1.style.display = "flex";
            footerQuickLinks2.style.display = "none";
            helpCenter1.style.display = "block";
            helpCenter2.style.display = "none";
            footerMenu.style.justifyContent = "space-between"
            footerAvailableOptions.style.justifyContent = "right"
            footerLine.style.width = "100%"
            footerLine.style.paddingBottom = "0px";
            footerSection.style.paddingRight = "3vw";
        } else {
            footerQuickLinks1.style.display = "none";
            footerQuickLinks2.style.display = "flex";
            helpCenter1.style.display = "none";
            helpCenter2.style.display = "block";
            footerMenu.style.justifyContent = "center"
            footerAvailableOptions.style.justifyContent = "center"
            footerLine.style.width = "450px"
            footerLine.style.paddingBottom = "0px";
            footerSection.style.paddingRight = "0px";
        }
    }

    window.addEventListener("resize", (event) => {
        updateFooter();
    });


    updateFooter();
});