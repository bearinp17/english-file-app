# English File API - Backend

FastAPI backend for the English File learning application.

## 🚀 Quick Start

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| GET | `/levels` | Get all levels |
| GET | `/levels/{id}` | Get level by ID |
| GET | `/levels/{id}/lessons` | Get lessons for level |
| GET | `/lessons/{id}` | Get specific lesson |
| POST | `/users` | Create user |
| GET | `/users/{id}/progress` | Get user progress |
| POST | `/progress` | Save progress |
| POST | `/ai/chat` | Chat with AI tutor |

## 📱 Mobile App Connection

The mobile app connects to this API. Set the API_URL in your mobile app config.

## 🔧 Environment Variables

Create `.env` file:
```
API_HOST=0.0.0.0
API_PORT=8000
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```
