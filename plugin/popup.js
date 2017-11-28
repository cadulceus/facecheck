function sendRequest(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            callback(xhr.responseText);
        }
    };
    xhr.open("GET", url, true);
    xhr.send();
}

document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('gen_pass');
    link.addEventListener('click', function() {
        sendRequest('http://localhost:8000', function (response) {
        alert('My request returned this: ' + response);
        });
        document.getElementById("status_msg").innerHTML = "test123";
        document.getElementById("status_msg").style.display = "block";
        document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
    });

    var link = document.getElementById('copy_pass');
    link.addEventListener('click', function() {
        document.getElementById("status_msg").innerHTML = "danny waz her";
        document.getElementById("status_msg").style.display = "block";
        document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
    });

    var link = document.getElementById('train');
    link.addEventListener('click', function() {
        document.getElementById("status_msg").innerHTML = "test123";
        document.getElementById("status_msg").style.display = "block";
        document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
    });

    var link = document.getElementById('wipe_user');
    link.addEventListener('click', function() {
        document.getElementById("status_msg").innerHTML = "test123";
        document.getElementById("status_msg").style.display = "block";
        document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
    });

    var link = document.getElementById('modify_password');
    link.addEventListener('click', function() {
        document.getElementById("status_msg").innerHTML = "test123";
        document.getElementById("status_msg").style.display = "block";
        document.getElementById("passbox").style.display = "block";
        document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
    });

});
