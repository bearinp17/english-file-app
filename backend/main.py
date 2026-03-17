"""
English File App - Backend API
Based on English File (Oxford) 4th Edition - Learn English through English!
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(title="English File API", version="1.0.0")

# ==================== ENGLISH FILE STRUCTURE ====================
# Based on English File Oxford 4th Edition
# 4 Books: Beginner → Advanced
# Each book has 12 modules (lessons)
# Learn English ONLY in English - no translation!

# English File Levels (4th Edition)
LEVELS = [
    {
        "id": 1, 
        "book": "English File Elementary", 
        "title": "Beginner", 
        "cefr": "A1",
        "description": "Start with pictures and simple sentences",
        "color": "#4CAF50"
    },
    {
        "id": 2, 
        "book": "English File Elementary", 
        "title": "Pre-Intermediate", 
        "cefr": "A2-B1",
        "description": "Build confidence in everyday situations",
        "color": "#2196F3"
    },
    {
        "id": 3, 
        "book": "English File Intermediate", 
        "title": "Intermediate", 
        "cefr": "B1",
        "description": "Communicate with fluency",
        "color": "#9C27B0"
    },
    {
        "id": 4, 
        "book": "English File Upper-Intermediate", 
        "title": "Advanced", 
        "cefr": "B2-C1",
        "description": "Master complex English",
        "color": "#FF5722"
    },
]

# ==================== LESSON STRUCTURE ====================
# Each lesson follows English File pattern:
# A. VOCABULARY & PRONUNCIATION (pictures → words)
# B. GRAMMAR (context → rule)
# C. PRACTICE (interactive exercises)
# D. SPEAKING (real communication)

LESSONS = [
    # ===== LEVEL 1: BEGINNER ===== (English File Book 1)
    {
        "id": "l1-01",
        "level_id": 1,
        "module": 1,
        "title": "Hello!",
        "topic": "Greetings & Introductions",
        # A. VOCABULARY - learn through pictures (no translation!)
        "vocabulary": [
            {"word": "hello", "picture": "wave_hand.png", "sound": "hello.mp3"},
            {"word": "goodbye", "picture": "wave_hand.png", "sound": "goodbye.mp3"},
            {"word": "please", "picture": "please.png", "sound": "please.mp3"},
            {"word": "thank you", "picture": "smile.png", "sound": "thankyou.mp3"},
        ],
        # B. GRAMMAR - shown in context
        "grammar": {
            "title": "Hello! I'm...",
            "pattern": "Hello! I'm [name]. What's your name?",
            "examples": ["Hello! I'm Anna.", "Hello! I'm Tom."],
        },
        # C. EXERCISES
        "exercises": [
            {"type": "listen", "instruction": "Listen and repeat"},
            {"type": "match", "instruction": "Match pictures to words"},
            {"type": "speak", "instruction": "Say Hello! I'm [your name]"},
        ],
        # D. SPEAKING
        "speaking": {
            "task": "Introduce yourself to the class",
            "phrases": ["Hello! I'm...", "What's your name?"],
        }
    },
    {
        "id": "l1-02",
        "level_id": 1,
        "module": 2,
        "title": "Numbers 1-20",
        "topic": "Counting",
        "vocabulary": [
            {"word": "one", "number": 1},
            {"word": "two", "number": 2},
            {"word": "three", "number": 3},
            {"word": "four", "number": 4},
            {"word": "five", "number": 5},
            {"word": "six", "number": 6},
            {"word": "seven", "number": 7},
            {"word": "eight", "number": 8},
            {"word": "nine", "number": 9},
            {"word": "ten", "number": 10},
        ],
        "grammar": {
            "title": "How many?",
            "pattern": "How many? — [Number]",
            "examples": ["How many? One!", "Two, three, four!"],
        },
        "exercises": [
            {"type": "listen", "instruction": "Listen and say the numbers"},
            {"type": "order", "instruction": "Put numbers in order"},
            {"type": "speak", "instruction": "Count from 1 to 10"},
        ],
    },
    {
        "id": "l1-03",
        "level_id": 1,
        "module": 3,
        "title": "Family",
        "topic": "People",
        "vocabulary": [
            {"word": "mother", "picture": "family_mother.png", "family": "female"},
            {"word": "father", "picture": "family_father.png", "family": "male"},
            {"word": "sister", "picture": "family_sister.png", "family": "female"},
            {"word": "brother", "picture": "family_brother.png", "family": "male"},
        ],
        "grammar": {
            "title": "This is my...",
            "pattern": "This is my [family word].",
            "examples": ["This is my mother.", "This is my brother."],
        },
        "exercises": [
            {"type": "listen", "instruction": "Listen and repeat"},
            {"type": "match", "instruction": "Match family words to pictures"},
            {"type": "speak", "instruction": "Say: This is my..."},
        ],
    },
]

# ==================== MODELS ====================

class User(BaseModel):
    id: str = None
    email: str
    name: str
    current_level: int = 1
    current_module: int = 1

class ExerciseAnswer(BaseModel):
    lesson_id: str
    exercise_index: int
    answer: str

# ==================== ROUTES ====================

@app.get("/")
def root():
    return {
        "message": "English File API", 
        "version": "1.0.0",
        "method": "Learn English through English!"
    }

@app.get("/levels")
def get_levels():
    """Get all 4 English File levels"""
    return LEVELS

@app.get("/levels/{level_id}")
def get_level(level_id: int):
    for level in LEVELS:
        if level["id"] == level_id:
            return level
    raise HTTPException(status_code=404, detail="Level not found")

@app.get("/levels/{level_id}/lessons")
def get_lessons(level_id: int):
    """Get all lessons for a level"""
    return [l for l in LESSONS if l["level_id"] == level_id]

@app.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str):
    """Get specific lesson with all components"""
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    raise HTTPException(status_code=404, detail="Lesson not found")

@app.get("/lessons/{lesson_id}/vocabulary")
def get_vocabulary(lesson_id: str):
    """Get vocabulary for a lesson (pictures + words)"""
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson.get("vocabulary", [])
    raise HTTPException(status_code=404, detail="Lesson not found")

@app.get("/lessons/{lesson_id}/exercises")
def get_exercises(lesson_id: str):
    """Get exercises for practice"""
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson.get("exercises", [])
    raise HTTPException(status_code=404, detail="Lesson not found")

# ==================== AI TUTOR ====================

@app.post("/ai/chat")
def chat_with_tutor(message: str, user_id: str = "demo"):
    """
    AI Tutor responds in English only!
    Following English File methodology - no translation
    """
    # In production, connect to Groq/OpenAI
    # Always respond in simple English
    return {
        "response": "Great! Try to speak in English. Practice makes perfect!",
        "user_id": user_id,
        "tip": "Don't worry about mistakes. Just speak!"
    }

# ==================== RUN ====================

if __name__ == "__main__":
    import uvicorn
    print("📚 English File API - Learn English through English!")
    print("Run: uvicorn main:app --host 0.0.0.0 --port 8000")
