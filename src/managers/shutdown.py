import asyncio
import signal
from datetime import timedelta, datetime

from fastapi import FastAPI


class ShutdownManager:
    def __init__(self, app: FastAPI, timeout: int = 5) -> None:
        self.manager = app.state.connection_manager

        self.timeout = timedelta(seconds=timeout)

        self.shutdown_event = asyncio.Event()
        self.triggered_at: datetime | None = None

    def setup_signal_handlers(self) -> None:
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(self.handle_shutdown_signal(s)))

    async def handle_shutdown_signal(self, sig) -> None:
        if self.triggered_at is not None:
            return  # already shutting down

        self.triggered_at = datetime.now()

        while True:
            remaining = self.timeout - (datetime.now() - self.triggered_at)

            if self.manager.connection_count() == 0 or remaining.total_seconds() <= 0:
                break
            await asyncio.sleep(5)

        self.shutdown_event.set()

