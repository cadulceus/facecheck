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
            return
        },   
        //handle error
        function (error) {
            console.log(error);
        })   
})();
