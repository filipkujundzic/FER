const connection = new WebSocket("ws://localhost:1234");
const button = document.querySelector("#send");

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

userID = getRandomInt(0, 10000)

connection.onopen = (event) => {
    console.log("WebSocket is open now.");
};

connection.onclose = (event) => {
    console.log("WebSocket is closed now.");
};

connection.onerror = (event) => {
    console.error("WebSocket error observed:", event);
};

connection.onmessage = (event) => {

    const chat = document.querySelector("#chat");
    chat.innerHTML += event.data;
};

button.addEventListener("click", () => {
    const message = document.querySelector("#message");
    const data = `<b>User#${userID} says:</b><p> ${message.value}</p>`;


    connection.send(data);

    message.value = "";
});


