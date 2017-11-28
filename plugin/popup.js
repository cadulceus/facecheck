function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

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

document.addEventListener('DOMContentLoaded', function() {
  var gen_pass = document.getElementById('gen_pass');
  gen_pass.addEventListener('click', function() {
    sendRequest('http://localhost:5000/gen_pass', function (response) {
      //alert('My request returned this: ' + response);
      var json = JSON.parse(response);
      var password = json['password'];
      document.getElementById("status_msg").innerHTML = "Your Password:"+password;

      sendRequest('http://localhost:5000/copy_pass?service='+window.location.hostname, function (response) {
      //alert('My request returned this: ' + response);
      var json = JSON.parse(response);
      var stat = json['status'];

      if(stat == "error"){
        document.getElementById("status_msg").innerHTML = stat;
      }else{
        document.getElementById("status_msg").innerHTML = "Your password is copied to the clipboard :)";
      }

      });
    
    });
    document.getElementById("status_msg").style.display = "block";
    document.getElementById("passbox").style.display = "none";
    document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
  });


  var copy_pass = document.getElementById('copy_pass');
  copy_pass.addEventListener('click', function() {
  	sendRequest('http://localhost:5000/copy_pass?service='+window.location.hostname, function (response) {
      //alert('My request returned this: ' + response);
      var json = JSON.parse(response);
      var stat = json['status'];

    	if(stat == "error"){
        document.getElementById("status_msg").innerHTML = stat;
    	}else{
        document.getElementById("status_msg").innerHTML = "Your password is copied to the clipboard :)";
    	}
    });
    document.getElementById("status_msg").style.display = "block";
    document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
  });


  var train = document.getElementById('train');
  train.addEventListener('click', function() {
     sendRequest('http://localhost:5000/train', function (response) {
     
      var json = JSON.parse(response);
      var stat = json['status'];

      document.getElementById("status_msg").innerHTML = stat;

    });

    document.getElementById("status_msg").style.display = "block";
    document.getElementById("passbox").style.display = "none";
    document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
  });


  var wipe_user = document.getElementById('wipe_user');
  wipe_user.addEventListener('click', function() {
     sendRequest('http://localhost:5000/clear_training', function (response) {
     var json = JSON.parse(response);
     var stat = json['status'];

     if(stat == "error"){
        document.getElementById("status_msg").innerHTML = json['message'];
     }else{
        document.getElementById("status_msg").innerHTML = stat;
	//train it again :)
    	sendRequest('http://localhost:5000/train', function (response) {
     
    	var json = JSON.parse(response);
    	var stat = json['status'];

    	document.getElementById("status_msg").innerHTML = stat;

    	});
     }

    });
      document.getElementById("status_msg").style.display = "block";
      document.getElementById("passbox").style.display = "none";
      document.getElementById("status_msg").style.backgroundColor = "#5fba7d";

    

  });


  var edit = document.getElementById('modify_password');
  var input = document.getElementById('confirm_modify_password');
  edit.addEventListener('click', function() {
    input.addEventListener('click', function() {
	    var password = document.getElementById("password").value;
      var service = window.location.hostname;
    	var id = "11111";
    	var json_data = {"service":service,"password":password,"id":id};	
    	sendRequestPost('http://localhost:5000/edit_item',json_data,function (response) {
      	var json = JSON.parse(response);
      	if (json['status'] == 'error' && json['message'] == null) {
              	document.getElementById("status_msg").innerHTML ='Something went wrong :(';        
      	}else{
              	document.getElementById("status_msg").innerHTML = json['message'];        
      	}
	    });
    });

    document.getElementById("status_msg").innerHTML = "Change your password :)";
    document.getElementById("status_msg").style.display = "block";
    document.getElementById("passbox").style.display = "block";
    document.getElementById("status_msg").style.backgroundColor = "#5fba7d";
  });
});

