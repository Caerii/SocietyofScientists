"""
FastAPI server for Society of Scientists frontend integration.

Provides REST API and WebSocket support for real-time communication.
"""
import logging
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import json
from datetime import datetime

from ..agents import create_society_of_mind_system
from ..utils import get_tracker, get_autogen_version, is_ag2

logger = logging.getLogger(__name__)

app = FastAPI(title="Society of Scientists API", version="0.1.0")

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                logger.warning("Failed to send message to WebSocket client")

ws_manager = ConnectionManager()

# Active proposal sessions
active_sessions: Dict[str, Any] = {}


@app.get("/")
async def root():
    return {
        "message": "Society of Scientists API",
        "version": "0.1.0",
        "autogen_version": get_autogen_version(),
        "is_ag2": is_ag2(),
    }


@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics."""
    try:
        tracker = get_tracker()
        summary = tracker.get_usage_stats()
    except Exception:
        summary = {"total_cost": 0, "total_tokens": 0, "total_calls": 0}

    return {
        "totalProposals": len(active_sessions),
        "activeConversations": len([s for s in active_sessions.values() if s.get("running")]),
        "totalCost": summary.get("total_cost", 0),
        "agentsActive": 13,
    }


@app.post("/api/proposal/start")
async def start_proposal(task: Dict[str, str]):
    """Start a new proposal generation."""
    task_text = task.get("task", "")
    if not task_text:
        raise HTTPException(status_code=400, detail="Task is required")

    session_id = str(uuid.uuid4())

    try:
        agent, user_proxy, manager_obj = create_society_of_mind_system(
            task=task_text,
            max_rounds=50,
            register_exa_tool=True
        )

        active_sessions[session_id] = {
            "id": session_id,
            "task": task_text,
            "agent": agent,
            "user_proxy": user_proxy,
            "manager": manager_obj,
            "running": True,
            "created_at": datetime.now().isoformat(),
            "conversation": [],
            "proposal": "",
        }

        return {"session_id": session_id, "status": "started"}
    except Exception as e:
        logger.error("Failed to start proposal: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/proposal/stop")
async def stop_proposal():
    """Stop current proposal generation."""
    return {"status": "stopped"}


@app.get("/api/proposal/status")
async def get_proposal_status():
    """Get current proposal status."""
    return {"status": "idle", "sessions": len(active_sessions)}


@app.get("/api/proposal/history")
async def get_proposal_history():
    """Get proposal history."""
    return [
        {
            "id": session_id,
            "task": session["task"],
            "created_at": session["created_at"],
            "status": "completed" if not session.get("running") else "running",
        }
        for session_id, session in active_sessions.items()
    ]


@app.get("/api/cost/summary")
async def get_cost_summary():
    """Get cost tracking summary."""
    tracker = get_tracker()
    return tracker.get_usage_stats()


@app.get("/api/cost/details")
async def get_cost_details():
    """Get detailed cost information."""
    tracker = get_tracker()
    return {
        "summary": tracker.get_usage_stats(),
        "log": [
            {
                "timestamp": u.timestamp,
                "model": u.model,
                "prompt_tokens": u.prompt_tokens,
                "completion_tokens": u.completion_tokens,
                "cost": u.cost,
                "operation": u.operation,
            }
            for u in tracker.usage_history[-100:]
        ],
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await ws_manager.connect(websocket)
    try:
        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket connected successfully"
        })

        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)

                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif message.get("type") == "subscribe":
                    session_id = message.get("session_id")
                    logger.info("Client subscribed to session %s", session_id)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON message"
                })
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error("WebSocket error: %s", e)
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
