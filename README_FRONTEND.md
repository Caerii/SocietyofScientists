# Frontend Setup & Development

## Quick Start

### Prerequisites
- Node.js 18+
- pnpm (install with `npm install -g pnpm`)

### Install & Run
```bash
cd frontend
pnpm install
pnpm dev
```

Frontend will run on http://localhost:5173

## Backend Setup

### Using uv (Recommended)
```bash
# Install uv if not installed
pip install uv

# Install dependencies
uv pip install -r requirements.txt

# Run API server
uv run python -m society_of_scientists.api.server
```

Backend will run on http://localhost:8000

## Testing

### Test Integration
```bash
uv run python scripts/test_integration.py
```

### Test Frontend
```bash
cd frontend
pnpm test  # If tests are added
```

## Architecture

- **Frontend**: React + Vite + TypeScript (port 5173)
- **Backend**: FastAPI + WebSocket (port 8000)
- **Communication**: REST API + WebSocket for real-time updates

## Features Implemented

✅ Modern React UI with Tailwind CSS
✅ Real-time WebSocket communication
✅ Cost analytics dashboard
✅ Conversation history
✅ Proposal builder
✅ Agent status monitoring
✅ Responsive design
