# FastAPI WebSocket Server with Graceful Shutdown

This project is a FastAPI WebSocket server that supports real-time notifications to connected clients. It includes a graceful shutdown mechanism that ensures the service only stops when there are no active WebSocket connections or 30 seconds have passed since a shutdown signal was received.

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/websockets-fastapi.git
cd websockets-fastapi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.tx

make app


```

For test use index.html file open it on browser and look in dev console