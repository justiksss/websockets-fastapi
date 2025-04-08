from fastapi import WebSocket, WebSocketException


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            if connection.client_state.CONNECTED:
                try:
                    await connection.send_text(message)
                except Exception:
                    self.disconnect(connection)

    def connection_count(self) -> int:
        return len(self.active_connections)
