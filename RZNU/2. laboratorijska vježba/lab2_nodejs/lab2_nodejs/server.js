const WebSocket = require('ws');

// starts server instance on http://localhost:1234
const wss = new WebSocket.Server({ port: 1234 });

var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname)).listen(5000, function(){
    console.log('Server running on 5000...');
});


wss.on('connection', (ws) => {

    ws.on('message', (data) => {

        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
    });
});