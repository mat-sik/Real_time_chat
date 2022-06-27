const chatroomId = JSON.parse(
    document.getElementById("chatroom-id").textContent
);

const userUsername = JSON.parse(
    document.getElementById("user-username").textContent
);

const chatSocket = new WebSocket(
    "ws://" +
    window.location.host +
    "/ws/chat/" +
    chatroomId +
    "/"
);

chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    const newDiv = document.createElement("div");
    newDiv.textContent = data.username + ": " + data.message + "\n";
    
    document.querySelector("#chat-text").appendChild(newDiv);
}

document.querySelector("#submit").onclick = function (event) {
    const messageInputDom = document.querySelector("#input");
    const message = messageInputDom.value;
    chatSocket.send(
        JSON.stringify(
            {
                "message": message,
                "username": userUsername
            }
        )
    );
    messageInputDom.value = "";
}