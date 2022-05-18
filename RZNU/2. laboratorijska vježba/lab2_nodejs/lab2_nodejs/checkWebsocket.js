
if (window.MozWebSocket) {
    window.WebSocket = window.MozWebSocket;
}

else if (window.WebSocket) {
}

else {
    window.location.replace("/error.html");
}