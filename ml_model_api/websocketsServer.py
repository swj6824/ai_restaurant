from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
  <head><title>Chat</title></head>
  <body>
    <h1>WebSocket Chat</h1>
    <form action="" onsubmit="sendMessage(event)">
        <input type="text" id="messageText" autocomplete="off"/>
        <button>Send</button>
    </form>
    <ul id='messages'></ul>

    <script>
        var ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            var messages = document.getElementById('messages');
            var message = document.createElement('li');
            var content = document.createTextNode(event.data);
            message.appendChild(content);
            messages.appendChild(message);
        };

        function sendMessage(event) {
            var input = document.getElementById("messageText");
            ws.send(input.value);
            input.value = '';
            event.preventDefault();
        }
    </script>
  </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")  # 클라이언트는 ws://localhost:8000/ws 로 연결
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 클라이언트의 WebSocket 연결 요청을 수락
    while True:  # 무한루프
        # 클라이언트로부터 텍스트 메시지를 기다림 (await -> 비동기)
        data = await websocket.receive_text()

        # 받은 메시지를 다시 클라이언트에게 전송 (Echo 방식)
        await websocket.send_text(f"Message text was: {data}")
