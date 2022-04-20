
import random, serial
import asyncio
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

from Config import Config
conf = Config()

ser= serial.Serial(conf.PORT, conf.BAUD_RATE, timeout=conf.TIMEOUT)

# TODO: set serial to notify arduino of on/off and to set different effects/ colours

@app.on_event("startup")
async def startup():
    print("Starting...")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.websocket_route("/ws/buttons")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        rx = await websocket.receive_text()
        ser.write(bytes(rx, "utf-8"))

@app.websocket_route("/ws/graph")
async def graph_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        print("graph")     

def parse_serial_input() -> str:
        """
        Return a string representation of binary data
        """
        bin_input = str(ser.readline().rstrip()).replace('b', '').replace("'", "")
        str_output = int(bin_input) if not ValueError else ''
        return str_output
