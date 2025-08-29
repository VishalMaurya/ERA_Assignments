#!/usr/bin/env python3
"""
🎮 TECH QUEST ACADEMY 🎮
A Gamified Learning Platform for AI/ML & DevOps

Learn LLMs, Agents, Neural Networks, CNNs, and DevOps through interactive challenges!
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Tech Quest Academy", description="Gamified Learning for AI/ML & DevOps")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory storage for game state (use database in production)
players = {}
leaderboard = []
daily_challenges = []

# Game Configuration
LEARNING_PATHS = {
    "foundations": {
        "name": "Programming Foundations",
        "icon": "🔧",
        "modules": ["variables", "functions", "data_structures", "algorithms"],
        "unlock_level": 1
    },
    "neural_networks": {
        "name": "Neural Networks",
        "icon": "🧠",
        "modules": ["perceptron", "backpropagation", "activation_functions", "training"],
        "unlock_level": 5
    },
    "cnn": {
        "name": "Convolutional Neural Networks",
        "icon": "👁️",
        "modules": ["convolution", "pooling", "filters", "image_classification"],
        "unlock_level": 10
    },
    "llm": {
        "name": "Large Language Models",
        "icon": "💬",
        "modules": ["transformers", "attention", "fine_tuning", "prompt_engineering"],
        "unlock_level": 15
    },
    "agents": {
        "name": "AI Agents",
        "icon": "🤖",
        "modules": ["agent_types", "reasoning", "tool_use", "multi_agent"],
        "unlock_level": 20
    },
    "devops": {
        "name": "DevOps & MLOps",
        "icon": "⚙️",
        "modules": ["docker", "ci_cd", "monitoring", "deployment"],
        "unlock_level": 12
    }
}

ACHIEVEMENTS = {
    "first_steps": {"name": "First Steps", "icon": "👶", "description": "Complete your first lesson"},
    "quick_learner": {"name": "Quick Learner", "icon": "⚡", "description": "Complete 3 lessons in a day"},
    "neural_master": {"name": "Neural Master", "icon": "🧠", "description": "Master Neural Networks path"},
    "code_warrior": {"name": "Code Warrior", "icon": "⚔️", "description": "Complete 10 coding challenges"},
    "perfectionist": {"name": "Perfectionist", "icon": "💯", "description": "Get 100% on 5 quizzes"},
    "streak_master": {"name": "Streak Master", "icon": "🔥", "description": "7-day learning streak"}
}

# Challenge Templates
CHALLENGES = {
    "neural_networks": {
        "perceptron": {
            "title": "Build a Perceptron",
            "description": "Implement a simple perceptron for binary classification",
            "difficulty": "beginner",
            "xp_reward": 100,
            "code_template": """
# Implement a Perceptron
import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
    
    def fit(self, X, y):
        # TODO: Initialize weights and bias
        # TODO: Implement training loop
        pass
    
    def predict(self, X):
        # TODO: Implement prediction
        pass

# Test your perceptron
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])  # AND gate

perceptron = Perceptron()
perceptron.fit(X, y)
predictions = perceptron.predict(X)
print(f"Predictions: {predictions}")
""",
            "solution": """
class Perceptron:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iterations):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                prediction = 1 if linear_output >= 0 else 0
                
                update = self.learning_rate * (y[idx] - prediction)
                self.weights += update * x_i
                self.bias += update
    
    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        return np.where(linear_output >= 0, 1, 0)
