
import random, serial
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates()
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

ser= serial.Serial(conf.PORT, conf.BAUD_RATE, timeout=conf.TIMEOUT)

# TODO: set serial to notify arduino of on/off and to set different effects/ colours

@app.on_event("startup")
async def startup():
    print("Starting...")

@app.get("/", response_class=HTMLResponse)
async def root():
    return templates.TemplateResponse(html)

@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        rx = await websocket.receive_text()
        
        d = ser.readline()
        await websocket.send_text(f"message: {d}")

        match rx:
            case "power":
                ser.write(bytes('1', "utf-8"))
            case "purple":
                ser.write(bytes('3', "utf-8"))
            case "blue":
                ser.write(bytes('4', "utf-8"))

def parse_serial_input() -> str:
        """
        Return a string representation of binary data
        """
        bin_input = str(ser.readline().rstrip()).replace('b', '').replace("'", "")
        str_output = int(bin_input) if not ValueError else ''
        return str_output
