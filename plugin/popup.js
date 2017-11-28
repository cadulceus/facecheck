document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('gen_pass');
    link.addEventListener('click', function() {
        document.getElementById("status_msg").innerHTML = "test123";
        document.getElementById("status_msg").style.display = "block";
        document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
    });

    var link = document.getElementById('copy_pass');
    link.addEventListener('click', function() {
        document.getElementById("status_msg").innerHTML = "test123";
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
