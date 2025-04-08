import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.exceptions import WebSocketException
from starlette.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.websockets import WebSocket

from src.managers.connection import ConnectionManager
from src.managers.shutdown import ShutdownManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.connection_manager = ConnectionManager()
    app.state.shutdown_manager = ShutdownManager(app)

    app.state.shutdown_manager.setup_signal_handlers()
    asyncio.create_task(notification_loop())

    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def notification_loop():
    while not app.state.shutdown_manager.shutdown_event.is_set():
        await asyncio.sleep(2)
        await app.state.connection_manager.broadcast("Test notification")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    manager: ConnectionManager = websocket.app.state.connection_manager
    await manager.connect(websocket)
    try:
        while websocket.client_state.CONNECTED:
            await websocket.receive_text()  # optional, just keeps the connection open
    except WebSocketException:
        manager.disconnect(websocket)



