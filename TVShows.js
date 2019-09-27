var listOfNames = []
function myname () {
fetch("http://localhost:8080/shows").then(function (response) {

    console.log("server response");
    response.json().then(function (data) {
        console.log("data received from server:", data);
        listOfNames = data;

        listOfNames.forEach(function () {
            
        });
    });

});
};
myname();
var addButton = document.querySelector("#add");
addButton.onclick = function () {

    var TVShowsInput = document.querySelector("#inputShow");
    var TVShowsValue = TVShowsInput.value;
    
    var bodyStr = "name=" + encodeURIComponent(TVShowsValue);
    fetch("http://localhost:8080/shows", {
        // request parameters:
        method: "POST",
        body: bodyStr,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function (response) {
        // handle the response
        console.log("server responded")
        myname();
    });

};

var list = document.querySelector("#text")
list.innerHTML = listOfNames.name




