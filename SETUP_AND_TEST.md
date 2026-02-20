# Setup & Testing Guide

## 🚀 Quick Start

### 1. Install Python Dependencies (using uv)

```bash
# Install uv if not installed
pip install uv

# Install all dependencies
uv pip install -r requirements.txt
```

### 2. Install Frontend Dependencies (using pnpm)

```bash
cd frontend
pnpm install
```

### 3. Run Tests

```bash
# Test Python backend
python scripts/test_integration.py

# Test frontend (after starting dev server)
cd frontend
pnpm dev
```

## 📋 Feature Recommendations

See `docs/development/FEATURE_RECOMMENDATIONS.md` for detailed recommendations:

### High Priority
1. ✅ **Real-Time WebSocket Communication** - Implemented in API server
2. ✅ **Conversation History & Persistence** - API endpoints created
3. ✅ **Progressive Proposal Generation** - Frontend components ready

### Medium Priority
4. ✅ **Interactive Agent Control** - Frontend UI ready
5. ✅ **Proposal Export & Formatting** - Export button in frontend
6. ✅ **Cost Optimization Dashboard** - Analytics page created

## 🏗️ Architecture

### Frontend (React + Vite + TypeScript)
- **Location**: `frontend/`
- **Port**: 5173
- **Tech Stack**:
  - React 18
  - TypeScript
  - Vite
  - Tailwind CSS
  - React Router
  - Zustand (state management)
  - Socket.io (WebSocket client)
  - Recharts (visualization)

### Backend (FastAPI + Python)
- **Location**: `society_of_scientists/api/`
- **Port**: 8000
- **Tech Stack**:
  - FastAPI
  - WebSocket support
  - AG2 (AutoGen fork)
  - AI21 Jamba models
  - Exa API integration

## 🧪 Testing

### Integration Test
```bash
python scripts/test_integration.py
```

Tests:
- ✅ Configuration loading
- ✅ AutoGen/AG2 detection
- ✅ Cost tracking
- ✅ System creation

### Manual Testing

1. **Start Backend**:
   ```bash
   python -m society_of_scientists.api.server
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   pnpm dev
   ```

3. **Test Flow**:
   - Open http://localhost:5173
   - Navigate to "Proposal Builder"
   - Enter a task
   - Click "Start"
   - Watch real-time updates

## 📁 Project Structure

```
SocietyofScientists/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable components
│   │   ├── services/     # API client
│   │   ├── hooks/        # Custom hooks
│   │   └── stores/       # State management
│   └── package.json
├── society_of_scientists/ # Python package
│   ├── api/              # FastAPI server
│   ├── agents/           # Agent factory
│   ├── clients/          # API clients
│   ├── config/           # Configuration
│   ├── tools/            # Tools (Exa, etc.)
│   └── utils/            # Utilities
├── scripts/              # Test scripts
└── docs/                 # Documentation
```

## ✅ What's Implemented

### Frontend
- ✅ Modern React UI with Tailwind CSS
- ✅ Dashboard with statistics
- ✅ Proposal builder with real-time updates
- ✅ Conversation history page
- ✅ Cost analytics dashboard
- ✅ Settings page
- ✅ WebSocket integration
- ✅ Responsive design

### Backend
- ✅ FastAPI REST API
- ✅ WebSocket support
- ✅ Agent system integration
- ✅ Cost tracking endpoints
- ✅ Proposal management
- ✅ CORS configuration

## 🔧 Next Steps

1. **Install dependencies** (see above)
2. **Run integration tests** to verify setup
3. **Start both servers** (backend + frontend)
4. **Test the full flow** end-to-end
5. **Implement remaining features** from recommendations

## 📝 Notes

- Backend uses **AG2** (recommended over Microsoft AutoGen)
- Frontend uses **pnpm** for package management
- Python uses **uv** for dependency management
- All API keys should be configured in `.env` file