"""
        }
    },
    "llm": {
        "prompt_engineering": {
            "title": "Master Prompt Engineering",
            "description": "Create effective prompts for different AI tasks",
            "difficulty": "intermediate",
            "xp_reward": 150,
            "tasks": [
                {
                    "question": "Write a prompt to make an AI act as a Python coding tutor",
                    "example_answer": "You are an expert Python programming tutor. Help students learn Python by:\n1. Explaining concepts clearly with examples\n2. Providing step-by-step guidance\n3. Encouraging best practices\n4. Being patient and supportive\n\nAlways include working code examples and explain each line."
                }
            ]
        }
    }
}

def generate_player_id():
    """Generate unique player ID"""
    return str(uuid.uuid4())[:8]

def calculate_level(xp):
    """Calculate player level based on XP"""
    return int(xp / 100) + 1

def get_next_level_xp(level):
    """Calculate XP needed for next level"""
    return level * 100

@app.get("/", response_class=HTMLResponse)
async def game_homepage(request: Request):
    """Main game interface"""
    return templates.TemplateResponse("tech_quest.html", {"request": request})

@app.post("/api/player/create")
async def create_player(data: dict):
    """Create new player profile"""
    player_id = generate_player_id()
    player_name = data.get("name", f"Player_{player_id}")
    
    players[player_id] = {
        "id": player_id,
        "name": player_name,
        "xp": 0,
        "level": 1,
        "completed_modules": [],
        "achievements": [],
        "current_streak": 0,
        "last_activity": datetime.now().isoformat(),
        "stats": {
            "challenges_completed": 0,
            "quizzes_passed": 0,
            "perfect_scores": 0,
            "total_study_time": 0
        }
    }
    
    return {"player_id": player_id, "player": players[player_id]}

@app.get("/api/player/{player_id}")
async def get_player(player_id: str):
    """Get player profile and progress"""
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    
    player = players[player_id]
    
    # Calculate unlocked paths
    unlocked_paths = {}
    for path_id, path_info in LEARNING_PATHS.items():
        if player["level"] >= path_info["unlock_level"]:
            unlocked_paths[path_id] = path_info
    
    return {
        "player": player,
        "unlocked_paths": unlocked_paths,
        "next_level_xp": get_next_level_xp(player["level"])
    }

@app.get("/api/learning-paths")
async def get_learning_paths():
    """Get all available learning paths"""
    return {"paths": LEARNING_PATHS}

@app.get("/api/path/{path_id}/modules")
async def get_path_modules(path_id: str):
    """Get modules for a specific learning path"""
    if path_id not in LEARNING_PATHS:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    path = LEARNING_PATHS[path_id]
    
    # Return detailed module information
    modules = []
    for i, module_id in enumerate(path["modules"]):
        modules.append({
            "id": module_id,
            "name": module_id.replace("_", " ").title(),
            "order": i + 1,
            "type": "lesson" if i % 2 == 0 else "challenge"
        })
    
    return {"path": path, "modules": modules}

@app.get("/api/challenge/{path_id}/{module_id}")
async def get_challenge(path_id: str, module_id: str):
    """Get specific coding challenge"""
    if path_id not in CHALLENGES or module_id not in CHALLENGES[path_id]:
        # Generate a basic challenge if not found
        return {
            "title": f"{module_id.replace('_', ' ').title()} Challenge",
            "description": f"Complete this {module_id} challenge to earn XP!",
            "difficulty": "intermediate",
            "xp_reward": 100,
            "type": "coding",
            "code_template": f"# {module_id.replace('_', ' ').title()} Challenge\n# Implement your solution here\n\npass"
        }
    
    return CHALLENGES[path_id][module_id]

@app.post("/api/challenge/submit")
async def submit_challenge(data: dict):
    """Submit challenge solution"""
    player_id = data.get("player_id")
    path_id = data.get("path_id")
    module_id = data.get("module_id")
    solution = data.get("solution", "")
    
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Simple solution validation (in production, use proper code execution sandbox)
    score = random.randint(70, 100)  # Simulate grading
    xp_earned = int(score * 1.5)  # XP based on score
    
    # Update player progress
    player = players[player_id]
    player["xp"] += xp_earned
    player["level"] = calculate_level(player["xp"])
    player["stats"]["challenges_completed"] += 1
    
    module_key = f"{path_id}_{module_id}"
    if module_key not in player["completed_modules"]:
        player["completed_modules"].append(module_key)
    
    # Check for achievements
    new_achievements = []
    if len(player["completed_modules"]) == 1 and "first_steps" not in player["achievements"]:
        player["achievements"].append("first_steps")
        new_achievements.append(ACHIEVEMENTS["first_steps"])
    
    if player["stats"]["challenges_completed"] == 10 and "code_warrior" not in player["achievements"]:
        player["achievements"].append("code_warrior")
        new_achievements.append(ACHIEVEMENTS["code_warrior"])
    
    return {
        "score": score,
        "xp_earned": xp_earned,
        "new_level": player["level"],
        "new_achievements": new_achievements,
        "feedback": "Great work!" if score >= 80 else "Good effort! Try to improve your solution."
    }

@app.get("/api/leaderboard")
async def get_leaderboard():
    """Get top players leaderboard"""
    sorted_players = sorted(players.values(), key=lambda x: x["xp"], reverse=True)[:10]
    return {"leaderboard": sorted_players}

@app.get("/api/achievements")
async def get_achievements():
    """Get all available achievements"""
    return {"achievements": ACHIEVEMENTS}

@app.post("/api/quiz/submit")
async def submit_quiz(data: dict):
    """Submit quiz answers"""
    player_id = data.get("player_id")
    answers = data.get("answers", [])
    quiz_id = data.get("quiz_id")
    
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Simple quiz grading (implement actual quiz logic)
    correct_answers = random.randint(len(answers)//2, len(answers))
    score = int((correct_answers / len(answers)) * 100)
    xp_earned = score
    
    # Update player stats
    player = players[player_id]
    player["xp"] += xp_earned
    player["level"] = calculate_level(player["xp"])
    player["stats"]["quizzes_passed"] += 1
    
    if score == 100:
        player["stats"]["perfect_scores"] += 1
        if player["stats"]["perfect_scores"] == 5 and "perfectionist" not in player["achievements"]:
            player["achievements"].append("perfectionist")
    
    return {
        "score": score,
        "correct_answers": correct_answers,
        "total_questions": len(answers),
        "xp_earned": xp_earned,
        "new_level": player["level"]
    }

if __name__ == "__main__":
    print("🎮 Starting Tech Quest Academy...")
    print("🚀 Game server will be available at: http://localhost:8000")
    print("📚 Ready to gamify learning!")
    
    uvicorn.run(
        "tech_quest_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=False
    )
