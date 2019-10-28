//var listOfNames = [];
var addButton = document.querySelector("#add");
var showList = document.querySelector("#text");


function shows () {
    fetch("http://localhost:8080/shows").then(function (response) {

        console.log("server response");
        response.json().then(function (data) {
            console.log("data received from server:", data);
            listOfNames = data;

            listOfNames.forEach(function (list) {

                var newListItem = document.createElement("h3");

                // h3 tag: contains the title
                var titleHeading = document.createElement("h1");
                titleHeading.innerHTML = list.name;
                newListItem.appendChild(titleHeading);
                
                // div tag: contains the genre
                var genreDiv = document.createElement("h1");
                genreDiv.innerHTML = list.genre;
                newListItem.appendChild(genreDiv);


                // button tag: the delete button 
                var deleteButton = document.createElement("button");
                deleteButton.innerHTML = "Delete";
                deleteButton.onclick = function () {
                    console.log("delete clicked", list.id);
                    if (confirm("are you sure you want to delete " + list.name + "?"))
                        deleteShows(list.id);
                };
                newListItem.appendChild(deleteButton);
                showList.appendChild(newListItem);
            });
        });

    });
};

addButton.onclick = function () {
    //var TVShowsInput = document.querySelector("#inputShow");
    //var TVShowsValue = TVShowsInput.value;
    //var bodyStr = "name=" + encodeURIComponent(TVShowsValue);

    var newShowName = document.querySelector("#new-show-name").value;
    var newShowGenre = document.querySelector("#new-show-genre").value;
    var newShowStatus = document.querySelector("#new-show-status").value;
    var newShowRating = document.querySelector("#new-show-rating").value;

    var bodyStr = "name=" + encodeURIComponent(newShowName);
    bodyStr += "&genre=" + encodeURIComponent(newShowGenre);
    bodyStr += "&status=" + encodeURIComponent(newShowStatus);
    bodyStr += "&rating=" + encodeURIComponent(newShowRating);

    fetch("http://localhost:8080/shows", {
        // request parameters:
        method: "POST",
        body: bodyStr,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function (response) {
        // handle the response
        console.log("server responded", response)
        shows();
    });

};

var deleteShows = function (showID) {

    fetch("http://localhost:8080/shows/" + showID, {

        method: "DELETE"
    }).then(function (response) {
        shows();

    });
}

shows();




