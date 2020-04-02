document.addEventListener('DOMContentLoaded', () => {
    
    // Connect to SocketIO
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        // Message send event
        document.querySelector('#send-button').addEventListener("click", () => {
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();
            let msg = document.getElementById("user-message").value;
            socket.emit('message', msg, timestamp);
            document.getElementById("user-message").value = '';
        });
    
    });


    // Add user's mmessage to textarea
    socket.on('announce message', data => {
        let row = '[' + `${data.user}` + ']: ' + `${data.msg}` + ' <' + `${data.timestamp}` + '>' + '\n'
        document.querySelector('#chat-box').append(row);
    });

});