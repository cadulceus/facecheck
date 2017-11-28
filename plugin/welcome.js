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

function sendRequestPost(url,data,callback) {
  
  var xhr = new XMLHttpRequest();

  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  xhr.send(JSON.stringify(data));
  xhr.onload = function(){  
	  callback(xhr.responseText);
  };
}

function moveOnMax(field, nextFieldID) {
    if (field.value.length == 1) {
        document.getElementById(nextFieldID).focus();
    }
}

function new_vault(first_try=true) {
    var container = document.getElementById('container');
    first = "";
    if (first_try) {
        container.innerHTML = '<h2>Enter a PIN</h2>'
    }
    else {
        container.innerHTML = '<h2 class="warning">PINs did not match.</h2>'
    }
    container.innerHTML += '<input class="ios" type="password" maxlength=1 id="1" />\
                           <input class="ios" type="password" maxlength=1 id="a" />\
                           <input class="ios" type="password" maxlength=1 id="b" />\
                           <input class="ios" type="password" maxlength=1 id="c" />'

    document.getElementById("1").addEventListener("keyup", function() {moveOnMax(this, 'a');});
    document.getElementById("a").addEventListener("keyup", function() {moveOnMax(this, 'b');});
    document.getElementById("b").addEventListener("keyup", function() {moveOnMax(this, 'c');});
    document.getElementById("c").addEventListener("keyup", function() {if (this.value.length == 1) {
                                                                           first += document.getElementById("1").value;
                                                                           first += document.getElementById("a").value;
                                                                           first += document.getElementById("b").value;
                                                                           first += document.getElementById("c").value;
                                                                           console.log(first);
                                                                           confirm_pin(first);
                                                                      }});

}

function train_handler() {
     sendRequest('http://localhost:5000/train', function (response) {
        
         var json = JSON.parse(response);
         var stat = json['status'];

         document.getElementById("container").innerHTML = '<h1>Successfully trained the vault</h1>';

    });
}

function send_pin(pin) { 
    sendRequest('http://localhost:5000/create?pin='+pin, function (response) {
        //alert('My request returned this: ' + response);
        var json = JSON.parse(response);
        var stat = json['status'];

        if(stat == "error") {
            document.getElementById("container").innerHTML = '<h2 class="warning">Error setting up new vault</h2>';
        }
        else {
            document.getElementById("container").innerHTML = '<h1>Vault Created! Keep the following passphrase safe to import later: </h1><br>\
                                                              <h2>' + json['secret'] + '</h2>' + '<br><button style="width:190px; height:50px;" id="train_new" class="button button1">Begin Training Facial Recognition</button>';

            var train_button = document.getElementById("train_new");
            train_button.addEventListener("click", train_handler);
        }
    });
}

function confirm_pin(input) {
    var container = document.getElementById('container');
    confirmation = ""
    container.innerHTML = '<h2>Confirm PIN</h2>'
    container.innerHTML += '<input class="ios" type="password" maxlength=1 id="1" />\
                           <input class="ios" type="password" maxlength=1 id="a" />\
                           <input class="ios" type="password" maxlength=1 id="b" />\
                           <input class="ios" type="password" maxlength=1 id="c" />'

    document.getElementById("1").addEventListener("keyup", function() {moveOnMax(this, 'a');});
    document.getElementById("a").addEventListener("keyup", function() {moveOnMax(this, 'b');});
    document.getElementById("b").addEventListener("keyup", function() {moveOnMax(this, 'c');});
    document.getElementById("c").addEventListener("keyup", function() {if (this.value.length == 1) {
                                                                           confirmation += document.getElementById("1").value;
                                                                           confirmation += document.getElementById("a").value;
                                                                           confirmation += document.getElementById("b").value;
                                                                           confirmation += document.getElementById("c").value;
                                                                           console.log(confirmation);
                                                                           if (input == confirmation) {
                                                                               send_pin(input);
                                                                           }
                                                                           else {
                                                                               new_vault(first_try=false);
                                                                           }
                                                                      }});
}

function import_vault() {
    var container = document.getElementById('container');
    container.innerHTML = '<h1>Inside the import_vault event handler</h1>'
}

(function () {
    navigator.getMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia);

    navigator.getMedia(
        // constraints
        {video:true, audio:false},

        // success callback
        function (mediaStream) {
        //    var video = document.getElementsByTagName('video')[0];
        //    video.src = window.URL.createObjectURL(mediaStream);
        //    video.play();
        //  window.close()
            mediaStream.getTracks()[0].stop();
            var container = document.getElementById('container');
            container.innerHTML = '<button style="width:190px; height:50px;" id="new_vault" class="button button1">Create new vault</button>\
                                  <br><button style="width:190px; height:50px;" id="import_vault" class="button button2">Import existing vault</button>';

            var new_button = document.getElementById("new_vault");
            new_button.addEventListener("click", new_vault);

            var existing_button = document.getElementById("import_vault");
            existing_button.addEventListener("click", import_vault);
        },   
        //handle error
        function (error) {
            console.log(error);
        })   
})();
