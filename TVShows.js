//var listOfNames = [];
var addButton = document.querySelector("#add");
var showList = document.querySelector("#text");
var userButton = document.querySelector("#user")



function shows () {
    fetch("http://localhost:8080/shows", {
        credentials: "include"
    }).then(function (response) {
        showList.innerHTML = ""

        console.log("server response");
        response.json().then(function (data) {
            console.log("data received from server:", data);
            listOfNames = data;

            listOfNames.forEach(function (list) {

                var newListItem = document.createElement("h3");

                // the title
                var titleHeading = document.createElement("h2");
                titleHeading.innerHTML = list.name;
                newListItem.appendChild(titleHeading);
                
                // the genre
                var genreDiv = document.createElement("h2");
                genreDiv.innerHTML = list.genre;
                newListItem.appendChild(genreDiv);

                // the status
                var statusDiv = document.createElement("h2");
                statusDiv.innerHTML = list.status;
                newListItem.appendChild(statusDiv);

                // the genre
                var ratingDiv = document.createElement("h2");
                ratingDiv.innerHTML = list.rating;
                newListItem.appendChild(ratingDiv);

                // button tag: the delete button 
                var deleteButton = document.createElement("button");
                deleteButton.innerHTML = "Delete";
                deleteButton.onclick = function () {
                    console.log("delete clicked", list.id);
                    if (confirm("are you sure you want to delete " + list.name + "?"))
                        deleteShows(list.id);
                };
                var editButton = document.createElement("button");
                editButton.innerHTML = "edit";
                editButton.onclick = function () {
                    console.log("edit clicked", list.id);
                    document.getElementById("mymodal").style.display = "flex"
                    document.querySelector("#edit-show-name").value = list.name;
                    document.querySelector("#edit-show-genre").value = list.genre;
                    document.querySelector("#edit-show-status").value = list.status;
                    document.querySelector("#edit-show-rating").value = list.rating;
                    editClickHandler(list)

                };
                newListItem.appendChild(deleteButton);
                newListItem.appendChild(editButton);
                showList.appendChild(newListItem);
            });
        });

    });
};
shows();

newUserButton.onclick = function () {
    //var TVShowsInput = document.querySelector("#inputShow");
    //var TVShowsValue = TVShowsInput.value;
    //var bodyStr = "name=" + encodeURIComponent(TVShowsValue);

    var newShowName = document.querySelector("#create-first-name").value;
    var newShowGenre = document.querySelector("#create-last-name").value;
    var newShowStatus = document.querySelector("#create-username").value;
    var newShowRating = document.querySelector("#create-user-password").value;

    var bodyStr = "name=" + encodeURIComponent(firstName);
    bodyStr += "&genre=" + encodeURIComponent(lastName);
    bodyStr += "&status=" + encodeURIComponent(username);
    bodyStr += "&rating=" + encodeURIComponent(pass_word);

    fetch("http://localhost:8080/shows", {
        // request parameters:
        method: "POST",
        credentials: "include",
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
        credentials: "include",
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

        method: "DELETE",
        credentials: "include"
    }).then(function (response) {
        shows();

    });
}

var editClickHandler = function (show) {

    var editButton = document.querySelector("#save");
    editButton.onclick = function () {
        //var TVShowsInput = document.querySelector("#inputShow");
        //var TVShowsValue = TVShowsInput.value;
        //var bodyStr = "name=" + encodeURIComponent(TVShowsValue);
    
        var editShowName = document.querySelector("#edit-show-name").value;
        var editShowGenre = document.querySelector("#edit-show-genre").value;
        var editShowStatus = document.querySelector("#edit-show-status").value;
        var editShowRating = document.querySelector("#edit-show-rating").value;
    
        var bodyStr = "name=" + encodeURIComponent(editShowName);
        bodyStr += "&genre=" + encodeURIComponent(editShowGenre);
        bodyStr += "&status=" + encodeURIComponent(editShowStatus);
        bodyStr += "&rating=" + encodeURIComponent(editShowRating);
        bodyStr += "&id=" + encodeURIComponent(show.id);
    
        fetch("http://localhost:8080/shows", {
            // request parameters:
            method: "PUT",
            credentials: "include",
            body: bodyStr,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }).then(function (response) {
            // handle the response
            console.log("server responded", response)
            document.getElementById("mymodal").style.display = "none"
            shows();
        });
    
    };
}


