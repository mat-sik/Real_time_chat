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
    document.querySelector("#chat-text").value += (
        data.user_name + ": " + data.message + "\n"
    );
}

document.querySelector("#submit").onclick = function (event) {
    const messageInputDom = document.querySelector("#input");
    const message = messageInputDom.value;
    chatSocket.send(
        JSON.stringify(
            {
                "message": message,
                "user_name": userUsername
            }
        )
    );
    messageInputDom.value = "";
}