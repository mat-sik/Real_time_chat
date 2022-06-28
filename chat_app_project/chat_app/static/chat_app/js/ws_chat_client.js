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

    if (data.hasOwnProperty("load")) {
        const loadedMessages = data.loaded_messages;
        for (let i = 0; i < loadedMessages.length; i++) {
            const firstMes = document.querySelector("#message");
            const newDiv = document.createElement("div");
            newDiv.id = "message";
            newDiv.textContent = loadedMessages[i].user__username + ": " + loadedMessages[i].text;
            document.querySelector("#chat-box").insertBefore(
                newDiv,
                firstMes
            );
        }

    } else {
        const newDiv = document.createElement("div");
        newDiv.id = "message";
        newDiv.textContent = data.username + ": " + data.message + "\n";
        
        document.querySelector("#chat-box").appendChild(newDiv);
    }

}

document.querySelector("#input").addEventListener("keyup", function(event) {
    if (event.key === 'Enter') {
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
  });

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

document.querySelector("#load").onclick = function (event) {
    chatSocket.send(
        JSON.stringify(
            {
                "load": "1"
            }
        )
    );
}