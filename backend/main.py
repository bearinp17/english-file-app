"""
English File App - Backend API
FastAPI application for language learning
"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(title="English File API", version="1.0.0")

# ==================== MODELS ====================

class User(BaseModel):
    id: str
    email: str
    name: str
    current_level: int = 1
    created_at: datetime = None

class Lesson(BaseModel):
    id: str
    level_id: int
    title: str
    content: str
    audio_url: Optional[str] = None
    exercises: List[dict] = []

class Exercise(BaseModel):
    id: str
    lesson_id: str
    type: str  # grammar, vocabulary, listening, speaking
    question: str
    answer: str
    options: Optional[List[str]] = None

class UserProgress(BaseModel):
    user_id: str
    lesson_id: str
    completed: bool = False
    score: Optional[int] = None

# ==================== DATA ====================

# English File Levels
LEVELS = [
    {"id": 1, "name": "Beginner", "cefr": "A1", "description": "Start learning English from scratch"},
    {"id": 2, "name": "Elementary", "cefr": "A1-A2", "description": "Basic conversations and grammar"},
    {"id": 3, "name": "Pre-Intermediate", "cefr": "A2-B1", "description": "More complex structures"},
    {"id": 4, "name": "Intermediate", "cefr": "B1", "description": "Fluency in everyday situations"},
    {"id": 5, "name": "Intermediate Plus", "cefr": "B1+", "description": "Advanced intermediate"},
    {"id": 6, "name": "Upper-Intermediate", "cefr": "B2", "description": "Complex topics and discussions"},
    {"id": 7, "name": "Advanced", "cefr": "C1", "description": "Near-native fluency"},
    {"id": 8, "name": "Advanced Plus", "cefr": "C1+", "description": "Mastery of English"},
]

# Sample lessons for Level 1
LESSONS = [
    {
        "id": "l1-01",
        "level_id": 1,
        "title": "Hello!",
        "content": """
# Hello!

## Greetings

- **Hello!** - Привет!
- **Hi!** - Привет! (неформально)
- **Good morning!** - Доброе утро!
- **Good afternoon!** - Добрый день!
- **Good evening!** - Добрый вечер!
- **Goodbye!** - До свидания!
- **See you!** - Увидимся!

## How are you?

- **How are you?** - Как дела?
- **I'm fine, thanks.** - Хорошо, спасибо.
- **Not bad.** - Неплохо.
- **And you?** - А у тебя?

## Practice

Try to greet someone in English!
        """,
        "audio_url": None,
        "exercises": [
            {
                "type": "vocabulary",
                "question": "How do you say 'Привет' in English?",
                "answer": "Hello",
                "options": ["Hello", "Goodbye", "Thanks", "Please"]
            },
            {
                "type": "grammar",
                "question": "Complete: How are ___?",
                "answer": "you",
                "options": ["you", "I", "he", "she"]
            }
        ]
    },
    {
        "id": "l1-02",
        "level_id": 1,
        "title": "Numbers 1-20",
        "content": """
# Numbers 1-20

## Numbers

| Number | Word |
|--------|------|
| 1 | one |
| 2 | two |
| 3 | three |
| 4 | four |
| 5 | five |
| 6 | six |
| 7 | seven |
| 8 | eight |
| 9 | nine |
| 10 | ten |
| 11 | eleven |
| 12 | twelve |
| 13 | thirteen |
| 14 | fourteen |
| 15 | fifteen |
| 16 | sixteen |
| 17 | seventeen |
| 18 | eighteen |
| 19 | nineteen |
| 20 | twenty |

## Practice

Count from 1 to 20!
        """,
        "exercises": [
            {
                "type": "vocabulary",
                "question": "What number is 'five'?",
                "answer": "5",
                "options": ["5", "6", "4", "7"]
            }
        ]
    }
]

# In-memory storage
users_db = {}
progress_db = {}

# ==================== ROUTES ====================

@app.get("/")
def root():
    return {"message": "English File API", "version": "1.0.0", "status": "running"}

@app.get("/levels")
def get_levels():
    """Get all levels"""
    return LEVELS

@app.get("/levels/{level_id}")
def get_level(level_id: int):
    """Get specific level"""
    for level in LEVELS:
        if level["id"] == level_id:
            return level
    raise HTTPException(status_code=404, detail="Level not found")

@app.get("/levels/{level_id}/lessons")
def get_lessons(level_id: int):
    """Get lessons for a level"""
    return [l for l in LESSONS if l["level_id"] == level_id]

@app.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str):
    """Get specific lesson"""
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    raise HTTPException(status_code=404, detail="Lesson not found")

@app.post("/users")
def create_user(user: User):
    """Create new user"""
    user.id = str(uuid.uuid4())
    user.created_at = datetime.now()
    users_db[user.id] = user
    return {"user_id": user.id, "message": "User created"}

@app.get("/users/{user_id}/progress")
def get_progress(user_id: str):
    """Get user progress"""
    user_progress = [p for p in progress_db.values() if p["user_id"] == user_id]
    return user_progress

@app.post("/progress")
def save_progress(progress: UserProgress):
    """Save exercise progress"""
    key = f"{progress.user_id}-{progress.lesson_id}"
    progress_db[key] = progress.dict()
    return {"message": "Progress saved", "score": progress.score}

# ==================== AI TUTOR ====================

@app.post("/ai/chat")
def chat_with_ai(message: str, user_id: str = "demo"):
    """
    Chat with AI tutor
    Note: This would connect to Groq/OpenAI in production
    """
    # For demo, return a simple response
    responses = [
        "Great question! Let's practice more.",
        "Very good! Keep going!",
        "Excellent work! You're making progress.",
        "That's correct! Well done!",
    ]
    import random
    return {
        "response": random.choice(responses),
        "user_id": user_id
    }

# ==================== RUN ====================

if __name__ == "__main__":
    import uvicorn
    print("🚀 English File API Server")
    print("Run: uvicorn main:app --host 0.0.0.0 --port 8000")
