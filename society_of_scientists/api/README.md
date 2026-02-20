# Society of Scientists API Server

FastAPI server providing REST API and WebSocket support for the frontend.

## Run Server

```bash
# Using uv
uv run python -m society_of_scientists.api.server

# Or directly
python -m society_of_scientists.api.server
```

## Endpoints

- `GET /` - API info
- `GET /api/stats` - Dashboard statistics
- `POST /api/proposal/start` - Start proposal generation
- `POST /api/proposal/stop` - Stop proposal generation
- `GET /api/proposal/status` - Get proposal status
- `GET /api/proposal/history` - Get conversation history
- `GET /api/cost/summary` - Get cost summary
- `GET /api/cost/details` - Get detailed cost info
- `WS /ws` - WebSocket for real-time updates
