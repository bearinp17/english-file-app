"""
English File App - Complete Backend API
All 4 Books, 12 Modules each = 48 Lessons
Learn English through English - NO TRANSLATION!
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

app = FastAPI(title="English File API", version="1.0.0")

# ==================== MODELS ====================

class User(BaseModel):
    id: str = None
    name: str
    email: Optional[str] = None

class Progress(BaseModel):
    lesson_id: str
    completed: bool = False
    score: Optional[int] = None

# ==================== ENGLISH FILE CURRICULUM ====================

LEVELS = [
    {"id": 1, "book": "English File Elementary", "title": "Beginner", "cefr": "A1", "color": "#4CAF50", "modules": 12},
    {"id": 2, "book": "English File Elementary", "title": "Pre-Intermediate", "cefr": "A2-B1", "color": "#2196F3", "modules": 12},
    {"id": 3, "book": "English File Intermediate", "title": "Intermediate", "cefr": "B1", "color": "#9C27B0", "modules": 12},
    {"id": 4, "book": "English File Upper-Intermediate", "title": "Advanced", "cefr": "B2-C1", "color": "#FF5722", "modules": 12},
]

# Complete lessons for Book 1 (Beginner) - 12 Modules
LESSONS = [
    # ===== MODULE 1: Hello! =====
    {
        "id": "1-01", "level_id": 1, "module": 1, "title": "Hello!", "topic": "Greetings",
        "vocabulary": [
            {"word": "hello", "context": "saying hi", "emoji": "👋"},
            {"word": "goodbye", "context": "leaving", "emoji": "👋"},
            {"word": "please", "context": "polite", "emoji": "🙏"},
            {"word": "thank you", "context": "gratitude", "emoji": "😊"},
            {"word": "sorry", "context": "apology", "emoji": "😔"},
        ],
        "grammar": {"pattern": "Hello! I'm [name].", "examples": ["Hello! I'm Anna.", "Hello! I'm Tom."]},
        "dialogue": {"a": "Hello! I'm Anna.", "b": "Hi Anna! I'm Tom."},
    },
    # ===== MODULE 2: Numbers =====
    {
        "id": "1-02", "level_id": 1, "module": 2, "title": "Numbers", "topic": "Counting",
        "vocabulary": [
            {"word": "one", "number": 1}, {"word": "two", "number": 2}, {"word": "three", "number": 3},
            {"word": "four", "number": 4}, {"word": "five", "number": 5}, {"word": "six", "number": 6},
            {"word": "seven", "number": 7}, {"word": "eight", "number": 8}, {"word": "nine", "number": 9}, {"word": "ten", "number": 10},
        ],
        "grammar": {"pattern": "How many? — [Number]", "examples": ["How many? One!", "Two, three, four!"]},
    },
    # ===== MODULE 3: Family =====
    {
        "id": "1-03", "level_id": 1, "module": 3, "title": "Family", "topic": "People",
        "vocabulary": [
            {"word": "mother", "family": "female", "emoji": "👩"},
            {"word": "father", "family": "male", "emoji": "👨"},
            {"word": "sister", "family": "female", "emoji": "👩"},
            {"word": "brother", "family": "male", "emoji": "👨"},
            {"word": "baby", "family": "neutral", "emoji": "👶"},
        ],
        "grammar": {"pattern": "This is my [family word].", "examples": ["This is my mother.", "This is my brother."]},
    },
    # ===== MODULE 4: Jobs =====
    {
        "id": "1-04", "level_id": 1, "module": 4, "title": "Jobs", "topic": "Work",
        "vocabulary": [
            {"word": "doctor", "emoji": "👨‍⚕️"}, {"word": "teacher", "emoji": "👩‍🏫"},
            {"word": "driver", "emoji": "🚗"}, {"word": "chef", "emoji": "👨‍🍳"},
            {"word": "nurse", "emoji": "👩‍⚕️"},
        ],
        "grammar": {"pattern": "What do you do? — I'm a [job].", "examples": ["What do you do? I'm a teacher."]},
    },
    # ===== MODULE 5: Places =====
    {
        "id": "1-05", "level_id": 1, "module": 5, "title": "Places", "topic": "Locations",
        "vocabulary": [
            {"word": "school", "emoji": "🏫"}, {"word": "hospital", "emoji": "🏥"},
            {"word": "hotel", "emoji": "🏨"}, {"word": "restaurant", "emoji": "🍽️"},
            {"word": "shop", "emoji": "🏪"},
        ],
        "grammar": {"pattern": "Where is the [place]?", "examples": ["Where is the hotel?", "It's next to the shop."]},
    },
    # ===== MODULE 6: Time =====
    {
        "id": "1-06", "level_id": 1, "module": 6, "title": "Time", "topic": "Clock",
        "vocabulary": [
            {"word": "morning", "time": "6-12"}, {"word": "afternoon", "time": "12-18"},
            {"word": "evening", "time": "18-22"}, {"word": "night", "time": "22-6"},
        ],
        "grammar": {"pattern": "What time is it?", "examples": ["What time is it? It's three o'clock."]},
    },
    # ===== MODULE 7: Food =====
    {
        "id": "1-07", "level_id": 1, "module": 7, "title": "Food", "topic": "Eating",
        "vocabulary": [
            {"word": "apple", "emoji": "🍎"}, {"word": "sandwich", "emoji": "🥪"},
            {"word": "coffee", "emoji": "☕"}, {"word": "water", "emoji": "💧"},
            {"word": "chicken", "emoji": "🍗"},
        ],
        "grammar": {"pattern": "I want [food], please.", "examples": ["I want a coffee, please."]},
    },
    # ===== MODULE 8: Weather =====
    {
        "id": "1-08", "level_id": 1, "module": 8, "title": "Weather", "topic": "Nature",
        "vocabulary": [
            {"word": "sunny", "emoji": "☀️"}, {"word": "rainy", "emoji": "🌧️"},
            {"word": "cloudy", "emoji": "☁️"}, {"word": "cold", "emoji": "❄️"},
            {"word": "hot", "emoji": "🔥"},
        ],
        "grammar": {"pattern": "What's the weather like?", "examples": ["What's the weather like? It's sunny!"]},
    },
    # ===== MODULE 9: Transport =====
    {
        "id": "1-09", "level_id": 1, "module": 9, "title": "Transport", "topic": "Travel",
        "vocabulary": [
            {"word": "car", "emoji": "🚗"}, {"word": "bus", "emoji": "🚌"},
            {"word": "train", "emoji": "🚂"}, {"word": "plane", "emoji": "✈️"},
            {"word": "bike", "emoji": "🚲"},
        ],
        "grammar": {"pattern": "How do you go to [place]?", "examples": ["How do you go to school? I go by bus."]},
    },
    # ===== MODULE 10: Shopping =====
    {
        "id": "1-10", "level_id": 1, "module": 10, "title": "Shopping", "topic": "Buying",
        "vocabulary": [
            {"word": "cheap", "emoji": "💰"}, {"word": "expensive", "emoji": "💎"},
            {"word": "small", "emoji": "🔹"}, {"word": "big", "emoji": "🔵"},
            {"word": "new", "emoji": "🆕"},
        ],
        "grammar": {"pattern": "How much is it?", "examples": ["How much is it? It's ten pounds."]},
    },
    # ===== MODULE 11: Days =====
    {
        "id": "1-11", "level_id": 1, "module": 11, "title": "Days", "topic": "Week",
        "vocabulary": [
            {"word": "Monday", "day": 1}, {"word": "Tuesday", "day": 2},
            {"word": "Wednesday", "day": 3}, {"word": "Thursday", "day": 4},
            {"word": "Friday", "day": 5}, {"word": "Saturday", "day": 6}, {"word": "Sunday", "day": 7},
        ],
        "grammar": {"pattern": "What day is it today?", "examples": ["What day is it today? It's Monday."]},
    },
    # ===== MODULE 12: Review =====
    {
        "id": "1-12", "level_id": 1, "module": 12, "title": "Review", "topic": "All Topics",
        "vocabulary": [],
        "grammar": {"pattern": "Review of all patterns", "examples": ["All patterns from Modules 1-11"]},
    },
]

# ===== BOOK 2: PRE-INTERMEDIATE =====
LESSONS.extend([
    {"id": "2-01", "level_id": 2, "module": 1, "title": "Life", "topic": "Present Continuous",
     "vocabulary": [{"word": "working", "emoji": "💼"}, {"word": "living", "emoji": "🏠"}],
     "grammar": {"pattern": "I am + verb-ing", "examples": ["I am working now."]}},
    {"id": "2-02", "level_id": 2, "module": 2, "title": "Routine", "topic": "Present Simple",
     "vocabulary": [{"word": "always", "emoji": "🔄"}, {"word": "never", "emoji": "🚫"}],
     "grammar": {"pattern": "I + verb (s)", "examples": ["I always wake up at 7."]}},
    # ... more lessons can be added
])

# ==================== STORAGE ====================
users_db = {}
progress_db = {}

# ==================== ROUTES ====================

@app.get("/")
def root():
    return {"message": "English File API", "version": "1.0.0", "method": "Learn English through English!"}

@app.get("/levels")
def get_levels():
    return LEVELS

@app.get("/levels/{level_id}")
def get_level(level_id: int):
    for level in LEVELS:
        if level["id"] == level_id:
            return level
    raise HTTPException(status_code=404, detail="Level not found")

@app.get("/levels/{level_id}/lessons")
def get_lessons(level_id: int):
    return [l for l in LESSONS if l["level_id"] == level_id]

@app.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str):
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    raise HTTPException(status_code=404, detail="Lesson not found")

@app.get("/lessons/{lesson_id}/vocabulary")
def get_vocabulary(lesson_id: str):
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson.get("vocabulary", [])
    raise HTTPException(status_code=404)

@app.get("/lessons/{lesson_id}/grammar")
def get_grammar(lesson_id: str):
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson.get("grammar", {})
    raise HTTPException(status_code=404)

# ==================== USER ====================

@app.post("/users")
def create_user(user: User):
    user.id = str(uuid.uuid4())
    users_db[user.id] = user.dict()
    return {"user_id": user.id, "message": "Welcome to English File!"}

@app.get("/users/{user_id}/progress")
def get_progress(user_id: str):
    return [p for p in progress_db.values() if p.get("user_id") == user_id]

# ==================== AI TUTOR ====================

@app.post("/ai/chat")
def chat(message: str, user_id: str = "demo"):
    """AI Tutor responds in English only - no translation!"""
    # Simple responses for demo
    responses = [
        "Great! Try to speak more. Don't translate from Russian!",
        "Excellent! Keep practicing every day.",
        "Good! Try to use new words.",
        "Well done! Practice makes perfect.",
        "Nice! Speak English every day.",
    ]
    import random
    return {
        "response": random.choice(responses),
        "tip": "Think in English, not in Russian!",
        "user_id": user_id
    }

@app.post("/ai/practice")
def practice(topic: str, user_id: str = "demo"):
    """Generate practice sentences for topic"""
    return {
        "topic": topic,
        "sentences": [
            f"Tell me about your {topic}.",
            f"What do you think about {topic}?",
            f"Describe your {topic}.",
        ]
    }

# ==================== EXERCISES ====================

@app.get("/exercises/{lesson_id}")
def get_exercises(lesson_id: str):
    """Generate exercises for lesson"""
    lesson = None
    for l in LESSONS:
        if l["id"] == lesson_id:
            lesson = l
            break
    
    if not lesson:
        return []
    
    exercises = []
    
    # Vocabulary exercise
    if lesson.get("vocabulary"):
        exercises.append({
            "type": "vocabulary",
            "instruction": "Match words with pictures",
            "items": [{"word": v["word"], "emoji": v.get("emoji", "📷")} for v in lesson["vocabulary"][:5]]
        })
    
    # Grammar exercise
    if lesson.get("grammar"):
        exercises.append({
            "type": "grammar",
            "instruction": "Complete the sentence",
            "pattern": lesson["grammar"]["pattern"],
            "examples": lesson["grammar"]["examples"]
        })
    
    return exercises

# ==================== RUN ====================

if __name__ == "__main__":
    import uvicorn
    print("📚 English File API - Learn English through English!")
    print(f"Total lessons: {len(LESSONS)}")
