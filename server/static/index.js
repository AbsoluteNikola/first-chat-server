function connect() {
    let name = document.getElementById('name').value.trim();
    let room = document.getElementById('room').value.trim();
    console.log(name);
    console.log(room);
    console.log(`${name}&room=${room}`);
    let ws = new WebSocket(`ws://${window.location.hostname}:${ window.location.port}/chat?name=${name}&room=${room}`);
    ws.onopen = function() {
        console.log('connected');
    };
    ws.onclose = function (event) {
        if(event.reason === 'UserAlreadyExists')
            alert('User already exists');
        console.log(event, 'connection closed');
    };
    ws.onmessage = receive;
    window.ws = ws;
    window.name = name;
    window.room = room;
}

function receive(event) {
    console.log(event.data);
    let msg = JSON.parse(event.data);
    addMessage(msg.name, msg.data);
}

function addMessage(name, text) {
    let d = document.getElementById("messages");
    d.innerHTML += `<div> ${name}: ${text} <\div>`;
}

function send() {
    let text = document.getElementById("newMessage").value;
    window.ws.send(JSON.stringify({
        name: window.name,
        data: text
    }));
    addMessage(window.name, text);
}