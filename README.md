# 📚 English File App

**Learn English through English!**

Based on the **English File (Oxford) 4th Edition** textbook methodology.

## 🎯 Our Method

Unlike other apps that translate to Russian, English File teaches **ONLY in English**:
- 📷 **Pictures** → learn words visually
- 📝 **Context** → grammar in real sentences  
- 🗣️ **Speaking** → practice from day one
- 🎧 **Audio** → listen and repeat

## 📖 English File Structure

| Book | Level | CEFR | Description |
|------|-------|------|-------------|
| 1 | Beginner | A1 | Start with pictures |
| 2 | Pre-Intermediate | A2-B1 | Build confidence |
| 3 | Intermediate | B1 | Communicate fluently |
| 4 | Advanced | B2-C1 | Master English |

## 📱 Features

- ✅ **4 Levels** (English File system)
- ✅ **Vocabulary** - pictures + words (no translation!)
- ✅ **Grammar** - shown in context
- ✅ **Exercises** - listen, speak, write
- ✅ **AI Tutor** - practice speaking
- ✅ **Progress Tracking**

## 🏗️ Architecture

```
english-file-app/
├── backend/          # FastAPI Python
│   └── main.py      # API with English File curriculum
├── mobile/          # React Native
│   └── App.js      # Mobile app
```

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Mobile
```bash
cd mobile
npm install
npx expo start
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/levels` | Get 4 English File levels |
| GET | `/levels/{id}/lessons` | Get lessons |
| GET | `/lessons/{id}` | Get lesson (vocab, grammar, exercises) |
| POST | `/ai/chat` | Practice with AI tutor |

## 🎓 Lesson Structure

Each lesson follows English File method:

1. **A. Vocabulary** - Learn through pictures
2. **B. Grammar** - See pattern in context
3. **C. Practice** - Interactive exercises
4. **D. Speaking** - Real communication

## 📄 License

MIT License
