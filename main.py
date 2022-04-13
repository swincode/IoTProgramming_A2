
import random, serial
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

from Config import Config
conf = Config()

ser= serial.Serial(conf.PORT, conf.BAUD_RATE)

# TODO: set serial to notify arduino of on/off and to set different effects/ colours



@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        rx = websocket.receive_text()
        d = ser.readline()
        if d != '':
        #something
            websocket.send_text(d)
            if rx == "Turn on":
                ser.write(bytes('1', "utf-8"))
                send_byte = 0
            elif rx == "Turn off":
                ser.write(bytes('0', "utf-8"))
                send_byte = 1

@app.get("/")
async def root():
    return HTMLResponse(html)

def parse_serial_input() -> str:
        """
        Return a string representation of binary data
        """
        bin_input = str(ser.readline().rstrip()).replace('b', '').replace("'", "")
        str_output = int(bin_input) if not ValueError else ''
        return str_output
