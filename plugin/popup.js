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


document.addEventListener('DOMContentLoaded',function(){
   
    var link = document.getElementById("test");

    link.addEventListener('click',function(){	
    	    sendRequest('http://localhost:8080', function (response) {
            alert('My request returned this: ' + response);
   	}); 
    });

		
});

